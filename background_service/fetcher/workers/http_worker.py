import time
import aiohttp
from aiohttp import ClientSession, ClientTimeout
from django.utils import timezone
from django.db import transaction
from monitor.models import Monitor, MonitorLog
from monitor.serializers import MonitorLogSerializer
from channels.db import database_sync_to_async
import logging
from background_service.fetcher.workers.base import BaseWorker


logger = logging.getLogger()


class HttpWorker(BaseWorker):

    @classmethod
    def get_monitors(cls):
        return Monitor.objects.get_nearest().filter(monitor_type=Monitor.MonitorType.HTTP)

    def start_request(self, session: ClientSession, url, timeout=5, method='get'):
        timeout = ClientTimeout(total=timeout)
        return session.request(method, url, timeout=timeout)

    def get_client_session(self, *args, **kwargs):
        return aiohttp.ClientSession()

    async def handle_response(self, response, monitor, response_time, body):
        return await self.write_to_db(response, monitor, response_time)

    @database_sync_to_async
    def write_to_db(self, response, monitor, response_time):
        with transaction.atomic():
            monitor.last_request = timezone.now()
            monitor.next_request = timezone.now() + monitor.interval
            monitor.save(update_fields=['last_request', 'next_request'])
            log = self.make_log(monitor, response_time, response_code=response.status)
            data = MonitorLogSerializer(log).data
            return data
