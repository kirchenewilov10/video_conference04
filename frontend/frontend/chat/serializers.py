from frontend.chat.models import MessageModel
from rest_framework.serializers import ModelSerializer
from frontend.common import constant as mcs
import tempfile
import shutil
import os
import json
from datetime import datetime


class MessageModelSerializer(ModelSerializer):

    def create(self, validated_data):
        request = self.context['request']
        type = validated_data['type']
        if type == 'TEXT':
            msg = MessageModel(recipientid=validated_data['recipientid'],
                               body=validated_data['body'],
                               userid=validated_data['userid'],
                               type=type)
            msg.save()
            return msg
        elif type == 'VIDEO':
            msg = MessageModel(recipientid=validated_data['recipientid'],
                               body=validated_data['body'],
                               userid=validated_data['userid'],
                               type=type)
            msg.save()
            return msg
        elif type == 'NOTI':
            msg = MessageModel(recipientid=validated_data['recipientid'],
                               body=validated_data['body'],
                               userid=validated_data['userid'],
                               type=type,
                               status=1)
            msg.save()
            return msg
        elif type == 'FILE':
            file = request.FILES.getlist('image')[0]

            tup = tempfile.mkstemp()
            f = os.fdopen(tup[0], 'wb')
            f.write(file.read())
            f.close()

            tup_path = str(tup[1])
            str_file = str(file)

            chatmsg_directory_name = "static/attach_files/1c29dkfhwid2/" + \
                                    datetime.now().strftime("%Y-%m-%d") + "/"
            if not os.path.exists(chatmsg_directory_name):
                os.makedirs(chatmsg_directory_name)

            real_path = chatmsg_directory_name + str_file
            shutil.move(tup_path, real_path)
            real_path = mcs.ui_url + real_path
            body_data = {'path': real_path, 'name': str_file}
            msg = MessageModel(recipientid=validated_data['recipientid'],
                               body=json.dumps(body_data),
                               userid=validated_data['userid'],
                               type=type)
            msg.save()
            return msg
        elif type == 'BLOB':
            msg = MessageModel(recipientid=validated_data['recipientid'],
                               body=validated_data['body'],
                               userid=validated_data['userid'],
                               type=type)
            msg.save()
            return msg
    class Meta:
        model = MessageModel
        fields = ('id', 'userid', 'recipientid', 'timestamp', 'body', 'status', 'type')
