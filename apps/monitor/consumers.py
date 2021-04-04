import json, time
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from monitor.models import Monitor
from background_service.fetcher.workers.http_worker import HttpWorker


class MessageConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.group_name = None
        super().__init__(*args, **kwargs)

    async def connect(self):
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            await self.close()
            return

        self.group_name = str(user)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        if self.group_name is not None:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content: dict, **kwargs):
        pass
        # event = content['event']
        # method = getattr(self, event, None)
        # if method is not None:
        #     await method(content['data'])
        # else:
        #     await self.send(json.dumps({'status': 'Method not exists'}))

    async def send_log(self, event):
        print(event)
        await self.send(json.dumps({"type": 'log', 'data': event['data']}))
