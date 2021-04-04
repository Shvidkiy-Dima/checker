from rest_framework import generics, permissions, exceptions
from monitor.models import Monitor
from monitor import serializers
from utils.views import SerializerMapMixin
from utils.async_drf.views import AsyncCreateViewMixin, AsyncApiView
from monitor.services.base import monitor_first_request


class MonitorView(SerializerMapMixin, AsyncApiView, AsyncCreateViewMixin, generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_map = {'get': serializers.ListMonitorSerializer,
                      'post': serializers.CreateMonitorSerializer}

    def get_queryset(self):
        return Monitor.objects.by_user(self.request.user).available()

    async def end_async_view(self, data, serializer, request, *args, **kwargs):
        monitor = serializer.instance
        try:
            data = await monitor_first_request(monitor, monitor.worker())
        except Exception as e:
            monitor.delete()
            raise exceptions.APIException(f'Something was wrong {e}')

        return data


class MonitorDetailView(SerializerMapMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_map = {'get': serializers.ListMonitorSerializer,
                      'patch': serializers.UpdateMonitorSerializer}

    def get_queryset(self):
        return Monitor.objects.by_user(self.request.user).available()
