__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('messages_view', views.messages_view, name='messages_view'),
    path('get_message_history', views.get_message_history, name='get_message_history'),
    path('update_message_status', views.update_message_status, name='update_message_status'),
    path('get_instantmessage_history', views.get_instantmessage_history, name='get_instantmessage_history'),
]