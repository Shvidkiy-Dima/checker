from uuid import uuid4
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.db import models, transaction
from utils.models import BaseModel


class ConfirmationEmailQuerySet(models.QuerySet):

    def new(self):
        return self.filter(status=ConfirmationEmail.Status.NEW)

    def not_expired(self):
        delta = timezone.now() - timedelta(hours=settings.CONFIRMATION_EMAIL_EXPIRATION)
        return self.filter(created__gt=delta)


class ConfirmationEmail(BaseModel):

    SUBJECT = 'auth/confirmation_email.txt'
    HTML_BODY = 'auth/confirmation_email.html'

    class Status(models.IntegerChoices):
        NEW = 0, 'New'
        CONFIRMED = 1, 'Confirmed'

    user = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True, default=None)

    password = models.CharField(max_length=64)
    email = models.EmailField()

    key = models.UUIDField(default=uuid4, unique=True, db_index=True)
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.NEW)

    objects = ConfirmationEmailQuerySet.as_manager()
