from django.shortcuts import redirect
from django.conf import settings
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from authorization.models import ConfirmationEmail
from authorization.services.base import confirm, logout
from authorization import serializers
from authorization.throttling import EmailDelayThrottle


class SignUpView(generics.CreateAPIView):
    serializer_class = serializers.SignUpSerializer
    throttle_classes = (EmailDelayThrottle,)


class SignUpConfirmView(generics.RetrieveAPIView):
    lookup_field = 'key'
    queryset = ConfirmationEmail.objects.new().not_expired()

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        confirm(obj)
        return redirect(settings.LOGIN_PAGE)


class SignInView(generics.CreateAPIView):
    serializer_class = serializers.SingInSerializer


class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request):
        logout(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
