import asyncio
import logging
import django
import os
import sys
import pathlib
from django.conf import settings
from django.db import transaction

sys.path.append(str(pathlib.PosixPath(os.path.abspath(__file__)).parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.deep_linking import get_start_link
from channels.db import database_sync_to_async
from notification.models import TelegramConfirmation

# Configure logging
logging.basicConfig(level=logging.INFO)


class TelegramSender:

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(bot)

    @staticmethod
    @database_sync_to_async
    def associate_user_with_telegram(chat_id, key):
        tc = TelegramConfirmation.objects.new().not_expired().filter(key=key).first()
        if not tc:
            return None

        with transaction.atomic():
            tc.status = TelegramConfirmation.Status.CONFIRMED
            user = tc.user
            user.telegram_chat_id = chat_id
            user.save(update_fields=['telegram_chat_id'])
            tc.save(update_fields=['status'])

        return user

    @staticmethod
    @dp.message_handler(commands=['start'])
    async def send_welcome(message: types.Message):
        key = message.get_args()
        channel_id = message.chat['id']
        if not key:
            await TelegramSender.bot.send_message(channel_id, 'Please, check url. That must be something like this '
                                   'https://t.me/IsaliveProjectNotificationsBot?start={token}')

        user = await TelegramSender.associate_user_with_telegram(channel_id, key)
        if user is None:
            await TelegramSender.bot.send_message(channel_id, 'Your link have been expired, please generate new link')

        await message.reply("Hi! Start monitoring")

    async def run(self):
        await self.dp.start_polling()

    async def send_message(self, chat_id, msg):
        await self.bot.send_message(chat_id, msg)
