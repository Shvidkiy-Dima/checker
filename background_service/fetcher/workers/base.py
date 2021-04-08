import asyncio
import traceback
import time
import json
import pytz
from datetime import timedelta, datetime
from abc import ABC, abstractmethod
from channels.layers import get_channel_layer
from aiohttp import ClientSession, ClientTimeout
from monitor.models import Monitor, MonitorLog
from monitor.serializers import MonitorLogSerializer
from rest_framework import status
from channels.db import database_sync_to_async
from django.utils import timezone
from django.db import transaction
from aio_pika import connect_robust,  Message
from aredis import StrictRedis


class BaseWorker(ABC):

    def __init__(self):
        redis_client = StrictRedis(host='127.0.0.1', port=6379, db=0)
        self.cache = redis_client.cache('cache_workers')

    @classmethod
    @abstractmethod
    def get_monitors(cls):
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

    def run(self, conn):
        asyncio.run(self.main(conn))

    async def main(self, conn):
        rmq_conn = await self.get_rmq_conn()
        rmq_channel = await rmq_conn.channel()
        while True:
            monitors_id = conn.recv()
            if monitors_id:
                print(f'{self.__class__.__name__} - {monitors_id}')

            try:
                qs = await self.fetch_monitors(monitors_id)
                async with self.get_client_session() as session:
                    tasks = [self.fetch(monitor, session, rmq_channel) for monitor in qs]
                    await asyncio.gather(*tasks)

            except Exception as e:
                print(traceback.format_exc())

            conn.send(1)

    async def fetch(self, monitor, session, rmq_channel):
        start = time.monotonic()
        error, response = await self.handle_request(monitor, session)
        response_time = time.monotonic() - start

        if not error:
            data = await self.handle_response(response, monitor, response_time)
        else:
            data = await self.handle_error(response, monitor, response_time)

        await self.send_to_channels(monitor, data)
        if error or status.is_server_error(response.status) or status.is_client_error(response.status):
            await self.send_error_msg(monitor, rmq_channel)

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

    async def get_rmq_conn(self):
        return await connect_robust()

    async def send_to_channels(self, monitor, data):
        layer = get_channel_layer()
        await layer.group_send(str(monitor.user), {'type': 'send_log', 'data': data})

    def start_request(self, session: ClientSession, monitor: Monitor):
        timeout = ClientTimeout(total=5)
        return session.head(monitor.url, timeout=timeout)

    async def handle_request(self,  monitor, session):
        try:
            async with self.start_request(session, monitor) as response:
                print(f'Response to {monitor.url} status {response.status}')
                return False, response

        except Exception as e:
            print(f'Response to {monitor.url} error {e}')
            return True, str(e)

    async def send_error_msg(self, monitor, rmq_channel):
        error_interval = monitor.user.userconfig.error_notification_interval
        cache_key = f'error_notify_monitor_{monitor.id}'
        last_error = await self.cache.get(cache_key, None)
        if last_error and \
                timezone.now() < (datetime.fromtimestamp(last_error, pytz.utc) + timedelta(minutes=error_interval)):
            return

        await self.cache.set(cache_key, time.time())
        data = {'url': monitor.url, 'name': monitor.name,
                'telegram_chat_id': monitor.user.telegram_chat_id,
                'user_id': monitor.user_id, 'enable_telegram': monitor.user.userconfig.enable_telegram}
        data = json.dumps(data).encode()
        await rmq_channel.default_exchange.publish(Message(data), routing_key="notification")

    @database_sync_to_async
    def fetch_monitors(self, ids):
        return list(Monitor.objects.filter(id__in=ids).active().select_related('user', 'user__userconfig'))
