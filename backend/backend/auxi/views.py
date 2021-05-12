import json
import itertools
from django.http import JsonResponse
from backend.basic.serializers import *
from django.db import transaction as transaction_orm
from datetime import datetime

# Create your views here.

def UiResponse(data={}, status=200):
    return JsonResponse(data=data, status=status)
    # return HttpResponse(data=data, status=status)

# def delete_multi_rtumodems(request):
#     try:
#         with transaction_orm.atomic():
#             rparams = json.loads(request.body.decode())
#             selected_items = json.loads(rparams["selected_items"])
#             userid = rparams["userid"]
#             tbl_rtu_modems.objects.filter(pk__in=selected_items, user=userid).delete()
#
#         return UiResponse({'result': 'OK'}, 200)  # success
#     except Exception as e:
#         print(e)
#         mcm.print_log(request, "delete_multi_rtumodems", str(e))
#         return UiResponse({'result': 'FL'}, 500)


def get_admins_v2(request):
    """
    get admins list by using query
    :param request: contains query from frontend
    :return: admins list
    """
    try:
        with transaction_orm.atomic():
            rparams = json.loads(request.body.decode())
            query = rparams["query"]

            admin_list = list(tbl_user.objects.filter(is_superuser=1).values(*query))

        return UiResponse({'result': admin_list}, 200)
    except Exception as e:
        print(e)
        return UiResponse({'result': 'FL'}, 500)


def get_users_v2(request):
    """
    get users list by using query
    :param request: contains query from frontend
    :return: users list
    """
    try:
        with transaction_orm.atomic():
            rparams = json.loads(request.body.decode())
            query = rparams["query"]

            user_list = list(tbl_user.objects.filter().values(*query))

        return UiResponse({'result': user_list}, 200)
    except Exception as e:
        print(e)
        return UiResponse({'result': 'FL'}, 500)


def create_services_list(request):
    """
    Create Service Category List
    :param request:
    :return:
    """
    try:
        with transaction_orm.atomic():
            rparams = json.loads(request.body.decode())
            service_id = rparams["service_id"]
            categories = rparams["categories"]

            # first, delete the records related with service_id
            services.objects.filter(index__contains=f"|{service_id}|").delete()
            prices.objects.filter(service_id=service_id).delete()

            # create service
            items_array = []
            for category in categories:
                new_params = {}
                new_params["parentid"] = service_id
                new_params["level"] = 1
                new_params["name"] = category["name"]
                new_params["index"] = f"0|{service_id}|"

                services_obj = services(**new_params)
                services_obj.save()

                category_id = services_obj.id
                category_items = []
                for item in category["items"]:
                    new_params = {}
                    new_params["parentid"] = category_id
                    new_params["level"] = 2
                    new_params["name"] = item
                    new_params["index"] = f"0|{service_id}|{category_id}|"

                    services_obj = services(**new_params)
                    services_obj.save()
                    category_items.append(services_obj.id)

                items_array.append(category_items)

            # make price list
            combinations = list(itertools.product(*items_array))
            for cb in combinations:
                new_params = {
                    "item_comb": json.dumps(cb),
                    "price": 0,
                    "service_id": service_id
                }
                prices_obj = prices(**new_params)
                prices_obj.save()

            if len(combinations) == 0:
                new_params = {
                    "item_comb": "[]",
                    "price": 0,
                    "service_id": service_id
                }
                prices_obj = prices(**new_params)
                prices_obj.save()


        return UiResponse({'result': 'OK'}, 200)
    except Exception as e:
        print(e)
        return UiResponse({'result': 'FL'}, 500)


def get_service_by_id(request):
    """
    Get Service By Id
    :param request: Contains Service_id
    :return:
    """
    try:
        with transaction_orm.atomic():
            rparams = json.loads(request.body.decode())
            service_id = rparams["service_id"]

            service = {}
            services_list = list(services.objects.filter(pk=service_id).values())
            if len(services_list) > 0:
                service = services_list[0]

                categories = list(services.objects.filter(parentid=service_id).values())
                for ctg in categories:
                    items = list(services.objects.filter(parentid=ctg["id"]).values())
                    ctg["items"] = []
                    for item in items:
                        ctg["items"].append(item["name"])
                service["categories"] = categories


        return UiResponse({'result': service}, 200)

    except Exception as e:
        print(e)
        return UiResponse({'result': 'FL'}, 500)


def delete_service(request):
    """
    Delete Service
    :param request:
    :return:
    """
    try:
        with transaction_orm.atomic():
            rparams = json.loads(request.body.decode())
            service_id = rparams["service_id"]

            services.objects.filter(pk=service_id).delete()
            services.objects.filter(index__contains=f"|{service_id}|").delete()
            prices.objects.filter(service_id=service_id).delete()

        return UiResponse({'result': 'OK'}, 200)

    except Exception as e:
        print(e)
        return UiResponse({'result': 'FL'}, 500)


def bulk_update_prices(request):
    """
    Bulk Update Prices
    :param request:
    :return:
    """
    try:
        with transaction_orm.atomic():
            rparams = json.loads(request.body.decode())
            price_ids = json.loads(rparams["price_ids"])
            price = rparams["price"]

            prices.objects.filter(pk__in=price_ids).update(price=price)

        return UiResponse({'result': 'OK'}, 200)

    except Exception as e:
        print(e)
        return UiResponse({'result': 'FL'}, 500)


def make_order(request):
    """
    Make Order
    :param request:
    :return:
    """
    try:
        with transaction_orm.atomic():
            rparams = json.loads(request.body.decode())
            userid = rparams["userid"]
            services_param = rparams["services"]

            for service in services_param:
                new_params = {}
                new_params["userid"] = userid
                new_params["service_id"] = service["service_id"]
                new_params["price"] = service["price"]
                new_params["pay_status"] = 0
                new_params["service_status"] = 0
                new_params["paid_price"] = 0
                if rparams["active_booking"] == "1":
                    new_params["date_booked"] = rparams["booking_datetime"]
                else:
                    new_params["date_booked"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")

                new_params["date_created"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
                new_params["category_type"] = service["categories"]
                new_params["description"] = service["description"]
                new_params["booked"] = rparams["active_booking"]

                new_order_obj = orders(**new_params)
                new_order_obj.save()

        return UiResponse({'result': 'OK'}, 200)

    except Exception as e:
        print(e)
        return UiResponse({'result': 'FL'}, 500)