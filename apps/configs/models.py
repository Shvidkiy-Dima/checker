from datetime import timedelta
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from utils.models import BaseModel


class UserConfig(BaseModel):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE)
    enable_telegram = models.BooleanField(default=False)
    error_notification_interval = models.DurationField(default=timedelta(minutes=5),
                                                       validators=[MinValueValidator(timedelta(minutes=5)),
                                                                   MaxValueValidator(timedelta(minutes=20))])
    @property
    def error_notification_interval_in_minutes(self):
        return int(self.error_notification_interval.total_seconds() // 60)