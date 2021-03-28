from django.db import models
from django.utils.translation import gettext_lazy as _


from push_notifications import models as device_models


class FCMDeviceManager(models.Manager):

    def get_queryset(self):
        qs = super().get_queryset()
        device_type = getattr(self.model, 'TYPE', None)
        if device_type:
            qs = qs.filter(type=device_type)

        return qs


class FCMDeviceQuerySet(device_models.GCMDeviceQuerySet):

    def by_user(self, user):
        return self.filter(user=user)


class FCMDevice(device_models.GCMDevice):

    class Type(models.Choices):
        IOS = 'ios'
        ANDROID = 'android'

    type = models.CharField(choices=Type.choices, max_length=10)
    objects = FCMDeviceManager.from_queryset(FCMDeviceQuerySet)()

    def unbound(self):
        self.user = None
        self.save(update_fields=['user'])


class FCMDeviceIos(FCMDevice):

    TYPE = FCMDevice.Type.IOS

    class Meta:
        proxy = True

    def send_background(self, data):
        data = {'data': data}
        self.send_message(None, content_available=True, priority='high', extra=data)


class FCMDeviceAndroid(FCMDevice):

    TYPE = FCMDevice.Type.ANDROID

    class Meta:
        proxy = True

    def send_background(self, data):
        data = {'data': data}
        self.send_message(None, content_available=True, priority='high', extra=data)

