
# chat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from frontend.common import common as mcm


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        group_name = "public"

        if mcm.encrypt("ipaddress") in self.scope["session"]:
            group_name = mcm.decrypt(self.scope["session"][mcm.encrypt("ipaddress")])

        if mcm.encrypt("userid") in self.scope["session"]:
            group_name = mcm.decrypt(self.scope["session"][mcm.encrypt("userid")])

        self.group_name = "{}".format(group_name)
        # Join room group

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data = None):

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        session_type = text_data_json['session_type']
        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'receive_group_message',
                'message': message,
                'session_type': session_type
            }
        )

    async def receive_group_message(self, event):
        message = event['message']
        session_type = event['session_type']
        # Send message to WebSocket
        await self.send(
             text_data=json.dumps({
                'message': message,
                'session_type': session_type
             })
        )