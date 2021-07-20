from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'mobile', 'land_line')
        extra_kwargs = {'password': {'min_length': 5, 'write_only': True}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
