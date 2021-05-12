__author__ = 'com'
from rest_framework import serializers


class ShAPISerializer(serializers.HyperlinkedModelSerializer):
    def log(self):
        return None
