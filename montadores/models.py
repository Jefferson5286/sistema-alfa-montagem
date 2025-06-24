# montadores/models.py

import uuid
from django.db import models
from django.conf import settings

class MontadorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='montador_profile',
        # Garante que apenas usuários marcados como montadores possam ter um perfil
        limit_choices_to={'is_montador': True}
    )
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    ganhos_totais = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_montagens = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.nome_completo