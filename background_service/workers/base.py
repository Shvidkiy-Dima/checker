import asyncio
import time
from abc import ABC, abstractmethod
from channels.layers import get_channel_layer
from aiohttp import ClientSession, ClientTimeout
from monitor.models import Monitor, MonitorLog
from monitor.serializers import MonitorLogSerializer
from rest_framework import status
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.utils import timezone
from django.db import transaction


class BaseWorker(ABC):

    @abstractmethod
    def get_monitors(self):
        pass

    @abstractmethod
    def get_client_session(self, *args, **kwargs):
        pass

    @abstractmethod
    async def handle_response(self, response, monitor, response_time):
        pass

    @abstractmethod
    def write_to_db(self):
        pass

    @database_sync_to_async
    def handle_error(self, error, monitor, response_time):
        with transaction.atomic():
            monitor.last_request = timezone.now()
            monitor.next_request = timezone.now() + monitor.interval
            monitor.save(update_fields=['last_request', 'next_request'])
            m = MonitorLog.objects.create(error=error, response_time=response_time, monitor=monitor)
            print('New log was created')
            data = MonitorLogSerializer(m).data
            return data

    async def send_to_channels(self, monitor, data):
        layer = get_channel_layer()
        await layer.group_send(str(monitor.user), {'type': 'send_log', 'data': data})

    def start_request(self, session: ClientSession, monitor: Monitor):
        timeout = ClientTimeout(total=5)
        return session.get(monitor.url, timeout=timeout)

    async def handle_request(self,  monitor, session):
        try:
            async with self.start_request(session, monitor) as response:
                print(f'Response to {monitor.url} status {response.status}')
                return False, response

        except Exception as e:
            print(f'Response to {monitor.url} error {e}')
            return True, str(e)

    @sync_to_async
    def send_push(self, response, monitor):
        user = monitor.user
        device = user.get_fcm_device()
        device.send_backround({'response': response.code, 'url': monitor.url})

    def run(self):
        try:
            qs = self.get_monitors()
            if qs.exists():
                print(qs.last().next_request)
                print(f"Start service {self.__class__.__name__}")
                print(f'Service {self.__class__.__name__} start handle {qs.count()} monitors')
                asyncio.run(self.main(list(qs)))
        except Exception as e:
            print(e)

    async def main(self, qs):
        async with self.get_client_session() as session:
            tasks = [self.fetch(monitor, session) for monitor in qs]
            await asyncio.gather(*tasks)

    async def fetch(self, monitor, session):
        start = time.monotonic()
        error, response = await self.handle_request(monitor, session)
        response_time = time.monotonic() - start
        if not error:
            data = await self.handle_response(response, monitor, response_time)
        else:
            data = await self.handle_error(response, monitor, response_time)

        await self.send_to_channels(monitor, data)
        if error or status.is_server_error(response.status) or status.is_client_error(response.status):
            pass
            #await self.send_push(response, monitor)

