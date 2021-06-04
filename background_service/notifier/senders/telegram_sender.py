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
from aiogram.utils import exceptions
from channels.db import database_sync_to_async
from notification.models import TelegramConfirmation
from account.models import User

logger = logging.getLogger()


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
            user.userconfig.enable_telegram = True
            user.userconfig.save(update_fields=['enable_telegram'])
            user.save(update_fields=['telegram_chat_id'])
            tc.save(update_fields=['status'])

        return user

    @staticmethod
    @dp.message_handler(commands=['start'])
    async def send_welcome(message: types.Message):
        key = message.get_args()
        channel_id = message.chat['id']
        if not key:
            msg = 'Please, check url. That must be something like this https://t.me/IsaliveProjectNotificationsBot?start={token}'
            await TelegramSender.bot.send_message(channel_id, msg)
            return

        user = await TelegramSender.associate_user_with_telegram(channel_id, key)
        if user is None:
            await TelegramSender.bot.send_message(channel_id, 'Your link have been expired, please generate new link')
            return

        logger.info(f'TELEGRAM: Start new dialog with {user.email}')
        await message.reply("Hi! Start monitoring")

    async def run(self):
        await self.dp.start_polling()

    async def send_message(self, msg, chat_id, user_id):
        try:
            await self.bot.send_message(chat_id, msg)
            logger.info(f"Message was sent to {user_id}")
        except Exception as e:
            await self._handle_send_message_error(e, user_id)

    @database_sync_to_async
    def _handle_send_message_error(self, error, user_id):
        if isinstance(error, exceptions.ChatNotFound):
            with transaction.atomic():
                user = User.objects.get(id=user_id)
                logger.info(f'TELEGRAM: Send message to {user.email} - chat not found')
                user.userconfig.enable_telegram = False
                user.telegram_chat_id = None
                user.save(update_fields=['telegram_chat_id'])
                user.userconfig.save(update_fields=['enable_telegram'])
                user.alerts.make_for_telegram('We could not find telegram dialog with our bot, please follow '
                                              'to config and enable telegram notifications again')
