from django.urls import path, include
from django.conf.urls import url

from rest_framework.routers import DefaultRouter
from frontend.chat.api import MessageModelViewSet

from . import views

router = DefaultRouter()
router.register(r'message', MessageModelViewSet, base_name='message-api')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('instantmessage', views.instant_message, name='instantmessage'),
    path('show_chatroom', views.show_chatroom, name='show_chatroom'),
    path('show_admin_chatroom', views.show_admin_chatroom, name='show_admin_chatroom'),
]
