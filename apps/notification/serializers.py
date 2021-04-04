from rest_framework import serializers
from notification import models


class TelegramConfirmationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TelegramConfirmation
        fields = ('deeplink',)
        read_only_fields = ('deeplink',)
