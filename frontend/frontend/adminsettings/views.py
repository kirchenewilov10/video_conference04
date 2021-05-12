from django.http import HttpResponse
import requests
import os
import json
import base64
from datetime import datetime, timedelta
from django.shortcuts import render
from django.shortcuts import redirect
from frontend.common import common as mcm
from frontend.common import constant as mcs
from frontend.common import excel
from frontend.html2pdf import pdf
from django.utils.translation import ugettext_lazy as _
from django.http import QueryDict

# Create your views here.


def services_view(request):
    """
    show services page for admin
    :param request:
    :return:
    """
    try:
        # make header for users table
        service_header_data = []
        service_header_data.append({"name": _("Service")})
        service_header_data.append({"name": _("Action")})

        res = requests.get(mcs.services_url)
        services = res.json()["results"]
        service_name_map = {}
        main_services = []
        for service in services:
            if service["level"] == 0:
                main_services.append(service)

            service_name_map[service["id"]] = service["name"]

        price_header_data = []
        price_header_data.append({"name": _("Service")})
        price_header_data.append({"name": _("Case")})
        price_header_data.append({"name": _("Price")})
        price_header_data.append({"name": _("Action")})

        res = requests.get(mcs.prices_url)
        prices = res.json()["results"]
        for price in prices:
            item_names = []
            item_comb = json.loads(price["item_comb"])
            for item in item_comb:
                if item in service_name_map:
                    item_names.append(service_name_map[item])
                else:
                    item_names.append("")

            if price["service_id"] in service_name_map:
                price["service_name"] = service_name_map[price["service_id"]]
            else:
                price["service_name"] = ""

            price["names_comb"] = " + ".join(item_names)

        return render(request, "adminsettings/services.html", {
            "serviceheaderdata": service_header_data,
            "services": main_services,
            "priceheaderdata": price_header_data,
            "prices": prices
        })

    except:
        mcm.print_exception()
        return redirect("/index")


def get_service_by_id(request):
    """
    get service info by id
    :param request: contains service_id
    :return:
    """
    params = request.POST
    service_id = params["service_id"]

    new_params = {
        "service_id": service_id
    }
    res = requests.post(mcs.get_service_by_id_url, json=new_params)
    service = res.json()["result"]

    return HttpResponse(json.dumps(service))


def save_service(request):
    """
    save service
    :param request:
    :return:
    """
    params = request.POST
    service_id = params["service_id"]
    service_name = params["service_name"]
    service_categories = json.loads(params["service_categories"])

    res = requests.get(mcs.services_url + "?level=0")
    services = res.json()["results"]

    for service in services:
        if int(service["id"]) == int(service_id):
            continue

        if service["name"] == service_name:
            return HttpResponse("duplicated_name")

    new_params = {}
    new_params["name"] = service_name
    new_params["index"] = "0|"

    if service_id == "0":
        res = requests.post(mcs.services_url, json=new_params)
        service_id = res.json()["id"]
    else:
        res = requests.put(mcs.services_url + str(service_id) + "/", json=new_params)

    if res.status_code < 300:
        new_params = {}
        new_params["service_id"] = service_id
        new_params["categories"] = service_categories
        rse = requests.post(mcs.create_services_list_url, json=new_params)
        if res.status_code < 300:
            return HttpResponse("success")
        else:
            return HttpResponse("failure")
    else:
        return HttpResponse("failure")


def remove_service(request):
    """
    remove service
    :param request: contains service_id
    :return:
    """
    params = request.POST
    service_id = params["service_id"]

    new_params = {}
    new_params["service_id"] = service_id

    res = requests.post(mcs.delete_service_url, json=new_params)
    if res.status_code < 300:
        return HttpResponse("success")
    else:
        return HttpResponse("failure")


def get_service_price_by_id(request):
    """
    Get Service Price
    :param request: contains price_id
    :return:
    """
    params = request.POST
    price_id = params["price_id"]

    res = requests.get(mcs.prices_url + str(price_id) + "/")
    if res.status_code < 300:
        price = res.json()

        res = requests.get(mcs.services_url)
        services = res.json()["results"]
        service_name_map = {}
        for service in services:
            service_name_map[service["id"]] = service["name"]

        names_comb = []
        for item in json.loads(price["item_comb"]):
            if item in service_name_map:
                names_comb.append(service_name_map[item])

        price["names_comb"] = names_comb

        return HttpResponse(json.dumps(price))
    else:
        return HttpResponse("failure")


def bulk_update_price(request):
    """
    Bulk update price
    :param request: contains price_ids, price
    :return:
    """
    params = request.POST

    res = requests.post(mcs.bulk_update_prices_url, json=params)
    if res.status_code < 300:
        return HttpResponse("success")
    else:
        return HttpResponse("failure")


def softwares_view(request):
    """
    Render software page
    :param request:
    :return:
    """

    software_header_data = []
    software_header_data.append({"name": _("Software")})
    software_header_data.append({"name": _("Action")})

    res = requests.get(mcs.softwares_url)
    softwares = res.json()["results"]

    return render(request, "adminsettings/softwares.html", {
        "softwareheaderdata": software_header_data,
        "softwares": softwares
    })


def save_software(request):
    """
    save software
    :param request: file
    :return:
    """
    try:
        if request.method == 'POST':
            params = request.POST
            file_data = params["file_data"]
            file_name = params["file"]
            start = params["start"]
            last = params["last"]
            software_name = params["software_name"]

            file_path = "static/softwares/" + file_name

            if int(start) == 0:
                if os.path.exists(file_path):
                    os.remove(file_path)

            file = open(file_path, "ab")

            file.write(decode_chunk(file_data))

            if int(last) == 1:
                new_params = {}
                new_params["name"] = software_name
                new_params["path"] = file_path
                res = requests.post(mcs.softwares_url, json=new_params)
                if res.status_code < 300:
                    res = {"status": "success"}
                else:
                    res = {"status": "failure"}
            else:
                res = {"status": "success"}
        else:
            res = {"status": "fail"}

        return HttpResponse(json.dumps(res))
    except:
        mcm.print_exception()
        res = {"status": "fail"}
        return HttpResponse(json.dumps(res))


def decode_chunk(file_data):
    data = file_data.split(";base64,")
    return base64.b64decode(data[1])


def get_software_by_id(request):
    """
    get software path by id
    :param request: contains software_id
    :return:
    """
    params = request.POST
    software_id = params["software_id"]

    res = requests.get(mcs.softwares_url + str(software_id) + "/")
    software = res.json()

    if res.status_code < 300:
        return HttpResponse(json.dumps(software))

    else:
        return HttpResponse("failure")


def remove_software(request):
    """
    remove software
    :param request:  contains software id
    :return:
    """
    params = request.POST
    software_id = params["software_id"]

    res = requests.delete(mcs.softwares_url + str(software_id) + "/")
    if res.status_code < 300:
        return HttpResponse("success")
    else:
        return HttpResponse("failure")


def orders_view(request):
    """
    Show Orders List to admin
    :param request:
    :return:
    """
    header_data = []
    header_data.append({"name": _("User")})
    header_data.append({"name": _("Service")})
    header_data.append({"name": _("Category")})
    header_data.append({"name": _("Description")})
    header_data.append({"name": _("Price")})
    header_data.append({"name": _("Pay Status")})
    header_data.append({"name": _("Service Status")})
    header_data.append({"name": _("Paid Price")})
    header_data.append({"name": _("Date Booked")})
    header_data.append({"name": _("Date Created")})
    header_data.append({"name": _("Date Paid")})
    header_data.append({"name": _("Comment")})
    header_data.append({"name": _("Review")})
    header_data.append({"name": _("Score")})
    header_data.append({"name": _("Booked")})
    header_data.append({"name": _("Action")})

    return render(request, 'adminsettings/orders.html', {
        'headerdata': header_data
    })


def orders_datatable_api(request):
    """
    Orders Datatable for Admin
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

    users = mcm.get_users(request)
    users_name_map = {}
    for user in users:
        users_name_map[user["id"]] = user["username"]

    user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])
    url = mcs.orders_url

    response = requests.request(request.method, url, **requests_args)
    content = json.loads(response.content)
    for item in content["data"]:
        if item["userid"] in users_name_map:
            item["username"] = users_name_map[item["userid"]]

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


def get_order_by_id(request):
    """
    Get Order Data by order_id
    :param request: contains order_id
    :return:
    """
    params = request.POST
    order_id = params["order_id"]

    res = requests.get(mcs.orders_url + str(order_id) + "/")
    if res.status_code < 300:
        order_data = res.json()

        users = mcm.get_users(request)
        users_name_map = {}
        for user in users:
            users_name_map[user["id"]] = user["username"]

        order_data["username"] = users_name_map[order_data["userid"]]

        services = mcm.get_services(request)
        services_name_map = {}
        for service in services:
            services_name_map[service["id"]] = service["name"]

        order_data["service_name"] = services_name_map[order_data["service_id"]]
        for item in json.loads(order_data["category_type"]):
            order_data["service_name"] += "/" + services_name_map[item]

        return HttpResponse(json.dumps(order_data))
    else:
        return HttpResponse("failure")


def save_comment(request):
    """
    Save Comment
    :param request: contains order_id & comment
    :return:
    """
    params = request.POST
    order_id = params["order_id"]
    price = params["price"]
    comment = params["comment"]

    new_params = {
        "price": price,
        "comment": comment
    }
    res = requests.put(mcs.orders_url + str(order_id) + "/", json=new_params)
    if res.status_code < 300:
        return HttpResponse("success")
    else:
        return HttpResponse("failure")


def accept_order(request):
    """
    Accept Order From Customer
    :param request: contains order_id
    :return:
    """
    params = request.POST
    order_id = params["order_id"]

    user_level = mcm.decrypt(request.session[mcm.encrypt("userlevel")])

    order_info = mcm.get_order(request, order_id)
    if user_level != 1:
        return HttpResponse("no_permission")

    if order_info != {} and order_info["service_status"] == 0:
        res = requests.put(mcs.orders_url + str(order_id) + "/", json={"service_status": 1})
        if res.status_code < 300:
            return HttpResponse("success")

    return HttpResponse("failure")


def cancel_accept_order(request):
    """
    Cancel the acceptance of selected order
    :param request: contains order_id
    :return:
    """
    params = request.POST
    order_id = params["order_id"]

    user_level = mcm.decrypt(request.session[mcm.encrypt("userlevel")])

    order_info = mcm.get_order(request, order_id)
    if user_level != 1:
        return HttpResponse("no_permission")

    if order_info != {} and order_info["service_status"] == 1:
        res = requests.put(mcs.orders_url + str(order_id) + "/", json={"service_status": 0})
        if res.status_code < 300:
            return HttpResponse("success")

    return HttpResponse("failure")


def reject_order(request):
    """
    Reject selected order
    :param request: contains order_id
    :return:
    """
    params = request.POST
    order_id = params["order_id"]

    user_level = mcm.decrypt(request.session[mcm.encrypt("userlevel")])

    order_info = mcm.get_order(request, order_id)
    if user_level != 1:
        return HttpResponse("no_permission")

    if order_info != {} and order_info["service_status"] == 0:
        res = requests.put(mcs.orders_url + str(order_id) + "/", json={"service_status": 4})
        if res.status_code < 300:
            return HttpResponse("success")

    return HttpResponse("failure")


def finish_order(request):
    """
    Finish Order
    :param request: contains order_id
    :return:
    """
    params = request.POST
    order_id = params["order_id"]

    user_level = mcm.decrypt(request.session[mcm.encrypt("userlevel")])

    order_info = mcm.get_order(request, order_id)
    if user_level != 1:
        return HttpResponse("no_permission")

    if order_info != {} and order_info["service_status"] == 1:
        res = requests.put(mcs.orders_url + str(order_id) + "/", json={"service_status": 3})
        if res.status_code < 300:
            return HttpResponse("success")

    return HttpResponse("failure")


def get_off_days(request):
    """
    Get All Off Days
    :param request:
    :return:
    """
    off_days = mcm.get_off_days(request)
    return HttpResponse(json.dumps(off_days))


def add_new_off_day(request):
    """
    Add New Off Day
    :param request: contains off_day(%Y/%m/%d)
    :return:
    """
    params = request.POST
    off_day = params["off_day"]

    user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])

    new_params = {
        "userid": user_id,
        "off_day": off_day
    }

    off_days = mcm.get_off_days(request)

    for day in off_days:
        if day["off_day"] == off_day:
            return HttpResponse("duplicated")

    res = requests.post(mcs.off_days_url, json=new_params)
    if res.status_code < 300:
        off_days.append(new_params)
        return HttpResponse(json.dumps(off_days))
    else:
        return HttpResponse("failure")


def remove_off_day(request):
    """
    Remove Off Day
    :param request: contains off_day_id
    :return:
    """
    params = request.POST
    off_day_id = params["off_day_id"]

    res = requests.delete(mcs.off_days_url + str(off_day_id) + "/")
    if res.status_code < 300:
        return HttpResponse("success")
    else:
        return HttpResponse("failure")


def show_calendar_view(request):
    """
    Show Calendar View
    :param request:
    :return:
    """
    return render(request, "adminsettings/calendar_view.html")

def get_admin_calendar_data(request):
    """
    Get Orders and Off days
    :param request:
    :return:
    """

    # check if the request is admins'
    user_id = mcm.decrypt(request.session[mcm.encrypt("userid")])
    user_level = mcm.decrypt(request.session[mcm.encrypt("userlevel")])

    if user_level != 1:
        return HttpResponse("access_denied")

    orders = mcm.get_all_orders(request)
    off_days = mcm.get_off_days(request)
    data = {
        "orders": orders,
        "off_days": off_days
    }

    return HttpResponse(json.dumps(data))

def export_booking(request):
    """
    Export Booking Data
    :param request: contains export_from, export_to, export_type
    :return:
    """
    params = request.POST
    export_from = params["export_from"]
    export_to = params["export_to"]
    export_type = params["export_type"]

    user_level = mcm.decrypt(request.session[mcm.encrypt("userlevel")])

    if user_level != 1:
        return HttpResponse("access_denied")

    # make users map
    users = mcm.get_users(request)
    user_map = {}
    for user in users:
        user_map[user["id"]] = user["first_name"] + " " + user["last_name"]

    # services_name_map
    services = mcm.get_services(request)
    services_name_map = {}
    for service in services:
        services_name_map[service["id"]] = service["name"]

    res = requests.get(mcs.orders_url + "?from=" + export_from + "&to=" + export_to)
    if res.status_code >= 300:
        return HttpResponse("failure")

    orders = res.json()["results"]
    orders.sort(key=mcm.sortDateBooked)

    cnt = 1
    for order in orders:
        order["no"] = cnt
        cnt += 1
        if order["userid"] in user_map:
            order["username"] = user_map[order["userid"]]

        if order["service_id"] in services_name_map:
            order["service_name"] = services_name_map[order["service_id"]]

            categories = json.loads(order["category_type"])
            for cg in categories:
                order["service_name"] += " / " + services_name_map[cg]

        if order["service_status"] == 0:
            order["service_status_name"] = "Created"
        elif order["service_status"] == 1:
            order["service_status_name"] = "Accepted"
        elif order["service_status"] == 2:
            order["service_status_name"] = "Cancelled by user"
        elif order["service_status"] == 3:
            order["service_status_name"] = "Finished"
        elif order["service_status"] == 4:
            order["service_status_name"] = "Rejected by admin"

        order["date_created"] = order["date_created"][0:10] + " " + order["date_created"][11:19]
        order["date_booked"] = order["date_booked"][0:10] + " " + order["date_booked"][11:19]

    if export_type == "excel":
        directory_name = "static/export_files/1cbpcj0FIzrq/"
        excel_filename = directory_name + "/" + "export_orders_" + datetime.today().strftime("%m-%d-%Y") + ".xlsx"

        context = {'contentAlias': 'exportorders',
                   'request': request,
                   'param': orders,
                   'export_from': export_from,
                   'export_to': export_to}

        excel.render_excel(context, excel_filename)
        return HttpResponse(excel_filename)


    if export_type == "pdf":
        directory_name = "static/export_files/2cbpcj0FIzrq/"
        pdf_filename = directory_name + "/" + "export_orders_" + datetime.today().strftime("%m-%d-%Y") + ".pdf"

        context = {'contentAlias': 'exportorders',
                   'request': request,
                   'param': orders,
                   'export_from': export_from,
                   'export_to': export_to}

        pdf.render_pdf(context, pdf_filename)
        return HttpResponse(pdf_filename)

    return HttpResponse("failure")