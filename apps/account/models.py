from django.db import models, transaction
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from utils.models import BaseModel
from device import models as device_models
from configs.models import UserConfig


class UserManager(BaseUserManager):
    use_in_migrations = False

    @transaction.atomic
    def make_client(self, email):
        user = self.create(email=email)
        ClientProfile.objects.create(user=user)
        UserConfig.objects.create(user=user)
        return user


class UserQuerySet(models.QuerySet):

    def by_email(self, email):
        return self.filter(email=email)


class User(AbstractUser):
    username = models.CharField(max_length=124, null=True, blank=True, default=None)
    email = models.EmailField(unique=True)
    telegram_chat_id = models.CharField(max_length=1024, null=True, blank=True, default=None)

    objects = UserManager.from_queryset(UserQuerySet)()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'user_{self.id}'

    def get_fcm_device(self):
        fcm_android = device_models.FCMDeviceAndroid.objects.by_user(self).first()
        fcm_ios = device_models.FCMDeviceIos.objects.by_user(self).first()
        return fcm_android or fcm_ios


class ClientProfile(BaseModel):

    class PlanType(models.IntegerChoices):
        FREE = 0, 'Free'
        PRO = 1, 'Pro'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # TODO: move value into setting !!!
    amount_monitors = models.PositiveIntegerField(default=5)
    type = models.PositiveSmallIntegerField(choices=PlanType.choices, default=PlanType.FREE)

    @property
    def is_pro(self):
        return self.type == ClientProfile.PlanType.PRO