import asyncio
import traceback
import time
import json
import pytz
import logging
from typing import Tuple, Union
from dataclasses import dataclass, asdict
from datetime import timedelta, datetime
from abc import ABC, abstractmethod
from channels.layers import get_channel_layer
from aiohttp import ClientSession, ClientTimeout, http_exceptions
from monitor.models import Monitor, MonitorLog
from monitor.serializers import MonitorLogSerializer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from django.core.serializers.json import DjangoJSONEncoder
from aio_pika import connect_robust, Message
from aio_pika.connection import ConnectionType
from aredis import StrictRedis
from utils.functions import is_successful_response_code

logger = logging.getLogger()


@dataclass
class ErrorMessage:
    url: str
    name: str
    telegram_chat_id: str
    user_id: int
    enable_telegram: bool
    by_telegram: bool
    by_email: bool
    email: str
    error_msg: str


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
    async def handle_response(self, monitor: Monitor, body: bytes, response_time: float,  response_code: int):
        pass

    @abstractmethod
    def write_to_db(self):
        pass

    def run(self, conn):
        # TODO: loop.run_until_complete  - run create new event loop
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

    async def fetch(self, monitor: Monitor, session: ClientSession, rmq_channel: ConnectionType):
        logger.info(f'Start processing monitor {monitor.url} for user {monitor.user.email}')

        is_error, body, response_time, response_code = await self.handle_request(session, monitor.url,
                                                                                 timeout=monitor.max_timeout.seconds)

        if not is_error:
            logger.info(f'Request to {monitor.url} status {response_code}')
            data = await self.handle_response(monitor, body, response_time,  response_code)
        else:
            logger.info(f'Request to {monitor.url} error {body}')
            data = await self.handle_error(monitor, body, response_time)

        logger.info(f'New log created for {monitor.url}. Next request - {data["monitor"]["next_request"]}')

        await self.send_to_channels(monitor, data)

        if is_error or not is_successful_response_code(response_code):
            status_code = response_code or "Server error"
            error_msg = f'{status_code}:  {body}'
            await self.send_error_msg(monitor, rmq_channel, error_msg)

    async def handle_request(self, session: ClientSession, url: str,
                             timeout: int, method: str = 'get') -> Tuple[bool, Union[str, bytes], float, Union[None, int]]:

        timeout = ClientTimeout(total=timeout)
        start = time.monotonic()
        try:
            async with session.request(method, url, timeout=timeout) as response:
                body = await response.read()
                response_code = response.status
                if is_successful_response_code(response_code):
                    is_error = False
                else:
                    is_error = True
                    body = self._convert_error_body(body)

        except Exception as e:
            is_error = True
            response_code = None
            body = self._convert_request_exception(e)

        response_time = time.monotonic() - start

        return is_error, body, response_time,  response_code


    @database_sync_to_async
    def handle_error(self, monitor: Monitor, body: str, response_time: float) -> dict:
        with transaction.atomic():
            monitor.last_request = timezone.now()
            monitor.next_request = timezone.now() + monitor.interval
            monitor.save(update_fields=['last_request', 'next_request'])
            log = self.make_log(monitor, response_time, error=body,
                                is_successful=False, response_code=None)
            data = MonitorLogSerializer(log).data
            return data

    def make_log(self, monitor, response_time, error, is_successful, response_code):
        log = MonitorLog.objects.create(response_code=response_code,
                                        response_time=response_time,
                                        error=error,
                                        monitor=monitor,
                                        is_successful=is_successful)
        return log

    async def get_rmq_conn(self):
        return await connect_robust(host=settings.MQ_HOST,
                                    port=settings.MQ_PORT,
                                    login=settings.MQ_USER,
                                    password=settings.MQ_PASS)


    def get_redis_conn(self):
        return StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    async def send_to_channels(self, monitor: Monitor, data: dict):
        layer = get_channel_layer()
        data = json.dumps(data, cls=DjangoJSONEncoder)
        await layer.group_send(str(monitor.user), {'type': 'send_log',
                                                   'data': data})

    async def send_error_msg(self, monitor: Monitor, rmq_channel: ConnectionType, error_msg: str):
        error_interval = monitor.error_notification_interval
        cache_key = f'error_notify_monitor_{monitor.id}'
        last_error = await self.cache.get(cache_key, None)
        if last_error and timezone.now() < (datetime.fromtimestamp(last_error, pytz.utc) + error_interval):
            logger.info(f'Error notification already was sent to {monitor.user.email}. '
                        f'Next {datetime.fromtimestamp(last_error, pytz.utc) + error_interval}')
        else:
            logger.info(f'Send error notification to {monitor.user.email}')
            await self.cache.set(cache_key, time.time())

            data = ErrorMessage(url=monitor.url,
                                name=monitor.name,
                                telegram_chat_id=monitor.user.telegram_chat_id,
                                user_id=monitor.user.id,
                                enable_telegram=monitor.user.userconfig.enable_telegram,
                                by_telegram=monitor.by_telegram,
                                by_email=monitor.by_email,
                                email=monitor.user.email,
                                error_msg=error_msg)

            data = json.dumps(asdict(data)).encode()
            await rmq_channel.default_exchange.publish(Message(data), routing_key="notification")

    @database_sync_to_async
    def fetch_monitors(self, ids):
        return list(Monitor.objects.filter(id__in=ids).active()
                    .select_related('user', 'user__userconfig')
                    .prefetch_for_day().annotate_avg_response_time())

    def _convert_request_exception(self, exc) -> str:
        if type(exc) == asyncio.exceptions.TimeoutError:
            return 'Timeout error'

        return f'{type(exc)}: {exc}'

    def _convert_error_body(self, body: bytes) -> str:
        try:
            return str(json.loads(body))
        except Exception:
            body = body.decode(encoding='utf8', errors='replace')[:300]
            return body
