from uuid import uuid4
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from utils.models import BaseModel
from rest_framework import status
from solo.models import SingletonModel


class MonitorManager(models.Manager):
    pass


class MonitorQuerySet(models.QuerySet):

    def available(self):
        return self.filter(last_request__isnull=False)

    def by_user(self, user):
        return self.filter(user=user)

    def get_nearest(self):
        return self.filter(next_request__lt=timezone.now()+timedelta(seconds=10))

    def active(self):
        return self.filter(is_active=True)


class Monitor(BaseModel):

    class MonitorType(models.IntegerChoices):
        HTTP = 0, 'HTTP-HTTPS'
        HTML = 1, 'Check HTML'

    id = models.UUIDField(primary_key=True, db_index=True, unique=True, default=uuid4)

    keyword = models.CharField(max_length=124, null=True, blank=True, default=None)
    user = models.ForeignKey('account.User', on_delete=models.PROTECT, related_name='monitors')
    monitor_type = models.PositiveSmallIntegerField(choices=MonitorType.choices)
    last_request = models.DateTimeField(null=True, blank=True, default=None)
    next_request = models.DateTimeField()
    interval = models.DurationField(validators=[MinValueValidator(timedelta(minutes=1)),
                                                MaxValueValidator(timedelta(minutes=60))])
    url = models.URLField()
    name = models.CharField(max_length=124)
    description = models.TextField(null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)

    objects = MonitorManager.from_queryset(MonitorQuerySet)()

    @property
    def last_request_in_seconds(self):
        if not self.last_request:
            return None

        return (timezone.now() - self.last_request).seconds


    @property
    def worker(self):
        from background_service.fetcher.workers.http_worker import HttpWorker
        return HttpWorker

    @property
    def last_log(self):
        return self.logs.order_by('created').last()

    def last_logs_for_hours(self, hours=24):
        delta = timezone.now() - timedelta(hours=hours)
        return self.logs.filter(created__gt=delta).order_by('created')

    @property
    def interval_in_minutes(self):
        return int(self.interval.total_seconds() // 60)

    def successful_percent(self, hours=24):
        logs = self.last_logs_for_hours(hours)
        if not logs:
            return None

        return logs.filter(response_code__gte=100,
                                response_code__lt=400,
                                error__isnull=True).count() * 100 // logs.count()

    @property
    def unsuccessful_percent(self, hours=24):
        successful_percent = self.successful_percent(hours)
        if not successful_percent:
            return None

        return 100 - successful_percent


class MonitorLogManager(models.Manager):

    def make(self, monitor, **kwargs):
        user = monitor.user
        config = MonitorConfig.get_solo()

        if user.profile.is_pro and monitor.logs.count() > config.pro_log_rotation:
            monitor.logs.last().delete()

        elif monitor.logs.count() > config.free_log_rotation:
            monitor.logs.last().delete()

        return self.create(monitor=monitor, **kwargs)


class MonitorLog(BaseModel):
    error = models.TextField(null=True, blank=True, default=None)
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, related_name='logs')
    response_code = models.IntegerField(null=True, blank=True, default=None)
    response_time = models.FloatField()
    keyword = models.BooleanField(null=True, blank=True, default=None)

    objects = MonitorLogManager()

    class Meta:
        ordering = ('-created',)

    @property
    def is_successful(self):
        if self.error or not self.response_code:
            return False

        return (not status.is_client_error(self.response_code) and not status.is_server_error(self.response_code))


class MonitorConfig(SingletonModel):
    pro_log_rotation = models.IntegerField(default=300000)
    free_log_rotation = models.IntegerField(default=20000)
    free_log_min_interval = models.DurationField(default=timedelta(minutes=5))
    pro_max_monitors = models.IntegerField(default=50)
    free_max_monitors = models.IntegerField(default=10)