from rest_framework import permissions, generics
from rest_framework.response import Response
from account import serializers


class ProfileView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        return self.request.user


class AlertView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.AlertSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.request.user.alerts.active()
        serializer = self.get_serializer(queryset, many=True)
        queryset.decrease()
        return Response(serializer.data)


class AlertDisableView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.AlertDisableSerializer

    def get_queryset(self):
        return self.request.user.alerts.active()
