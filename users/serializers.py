import uuid

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import SystemUser
from django.contrib.auth.hashers import make_password

class MontadorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = SystemUser
        fields = ['email', 'full_name', 'phone', 'cpf', 'city', 'state', 'region_lat', 'region_lng', 'password']

    def create(self, validated_data):
        validated_data['user_type'] = 'assembler'
        validated_data['username'] = str(uuid.uuid4())[:30]
        validated_data['is_active'] = False
        validated_data['password'] = make_password(validated_data['password'])

        return super().create(validated_data)

class GerenteRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = SystemUser
        fields = ['email', 'full_name', 'phone', 'cpf', 'city', 'state', 'password']

    def create(self, validated_data):
        validated_data['user_type'] = 'manager'
        validated_data['is_active'] = True
        validated_data['username'] = str(uuid.uuid4())[:30]
        validated_data['password'] = make_password(validated_data['password'])

        return super().create(validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_type'] = user.user_type
        token['full_name'] = user.full_name
        token['email'] = user.email

        return token


class MontadorStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemUser
        fields = ['id', 'full_name', 'email', 'is_active']
