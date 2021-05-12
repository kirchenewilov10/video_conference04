__author__ = 'com'
# from rest_framework import serializers
from .models import *
from rbasis.serializers import *

class contactusSerializer(ShAPISerializer):
    class Meta:
        model = contactus
        fields = ('id', 'name', 'email', 'content')

class devicetypesSerializer(ShAPISerializer):
    class Meta:
        model = devicetypes
        fields = ('id', 'name')

class menuTreeSerializer(ShAPISerializer):
    class Meta:
        model = menu_tree
        fields = ('id', 'parent_id', 'has_child', 'name', 'icon', 'url', 'level')

class offdaysSerializer(ShAPISerializer):
    class Meta:
        model = off_days
        fields = ('id', 'userid', 'off_day')

class ordersSerializer(ShAPISerializer):
    class Meta:
        model = orders
        fields = ('id', 'userid', 'service_id', 'category_type', 'description', 'price', 'pay_status', 'service_status', 'paid_price', 'date_created',
                  'date_paid', 'comment', 'review', 'score', 'user_response', 'booked', 'date_booked')

class ossSerializer(ShAPISerializer):
    class Meta:
        model = oss
        fields = ('id', 'name')

class roomSerializer(ShAPISerializer):
    class Meta:
        model = Room
        fields = ('id', 'users', 'source', 'timestamp', 'track', 'status')

class pricesSerializer(ShAPISerializer):
    class Meta:
        model = prices
        fields = ('id', 'service_id', 'item_comb', 'price')

class servicesSerializer(ShAPISerializer):
    class Meta:
        model = services
        fields = ('id', 'level', 'parentid', 'name', 'index')

class softwaresSerializer(ShAPISerializer):
    class Meta:
        model = softwares
        fields = ('id', 'name', 'path')

class transactionsSerializer(ShAPISerializer):
    class Meta:
        model = transactions
        fields = ('id', 'userid', 'deposit_date', 'mode', 'amount', 'tracking_number', 'description')

class tblUsersSerializer(ShAPISerializer):
    class Meta:
        model = tbl_user
        fields = ('id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_active', 'date_joined', 'phone', 'address1', 'address2', 'city', 'state', 'country',
                  'zipcode', 'parent_id', 'permission', 'image_path', 'deleted', 'spent_money', 'current_money',
                  'service_usable')
