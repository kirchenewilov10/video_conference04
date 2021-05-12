from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
import requests
import time
import hashlib
import json
from datetime import datetime, timedelta
from operator import itemgetter

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from frontend.dashboard.forms import ImageForm
from django.shortcuts import render
from django.shortcuts import redirect

from frontend.common import common as mcm
from frontend.common import constant as mcs

from django.utils import translation


# Create your views here.


def change_password_view(request):
    return render(request, "accountsetting/change_password.html")


def change_user_password(request):
    result = {}
    try:
        params = request.POST
        current_password = params["current_password"]
        new_password = params["new_password"]

        user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])
        user_info = requests.get(mcs.users_url + str(user_id) + "/")
        user_info = user_info.json()

        if not user_info["password"] == hashlib.md5(current_password.encode()).hexdigest():
            result["status"] = "false"
            result["msg"] = "wrong_password"
            return HttpResponse(json.dumps(result))

        new_param = {}
        new_param["password"] = hashlib.md5(new_password.encode()).hexdigest()
        res = requests.put(mcs.users_url + str(user_id) + "/", json=new_param)
        if res.status_code < 300:
            result["status"] = "true"
            return HttpResponse(json.dumps(result))
        else:
            result["status"] = "false"
            result["msg"] = "update_failed"
            return HttpResponse(json.dumps(result))

    except Exception as e:
        mcm.print_exception()
        result["status"] = "false"
        result["msg"] = str(e)
        return HttpResponse(json.dumps(result))


def update_user_profile(request):
    param = request.POST
    result = {}
    user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])

    # check duplicate
    users_list = requests.get(mcs.users_url)
    users_list = users_list.json()['results']
    for user in users_list:
        if user["id"] == user_id:
            continue

        # check username duplicate
        if user["username"] == param["username"]:
            result["status"] = "false"
            result["msg"] = "username_duplicated"
            return HttpResponse(json.dumps(result))

        # check email duplicate
        if user["email"] == param["email"]:
            result["status"] = "false"
            result["msg"] = "email_duplicated"
            return HttpResponse(json.dumps(result))

    # update the user profile
    new_param = {}
    new_param["username"] = param["email"]
    new_param["first_name"] = param["first_name"]
    new_param["last_name"] = param["last_name"]
    new_param["phone"] = param["phone"]
    new_param["email"] = param["email"]
    new_param["address1"] = param["address1"]
    new_param["address2"] = param["address2"]
    new_param["city"] = param["city"]
    new_param["state"] = param["state"]
    new_param["zipcode"] = param["zipcode"]
    new_param["country"] = param["country"]

    # get image file path from session for user avatar
    if mcm.encrypt("user_avatar_file") in request.session and not mcm.decrypt(
            request.session[mcm.encrypt("user_avatar_file")]) == "":
        new_param["image_path"] = mcm.decrypt(request.session[mcm.encrypt("user_avatar_file")])
    else:
        # if there is no image_path, then use default avatar
        new_param["image_path"] = "/static/img/user-avatar1.jpg"

    # update the data in database
    res = requests.put(mcs.users_url + str(user_id) + "/", json=new_param)
    if res.status_code < 300:
        request.session[mcm.encrypt("username")] = mcm.encrypt(param["username"])
        result["status"] = "true"
        result["msg"] = "success"
        result["image_path"] = new_param["image_path"]
        return HttpResponse(json.dumps(result))
    else:
        result["status"] = "false"
        result["msg"] = "failure"
        return HttpResponse(json.dumps(result))


def change_user_avatar(request):
    """
    user changes own avatar
    :param request: contains the image file for user avatar
    :return: if success, return image_path saved on server.
    if failure, return error message - "Form invalid".
    """
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # save image on server
            image = form.save(commit=False)
            image.save()
            image_path = image.image

            # save image_path into session
            request.session[mcm.encrypt("user_avatar_file")] = mcm.encrypt(str(image_path))
            request.session.save()

            return HttpResponse(str(image_path))
        else:
            return HttpResponse("Form invalid", status=500)


def set_language(request):
    """
    change the language
    :param request: contains lang_code
    :return: if success, return "success", if fail, return "failure"
    """
    param = request.POST
    try:
        lang_code = param["lang_code"]
        translation.activate(lang_code)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
        return HttpResponse("success")
    except Exception as e:
        return HttpResponse("failure")