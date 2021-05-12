import os
from django.utils.translation import gettext as _

api_proto = "http"
ui_proto = "http"
# ui_proto = "https"

api_port = "8001"
api_host = "127.0.0.1"
ui_port = "80"
ui_host = "127.0.0.1"
# ui_host = "securology.net"

api_url = api_proto + "://" + api_host + ":" + api_port + "/"
if ui_port != "80":
    ui_url = ui_proto + "://" + ui_host + ":" + ui_port + "/"
else:
    ui_url = ui_proto + "://" + ui_host + "/"

# system_project_path = "D:/Workspace/Python/Django/WebRTC(Mohamed)/frontend"
system_project_path = "/home/dev_ext/webrtc/frontend"

admin_email = "codestar0714@outlook.com"
# admin_email = "info@securology.net"


chatmessage_url = api_url + "chatmessage/"
contactus_url = api_url + "contactus/"
devicetypes_url = api_url + "devicetypes/"
menu_url = api_url + "menu/"
off_days_url = api_url + "offdays/"
orders_url = api_url + "orders/"
oss_url = api_url + "oss/"
prices_url = api_url + "prices/"
services_url = api_url + "services/"
softwares_url = api_url + "softwares/"
transactions_url = api_url + "transactions/"
users_url = api_url + "users/"

# auxi
get_admins_v2_url = api_url + "get_admins_v2"
get_users_v2_url = api_url + "get_users_v2"
create_services_list_url = api_url + "create_services_list"
get_service_by_id_url = api_url + "get_service_by_id"
delete_service_url = api_url + "delete_service"
bulk_update_prices_url = api_url + "bulk_update_prices"
make_order_url = api_url + "make_order"

instant_chat_url = "/chat/instantmessage"
instant_messages = []
instant_message_id = 0
notification_email_token = {"token": "", "created_time": ""}

PUBLIC_URL_LIST = [
    '/',
    '/chat/instantmessage',
    '/login_view',
    '/userlogin',
    '/register_view',
    '/userregister',
    '/forget_password',
    '/index',
    '/set_language',
    '/send_message',
    '/handler_401',
    '/handler_403',
    '/handler_440',
    '/jsi18n/',
]

HttpResponse_OK = 200
HttpResponse_Created = 201
HttpResponse_Accepted = 202
HttpResponse_NonAuthoritativeInformation = 203
HttpResponse_NoContent = 204

HttpResponse_BadRequest = 400
HttpResponse_Unauthorized = 401
HttpResponse_PaymentRequired = 402
HttpResponse_Forbidden = 403
HttpResponse_NotFound = 404
HttpResponse_MethodNotAllowed = 405
HttpResponse_NotAcceptable = 406
HttpResponse_ProxyAuthenticationRequired = 407
HttpResponse_RequestTimeout = 408
HttpResponse_Conflict = 409
HttpResponse_Gone = 410
HttpResponse_SessionExpired = 440

HttpResponse_InternalServerError = 500


default_user_avatar_path = "/static/img/user-avatar1.jpg"
