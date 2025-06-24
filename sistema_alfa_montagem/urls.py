# config/urls.py (arquivo completo)

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserCreateAPIView
from montagens.views import MontagemViewSet
# Importe outras views aqui...

router = DefaultRouter()
router.register(r'montagens', MontagemViewSet, basename='montagem')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth
    path('api/register/', UserCreateAPIView.as_view(), name='user_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('api/', include(router.urls)),
]