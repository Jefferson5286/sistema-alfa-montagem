from rest_framework import serializers
from .models import User

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'cpf', 'is_montador')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'], # Usamos o email como username
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            cpf=validated_data.get('cpf'),
            is_montador=validated_data.get('is_montador', False)
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'nome_completo', 'cpf', 'is_montador', 'is_admin_empresa')