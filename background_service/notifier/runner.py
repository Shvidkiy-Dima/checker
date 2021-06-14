import asyncio
import logging
import django
import os
import sys
import pathlib
from django.conf import settings

sys.path.append(str(pathlib.PosixPath(os.path.abspath(__file__)).parent.parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from background_service.notifier.senders.telegram_sender import TelegramSender
from background_service.notifier.senders.fcm_sender import FCMSender
from background_service.notifier.senders.email_sender import EmailSender
from background_service.utils import prepare_background_logging
from aio_pika import IncomingMessage, connect_robust
import json

logger = logging.getLogger()


class Dispatcher:

    senders = {'telegram': TelegramSender(),
               'fcm': FCMSender(),
               'email': EmailSender()}

    async def on_message(self, message: IncomingMessage):
        data = json.loads(message.body.decode())
        msg = f'Something wrong - {data["name"]} - {data["url"]} - {data["error_msg"]}'
        logger.info(msg)

        if data['telegram_chat_id'] and data['enable_telegram'] and data['monitor_telegram']:
            await self.senders['telegram'].send_message(msg, data['telegram_chat_id'], data['user_id'])

        if data['by_email'] and data['email']:
            await self.senders['email'].send_message(msg, data['email'])

        # await self.senders['fcm'].send_message(msg, data['user_id'])

    async def check_queue(self):
        connection = await connect_robust(host=settings.MQ_HOST,
                                          port=settings.MQ_PORT,
                                          login=settings.MQ_USER,
                                          password=settings.MQ_PASS)

        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue("notification")

        # Start listening the queue with name 'hello'
        await queue.consume(self.on_message, no_ack=True)

    async def run(self):
        #tasks = [self.senders['telegram'].run(), self.senders['fcm'].run(), self.check_queue()]

        tasks = [self.senders['telegram'].run(),
                 self.senders['email'].run(),
                 self.check_queue()]

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    with prepare_background_logging(settings.NOTIFIER_DIR / 'logs/app.log'):
        asyncio.run(Dispatcher().run())
