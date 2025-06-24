import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class SystemUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('manager', 'Gerente'),
        ('assembler', 'Montador'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)

    region_lat = models.FloatField(null=True, blank=True)
    region_lng = models.FloatField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'phone', 'cpf', 'city', 'state', 'user_type']

    def __str__(self):
        return f"{self.full_name} ({self.get_user_type_display()})"
