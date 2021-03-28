from django.utils import timezone
from rest_framework import serializers
from monitor.models import Monitor, MonitorLog


class MonitorNestedLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonitorLog
        fields = ('response_code', 'response_time', 'is_successful', 'error')


class ListMonitorSerializer(serializers.ModelSerializer):
    log = MonitorNestedLogSerializer(source='last_log', read_only=True)
    request_count = serializers.IntegerField(source='logs.count', read_only=True)

    class Meta:
        model = Monitor
        fields = ('id', 'monitor_type', 'interval', 'url', 'name', 'description', 'is_active', 'keyword', 'log',
                  'last_request', 'next_request', 'successful_percent', 'request_count')
        read_only_fields = ('is_active', 'last_request', 'next_request', 'successful_percent')


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

        if user.monitors.count()+1 > user.profile.amount_monitors:
            raise serializers.ValidationError('Max amount monitors for current plan')

        attrs['user'] = user
        attrs['next_request'] = timezone.now() + attrs['interval']
        return attrs


class MonitorLogSerializer(serializers.ModelSerializer):

    monitor = ListMonitorSerializer(read_only=True, many=False)

    class Meta:
        model = MonitorLog
        fields = ('response_code', 'response_time', 'is_successful', 'monitor', 'error')
