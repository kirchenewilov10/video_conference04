__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('change_password_view', views.change_password_view, name='change_password_view'),
    path('change_user_password', views.change_user_password, name='change_user_password'),
    path('update_user_profile', views.update_user_profile, name='update_user_profile'),
    path('change_user_avatar', views.change_user_avatar, name='change_user_avatar'),
    path('set_language', views.set_language, name='set_language'),
]