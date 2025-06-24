from rest_framework import serializers
from .models import Montagem, ProblemaReportado
from users.serializers import UserSerializer

class MontagemSerializer(serializers.ModelSerializer):
    montador_info = UserSerializer(source='montador', read_only=True)

    class Meta:
        model = Montagem
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

class ProblemaReportadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemaReportado
        fields = '__all__'