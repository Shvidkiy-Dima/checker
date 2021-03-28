import time
import aiohttp
from django.utils import timezone
from django.db import transaction
from monitor.models import Monitor, MonitorLog
from monitor.serializers import MonitorLogSerializer
from channels.db import database_sync_to_async
import logging
from background_service.workers.base import BaseWorker


logger = logging.getLogger(__name__)


class HttpWorker(BaseWorker):

    def get_monitors(self):
        return Monitor.objects.get_nearest().select_related('user').filter(monitor_type=Monitor.MonitorType.HTTP)

    def get_client_session(self, *args, **kwargs):
        return aiohttp.ClientSession()

    async def handle_response(self, response, monitor, response_time):
        return await self.write_to_db(response, monitor, response_time)

    @database_sync_to_async
    def write_to_db(self, response, monitor, response_time):
        with transaction.atomic():
            monitor.last_request = timezone.now()
            monitor.next_request = timezone.now() + monitor.interval
            monitor.save(update_fields=['last_request', 'next_request'])
            m = MonitorLog.objects.create(response_code=response.status, response_time=response_time, monitor=monitor)
            print('New log was created')
            data = MonitorLogSerializer(m).data
            return data

