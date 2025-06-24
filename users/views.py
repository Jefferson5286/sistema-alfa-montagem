from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import SystemUser
from .permissions import IsManager
from .serializers import (
    MontadorRegisterSerializer,
    GerenteRegisterSerializer,
    CustomTokenObtainPairSerializer,
    MontadorStatusSerializer
)
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings


class MontadorRegisterView(generics.CreateAPIView):
    serializer_class = MontadorRegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        send_mail(
            subject='Cadastro recebido',
            message=f'Olá {user.full_name}, seu cadastro como montador foi recebido e está aguardando aprovação.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )


class GerenteRegisterView(generics.CreateAPIView):
    serializer_class = GerenteRegisterSerializer
    permission_classes = [AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

class ListarMontadoresPendentesView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]
    serializer_class = MontadorStatusSerializer

    def get_queryset(self):
        return SystemUser.objects.filter(user_type='assembler', is_active=False)


class AprovarMontadorView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]
    queryset = SystemUser.objects.filter(user_type='assembler', is_active=False)
    serializer_class = MontadorStatusSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = True
        instance.save()

        send_mail(
            subject='Cadastro aprovado!',
            message=f'Olá {instance.full_name}, seu cadastro foi aprovado. Agora você pode fazer login no sistema.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )

        return Response({'status': 'aprovado com sucesso'})


class RejeitarMontadorView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]
    queryset = SystemUser.objects.filter(user_type='assembler', is_active=False)
    serializer_class = MontadorStatusSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        send_mail(
            subject='Cadastro recusado',
            message=f'Olá {instance.full_name}, infelizmente seu cadastro como montador não foi aprovado. '
                    f'Caso deseje tentar novamente, entre em contato com nossa equipe.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )

        instance.delete()
        return Response({'status': 'montador rejeitado e removido com sucesso'})
