import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    is_montador = models.BooleanField(default=False)
    is_admin_empresa = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.get_full_name()

    @property
    def nome_completo(self):
        """Retorna o nome completo do usuário."""
        return f"{self.first_name} {self.last_name}".strip()