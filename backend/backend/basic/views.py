import json
from django.http import HttpResponse
from rest_framework.response import Response
from rbasis.views import *
from .models import *
import random
from .serializers import *
from backend.basic.constant import *
from django.db.models import Q

# Create your views here.
class contactusView(ShAPIView):
    queryset = contactus.objects.all()
    serializer_class = contactusSerializer
    pass

class devicetypesView(ShAPIView):
    queryset = devicetypes.objects.all()
    serializer_class = devicetypesSerializer
    pass

class menu(ShAPIView):
    queryset = menu_tree.objects.all()
    serializer_class = menuTreeSerializer
    pass

class offdaysView(ShAPIView):
    queryset = off_days.objects.all()
    serializer_class = offdaysSerializer
    pass

class ordersView(ShAPIView):
    queryset = orders.objects.all()
    serializer_class = ordersSerializer

    def list(self, request, *args, **kwargs):
        if len(request.query_params) == 0:
            return super().list(request, args, kwargs)

        params = request.query_params

        orders_obj = orders.objects.all()

        if "userid" in params:
            orders_obj = orders_obj.filter(userid=params["userid"])
        if "service_id" in params:
            orders_obj = orders_obj.filter(service_id=params["service_id"])
        if "pay_status" in params:
            orders_obj = orders_obj.filter(pay_status=params["pay_status"])
        if "service_status" in params:
            orders_obj = orders_obj.filter(service_status=params["service_status"])

        if "booked_date" in params:
            start_date = params["booked_date"] + " 00:00:00"
            end_date = params["booked_date"] + " 23:59:59"
            orders_obj = orders_obj.filter(date_booked__gte=start_date, date_booked__lte=end_date)

        if "from" in params:
            start_date = params["from"] + " 00:00:00"
            orders_obj = orders_obj.filter(date_booked__gte=start_date)

        if "to" in params:
            end_date = params["to"] + " 23:59:59"
            orders_obj = orders_obj.filter(date_booked__lte=end_date)

        self.queryset = orders_obj

        return super().list(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = True
            return super().update(request, args, **kwargs)
        except Exception as e:
            return self.log(e)

class ossView(ShAPIView):
    queryset = oss.objects.all()
    serializer_class = ossSerializer
    pass

class pricesView(ShAPIView):
    queryset = prices.objects.all()
    serializer_class = pricesSerializer

    def list(self, request, *args, **kwargs):
        if len(request.query_params) == 0:
            return super().list(request, args, kwargs)

        params = request.query_params

        prices_obj = prices.objects.all()
        if "id" in request.query_params:
            prices_obj = prices_obj.filter(id=params["id"])
        if "service_id" in request.query_params:
            prices_obj = prices_obj.filter(service_id=params["service_id"])
        if "item_comb" in request.query_params:
            prices_obj = prices_obj.filter(item_comb=params["item_comb"])

        self.queryset = prices_obj

        return super().list(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = True
            return super().update(request, args, **kwargs)
        except Exception as e:
            return self.log(e)


class roomView(ShAPIView):
    queryset = Room.objects.all()
    serializer_class = roomSerializer
    pass


class servicesView(ShAPIView):
    queryset = services.objects.all()
    serializer_class = servicesSerializer

    def list(self, request, *args, **kwargs):
        if len(request.query_params) == 0:
            return super().list(request, args, kwargs)

        params = request.query_params

        services_obj = services.objects.all()
        if "id" in request.query_params:
            services_obj = services_obj.filter(id=params["id"])
        if "parentid" in request.query_params:
            services_obj = services_obj.filter(parentid=params["parentid"])
        if "level" in request.query_params:
            services_obj = services_obj.filter(level=params["level"])
        if "index" in request.query_params:
            services_obj = services_obj.filter(index__contains=f"|{params['index']}|")

        self.queryset = services_obj

        return super().list(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = True
            return super().update(request, args, **kwargs)
        except Exception as e:
            return self.log(e)


class softwaresView(ShAPIView):
    queryset = softwares.objects.all()
    serializer_class = softwaresSerializer
    pass


class transactionsView(ShAPIView):
    queryset = transactions.objects.all()
    serializer_class = transactionsSerializer

    def list(self, request, *args, **kwargs):
        if len(request.query_params) == 0:
            return super().list(request, args, kwargs)

        params = request.query_params

        if "id" in request.query_params:
            self.queryset = transactions.objects.filter(id=params["id"])
        elif "userid" in request.query_params:
            self.queryset = transactions.objects.filter(userid=params["userid"])

        return super().list(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = True
            return super().update(request, args, **kwargs)
        except Exception as e:
            return self.log(e)


class tblusersView(ShAPIView):
    queryset = tbl_user.objects.all()
    serializer_class = tblUsersSerializer

    def list(self, request, *args, **kwargs):
        if len(request.query_params) == 0:
            return super().list(request, args, kwargs)

        params = request.query_params

        if "id" in request.query_params:
            self.queryset = tbl_user.objects.filter(id=params["id"])
        elif "username" in request.query_params:
            self.queryset = tbl_user.objects.filter(username=params["username"])
        elif ("email" in request.query_params) and ("password" in request.query_params):
            self.queryset = tbl_user.objects.filter(email=params["email"], password=params["password"])
        elif "userid" in request.query_params and "is_superuser" in request.query_params:
            self.queryset = tbl_user.objects.filter(id=params["userid"], is_superuser=params["is_superuser"])
        elif "email" in request.query_params:
            self.queryset = tbl_user.objects.filter(email=params["email"])
        elif "is_superuser" in request.query_params:
            self.queryset = tbl_user.objects.filter(is_superuser=params["is_superuser"])

        return super().list(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, args, **kwargs)
        except Exception as e:
            return self.log(e)

    def update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = True
            return super().update(request, args, **kwargs)
        except Exception as e:
            return self.log(e)
