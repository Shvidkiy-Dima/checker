from rest_framework import generics, permissions
from notification import models, serializers


class TelegramConfirmationCreateView(generics.CreateAPIView):
    serializer_class = serializers.TelegramConfirmationCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TelegramDisableView(generics.CreateAPIView):
    serializer_class = serializers.TelegramDisableSerializer
    permission_classes = (permissions.IsAuthenticated,)
