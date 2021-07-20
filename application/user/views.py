from user.serializers import UserSerializer
from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView)


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer


class GetUserView(RetrieveAPIView):
    serializer_class = UserSerializer


class UpdateUserView(UpdateAPIView):
    serializer_class = UserSerializer


class DeleteUserView(DestroyAPIView):
    serializer_class = UserSerializer


class ListUserView(ListAPIView):
    serializer_class = UserSerializer
