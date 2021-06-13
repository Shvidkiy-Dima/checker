import asyncio
import traceback
import time
import json
import pytz
import logging
from datetime import timedelta, datetime
from abc import ABC, abstractmethod
from channels.layers import get_channel_layer
from aiohttp import ClientSession, ClientTimeout, http_exceptions
from monitor.models import Monitor, MonitorLog
from monitor.serializers import MonitorLogSerializer
from rest_framework import status
from channels.db import database_sync_to_async
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from aio_pika import connect_robust,  Message
from aredis import StrictRedis

logger = logging.getLogger()


class BaseWorker(ABC):

    def __init__(self):
        self.cache = None

    @classmethod
    @abstractmethod
    def get_monitors(cls):
        pass

    @abstractmethod
    def get_client_session(self, *args, **kwargs):
        pass

    @abstractmethod
    async def handle_response(self, response, monitor, response_time, body):
        pass

    @abstractmethod
    def write_to_db(self):
        pass

    def run(self, conn):
        logger.info(f'Start {self.__class__.__name__}')
        asyncio.run(self.main(conn))

    async def main(self, conn):
        redis_client = self.get_redis_conn()
        self.cache = redis_client.cache('cache_workers')
        rmq_conn = await self.get_rmq_conn()
        rmq_channel = await rmq_conn.channel()
        while True:
            monitors_id = conn.recv()
            if monitors_id:
                logger.info(f'New batch: {self.__class__.__name__} - {len(monitors_id)} monitors')

            try:
                qs = await self.fetch_monitors(monitors_id)
                async with self.get_client_session() as session:
                    tasks = [self.fetch(monitor, session, rmq_channel) for monitor in qs]
                    await asyncio.gather(*tasks)

            except Exception as e:
                logger.error(f'ERROR: {traceback.format_exc()}')

            conn.send(1)

    async def fetch(self, monitor, session, rmq_channel):
        logger.info(f'Start processing monitor {monitor.url} for user {monitor.user.email}')
        error, response, body, response_time\
            = await self.handle_request(session, monitor.url, timeout=monitor.max_timeout.seconds)

        if not error:
            logger.info(f'Request to {monitor.url} status {response.status}')
        else:
            logger.info(f'Request to {monitor.url} error {response}')

        if not error:
            data = await self.handle_response(response, monitor, response_time, body)
        else:
            data = await self.handle_error(response, monitor, response_time)

        logger.info(f'New log created for {monitor.url}. Next request - {data["monitor"]["next_request"]}')
        await self.send_to_channels(monitor, data)
        if error or status.is_server_error(response.status) or status.is_client_error(response.status):
            status_code = response.status if not error else "Server error"
            reason = response if error else response.reason
            error_msg = f'{status_code}:  {reason}'
            await self.send_error_msg(monitor, rmq_channel, error_msg)

    @database_sync_to_async
    def handle_error(self, error, monitor, response_time):
        with transaction.atomic():
            monitor.last_request = timezone.now()
            monitor.next_request = timezone.now() + monitor.interval
            monitor.save(update_fields=['last_request', 'next_request'])
            log = self.make_log(monitor, response_time, error=error)
            data = MonitorLogSerializer(log).data
            return data

    def make_log(self, monitor, response_time, body=b'', error=None, response_code=None):
        log = MonitorLog.objects.create(response_code=response_code,
                                        response_time=response_time,
                                        error=error,
                                        monitor=monitor)
        return log

    async def get_rmq_conn(self):
        return await connect_robust(host=settings.MQ_HOST,
                                    port=settings.MQ_PORT,
                                    login=settings.MQ_USER,
                                    password=settings.MQ_PASS)


    def get_redis_conn(self):
        return StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    async def send_to_channels(self, monitor, data):
        layer = get_channel_layer()
        await layer.group_send(str(monitor.user), {'type': 'send_log', 'data': data})

    async def handle_request(self, session: ClientSession, url, timeout, method='get'):
        timeout = ClientTimeout(total=timeout)
        start = time.monotonic()
        try:
            async with session.request(method, url, timeout=timeout) as response:
                body = await response.read()
                error, response, body = False, response, body

        except Exception as e:
            error, response, body = True, self._convert_request_exception(e), b''

        response_time = time.monotonic() - start

        return error, response, body, response_time

    async def send_error_msg(self, monitor, rmq_channel, error_msg):
        error_interval = monitor.error_notification_interval
        cache_key = f'error_notify_monitor_{monitor.id}'
        last_error = await self.cache.get(cache_key, None)
        if last_error and timezone.now() < (datetime.fromtimestamp(last_error, pytz.utc) + error_interval):
            logger.info(f'Error notification already was sent to {monitor.user.email}. '
                        f'Next {datetime.fromtimestamp(last_error, pytz.utc) + error_interval}')
            return

        logger.info(f'Send error notification to {monitor.user.email}')
        await self.cache.set(cache_key, time.time())
        data = {'url': monitor.url, 'name': monitor.name,
                'telegram_chat_id': monitor.user.telegram_chat_id,
                'user_id': monitor.user_id,
                'enable_telegram': monitor.user.userconfig.enable_telegram,
                'monitor_telegram': monitor.by_telegram,
                'error_msg': error_msg}
        data = json.dumps(data).encode()
        await rmq_channel.default_exchange.publish(Message(data), routing_key="notification")

    @database_sync_to_async
    def fetch_monitors(self, ids):
        return list(Monitor.objects.filter(id__in=ids).active().select_related('user', 'user__userconfig'))

    def _convert_request_exception(self, exc):
        if type(exc) == asyncio.exceptions.TimeoutError:
            return 'Timeout error'

        return f'{type(exc)}: {exc}'
