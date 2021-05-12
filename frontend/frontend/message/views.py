from django.http import HttpResponse
import requests
import json
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from frontend.chat.serializers import *
from django.db.models import Q
from frontend.common import common as mcm
from frontend.common import constant as mcs
from frontend.middleware import active_user as acu
from django.utils.translation import ugettext_lazy as _

# Create your views here.

def messages_view(request):
    """
    render messages page
    :param request:
    :return:
    """
    # get all users
    res = requests.get(mcs.users_url)
    total_users = res.json()["results"]

    # get current userid from session
    user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])
    user_level = mcm.decrypt(request.session[mcm.encrypt("userlevel")])

    users = []
    for user in total_users:
        if user["is_superuser"] == user_level:
            continue

        temp= {}
        temp["id"] = user["id"]
        temp["username"] = user["username"]
        temp["first_name"] = user["first_name"]
        temp["last_name"] = user["last_name"]
        if user["image_path"] == "":
            temp["image_path"] = "/static/user-avatar/default-avatar.jpg"
        else:
            temp["image_path"] = user["image_path"]
        temp["online"] = acu.online(user["username"])
        temp["type"] = "registered"

        # get unread messages count
        res = list(MessageModel.objects.filter(Q(userid=user["id"], recipientid=user_id, status=0)).values())
        temp["unread_messages_cnt"] = len(res)

        users.append(temp)

    # if user is admin, add unregistered users
    if user_level == 1:
        instant_users_map = {}
        for message in mcs.instant_messages:
            if not validIP(message["userid"].split("_")[0]):
                continue

            if not message["userid"] in instant_users_map:
                if message["status"] == 0:
                    instant_users_map[message["userid"]] = 1
                else:
                    instant_users_map[message["userid"]] = 0
            else:
                if message["status"] == 0:
                    instant_users_map[message["userid"]] += 1


        for key in instant_users_map:
            temp = {}
            temp["id"] = key
            temp["username"] = key.split("_")[0]
            temp["first_name"] = key.split("_")[0]
            temp["last_name"] = ""
            temp["image_path"] = "/static/user-avatar/default-avatar.jpg"
            temp["online"] = 0
            temp["type"] = "unregistered"
            temp["unread_messages_cnt"] = instant_users_map[key]
            users.append(temp.copy())

    if user_level == 1:
        template = "messages/admin_messages_view.html"
    else:
        template = "messages/user_messages_view.html"
    return render(request, template, {
        "users": users,
        "userid": user_id,
        "user_level": user_level
    })


def validIP(address):
    """
    check if the string is valid ip address or not.
    :param address: test string
    :return: true or false
    """
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        if not 0 <= int(item) <= 255:
            return False
    return True


def get_message_history(request):
    """
    get history of messages for seleted user
    :param request: contains selected "userid"
    :return: return history of messages
    """
    params = request.POST
    selected_userid = params["userid"]

    # get current userid from session
    user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])

    # get messages and update the read status
    res = list(MessageModel.objects.filter(Q(userid=user_id, recipientid=selected_userid) |
                                           Q(userid=selected_userid, recipientid=user_id)).values())

    MessageModel.objects.filter(Q(userid=selected_userid, recipientid=user_id)).update(status=1)

    messages = []
    for message in res:
        message["timestamp"] = datetime.strftime(message["timestamp"], "%Y-%m-%d %H:%M:%S")
        messages.append(message)

    messages.sort(key=timeStamp)

    return HttpResponse(json.dumps(messages))


def timeStamp(val):
    return str(val["timestamp"])


def update_message_status(request):
    """
    update message read status
    :param request: contains message_id
    :return: status code
    """
    try:
        params = request.POST
        message_id = params["message_id"]

        MessageModel.objects.filter(pk=message_id).update(status=1)

        return HttpResponse("success")
    except:
        mcm.print_exception()
        return HttpResponse("failure")


def get_instantmessage_history(request):
    """
    get all history of instant messages by user ip address
    :param request: contains ip
    :return:
    """
    params = request.POST
    userid = params["userid"]

    # get unread messages count
    messages = []
    for message in mcs.instant_messages:
        if message["userid"] == userid or message["recipientid"] == userid:
            message["status"] = 1
            messages.append(message)

    messages.sort(key=timeStamp)

    return HttpResponse(json.dumps(messages))