from rest_framework import generics
from rest_framework.permissions import AllowAny
from device import serializers, models
from push_notifications.api.rest_framework import DeviceViewSetMixin


class DeviceView(DeviceViewSetMixin, generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        self._save(serializer)

    def perform_update(self, serializer):
        self._save(serializer)

    def _save(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class FCMView(DeviceView):
    serializer_class = serializers.FCMDeviceSerializer
    queryset = models.FCMDevice.objects.all()
