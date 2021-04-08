from rest_framework import serializers
from configs import models


class UserConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserConfig
        fields = ('enable_telegram', 'error_notification_interval', 'error_notification_interval_in_minutes')
        read_only_fields = ('error_notification_interval_in_minutes',)
