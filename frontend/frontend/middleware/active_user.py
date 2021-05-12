from datetime import datetime
from datetime import timedelta
from django.core.cache import cache
from frontend import settings
from django.utils.deprecation import MiddlewareMixin
from frontend.common import common as mcm
from frontend.common import constant as mcs

from ipware import get_client_ip
import requests
import random
from django.shortcuts import redirect
from django.shortcuts import render
from frontend.middleware import sgexceptions
from django.http import HttpResponse
import json
from django.http import HttpResponseRedirect
from django import http


class ActiveUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        ip, is_routable = get_client_ip(request)
        if not mcm.encrypt("ipaddress") in request.session:
            rand = random.randint(100000, 999999)
            chat_session = ip + "_" + str(rand)
            request.session[mcm.encrypt("ipaddress")] = mcm.encrypt(chat_session)

        if request.META['PATH_INFO'] == '/undefined':
            return redirect("/")
        if not 'username' in request.session or not "userid" in request.session:
            if not "static/" in request.META['PATH_INFO'] and not request.META['PATH_INFO'] in mcs.PUBLIC_URL_LIST and not mcs.instant_chat_url in request.META['PATH_INFO']:
                if request.is_ajax():
                    response_unauthenticated_user = HttpResponse(status=mcs.HttpResponse_Forbidden)
                    response_unauthenticated_user['X-WebRTC-Location'] = 'handler_403'
                    response_unauthenticated_user['logout'] = 1  # 1 means allow logout
                    return response_unauthenticated_user
                return redirect("/handler_403")
        if 'username' in request.session and "userid" in request.session:
            username = mcm.decrypt(request.session[mcm.encrypt("username")])

            user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])

            # 1. setting up user access time
            now = datetime.now()
            cache.set('seen_%s' % username, now, settings.USER_LASTSEEN_TIMEOUT)

            # 2. setting up user ip,routable status
            if ip != ipaddr(username):
                cn = mcm.get_country_code(ip)
                access_info = {'ip': ip, 'cn': cn}
                access_info = json.dumps(access_info)
                new_params = {'access_ip': access_info}
                requests.put(mcs.users_url + str(user_id) + '/', json=new_params)
            cache.set('ipaddr_%s' % username, ip, settings.USER_LASTSEEN_TIMEOUT)
            if is_routable:
                is_routable = 1
            else:
                is_routable = 0
            cache.set('routable_%s' % username, is_routable, settings.USER_LASTSEEN_TIMEOUT)

    def process_response(self, request, response):
        return response


class HandleExceptionMiddleware(MiddlewareMixin):
    # in order to catch an exception of middleware, upper middleware can be defined but not used yet
    def process_exception(self, request, exception):
        if isinstance(exception, sgexceptions.InternelServerError):
            response_500 = HttpResponse(status=500)
            return response_500
        if isinstance(exception, sgexceptions.BadRequest):
            response_400 = HttpResponse(status=400)
            return response_400


def last_seen(username):
    return cache.get('seen_%s' % username)


def ipaddr(username):
    if cache.get('ipaddr_%s' % username):
        return cache.get('ipaddr_%s' % username)
    else:
        return ''


def is_routable(username):
    if cache.get('routable_%s' % username):
        return cache.get('routable_%s' % username)
    else:
        return ''


def online(user_name):
    if last_seen(user_name):
        now = datetime.now()
        if now > last_seen(user_name) + timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
            return 0
        else:
            return 1
    else:
        return 0

def is_removable_offline_session(user_name):
    if last_seen(user_name):
        now = datetime.now()
        if now > last_seen(user_name) + timedelta(seconds=settings.USER_OFFLINE_SESSION_TIMEOUT):
            return 1
        else:
            return 0
    else:
        return 0
"""
    #hostname = socket.gethostname()
    #IPAddr = socket.gethostbyname(hostname)
    ip, is_routable = get_client_ip(request)
"""
