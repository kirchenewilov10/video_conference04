__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('users_view', views.users_view, name='users_view'),
    path('users_datatable_api', views.users_datatable_api, name='users_datatable_api'),
    path('active_user_service', views.active_user_service, name='active_user_service'),
    path('user_transactions_datatable_api', views.user_transactions_datatable_api, name='user_transactions_datatable_api'),
]