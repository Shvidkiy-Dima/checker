from rest_framework import serializers
from account.models import User, ClientAlert


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'has_telegram')


class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientAlert
        fields = ('alert_type', 'msg', 'id')


class AlertDisableSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        instance.enable = False
        instance.save(update_fields=['enable'])
        return {}