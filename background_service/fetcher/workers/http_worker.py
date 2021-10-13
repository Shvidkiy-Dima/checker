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
        return Monitor.objects.get_nearest().all().prefetch_related().annotate_avg_response_time()

    def start_request(self, session: ClientSession, url, timeout=5, method='get'):
        timeout = ClientTimeout(total=timeout)
        return session.request(method, url, timeout=timeout)

    def get_client_session(self, *args, **kwargs):
        return aiohttp.ClientSession()

    async def handle_response(self, monitor: Monitor, body: bytes, response_time: float,  response_code: int) -> dict:
        return await self.write_to_db(monitor, response_time, response_code)

    @database_sync_to_async
    def write_to_db(self, monitor: Monitor, response_time: float, response_code: int) -> dict:

        with transaction.atomic():
            monitor.last_request = timezone.now()
            monitor.next_request = timezone.now() + monitor.interval
            monitor.save(update_fields=['last_request', 'next_request'])
            log = self.make_log(monitor, response_time, error=None,
                                is_successful=True, response_code=response_code)
            data = MonitorLogSerializer(log).data
            return data
