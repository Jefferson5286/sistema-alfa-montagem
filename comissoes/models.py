# comissoes/models.py

import uuid
from django.db import models

class Comissao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    faixa_min = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor mínimo da montagem para aplicar esta comissão.")
    faixa_max = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor máximo da montagem para aplicar esta comissão.")
    porcentagem = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentual da comissão (ex: 5.00 para 5%).")

    class Meta:
        verbose_name_plural = "Comissões"
        ordering = ['faixa_min']

    def __str__(self):
        return f"Faixa de R${self.faixa_min} a R${self.faixa_max}: {self.porcentagem}%"