from rest_framework import generics, permissions
from configs import serializers


class UserConfigView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserConfigSerializer

    def get_object(self):
        return self.request.user.userconfig
