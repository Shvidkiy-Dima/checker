from rest_framework import serializers
from device import models
from push_notifications.api.rest_framework import GCMDeviceSerializer


class FCMDeviceSerializer(GCMDeviceSerializer):
    cloud_message_type = serializers.HiddenField(default="FCM")

    class Meta(GCMDeviceSerializer.Meta):
        model = models.FCMDevice
        fields = ("id", "name", "registration_id", "device_id",
                  'type', 'cloud_message_type')
