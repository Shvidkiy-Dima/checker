import time
from django.utils import timezone
from django.db import transaction
from rest_framework import serializers
from account.models import ClientProfile
from monitor.models import Monitor, MonitorLog, MonitorConfig
from monitor.services.base import monitor_first_request


class MonitorNestedLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonitorLog
        fields = ('response_code', 'response_time', 'is_successful', 'error', 'created')


class MonitorNestedIntervalLogSerializer(MonitorNestedLogSerializer):
    interval_avg = serializers.FloatField(source='q1', read_only=True)

    class Meta(MonitorNestedLogSerializer.Meta):
        fields = ('interval_avg', 'created')


class ListMonitorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Monitor
        fields = ('id', 'interval_in_minutes', 'url', 'name', 'is_active',
                  'interval', 'next_request', 'successful_percent', 'unsuccessful_percent',
                  'last_request_in_seconds','created', 'error_notification_interval',
                  'error_notification_interval_in_minutes','by_telegram', 'by_email', 'max_timeout', 'avg_response_time', 'log_last_count')

        read_only_fields = ('is_active', 'next_request', 'log', 'error_notification_interval_in_minutes',
                            'successful_percent', 'last_request_in_seconds', 'log_last_count', 'avg_response_time')


class DetailMonitorSerializer(ListMonitorSerializer):
    last_error_logs = MonitorNestedLogSerializer(many=True)
    interval_logs = MonitorNestedIntervalLogSerializer(many=True)
    log_groups = serializers.JSONField(source='get_groups', read_only=True)
    last_log = MonitorNestedLogSerializer(read_only=True)

    class Meta(ListMonitorSerializer.Meta):
        fields = ListMonitorSerializer.Meta.fields + ('interval_logs', 'last_error_logs',
                                                      'log_groups', 'description', 'last_log')
        read_only_fields = ListMonitorSerializer.Meta.read_only_fields + ('interval_logs', 'last_error_logs',
                                                                          'log_groups', 'description', 'last_log')


class CreateMonitorSerializer(ListMonitorSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.async_validated_data = {}
        self.async_validated = False
        self.worker = None

    def validate_interval(self, value):
        mc = MonitorConfig.get_solo()
        user = self.context.get('request').user
        if user.profile.type == ClientProfile.PlanType.FREE and mc.free_log_min_interval > value:
            raise serializers.ValidationError(f'Min interval for free account {mc.free_log_min_interval}')
        return value

    def validate(self, attrs):

        if not self.async_validated:
            raise RuntimeError('You must call async_validate first')

        user = self.context.get('request').user

        if not attrs.get('by_telegram', False) and not attrs.get('by_email', False):
            raise serializers.ValidationError('You must set at least one notification option')

        m_amount = user.monitors.count()+1
        config = MonitorConfig.get_solo()

        if user.profile.type == ClientProfile.PlanType.FREE and m_amount > config.free_max_monitors:
            raise serializers.ValidationError('Max amount monitors for free plan')

        attrs['user'] = user
        attrs['next_request'] = self.async_validated_data.pop('next_request')
        attrs['last_request'] = self.async_validated_data.pop('last_request')
        return attrs

    async def async_validate(self):
        # TODO: fix it
        from background_service.fetcher.workers.http_worker import HttpWorker
        url = self.initial_data.get('url', None)
        interval = self.initial_data.get('interval', None)
        max_timeout = self.initial_data.get('max_timeout', None)

        method = self.initial_data.get('method', 'get')
        if list(filter(lambda e: e is None, [url, interval, max_timeout])):
            raise serializers.ValidationError('You must set all values')

        self.worker = HttpWorker()
        self.async_validated_data = \
            await monitor_first_request(self.worker,  url, method, interval, max_timeout)
        self.async_validated = True

    def create(self, validated_data):
        with transaction.atomic():
            monitor = super().create(validated_data)
            log_attrs = self.async_validated_data

            log = self.worker.make_log(monitor, **log_attrs)

        return log.monitor


class MonitorLogSerializer(serializers.ModelSerializer):

    monitor = ListMonitorSerializer(read_only=True, many=False)

    class Meta:
        model = MonitorLog
        fields = ('response_code', 'response_time', 'is_successful', 'monitor', 'error')


class UpdateMonitorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Monitor
        fields = ('is_active',)


