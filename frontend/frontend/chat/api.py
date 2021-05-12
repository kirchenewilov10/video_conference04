from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication
from frontend import settings
from frontend.chat.models import MessageModel
from frontend.chat.serializers import MessageModelSerializer
from frontend.common import common as mcm
from datetime import datetime
class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """
    page_size = settings.MESSAGES_TO_LOAD


class MessageModelViewSet(ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    #authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        target = int(self.request.query_params.get('target', None))
        user = int(self.request.query_params.get('user', None))
        if target is not None and user is not None:
            self.queryset = self.queryset.filter(
                Q(recipientid=user, userid=target) |
                Q(recipientid=target, userid=user))
        res =  super(MessageModelViewSet, self).list(request, *args, **kwargs)
        res = self.get_date_formated(request, res)
        return res

    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)
        res = serializer.data
        res = self.get_date_formated_retrieve(request, res)
        return Response(res)

    def update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = True
            res = super().update(request, args, **kwargs)
            return res
        except Exception as e:
            return self.log(e)

    def create(self, request, *args, **kwargs):
        try:
            params = request.POST
            file_check = 0
            if "type" in params and params['type'] == 'FILE':
                file = request.FILES.getlist('image')[0]
                file_name = file.name
                namesparray = file_name.split('.')
                file_ext = namesparray[len(namesparray) - 1]
                file_size = file.size

                if file_size > 200 * (2 ** 20):
                    file_check = 1

            if file_check:
                if file_check == 1:
                    return Response(data='FILE_SIZE_ERROR')
            else:
                return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(data='ERROR')

    def get_date_formated(self, request, res):
        time_zone = mcm.get_time_zone(request)
        for item in res.data['results']:
            msg_date = datetime.strptime(item['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
            # item['timestamp'] = mcm.change_time_zone(request, msg_date, time_zone, 1, "%m-%d-%Y %I:%M %p")
            item['timestamp'] = msg_date.strftime("%Y-%m-%dT%H:%M")
        return res

    def get_date_formated_retrieve(self, request, res):
        time_zone = mcm.get_time_zone(request)
        msg_date = datetime.strptime(res['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # res['timestamp'] = mcm.change_time_zone(request, msg_date, time_zone, 1, "%m-%d-%Y %I:%M %p")
        res['timestamp'] = msg_date.strftime("%Y-%m-%dT%H:%M")
        return res
