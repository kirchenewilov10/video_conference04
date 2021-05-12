from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
import requests
import time
import hashlib
import json
from django.conf import settings
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q
from frontend.chat.serializers import *
from frontend.common import common as mcm
from frontend.common import constant as mcs
from frontend.common import country_list as countrylist
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django.http import QueryDict

# Create your views here.
def welcome(request):
    """
    show landing page
    :param request:
    :return: render landingpage/index.html
    """
    try:
        param = request.POST
        lang_code = param["language_code"]
        translation.activate(lang_code)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
    except:
        pass

    admin_id = 0
    try:
        ip_address = mcm.decrypt(request.session[mcm.encrypt("ipaddress")])

        # get admin id
        admin = mcm.get_admin(request)
        if admin != {}:
            admin_id = admin["id"]
    except:
        ip_address = "unknown"

    session_key = request.session.session_key
    chat_param = {'session_key': session_key, 'ip_address': ip_address, 'admin_id': admin_id}

    request.session[mcm.encrypt("admin_login_from_email")] = mcm.encrypt(0)
    try:
        param = request.GET
        if "token" in param:
            token = param["token"]
            if token == mcs.notification_email_token["token"]:
                token_created_time = datetime.strptime(mcs.notification_email_token["created_time"], "%Y-%m-%d %H:%M:%S")
                now_time = datetime.now()
                if now_time - token_created_time < timedelta(seconds=3600):
                    if admin != {}:
                        request.session[mcm.encrypt("email")] = mcm.encrypt(admin["email"])
                        request.session[mcm.encrypt("userid")] = mcm.encrypt(admin["id"])
                        request.session[mcm.encrypt("username")] = mcm.encrypt(admin["username"])
                        request.session[mcm.encrypt("userlevel")] = mcm.encrypt(admin["is_superuser"])

                        new_params = {}
                        new_params["last_login"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
                        res = requests.put(mcs.users_url + str(admin["id"]) + "/", json=new_params)

                        request.session[mcm.encrypt("admin_login_from_email")] = mcm.encrypt(1)
                        return redirect("/index")
    except:
        pass

    return render(request, 'landingpage/index.html', {
        "chat_param": chat_param
    })


def userregister(request):
    """
    register new user
    :param request: contains the values set by user from register page
    :return: if registered successfully, then return "success"
    if error occurs, then return following error messages
    "existedname": username exists already
    "existedemail": email exists already
    "failure": unknown error
    """
    try:
        params = request.POST

        new_params = {}

        # prepare the new_params to insert into database
        new_params["last_login"] = datetime(1970, 1, 1).strftime("%Y-%m-%d %H:%M:%S.000000")
        new_params["password"] = hashlib.md5(params["password"].encode()).hexdigest()
        new_params["is_superuser"] = 0
        new_params["username"] = params["username"]
        new_params["first_name"] = params["firstname"]
        new_params["last_name"] = params["lastname"]
        new_params["email"] = params["email"]
        new_params["is_staff"] = 1
        new_params["is_active"] = 1
        new_params["date_joined"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.000000")
        new_params["parent_id"] = 0
        new_params["permission"] = "0000000000"
        new_params["image_path"] = ""
        new_params["deleted"] = 0

        # get all user list from database
        user_info = requests.get(mcs.users_url)
        user_info = user_info.json()["results"]

        # check if there is same username already or not
        query = {"username": new_params["username"]}
        user_info_by_name = mcm.get_by_query(user_info, query)
        if len(user_info_by_name) == 1:
            return HttpResponse("existedname")

        # check if there is same email already or not
        query = {"email": new_params['email']}
        user_info_by_email = mcm.get_by_query(user_info, query)
        if len(user_info_by_email) == 1:
            return HttpResponse("existedemail")

        # save userinfo into database
        res = requests.post(mcs.users_url, json=new_params)

        # if failure, then return "fail"
        if res.status_code >= 300:
            return HttpResponse("fail")

        # if success, then return "success"
        return HttpResponse("success")
    except:
        mcm.print_exception()
        # if exception, then return "failure"
        return HttpResponse("failure")


def userlogin(request):
    """
    user login
    :param request: contains username/email and password which is input from login page
    :return:
    """
    try:
        params = request.POST
        time.sleep(1)

        # get all users list
        user_info = requests.get(mcs.users_url)
        user_info = user_info.json()["results"]

        user_level = -1
        user_id = 0
        user_email = ""
        user_name = ""
        for info in user_info:
            if info["is_active"] != 1:
                continue

            # check if username and password are correct or not
            if info["username"] == params["username"] and info["password"] == hashlib.md5(
                    params["password"].encode()).hexdigest():
                user_level = info["is_superuser"]
                user_id = info["id"]
                user_email = info["email"]
                user_name = info["username"]
                break

        if user_level != -1:
            request.session[mcm.encrypt("email")] = mcm.encrypt(user_email)
            request.session[mcm.encrypt("userid")] = mcm.encrypt(user_id)
            request.session[mcm.encrypt("username")] = mcm.encrypt(user_name)
            request.session[mcm.encrypt("userlevel")] = mcm.encrypt(user_level)

            new_params = {}
            new_params["last_login"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
            res = requests.put(mcs.users_url + str(user_id) + "/", json=new_params)

            # if success, return "success"
            return HttpResponse("success")
        else:
            # if failure, return "failure"
            return HttpResponse("failure")

    except:
        mcm.print_exception()
        return HttpResponse("failure")


def forget_password(request):
    """
    reset password and send email to user
    :param request: contains user email
    :return:
    """
    params = request.POST
    email = params["email"]

    res = requests.get(mcs.users_url + "?email=" + str(email))
    if res.status_code >= 300:
        return HttpResponse("unknown_error")

    user_info = res.json()["results"]

    if len(user_info) == 0:
        return HttpResponse("unknown_email")

    userid = user_info[0]["id"]
    new_password = mcm.generate_random_string(6)

    # send email to inform new password
    content = "Your new password is \"" + new_password + "\". "
    content += "This is the auto-generated password, please change it for the secure of your account after login."

    msg = MIMEMultipart('alternative')
    msg["from"] = mcm.get_mail_account(request)["email"]
    msg["to"] = email
    msg["subject"] = "Your new password is set."

    token = mcm.generate_random_string(12)
    mcs.notification_email_token["token"] = token
    mcs.notification_email_token["created_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    email_content = render_to_string("email_template.html", {"subject": msg["subject"],
                                                             "new_password": new_password,
                                                             "content": content,
                                                             "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                             "type": "forgetpassword",
                                                             "token": token})

    part1 = MIMEText(email_content, 'html')

    msg.attach(part1)

    res = mcm.send_email(request, msg)

    if res == -1:
        return HttpResponse("fail_send_email")


    # update database with new password
    new_params = {}
    new_params["password"] = hashlib.md5(new_password.encode()).hexdigest()

    res = requests.put(mcs.users_url + str(userid) + "/", json=new_params)

    if res.status_code >= 300:
        return HttpResponse("fail_update")

    return HttpResponse("success")


def userlogout(request):
    """
    user logout
    :param request:
    :return:
    """

    try:
        # remove session
        if mcm.encrypt("userid") in request.session:
            request.session.delete(request.COOKIES["sessionid"])
            # return redirect("/")
            return HttpResponse("success")

    except:
        pass
    return HttpResponse("fail")

def indexView(request):
    """
    show firstpage after login
    :param request:
    :return:
    """
    try:
        param = request.POST
        if "language_code" in param:
            lang_code = param["language_code"]
            translation.activate(lang_code)
            request.session[translation.LANGUAGE_SESSION_KEY] = lang_code

        user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])
        user_level = mcm.decrypt(request.session[mcm.encrypt("userlevel")])
        user_name = mcm.decrypt(request.session[mcm.encrypt("username")])

        # get current user info
        user_info = requests.get(mcs.users_url + str(user_id))
        user_info = user_info.json()

        # get all services list
        services = requests.get(mcs.services_url + "?level=0")
        services = services.json()["results"]

        # get all softwares list
        softwares = requests.get(mcs.softwares_url)
        softwares = softwares.json()["results"]

        # make header for orders table in first page
        header_data = []
        header_data.append({"name": _("Service")})
        header_data.append({"name": _("Type")})
        header_data.append({"name": _("Price")})
        header_data.append({"name": _("Pay Status")})
        header_data.append({"name": _("Status")})
        header_data.append({"name": _("Paid Price")})
        header_data.append({"name": _("Date Booked")})
        header_data.append({"name": _("Date Created")})
        header_data.append({"name": _("Date Paid")})
        header_data.append({"name": _("Comment")})
        header_data.append({"name": _("Review")})
        header_data.append({"name": _("Score")})
        header_data.append({"name": _("Response")})
        header_data.append({"name": _("Booked")})
        header_data.append({"name": _("Action")})

        session_key = request.session.session_key
        chat_param = {'sessionKey': session_key, 'userid': user_id, 'username': user_name}

        # check unread messages
        res = list(MessageModel.objects.filter(recipientid=user_id, status=0).values())
        unread_messages_cnt = len(res)
        for message in mcs.instant_messages:
            if message["status"] == 0:
                unread_messages_cnt += 1

        if int(user_level) == 0:
            template = "dashboard/index.html"
        else:
            template = "dashboard/admin_index.html"

        if mcm.decrypt(request.session[mcm.encrypt("admin_login_from_email")]) == 1:
            admin_login_from_email = 1
            request.session[mcm.encrypt("admin_login_from_email")] = mcm.encrypt(0)
        else:
            admin_login_from_email = 0

        return render(request, template, {
            "userid": user_id,
            "username": user_info["first_name"] + " " + user_info["last_name"],
            "userinfo": user_info,
            "admininfo": mcm.get_admin(request),
            "countries": countrylist.countries,
            "services": services,
            "softwares": softwares,
            "headerdata": header_data,
            "chat_param": chat_param,
            "unread_messages_cnt": unread_messages_cnt,
            "admin_login_from_email": admin_login_from_email
        })
    except:
        mcm.print_exception()
        return redirect("/")


def set_language(request):
    """
    set language
    :param request:
    :return:
    """
    param = request.POST
    try:
        lang_code = param["lang_code"]
        translation.activate(lang_code)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
        request.LANGUAGE_CODE = lang_code
        # return HttpResponse("success")
        return redirect("/index")
    except Exception as e:
        return HttpResponse("failure")


def send_message(request):
    """
    send message to admin
    :param request:
    :return:
    """
    params = request.POST

    try:
        contact_name = params["contact_name"]
        contact_email = params["contact_email"]
        contact_message = params["contact_message"]

        content = "Hi, My name is " + contact_name + ". \n"
        content += contact_message
        content += "\n Please contact me via e-mail: " + contact_email

        msg = MIMEMultipart('alternative')
        msg["from"] = mcm.get_mail_account(request)["email"]
        msg["to"] = mcs.admin_email
        msg["subject"] = "You have a message from " + contact_email + "."

        token = mcm.generate_random_string(12)
        mcs.notification_email_token["token"] = token
        mcs.notification_email_token["created_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        email_content = render_to_string("email_template.html", {"subject": msg["subject"],
                                                                 "content": content,
                                                                 "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                                 "type": "contactus",
                                                                 "token": token})

        part1 = MIMEText(email_content, 'html')

        msg.attach(part1)

        res = mcm.send_email(request, msg)

        if res == -1:
            return HttpResponse("fail")

        new_params = {}
        new_params["name"] = contact_name
        new_params["email"] = contact_email
        new_params["content"] = contact_message

        res = requests.post(mcs.contactus_url, json=new_params)
        if res.status_code < 300:
            return HttpResponse("success")
        else:
            return HttpResponse("fail")
    except:
        return HttpResponse("fail")


def get_service_categories(request):
    """
    Get Service Categories
    :param request: contains service_id
    :return:
    """
    params = request.POST
    service_id = params["service_id"]

    categories = []
    res = requests.get(mcs.services_url + "?index=" + str(service_id))
    if res.status_code < 300:
        categories = res.json()["results"]

    return HttpResponse(json.dumps(categories))


def get_price_by_category(request):
    """
    Get Price by Category
    :param request:
    :return:
    """
    params = request.POST
    service_id = params["service_id"]
    item_comb = json.loads(params["item_comb"])

    price = 0
    res = requests.get(mcs.prices_url + "?item_comb=" + json.dumps(item_comb) + "&service_id=" + str(service_id))
    if res.status_code < 300:
        prices = res.json()["results"]
        if len(prices) > 0:
            price = prices[0]["price"]

    return HttpResponse(price)


def orders_datatable_api(request):
    """
    Orders Datatable API
    :param request:
    :return:
    """
    requests_args = {}
    headers = mcm.get_headers(request.META)
    params = request.GET.copy()

    if 'headers' not in requests_args:
        requests_args['headers'] = {}
    if 'data' not in requests_args:
        requests_args['data'] = request.body
    if 'params' not in requests_args:
        requests_args['params'] = QueryDict('', mutable=True)

    # Overwrite any headers and params from the incoming request with explicitly
    # specified values for the requests library.
    headers.update(requests_args['headers'])
    params.update(requests_args['params'])

    # If there's a content-length header from Django, it's probably in all-caps
    # and requests might not notice it, so just remove it.
    for key in list(headers.keys()):
        if key.lower() == 'content-length':
            del headers[key]

    requests_args['headers'] = headers
    requests_args['params'] = params

    services = mcm.get_services(request)
    services_name_map = {}
    for service in services:
        services_name_map[service["id"]] = service["name"]

    user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])
    url = mcs.orders_url + "?userid=" + str(user_id)

    response = requests.request(request.method, url, **requests_args)
    content = json.loads(response.content)
    for item in content["data"]:
        if item["service_id"] in services_name_map:
            item["service_name"] = services_name_map[item["service_id"]]

            categories = json.loads(item["category_type"])
            for cg in categories:
                item["service_name"] += "/" + services_name_map[cg]

    proxy_response = HttpResponse(
        json.dumps(content),
        status=response.status_code)

    excluded_headers = set([
        # Hop-by-hop headers
        # ------------------
        # Certain response headers should NOT be just tunneled through.  These
        # are they.  For more info, see:
        # http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec13.5.1
        'connection', 'keep-alive', 'proxy-authenticate',
        'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
        'upgrade',

        # Although content-encoding is not listed among the hop-by-hop headers,
        # it can cause trouble as well.  Just let the server set the value as
        # it should be.
        'content-encoding',

        # Since the remote server may or may not have sent the content in the
        # same encoding as Django will, let Django worry about what the length
        # should be.
        'content-length',
    ])
    for key, value in response.headers.items():
        if key.lower() in excluded_headers:
            continue
        elif key.lower() == 'location':
            # If the location is relative at all, we want it to be absolute to
            # the upstream server.
            proxy_response[key] = mcm.make_absolute_location(response.url, value)
        else:
            proxy_response[key] = value

    return proxy_response


def make_order(request):
    """
    Make Order
    :param request: contains services
    :return:
    """
    params = request.POST
    services = json.loads(params["services"])
    active_booking = params["active_booking"]

    if active_booking == "1":
        try:
            booking_datetime = datetime.strptime(params["booking_datetime"], "%m/%d/%Y %H:%M")
        except Exception as e:
            return HttpResponse("invalid_datetime_format")
    else:
        booking_datetime = datetime.now()

    user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])

    new_params = {
        "userid": user_id,
        "services": services,
        "booking_datetime": booking_datetime.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "active_booking": active_booking
    }

    res = requests.post(mcs.make_order_url, json=new_params)

    if res.status_code < 300:
        return HttpResponse("success")
    else:
        return HttpResponse("failure")


def get_order_comment_and_response(request):
    """
    Get Order Comment
    :param request: contains order_id
    :return:
    """
    params = request.POST
    order_id = params["order_id"]

    comment = ""
    res = requests.get(mcs.orders_url + str(order_id) + "/")
    if res.status_code < 300:
        order_info = res.json()
        comment = order_info["comment"]
        user_response = order_info["user_response"]

    return HttpResponse(json.dumps({"comment": comment, "user_response": user_response}))


def send_order_response(request):
    """
    Send Order Response to Administrator
    :param request: contains order_id, response_str
    :return:
    """
    params = request.POST
    order_id = params["order_id"]
    user_response = params["order_response"]

    user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])

    res = requests.get(mcs.orders_url + str(order_id) + "/")
    if res.status_code < 300:
        order_info = res.json()
        if order_info["userid"] == user_id:
            new_params = {
                "user_response": user_response
            }

            res = requests.put(mcs.orders_url + str(order_id) + "/", json=new_params)
            if res.status_code < 300:
                return HttpResponse("success")

    return HttpResponse("failure")


def cancel_order(request):
    """
    Cancel Order
    :param request: contains order_id
    :return:
    """
    params = request.POST
    order_id = params["order_id"]

    user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])

    res = requests.get(mcs.orders_url + str(order_id) + "/")
    if res.status_code < 300:
        order_info = res.json()
        if order_info["userid"] == user_id:
            new_params = {
                "service_status": 2
            }

            res = requests.put(mcs.orders_url + str(order_id) + "/", json=new_params)
            if res.status_code < 300:
                return HttpResponse("success")

    return HttpResponse("failure")


def get_book_setting(request):
    """
    Get Off Days and Duty time
    :param request:
    :return:
    """
    off_days = mcm.get_off_days(request)

    return HttpResponse(json.dumps({"off_days": off_days}))


def get_unable_time_list(request):
    """
    Get Unable Time List
    :param request:
    :return:
    """
    try:
        params = request.POST
        selected_date = datetime.strptime(params["booking_date"], "%m/%d/%Y").strftime("%Y-%m-%d")

        res = requests.get(mcs.orders_url + "?booked_date=" + str(selected_date))
        booked_time_list = []
        if res.status_code < 300:
            orders = res.json()["results"]
            orders.sort(key=mcm.sortDateBooked)
            for order in orders:
                booked_time = datetime.strptime(order["date_booked"], "%Y-%m-%dT%H:%M:%SZ").strftime("%H:%M")
                one_hour_later = (datetime.strptime(order["date_booked"], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=1)).\
                    strftime("%H:%M")

                flag = 0
                for bt in booked_time_list:
                    if bt["from"] == booked_time:
                        flag = 1
                        break

                if flag == 0:
                    booked_time_list.append({"from": booked_time, "to": one_hour_later})

        return HttpResponse(json.dumps(booked_time_list))

    except:
        return HttpResponse("[]")


def handler401View(request):
    """
    handler 401
    :param request:
    :return:
    """
    # get user_id from session
    user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])

    if user_id is not None:
        # delete session
        request.session.delete(request.COOKIES["sessionid"])

    return redirect("/")

def handler403View(request):
    """
    handler 403
    :param request:
    :return:
    """
    # get user_id from session
    try:
        user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])

        if user_id is not None:
            # delete session
            request.session.delete(request.COOKIES["sessionid"])
    except:
        pass

    return redirect("/")

def handler440View(request):
    """
    handler 440
    :param request:
    :return:
    """
    # get user_id from session
    user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])

    if user_id is not None:
        # delete session
        request.session.delete(request.COOKIES["sessionid"])

    return redirect("/")