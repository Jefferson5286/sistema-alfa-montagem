# montagens/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Montagem
from .serializers import MontagemSerializer
from comissoes.models import Comissao
from utils.geolocation import haversine


class MontagemViewSet(viewsets.ModelViewSet):
    serializer_class = MontagemSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_montador:
            # Regra: Montador só vê montagens num raio de 50km
            profile = user.montador_profile
            if not profile or not profile.latitude or not profile.longitude:
                return Montagem.objects.none()  # Retorna vazio se o montador não tem localização

            raio_km = 50
            montagens_proximas_ids = []
            montagens_pendentes = Montagem.objects.filter(status='pendente')

            for montagem in montagens_pendentes:
                distancia = haversine(
                    profile.longitude, profile.latitude,
                    montagem.longitude_cliente, montagem.latitude_cliente
                )
                if distancia <= raio_km:
                    montagens_proximas_ids.append(montagem.id)

            return Montagem.objects.filter(id__in=montagens_proximas_ids)

        elif user.is_admin_empresa or user.is_staff:
            # Admin vê todas
            return Montagem.objects.all()

        return Montagem.objects.none()  # Outros usuários não veem montagens

    # Regra: Cálculo automático da comissão (exemplo)
    def perform_create(self, serializer):
        # ...lógica para calcular comissão...
        # Esta lógica seria melhor em um `signal` ou no método `save` do modelo
        montagem = serializer.save()

        # Exemplo simplificado de cálculo de comissão
        try:
            faixa_comissao = Comissao.objects.get(
                faixa_min__lte=montagem.valor,
                faixa_max__gte=montagem.valor
            )
            valor_comissao = (montagem.valor * faixa_comissao.porcentagem) / 100
            print(f"Comissão calculada para a montagem {montagem.id}: R$ {valor_comissao}")
            # Aqui você poderia salvar esse valor em outro campo ou modelo.
        except Comissao.DoesNotExist:
            print(f"Nenhuma faixa de comissão encontrada para o valor R$ {montagem.valor}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Regra: Admin atribui montagem a um montador disponível
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def atribuir_montador(self, request, pk=None):
        montagem = self.get_object()
        montador_id = request.data.get('montador_id')

        if not montador_id:
            return Response({'error': 'ID do montador é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificação de disponibilidade (exemplo simples)
        # Uma lógica mais complexa poderia checar a agenda do montador.
        if montagem.status != 'pendente':
            return Response({'error': 'Esta montagem não está pendente.'}, status=status.HTTP_400_BAD_REQUEST)

        montagem.montador_id = montador_id
        montagem.status = 'aceita'
        montagem.save()

        return Response(MontagemSerializer(montagem).data, status=status.HTTP_200_OK)