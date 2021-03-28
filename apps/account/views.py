from rest_framework import permissions
from rest_framework import generics
from account.serializers import ProfileSerializer


class ProfileView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user
