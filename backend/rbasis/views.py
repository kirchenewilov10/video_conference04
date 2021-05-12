# Create your views here.
from rest_framework import viewsets
from backend.settings import DEBUG
from datetime import datetime, date, time
from rest_framework.response import *
from rest_framework.request import *

class ShAPIView(viewsets.ModelViewSet):

    def logHttp(self,request,*args,**kwargs):
        if(DEBUG):
            print("StrutsViewSet Log : request : ")
            print(request)
            print("StrutsViewSet Log : args : ")
            print(args)
            print("StrutsViewSet Log : kwargs : ")
            print(kwargs)

        # --- log into database in future --- #
        logtime =datetime.now()
        #requester=request._request.META['REMOTE_ADDR']
        #requesturl=request._request.META['PATH_INFO']
        #requestmethod=request._request.META['REQUEST_METHOD']
        #requestdata=""

        #functions.getLocalNetworkAddress()

        print(logtime)

    def list(self, request, *args, **kwargs):
        res = super().list(request,args,kwargs)
        return res

    def update(self, request, *args, **kwargs):
        res = super().update(request,args,**kwargs)
        return res

    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request,args,kwargs)
        return res

    def destroy(self, request, *args, **kwargs):
        res = super().destroy(request,args,kwargs)
        return res

    def partial_update(self, request, *args, **kwargs):
        res = super().partial_update(request,args,kwargs)
        return res

    def create(self, request, *args, **kwargs):
        res = super().create(request,args,kwargs)
        return res