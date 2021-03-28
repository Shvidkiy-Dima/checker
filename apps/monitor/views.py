from rest_framework import generics, permissions
from monitor.models import Monitor
from monitor import serializers
from utils.views import SerializerMapMixin


class MonitorView(SerializerMapMixin, generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_map = {'get': serializers.ListMonitorSerializer,
                      'post': serializers.CreateMonitorSerializer}

    def get_queryset(self):
        return Monitor.objects.by_user(self.request.user)
