from django.db import models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class MessageModel(models.Model):
    """
    This class represents a chat message. It has a owner (user), timestamp and
    the message body.

    """

    userid = models.IntegerField(blank=True)
    recipientid = models.IntegerField(blank=True)
    timestamp = models.DateTimeField('timestamp', auto_now_add=True, editable=False,db_index=True)
    body = models.TextField('body')
    status = models.IntegerField(blank=True, default=0)
    type = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.id)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.body)

    def notify_ws_clients(self):
        """
        Inform clients there is a new message.
        """
        if self.type == 'BLOB':
            self.id = -1 * self.userid
        notification = {
            'type': 'receive_group_message',
            'message': '{}'.format(self.id),
            'session_type': 'registered'
        }

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)("{}".format(self.userid), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipientid), notification)

    def notify_ws_video_recipient(self):
        """
        Send message to recipient on video chatting
        :return:
        """
        notification = {
            'type': 'receive_group_message',
            'message': self.body,
            'session_type': 'video_chatting'
        }
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)("{}".format(self.userid), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipientid), notification)


    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.body = self.body.strip()  # Trimming whitespaces from the body
        if self.type != 'BLOB' and self.type != 'VIDEO':
            super(MessageModel, self).save(*args, **kwargs)
        if new is None:
            if self.type == 'VIDEO':
                self.notify_ws_video_recipient()
            else:
                self.notify_ws_clients()

    # Meta
    class Meta:
        app_label = 'chat'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-timestamp',)
