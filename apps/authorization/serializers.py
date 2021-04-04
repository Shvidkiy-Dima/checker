from rest_framework import serializers
from rest_framework.authtoken.models import Token
from account.models import User
from authorization.models import ConfirmationEmail
from authorization.tasks import send_conf_email
from utils.functions import is_valid_password
from utils.celery import run_task


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfirmationEmail
        fields = ('email', 'password')

    def validate_password(self, value):
        is_valid, message = is_valid_password(value)
        if not is_valid:
            raise serializers.ValidationError(message)

        return value

    def create(self, validated_data):
        confirmation_email = super().create(validated_data)
        run_task(send_conf_email, confirmation_email.id)
        return confirmation_email


class SingInSerializer(serializers.Serializer):

    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True, write_only=True)
    token = serializers.CharField(source='key', read_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        email = attrs.get('email')

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError('Invalid credentials')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        token, _ = Token.objects.get_or_create(user=validated_data['user'])
        return token
