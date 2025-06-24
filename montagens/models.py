# montagens/models.py

import uuid
from django.db import models
from django.conf import settings

class Montagem(models.Model):
    class StatusChoices(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        ACEITA = 'aceita', 'Aceita'
        CONCLUIDA = 'concluida', 'Concluída'
        PROBLEMA = 'problema', 'Com Problema'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loja = models.CharField(max_length=100)
    endereco_cliente = models.TextField()
    latitude_cliente = models.DecimalField(max_digits=10, decimal_places=8)
    longitude_cliente = models.DecimalField(max_digits=11, decimal_places=8)
    descricao_movel = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_agendada = models.DateTimeField()
    status = models.CharField(max_length=15, choices=StatusChoices.choices, default=StatusChoices.PENDENTE)
    montador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='montagens',
        limit_choices_to={'is_montador': True}
    )
    comprovante = models.ImageField(upload_to='comprovantes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Montagem {self.id} - {self.loja}"

class ProblemaReportado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    montagem = models.ForeignKey(Montagem, on_delete=models.CASCADE, related_name='problemas')
    descricao = models.TextField()
    foto = models.ImageField(upload_to='problemas_fotos/')
    data_reportado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Problema na Montagem {self.montagem.id}"