from rest_framework import serializers
from montadores.models import MontadorProfile

class MontadorProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField() # Exibe o nome do usuário
    nome_completo = serializers.CharField(source='user.nome_completo', read_only=True)

    class Meta:
        model = MontadorProfile
        fields = '__all__'