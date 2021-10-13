from rest_framework import serializers
from notification import models


class TelegramConfirmationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TelegramConfirmation
        fields = ('deeplink',)
        read_only_fields = ('deeplink',)


class TelegramDisableSerializer(serializers.Serializer):

    def save(self):
        user = self.context.get('request').user
        user.userconfig.enable_telegram = False
        user.telegram_chat_id = None
        user.save(update_fields=['telegram_chat_id'])
        user.userconfig.save(update_fields=['enable_telegram'])
