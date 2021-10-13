import json, time
from typing import Union
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from monitor.models import Monitor
from background_service.fetcher.workers.http_worker import HttpWorker
from django.contrib.auth.models import AnonymousUser
from account.models import User


class MessageConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.group_name = None
        super().__init__(*args, **kwargs)

    async def connect(self):
        user: Union[AnonymousUser, User] = self.scope.get('user')
        if not user or not user.is_authenticated:
            await self.close()
            return

        self.group_name = user.channel_group_name
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        if self.group_name is not None:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content: dict, **kwargs):
        pass

    async def send_log(self, event):
        await self.send(json.dumps({"type": 'log', 'data': event['data']}))

    async def telegram_response(self, event):
        await self.send(json.dumps({"type": "telegram_response"}))
