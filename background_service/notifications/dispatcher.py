import asyncio
import logging
import django
import os
import sys
import pathlib

sys.path.append(str(pathlib.PosixPath(os.path.abspath(__file__)).parent.parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from background_service.notifications.senders.telegram_sender import TelegramSender
from background_service.notifications.senders.fcm_sender import FCMSender
from aio_pika import IncomingMessage,connect_robust
import json

# Configure logging
logging.basicConfig(level=logging.INFO)


class Dispatcher:

    senders = {'telegram': TelegramSender(), 'fcm': FCMSender()}

    async def on_message(self, message: IncomingMessage):
        data = json.loads(message.body.decode())
        msg = f'Something wrong - {data["name"]} - {data["url"]}'
        print(msg, data)

        if chat_id := data['telegram_chat_id'] and data['enable_telegram']:
            await self.senders['telegram'].send_message(chat_id, msg)

        await self.senders['fcm'].send_message(msg, data['user_id'])

    async def check_queue(self):
        connection = await connect_robust()

        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue("notification")

        # Start listening the queue with name 'hello'
        await queue.consume(self.on_message, no_ack=True)

    async def run(self):
        tasks = [self.senders['telegram'].run(), self.senders['fcm'].run(), self.check_queue()]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(Dispatcher().run())
