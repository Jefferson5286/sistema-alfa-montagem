# users/views.py
from rest_framework import generics
from .models import User
from .serializers import UserCreateSerializer
from rest_framework.permissions import AllowAny

class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny] # Permite que qualquer um se cadastre