from typing import Tuple, Union
from functools import cached_property, lru_cache
from uuid import uuid4
from datetime import timedelta
from django.db import models
from django.db.models import QuerySet
from django.db.models import Avg, F, Q, Count, Case, When
from django.db.models.expressions import RawSQL
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from utils.models import BaseModel
from rest_framework import status
from solo.models import SingletonModel
from utils.db_funcs import Round


class MonitorManager(models.Manager):
    pass


class MonitorQuerySet(QuerySet):

    def by_user(self, user):
        return self.filter(user=user)

    def get_nearest(self):
        return self.filter(next_request__lt=timezone.now()+timedelta(seconds=10))

    def active(self):
        return self.filter(is_active=True)

    def prefetch_for_day(self):
        hours = 24
        monitor_logs_qs = MonitorLog.objects.for_hours(hours)
        qs = self.prefetch_related(models.Prefetch('logs',
                                                   queryset=monitor_logs_qs,
                                                   to_attr='last_logs'),
                                   models.Prefetch('logs',
                                                   queryset=monitor_logs_qs.filter(is_successful=False),
                                                   to_attr='_last_error_logs'))
        return qs


    def annotate_avg_response_time(self):
        hours = 24
        now = timezone.now()
        delta_start = now - timedelta(hours=hours)
        return self.annotate(_avg_response_time=Avg('logs__response_time',
                                                   filter=(models.Q(logs__created__gt=delta_start,
                                                                    logs__created__lt=now))))

    def annotate_count_and_percent(self):
        hours = 24
        base_filter = Q(logs__created__gt=timezone.now()-timedelta(hours=hours),
                        logs__created__lt=timezone.now())

        qs = self.annotate(_log_last_count=Count('logs', filter=base_filter))

        successful_filter = base_filter & Q(logs__is_successful=True)
        qs = qs.annotate(_successful_percent=Case(
            When(_log_last_count=0, then=0.0),
            default=Round(
                Count('logs', filter=successful_filter)*100.0 / F('_log_last_count')
            ))
        )
        unsuccessful_filter = base_filter & Q(logs__is_successful=False)
        qs = qs.annotate(_unsuccessful_percent=Case(
            When(_log_last_count=0, then=0.0),
            default=Round(
                Count('logs', filter=unsuccessful_filter)*100.0 / F('_log_last_count'))
        ))

        return qs

    def prefetch_interval(self, monitor_id):
        hours = 24
        monitor_logs_qs = MonitorLog.objects.for_hours(hours)\
            .annotate_response_interval(monitor_id)

        qs = self.prefetch_related(models.Prefetch('logs', monitor_logs_qs,
                                                    to_attr='_interval_logs'))
        return qs

    # def prefetch_groups(self):
    #     query = """
    #         select Array((select jsonb_build_array(jsonb_build_object('successful', successful, 'e', prev_error, 'e2', prev_response_code, 'r', (SELECT COUNT(*) FROM unnest(g) as e(i) WHERE not exists(
    #
    #             SELECT 1 FROM unnest(old_g) as s2(e)
    #               where s2.e = e.i
    #
    #             )))) from (SELECT LAG(g, 1) OVER () as old_g, g, prev_successful as successful, prev_error, prev_response_code FROM (SELECT (
    #             CASE
    #             WHEN prev_successful != successful THEN (select array_agg(id) FROM monitor_monitorlog WHERE monitor_id = "monitor_monitor"."id" AND u2.created > created)
    #             WHEN NOT prev_successful AND NOT successful AND prev_error != error OR response_code != prev_response_code THEN (select array_agg(id) FROM monitor_monitorlog WHERE monitor_id = '9e607e67-96c2-432f-b97f-027e9e76d4ca' AND u2.created > created)
    #             WHEN id = l THEN (select array_agg(id) FROM monitor_monitorlog  WHERE monitor_id = "monitor_monitor"."id" AND u2.created >= created)
    #             END
    #             ) as g, prev_successful, successful, id, error, prev_error, prev_response_code
    #         FROM (SELECT successful, LAG(successful, 1) OVER (order by created) as prev_successful, created, id, error, response_code, LAG(response_code, 1) OVER (order by created) as prev_response_code, LAG(error, 1) OVER (order by created) as prev_error, last_value(id) over () as l  FROM
    #             (select created, id, error, response_code, CASE
    #                 WHEN error IS NOT NULL THEN false
    #                 WHEN response_code IS NULL THEN false
    #                 WHEN response_code > 0 and response_code < 400 THEN true
    #                 ELSE false
    #                 END
    #                  as successful from monitor_monitorlog  where monitor_id = "monitor_monitor"."id" )u3 ) u2) u3
    #         WHERE g is not NULL) u5))
    #     """
    #     return self.annotate(log_groups=RawSQL(query, params=[]))


class Monitor(BaseModel):

    id = models.UUIDField(primary_key=True, db_index=True, unique=True, default=uuid4)

    created = models.DateTimeField(default=timezone.now, editable=False, db_index=True)
    user = models.ForeignKey('account.User', on_delete=models.PROTECT, related_name='monitors')
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
                                                       validators=[MinValueValidator(timedelta(minutes=1)),
                                                                   MaxValueValidator(timedelta(minutes=60))])

    objects = MonitorManager.from_queryset(MonitorQuerySet)()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    @cached_property
    def successful_percent(self):
        if hasattr(self, '_successful_percent'):
            return self._successful_percent

        logs = self.last_logs_for_day()
        count = 0

        if isinstance(logs, list):
            count = len(list(filter(lambda l: l.is_successful, logs)))

        elif logs is not None:
            count = logs.filter(is_successful=True).count()

        return round(count * 100 / len(logs) if count != 0 else count, 3)

    @cached_property
    def unsuccessful_percent(self):
        if hasattr(self, '_unsuccessful_percent'):
            return self._unsuccessful_percent

        if self.successful_percent is not None:
            return round(100 - self.successful_percent, 3)

        return None

    @cached_property
    def avg_response_time(self):
        if hasattr(self, '_avg_response_time'):
            return self._avg_response_time

        logs = self.last_logs_for_day(convert=True)
        avg = logs.aggregate(avg_res_time=Avg('response_time'))['avg_res_time'] or 0
        return round(avg, 3)

    @cached_property
    def log_last_count(self):
        if hasattr(self, '_log_last_count'):
            return self._log_last_count

        return self.last_logs_for_day(convert=True).count()

    @cached_property
    def last_request_in_seconds(self):
        if not self.last_request:
            return None

        return (timezone.now() - self.last_request).seconds

    @cached_property
    def worker(self):
        from background_service.fetcher.workers.http_worker import HttpWorker
        return HttpWorker

    @cached_property
    def last_log(self):
        last_logs = self.last_logs_for_day()

        if isinstance(last_logs, list):
            return last_logs[-1] if len(last_logs) > 0 else None

        return last_logs.last()

    @cached_property
    def interval_in_minutes(self):
        return int(self.interval.total_seconds() // 60)

    @cached_property
    def error_notification_interval_in_minutes(self):
        return int(self.error_notification_interval.total_seconds() // 60)

    @cached_property
    def interval_logs(self):
        if hasattr(self, '_interval_logs'):
            return self._interval_logs

        return None

    @cached_property
    def last_error_logs(self):
        if hasattr(self, '_last_error_logs'):
            return self._last_error_logs

        return None

    @lru_cache()
    def last_logs_for_day(self, convert: bool = False) -> Union[list, QuerySet]:
        hours = 24

        if hasattr(self, 'last_logs'):
            logs = self.last_logs

        else:
            logs = self.logs.for_hours(hours)

        if isinstance(logs, list) and convert:
            logs = MonitorLog.objects.filter(id__in=[l.id for l in logs])

        return logs

    @lru_cache()
    def get_groups(self):

        #TODO: try move to sql

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
        now = timezone.now()
        delta_start = now - timedelta(hours=hours)
        return self.filter(created__gt=delta_start, created__lt=now)

    def annotate_response_interval(self, monitor_id, frame=20, hours=24):

        now = timezone.now()
        delta_start = now - timedelta(hours=hours)

        query1 = f"SELECT res_time FROM (SELECT AVG(response_time) as res_time, (array_agg(id))[1] as start_id " \
        f"FROM (SELECT NTILE({frame}) over (ORDER BY created) as group_num, response_time, id " \
                 f"FROM (SELECT * from monitor_monitorlog " \
                 f"WHERE (monitor_id='{monitor_id}'  AND created > '{delta_start.strftime('%Y-%m-%d %H:%M:%S')}')  ) u4) u1 " \
        f"group by group_num ORDER BY group_num) u2 WHERE start_id = monitor_monitorlog.id"

        return self.annotate(q1=RawSQL(query1, [])).exclude(q1__isnull=True)


class MonitorLog(BaseModel):

    created = models.DateTimeField(default=timezone.now, editable=False, db_index=True)
    error = models.TextField(null=True, blank=True, default=None)
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, related_name='logs')
    response_code = models.IntegerField(null=True, blank=True, default=None)
    response_time = models.FloatField()
    is_successful = models.BooleanField()

    objects = MonitorLogManager.from_queryset(MonitorLogQuerySet)()

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        self.is_successful = self._check_successful()
        return super().save(*args, **kwargs)

    def _check_successful(self):

        if self.error or not self.response_code:
            return False

        return (not status.is_client_error(self.response_code) and
                not status.is_server_error(self.response_code))


class MonitorConfig(SingletonModel):
    pro_log_rotation = models.IntegerField(default=300000)
    free_log_rotation = models.IntegerField(default=20000)
    free_log_min_interval = models.DurationField(default=timedelta(minutes=1))
    pro_max_monitors = models.IntegerField(default=50)
    free_max_monitors = models.IntegerField(default=10)

