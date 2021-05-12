__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('userregister', views.userregister, name='register'),
    path('userlogin', views.userlogin, name='login'),
    path('forget_password', views.forget_password, name='forget_password'),
    path('logout', views.userlogout, name='logout'),
    path('index', views.indexView, name='index'),
    path('set_language', views.set_language, name='set_language'),
    path('send_message', views.send_message, name='send_message'),
    path('get_service_categories', views.get_service_categories, name='get_service_categories'),
    path('get_price_by_category', views.get_price_by_category, name='get_price_by_category'),
    path('orders_datatable_api', views.orders_datatable_api, name='orders_datatable_api'),
    path('make_order', views.make_order, name='make_order'),
    path('get_order_comment_and_response', views.get_order_comment_and_response, name='get_order_comment_and_response'),
    path('send_order_response', views.send_order_response, name='send_order_response'),
    path('cancel_order', views.cancel_order, name='cancel_order'),
    path('get_book_setting', views.get_book_setting, name='get_book_setting'),
    path('get_unable_time_list', views.get_unable_time_list, name='get_unable_time_list'),

    path('handler_401', views.handler401View, name='handler_401'),
    path('handler_403', views.handler403View, name='handler_403'),
    path('handler_440', views.handler440View, name='handler_440'),

]
