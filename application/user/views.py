from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework import authentication, permissions
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView,
                                     RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.contrib.auth import get_user_model


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer


class RudManagerUserView(RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UpdateUserView(UpdateAPIView):
    serializer_class = UserSerializer


class DeleteUserView(DestroyAPIView):
    serializer_class = UserSerializer


class ListUserView(ListAPIView):
    serializer_class = UserSerializer


# Token Views

class CreateAuthTokenView(ObtainAuthToken):
    """
    Auth token class
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
