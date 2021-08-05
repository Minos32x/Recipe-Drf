from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import (TagSerializer, IngredientSerializer)
from .models import (Tag, Ingredient)
from rest_framework.generics import (CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_tags(request):
    result = {'data': 'Empty', 'status': status.HTTP_204_NO_CONTENT}
    tags = Tag.objects.all()
    serialized_tags = TagSerializer(tags, many=Tag)
    if serialized_tags.data:
        result = {'data': serialized_tags.data, 'status': status.HTTP_200_OK}

    return Response(**result)


@api_view(['POST'])
def create_tag(request):
    print("INSIDE CREATING TAG")
    result = {'data': 'Empty', 'status': status.HTTP_204_NO_CONTENT}
    print(request.data)

    data = {'user': request.user.id, 'name': request.data.get('name')}
    # data.update(request.data)
    print("USER -> ", request.user)
    print("Name -> ", request.data.get('name'))

    tag = TagSerializer(data=data)
    # print(tag)

    if tag and tag.is_valid():
        tag.save()
        print('VALID TAG ->>>>>>>>>>>>>>>>>>>>>>>>>>>', tag.data)

        result = {'data': tag.data, 'status': status.HTTP_201_CREATED}
    elif tag.errors:
        print("TAG ERROR ->>>>>>> ", tag.errors)
        result = {'data': tag.errors, 'status': status.HTTP_400_BAD_REQUEST}

    return Response(**result)


@api_view(['PUT', 'PATCH'])
def update_tag(request):
    print("INSIDE UPDATING TAG")

    result = {'data': '-Empty-', 'status': status.HTTP_204_NO_CONTENT}
    print(request.data)

    data = {'user': request.user.id}
    data.update(request.data)
    print("final data -> ", data)

    tag = TagSerializer(instance=Tag.objects.get(pk=request.data.get('id')), data=data)
    if tag and tag.is_valid():
        tag.save()
        print(tag.data)

        result = {'data': tag.data, 'status': status.HTTP_204_NO_CONTENT}
    else:
        result = {'data': tag.errors, 'status': status.HTTP_204_NO_CONTENT}

    return Response(**result)


@api_view(['GET'])
def view_tag(request):
    print("INSIDE VIEW TAG")
    result = {'data': '-Empty-', 'status': status.HTTP_204_NO_CONTENT}
    try:
        serializer = TagSerializer(instance=Tag.objects.get(pk=request.data.get('id')))
        if serializer:
            result['data'] = serializer.data
            result['status'] = status.HTTP_200_OK

    except Exception as e:
        result['data'] = '{}'.format(e)
        result['status'] = status.HTTP_400_BAD_REQUEST

    return Response(**result)


@api_view(['DELETE'])
def delete_tag(request):
    print("INSIDE DELETE TAG")
    result = {'data': '-Empty-', 'status': status.HTTP_204_NO_CONTENT}

    instance = Tag.objects.filter(pk=request.data.get('id'))
    instance = instance.first() if instance.exists() else None
    if instance:
        instance.delete()
        result['data'] = 'Deleted Successfully'
        result['status'] = status.HTTP_200_OK
    else:
        result['data'] = 'Not Found'
        result['status'] = status.HTTP_400_BAD_REQUEST

    return Response(**result)


class BaseIngredient:
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IngredientList(BaseIngredient, ListAPIView):
    pass
    # queryset = Ingredient.objects.all()
    # serializer_class = IngredientSerializer
    #
    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user)


class IngredientCreate(BaseIngredient, CreateAPIView):
    pass
    # queryset = Ingredient.objects.all()
    # serializer_class = IngredientSerializer
    #
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class IngredientRetrieve(RetrieveAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class IngredientUpdate(UpdateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class IngredientDestroy(UpdateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
