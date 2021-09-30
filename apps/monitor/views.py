from typing import Tuple
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from monitor.models import Monitor
from monitor import serializers
from utils.views import SerializerMapMixin
from utils.async_drf.views import AsyncApiView
from channels.db import database_sync_to_async


class MonitorView(SerializerMapMixin, AsyncApiView, generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_map = {'get': serializers.ListMonitorSerializer,
                      'post': serializers.CreateMonitorSerializer}

    def get_queryset(self):
        return Monitor.objects.by_user(self.request.user).prefetch_for_day()\
            .annotate_avg_response_time().annotate_count_and_percent()

    async def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        await serializer.async_validate()
        data, serializer = await self.handle_serializer(serializer)
        return Response(data, status=status.HTTP_201_CREATED)

    @database_sync_to_async
    def handle_serializer(self, serializer: Serializer) -> Tuple[dict, Serializer]:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data, serializer


class MonitorDetailView(SerializerMapMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_map = {'get': serializers.DetailMonitorSerializer,
                      'patch': serializers.UpdateMonitorSerializer}

    def get_queryset(self):
        monitor_id = self.kwargs['pk']
        return Monitor.objects.by_user(self.request.user).prefetch_for_day()\
            .prefetch_interval(monitor_id).annotate_avg_response_time()\
            .annotate_count_and_percent()
