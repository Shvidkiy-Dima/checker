from django.db import models
from utils.models import BaseModel


class UserConfig(BaseModel):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE)
    enable_telegram = models.BooleanField(default=False)