import aiohttp
from django.db import transaction
from django.utils import timezone
from background_service.workers.base import BaseWorker
from monitor.models import MonitorLog, Monitor
from monitor.serializers import MonitorLogSerializer
from channels.db import database_sync_to_async


class HtmlCheckWorker(BaseWorker):

    def get_monitors(self):
        return Monitor.objects.get_nearest().select_related('user').filter(monitor_type=Monitor.MonitorType.HTML)

    async def handle_response(self, response, monitor, response_time):
        body = await response.read()
        return await self.write_to_db(response, monitor, response_time, body)

    def get_client_session(self, *args, **kwargs):
        return aiohttp.ClientSession()

    @database_sync_to_async
    def write_to_db(self, response, monitor, response_time, body):
        with transaction.atomic():
            keyword = monitor.keyword.encode()
            monitor.last_request = timezone.now()
            monitor.next_request = timezone.now() + monitor.interval
            monitor.save(update_fields=['last_request', 'next_request'])

            is_there_key = keyword in body
            m = MonitorLog.objects.create(response_code=response.status, response_time=response_time,
                                          monitor=monitor, keyword=is_there_key)

            print('New log was created')
            data = MonitorLogSerializer(m).data
            return data
