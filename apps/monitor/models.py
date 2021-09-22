import statistics
from uuid import uuid4
from datetime import timedelta
from django.db import models
from django.db.models import Avg, F
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from utils.models import BaseModel
from rest_framework import status
from solo.models import SingletonModel


class MonitorManager(models.Manager):
    pass


class MonitorQuerySet(models.QuerySet):

    def by_user(self, user):
        return self.filter(user=user)

    def get_nearest(self):
        return self.filter(next_request__lt=timezone.now()+timedelta(seconds=10))

    def active(self):
        return self.filter(is_active=True)

    def prefetch_for_day(self):
        hours = 24
        return self.prefetch_related(
            models.Prefetch('logs',
                            queryset=MonitorLog.objects.for_hours(hours).order_by('created'),
                            to_attr='last_logs'))


class Monitor(BaseModel):

    class MonitorType(models.IntegerChoices):
        HTTP = 0, 'HTTP-HTTPS'
        HTML = 1, 'Check HTML'

    id = models.UUIDField(primary_key=True, db_index=True, unique=True, default=uuid4)

    keyword = models.CharField(max_length=124, null=True, blank=True, default=None)
    user = models.ForeignKey('account.User', on_delete=models.PROTECT, related_name='monitors')
    monitor_type = models.PositiveSmallIntegerField(choices=MonitorType.choices)
    last_request = models.DateTimeField()
    next_request = models.DateTimeField()
    interval = models.DurationField(validators=[MinValueValidator(timedelta(minutes=1)),
                                                MaxValueValidator(timedelta(minutes=60))])
    max_timeout = models.DurationField(validators=[MinValueValidator(timedelta(seconds=1)),
                                                   MaxValueValidator(timedelta(seconds=30))],
                                       default=timedelta(seconds=10))
    url = models.URLField()
    name = models.CharField(max_length=124)
    description = models.TextField(null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)
    by_telegram = models.BooleanField(null=True, blank=True, default=None)
    by_email = models.BooleanField(default=False)
    error_notification_interval = models.DurationField(default=timedelta(minutes=5),
                                                       validators=[MinValueValidator(timedelta(minutes=5)),
                                                                   MaxValueValidator(timedelta(minutes=60))])

    objects = MonitorManager.from_queryset(MonitorQuerySet)()

    class Meta:
        ordering = ('-created',)

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

    def last_error_requests(self):
        pass

    def last_logs_for_day(self, convert=False):
        hours = 24
        if hasattr(self, 'last_logs'):
            logs = self.last_logs

        else:
            logs = self.logs.for_hours(hours)

        if isinstance(logs, list) and convert:
            logs = MonitorLog.objects.filter(id__in=[l.id for l in logs])

        return logs

    @property
    def log_last_count(self):
        return self.last_logs_for_day(convert=True).count()

    @property
    def avg_response_time(self):
        hours = 24
        logs = self.last_logs_for_day(convert=True)
        avg = logs.aggregate(avg_res_time=Avg('response_time'))['avg_res_time'] or 0
        return round(avg, 3)

    def response_time_for_day(self):
        #TODO: move to DB request

        group_count = 20
        group_temp = []
        groups = []
        logs = self.last_logs_for_day()
        for log in logs:
            group_temp.append(log)
            if len(group_temp) == group_count:
                start = group_temp[0].created
                end = group_temp[-1].created
                md = statistics.median([l.response_time for l in group_temp])
                groups.append({'start': start, 'end': end, 'md': round(md, 3)})
                group_temp.clear()

        if len(group_temp) > 0:
            start = group_temp[0].created
            end = group_temp[-1].created
            md = statistics.median([l.response_time for l in group_temp])
            groups.append({'start': start, 'end': end, 'md': round(md, 3)})
            group_temp.clear()

        return groups

    def get_groups(self):
        data = self.last_logs_for_day()
        groups = []
        
        for i in data:
            if not groups:
                groups.append({'start': i.created,
                               'successful': i.is_successful,
                               'count': 1,
                               'error': i.error,
                               'res_code': i.response_code})

            last = groups[-1]
            if last['successful'] != i.is_successful:
                last['end'] = i.created
                groups.append({'start': i.created,
                               'successful': i.is_successful,
                               'count': 1,
                               'error': i.error,
                               'res_code': i.response_code})

            elif (not last['successful']) and (not i.is_successful) and \
                    i.error != last['error'] or i.response_code != last['res_code']:
                    last['end'] = i.created
                    groups.append({'start': i.created,
                                   'successful': i.is_successful,
                                   'count': 1,
                                   'error': i.error,
                                   'res_code': i.response_code})

            else:
                last['count'] += 1

        return groups

    @property
    def interval_in_minutes(self):
        return int(self.interval.total_seconds() // 60)

    def successful_percent(self):
        logs = self.last_logs_for_day()
        count = 0

        if isinstance(logs, list):
            count = len(list(filter(lambda l: l.is_successful, logs)))

        elif logs is not None:
            count = logs.filter(response_code__gte=100,
                                    response_code__lt=400,
                                    error__isnull=True).count()

        return round(count * 100 / len(logs) if count != 0 else count, 3)

    @property
    def unsuccessful_percent(self):
        successful_percent = self.successful_percent()
        if successful_percent is None:
            return None

        return round(100 - successful_percent, 3)

    @property
    def error_notification_interval_in_minutes(self):
        return int(self.error_notification_interval.total_seconds() // 60)


class MonitorLogManager(models.Manager):

    def make(self, monitor, **kwargs):
        user = monitor.user
        config = MonitorConfig.get_solo()

        if user.profile.is_pro and monitor.logs.count() > config.pro_log_rotation:
            monitor.logs.last().delete()

        elif monitor.logs.count() > config.free_log_rotation:
            monitor.logs.last().delete()

        return self.create(monitor=monitor, **kwargs)


class MonitorLogQuerySet(models.QuerySet):

    def for_hours(self, hours=24):
        #now = timezone.now()
        now = timezone.now() - timedelta(hours=2360)
        delta_start = now - timedelta(hours=hours)
        return self.filter(created__gt=delta_start, created__lt=now)


class MonitorLog(BaseModel):
    error = models.TextField(null=True, blank=True, default=None)
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, related_name='logs')
    response_code = models.IntegerField(null=True, blank=True, default=None)
    response_time = models.FloatField()
    keyword = models.BooleanField(null=True, blank=True, default=None)

    objects = MonitorLogManager.from_queryset(MonitorLogQuerySet)()

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
    free_log_min_interval = models.DurationField(default=timedelta(minutes=1))
    pro_max_monitors = models.IntegerField(default=50)
    free_max_monitors = models.IntegerField(default=10)