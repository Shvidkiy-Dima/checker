from django.utils import timezone
from rest_framework import serializers
from monitor.models import Monitor, MonitorLog


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
                  'request_count', 'last_request_in_seconds',)

        read_only_fields = ('is_active', 'next_request', 'log',
                            'successful_percent', 'last_requests', 'last_request_in_seconds')


class CreateMonitorSerializer(ListMonitorSerializer):

    def validate_interval(self, value):
        # TODO: check for plan
        return value

    def validate_keyword(self, value):
        try:
            value.encode()
        except Exception as e:
            raise serializers.ValidationError(e)

        return value

    def validate(self, attrs):
        user = self.context.get('request').user

        if attrs['monitor_type'] == Monitor.MonitorType.HTML and not attrs.get('keyword'):
            raise serializers.ValidationError('You must set keyword if use type HTML')

        # if user.monitors.count()+1 > user.profile.amount_monitors:
        #     raise serializers.ValidationError('Max amount monitors for current plan')

        attrs['user'] = user
        attrs['next_request'] = timezone.now()
        return attrs


class MonitorLogSerializer(serializers.ModelSerializer):

    monitor = ListMonitorSerializer(read_only=True, many=False)

    class Meta:
        model = MonitorLog
        fields = ('response_code', 'response_time', 'is_successful', 'monitor', 'error')


class UpdateMonitorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Monitor
        fields = ('is_active',)


