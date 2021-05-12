from django.shortcuts import render
import requests
import tempfile
import shutil
import os
import json
from datetime import datetime, timedelta
from django.http import HttpResponse
from frontend.common import constant as mcs
from frontend.common import common as mcm
from frontend.middleware import active_user as acu
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from frontend.chat.serializers import *
from django.db.models import Q
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

# Create your views here.
def instant_message(request):
    """

    :param request:
    :return:
    """
    ipaddress = mcm.decrypt(request.session[mcm.encrypt("ipaddress")])

    if request.method == "POST":
        params = request.POST
        mcs.instant_message_id += 1
        message = params.copy()

        # remake message variable
        message_type = message["type"]
        message["id"] = mcs.instant_message_id
        message["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message["status"] = 0

        if message_type == "FILE":
            file = request.FILES.getlist('image')[0]
            file_size = file.size
            file_size_check = 0
            if file_size > 200 * (2 ** 20):
                file_size_check = 1

            if file_size_check == 1:
                return HttpResponse("FILE_SIZE_ERROR")

            tup = tempfile.mkstemp()
            f = os.fdopen(tup[0], 'wb')
            f.write(file.read())
            f.close()

            tup_path = str(tup[1])
            str_file = str(file)

            chatmsg_directory_name = "static/attach_files/2b30feghwid3/" + \
                                     datetime.now().strftime("%Y-%m-%d") + "/"
            if not os.path.exists(chatmsg_directory_name):
                os.makedirs(chatmsg_directory_name)

            real_path = chatmsg_directory_name + ipaddress + "_" + str_file
            shutil.move(tup_path, real_path)
            real_path = mcs.ui_url + real_path
            body_data = {'path': real_path, 'name': ipaddress + "_" + str_file}
            message["body"] = body_data

        # save message in buffer
        mcs.instant_messages.append(message)

        # send message
        notify_ws_clients(message)

        # check if admin is online or not
        admin = mcm.get_admin(request)
        if len(admin) > 0:
            admin_online_status = acu.online(admin["username"])
            if admin_online_status == 0:

                if str(message["recipientid"]) == str(admin["id"]):
                    # send email notification
                    msg = MIMEMultipart('alternative')
                    msg["from"] = mcm.get_mail_account(request)["email"]
                    msg["to"] = mcs.admin_email
                    msg["subject"] = "Instant message on securology.net"
                    email_content = "You have a message from " + message["userid"] + " on securology.net."

                    token = mcm.generate_random_string(12)
                    mcs.notification_email_token["token"] = token
                    mcs.notification_email_token["created_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    email_content = render_to_string("email_template.html", {"subject": msg["subject"],
                                                                             "content": email_content,
                                                                             "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                                             "type": "instantmessage",
                                                                             "token": token})

                    part1 = MIMEText(email_content, 'html')

                    msg.attach(part1)

                    mcm.send_email(request, msg)

                    # send bot message
                    new_instant_message = {}
                    new_instant_message["userid"] = str(admin["id"])
                    new_instant_message["recipientid"] = message["userid"]
                    new_instant_message["body"] = "Our representative will join in a moment."
                    new_instant_message["type"] = "TEXT"
                    new_instant_message["session_type"] = "unregistered"
                    mcm.send_instant_message(request, new_instant_message)

        return HttpResponse("success")

    elif request.method == "GET":
        params = request.GET
        instant_message = {}
        for message in mcs.instant_messages:
            if message["id"] == int(params["id"]):
                instant_message = message

        return HttpResponse(json.dumps(instant_message))


def notify_ws_clients(params):
    """
    Inform client there is a new message.
    """
    # if self.type == 'BLOB':
    #     self.id = -1 * self.userid
    notification = {
        'type': 'receive_group_message',
        'message': '{}'.format(params["id"]),
        'session_type': 'unregistered'
    }

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)("{}".format(params["userid"]), notification)
    async_to_sync(channel_layer.group_send)("{}".format(params["recipientid"]), notification)


def show_chatroom(request):
    """
    show chatting page when customer clicks "A/V" button from firstpage.
    :param request:
    :return: return dashboard/videochat.html
    """
    # get userid from session
    user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])

    # get admin data
    new_params = {}
    new_params["query"] = ["id", "username", "first_name", "last_name", "image_path"]
    res = requests.post(mcs.get_admins_v2_url, json=new_params)
    admins_total_data = res.json()["result"]

    # extract admin data
    default_admin = {}
    if len(admins_total_data) > 0:
        default_admin = admins_total_data[0]
        if default_admin["image_path"] == "":
            default_admin["image_path"] = "static/img/user-avatar1.jpg"
        default_admin["online"] = acu.online(default_admin["username"])

    # get chat history
    chat_history = []
    if default_admin != {}:
        # get chat history
        res = list(MessageModel.objects.filter(Q(userid=user_id, recipientid=default_admin["id"]) |
                                               Q(userid=default_admin["id"], recipientid=user_id)).values())

        MessageModel.objects.filter(Q(userid=default_admin["id"], recipientid=user_id)).update(status=1)

        for message in res:
            message["timestamp"] = datetime.strftime(message["timestamp"], "%Y-%m-%d %H:%M:%S")
            chat_history.append(message)

        chat_history.sort(key=timeStamp)

    return render(request, 'videochatting/videochat.html', {
        "userid": user_id,
        "receiver": default_admin,
        "chat_logs": chat_history,
        "page_type": "request_call"
    })


def timeStamp(val):
    return str(val["timestamp"])


def show_admin_chatroom(request):
    """
    show admin the admin chatpage when admin accepts the calling from user
    :param request: contains calling user id
    :return: render admin_chat.html
    """
    params = request.POST
    try:
        calling_user = int(params["calling_user"])
    except:
        calling_user = 0

    # get userid from session
    user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])

    # get calling user's data
    new_params = {}
    new_params["query"] = ["id", "username", "first_name", "last_name", "image_path"]
    res = requests.post(mcs.get_users_v2_url, json=new_params)
    calling_users_data = res.json()["result"]

    receiver = {}
    for user in calling_users_data:
        if int(user["id"]) == int(calling_user):
            receiver = user
            if receiver["image_path"] == "":
                receiver["image_path"] = "static/img/user-avatar1.jpg"
            receiver["online"] = acu.online(receiver["username"])
            break

    chat_history = []
    if calling_user != 0:
        # get chat history
        chat_history = list(MessageModel.objects.filter(Q(userid=user_id, recipientid=receiver["id"]) |
                                               Q(userid=receiver["id"], recipientid=user_id)).values())

        MessageModel.objects.filter(Q(userid=receiver["id"], recipientid=user_id)).update(status=1)

    return render(request, 'videochatting/videochat.html', {
        "userid": user_id,
        "receiver": receiver,
        "chat_logs": chat_history,
        "page_type": "receive_call"
    })