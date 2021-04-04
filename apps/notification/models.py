from uuid import uuid4
from datetime import timedelta
from django.db import models
from django.conf import settings
from django.utils import timezone
from utils.models import BaseModel


class TelegramConfirmationQuerySet(models.QuerySet):

    def new(self):
        return self.filter(status=TelegramConfirmation.Status.NEW)

    def not_expired(self):
        delta = timezone.now() - timedelta(hours=settings.CONFIRMATION_TELEGRAM_EXPIRATION)
        return self.filter(created__gt=delta)


class TelegramConfirmation(BaseModel):

    class Status(models.IntegerChoices):
        NEW = 0, 'New'
        CONFIRMED = 1, 'Confirmed'

    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid4)
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.NEW)

    objects = TelegramConfirmationQuerySet.as_manager()

    @property
    def deeplink(self):
        link_type = 'start'
        payload = self.key
        return f'https://t.me/{settings.TELEGRAM_BOT_NAME}?{link_type}={payload}'
