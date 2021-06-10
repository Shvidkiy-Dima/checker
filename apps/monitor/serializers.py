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


class ListMonitorSerializer(serializers.ModelSerializer):
    log = MonitorNestedLogSerializer(source='last_log', read_only=True)
    request_count = serializers.IntegerField(source='logs.count', read_only=True)
    last_requests = MonitorNestedLogSerializer(source='last_logs_for_hours', many=True, read_only=True)

    class Meta:
        model = Monitor
        fields = ('id', 'monitor_type', 'interval_in_minutes', 'url', 'name', 'description', 'is_active', 'keyword', 'log',
                  'last_requests', 'interval', 'next_request', 'successful_percent', 'unsuccessful_percent',
                  'request_count', 'last_request_in_seconds','created', 'error_notification_interval',
                  'error_notification_interval_in_minutes', 'unsuccessful_percent', 'by_telegram')

        read_only_fields = ('is_active', 'next_request', 'log', 'error_notification_interval_in_minutes',
                            'successful_percent', 'last_requests', 'last_request_in_seconds')


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

    # def validate_keyword(self, value):
    #     try:
    #         value.encode()
    #     except Exception as e:
    #         raise serializers.ValidationError(e)
    #
    #     return value

    def validate(self, attrs):

        if not self.async_validated:
            raise RuntimeError('You must call async_validate first')

        user = self.context.get('request').user

        if not attrs.get('by_telegram', False):
            raise serializers.ValidationError('You must set at least one notification option')

        # if attrs['monitor_type'] == Monitor.MonitorType.HTML and not attrs.get('keyword'):
        #     raise serializers.ValidationError('You must set keyword if use type HTML')

        m_amount = user.monitors.count()+1
        config = MonitorConfig.get_solo()

        if user.profile.type == ClientProfile.PlanType.FREE and m_amount > config.free_max_monitors:
            raise serializers.ValidationError('Max amount monitors for free plan')

        # elif user.profile.type == ClientProfile.PlanType.PRO and m_amount > config.pro_max_monitors:
        #     raise serializers.ValidationError('Max amount monitors for pro plan')

        attrs['user'] = user
        attrs['next_request'] = self.async_validated_data['next_request']
        attrs['last_request'] = self.async_validated_data['last_request']
        return attrs

    async def async_validate(self):
        # TODO: fix it
        from background_service.fetcher.workers.http_worker import HttpWorker
        monitor_type = self.initial_data.get('monitor_type', None)
        url = self.initial_data.get('url', None)
        interval = self.initial_data.get('interval', None)

        method = self.initial_data.get('method', 'get')
        if list(filter(lambda e: e is None, [monitor_type, url, interval])):
            raise serializers.ValidationError('You must set all values')

        self.worker = HttpWorker()
        self.async_validated_data = await monitor_first_request(self.worker,  url, method, interval)
        self.async_validated = True

    def create(self, validated_data):
        with transaction.atomic():
            monitor = super().create(validated_data)
            log_attrs = self.async_validated_data

            log = self.worker.make_log(monitor, log_attrs['response_time'], log_attrs['body'],
                                        error=log_attrs['error'], response_code=log_attrs['response_code']
                                        )
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


