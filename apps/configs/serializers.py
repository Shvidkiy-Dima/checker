from rest_framework import serializers
from configs import models


class UserConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserConfig
        fields = ('enable_telegram',)