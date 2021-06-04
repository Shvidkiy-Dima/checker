import aiohttp
from aiohttp import ClientSession, ClientTimeout
from django.db import transaction
from django.utils import timezone
from background_service.fetcher.workers.base import BaseWorker
from monitor.models import MonitorLog, Monitor
from monitor.serializers import MonitorLogSerializer
from channels.db import database_sync_to_async


class HtmlCheckWorker(BaseWorker):

    @classmethod
    def get_monitors(cls):
        return Monitor.objects.get_nearest().filter(monitor_type=Monitor.MonitorType.HTML)

    def start_request(self, session: ClientSession, url, timeout=5, method='get'):
        timeout = ClientTimeout(total=timeout)
        return session.request(method, url, timeout=timeout)

    async def handle_response(self, response, monitor, response_time, body):
        return await self.write_to_db(response, monitor, response_time, body)

    def get_client_session(self, *args, **kwargs):
        return aiohttp.ClientSession()

    @database_sync_to_async
    def write_to_db(self, response, monitor, response_time, body):
        with transaction.atomic():
            monitor.last_request = timezone.now()
            monitor.next_request = timezone.now() + monitor.interval
            monitor.save(update_fields=['last_request', 'next_request'])

            log = self.make_log(monitor, response_time,  body, response_code=response.status)

            data = MonitorLogSerializer(log).data
            return data

    def make_log(self, monitor, response_time, body=b'', error=None, response_code=None):
        keyword = monitor.keyword.encode()
        is_there_key = keyword in body
        log = MonitorLog.objects.create(response_code=response_code, response_time=response_time,
                                        monitor=monitor, keyword=is_there_key, error=error)
        return log
