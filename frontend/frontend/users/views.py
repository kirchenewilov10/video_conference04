from django.http import HttpResponse
import requests
import json
from datetime import datetime, timedelta
from django.http import QueryDict
from django.shortcuts import render
from django.shortcuts import redirect

from frontend.common import common as mcm
from frontend.common import constant as mcs
from frontend.middleware import active_user as acu
from django.utils.translation import ugettext_lazy as _

# Create your views here.


def users_view(request):
    """
    show users page
    :param request:
    :return:
    """
    try:
        # make header for users table
        header_data = []
        header_data.append({"name": _("Photo")})
        header_data.append({"name": _("Name")})
        header_data.append({"name": _("Admin")})
        header_data.append({"name": _("Address")})
        header_data.append({"name": _("Address2")})
        header_data.append({"name": _("City")})
        header_data.append({"name": _("State")})
        header_data.append({"name": _("Country")})
        header_data.append({"name": _("Zipcode")})
        header_data.append({"name": _("Phone")})
        header_data.append({"name": _("Spent Money")})
        header_data.append({"name": _("Current Money")})
        header_data.append({"name": _("Service Available")})
        header_data.append({"name": _("Online Status")})
        header_data.append({"name": _("Action")})

        body_data = []

        # get all users
        new_params = {}
        new_params["query"] = ["id", "username", "last_login", "is_superuser", "first_name", "last_name", "email",
                               "date_joined", "image_path", "address1", "address2", "city", "country", "phone", "zipcode"]

        res = requests.post(mcs.get_users_v2_url, json=new_params)
        users = res.json()["result"]

        users_data = []
        for user in users:
            user["online"] = acu.online(user["username"])
            if user["image_path"] == "":
                user["image_path"] = mcs.default_user_avatar_path
            users_data.append(user)

        transaction_header_data = []
        transaction_header_data.append({"name": _("Deposit Date")})
        transaction_header_data.append({"name": _("Mode")})
        transaction_header_data.append({"name": _("Amount")})
        transaction_header_data.append({"name": _("Tracking Number")})
        transaction_header_data.append({"name": _("Description")})

        return render(request, "user/users_list.html", {
            "headerdata": header_data,
            "transaction_header_data": transaction_header_data,
            "bodydata": users_data
        })

    except:
        mcm.print_exception()
        return redirect("/index")


def users_datatable_api(request):
    """
    Users datatable api
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

    url = mcs.users_url

    response = requests.request(request.method, url, **requests_args)
    content = json.loads(response.content)
    for user in content['data']:
        try:
            user["online"] = acu.online(user["username"])
            if user["image_path"] == "":
                user["image_path"] = mcs.default_user_avatar_path
        except:
            pass

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


def active_user_service(request):
    """
    Change user's service usable status
    :param request: contains userid, active
    :return:
    """
    params = request.POST
    userid = params["userid"]
    active = params["active"]

    new_params = {
        "service_usable": active
    }

    res = requests.put(mcs.users_url + str(userid) + "/", json=new_params)
    if res.status_code < 300:
        return HttpResponse("success")
    else:
        return HttpResponse("failure")


def user_transactions_datatable_api(request):
    """
    User's transaction datatable api
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

    url = mcs.transactions_url

    response = requests.request(request.method, url, **requests_args)

    proxy_response = HttpResponse(
        response,
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
