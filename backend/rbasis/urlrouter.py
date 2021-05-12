__author__ = 'com'
from rest_framework import routers

class ApiRouter:
    router = routers.DefaultRouter()
    def register(self, regex, classobject, name, description):
        self.router.register(regex, classobject, name, description)
    def urls(self):
        return self.router.urls

router = ApiRouter()

