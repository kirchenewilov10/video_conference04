from sty import fg, bg, ef, rs
import sys, re, requests, json, smtplib, random, string
from urllib.parse import urlparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from frontend.common import constant as mcs
from frontend.chat import constant as chat_mcs
from datetime import datetime


def print_exception():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    error_msg = bg.red
    error_msg += str(exc_obj) + ", File: " + str(exc_tb.tb_frame.f_code.co_filename) + ", Line: " + str(exc_tb.tb_lineno)
    error_msg += bg.rs
    print(error_msg)

def encrypt(text):
    return text

def decrypt(text):
    return text

def get_by_query(array, queries):
    newArray = []
    for item in array:
        query_keys = queries.keys()
        g_query_success = 0
        for key in query_keys:
            if queries[key] != item[key]:
                g_query_success = 1
                break
        if g_query_success == 0:
            newArray.append(item)
    return newArray


def get_headers(environ):
    """
    Retrieve the HTTP headers from a WSGI environment dictionary.  See
    https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META
    """
    headers = {}
    for key, value in environ.items():
        # Sometimes, things don't like when you send the requesting host through.
        if key.startswith('HTTP_') and key != 'HTTP_HOST':
            headers[key[5:].replace('_', '-')] = value
        elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            headers[key.replace('_', '-')] = value

    return headers


def make_absolute_location(base_url, location):
    """
    Convert a location header into an absolute URL.
    """
    absolute_pattern = re.compile(r'^[a-zA-Z]+://.*$')
    if absolute_pattern.match(location):
        return location

    parsed_url = urlparse(base_url)

    if location.startswith('//'):
        # scheme relative
        return parsed_url.scheme + ':' + location

    elif location.startswith('/'):
        # host relative
        return parsed_url.scheme + '://' + parsed_url.netloc + location

    else:
        # path relative
        return parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path.rsplit('/', 1)[0] + '/' + location

    return location


def get_country_code(ip):
    try:
        location_url = 'https://geolocation-db.com/jsonp/'
        res = requests.get(location_url + str(ip))
        if res.status_code >= 300:
            return ''
        locationinfo = json.loads(res.text.split('(')[1].split(')')[0])
        return locationinfo['country_code']
    except:
        return ''


def get_access_info(access_ip):
    try:
        accessinfo = json.loads(access_ip)
        ip = accessinfo['ip']
        cn = str(accessinfo['cn']).swapcase()
    except:
        ip = ''
        cn = ''
    return ip, cn


def get_time_zone(request):
    time_zone = "AST"

    return time_zone


def get_mail_account(request):
    """
    get our support team email account
    :param request:
    :return:
    """
    mail_account = {}
    mail_account["email"] = "securology.net@gmail.com"
    mail_account["password"] = "xxxxx"
    return mail_account


def send_email(request, msg):
    mail_account = get_mail_account(request)

    try:
        # for gmail
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        # s = smtplib.SMTP(host='smtp.office365.com', port=587)
        s.ehlo()
        s.starttls()
        s.login(mail_account["email"], mail_account["password"])
        s.send_message(msg)

    except Exception as e:
        print(e)
        return -1

    return 0

def send_single_email(request, to, subject, content):
    msg = MIMEMultipart("alternative")
    msg["from"] = get_mail_account(request)["email"]
    msg["to"] = to
    msg["Subject"] = subject
    content = content
    msg.attach(MIMEText(content))
    return send_email(request, msg)


def get_admin(request):
    """
    get admin info
    :param request:
    :return:
    """
    admin = {}
    res = requests.get(mcs.users_url + "?is_superuser=1")
    if res.status_code < 300:
        admins = res.json()["results"]
        if len(admins) > 0:
            admin["id"] = admins[0]["id"]
            admin["username"] = admins[0]["username"]
            admin["email"] = admins[0]["email"]
            admin["is_superuser"] = admins[0]["is_superuser"]

    return admin


def send_instant_message(request, params):
    """
    send instant message from service desk to user
    :param request:
    :param params:
    :return:
    """
    res = requests.post(chat_mcs.instant_chat_url, data=params)
    if res.status_code < 300:
        return 1
    else:
        return 0


def generate_random_string(length):
    """
    Generate random string
    This function will be used for token generation
    :param length:
    :return:
    """
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_services(request):
    """
    Get Services List
    :param request:
    :return:
    """
    services = []
    res = requests.get(mcs.services_url)
    if res.status_code < 300:
        services = res.json()["results"]

    return services

def get_users(request):
    """
    Get All Users
    :param request:
    :return:
    """
    users = []
    res = requests.get(mcs.users_url)
    if res.status_code < 300:
        users = res.json()["results"]

    return users

def get_order(request, order_id):
    """
    Get Order Info by order_id
    :param request:
    :param order_id:
    :return:
    """
    res = requests.get(mcs.orders_url + str(order_id) + "/")
    if res.status_code < 300:
        return res.json()

    else:
        return {}

def get_all_orders(request):
    """
    Get all orders
    :param request:
    :return:
    """
    orders = []
    res = requests.get(mcs.orders_url)
    if res.status_code < 300:
        orders = res.json()["results"]

    return orders

def get_off_days(request):
    """
    Get All Off Days List
    :param request:
    :return:
    """
    res = requests.get(mcs.off_days_url)
    if res.status_code < 300:
        return res.json()["results"]

    return []

def sortDateBooked(val):
    return str(val["date_booked"])
