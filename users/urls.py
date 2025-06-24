from django.urls import path
from .views import (
    MontadorRegisterView, GerenteRegisterView,
    CustomTokenObtainPairView, ListarMontadoresPendentesView,
    AprovarMontadorView, RejeitarMontadorView
)

urlpatterns = [
    path('register/montador/', MontadorRegisterView.as_view(), name='register_montador'),
    path('register/gerente/', GerenteRegisterView.as_view(), name='register_gerente'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('gerente/montadores/pendentes/', ListarMontadoresPendentesView.as_view(), name='listar_montadores'),
    path('gerente/montadores/aprovar/<uuid:pk>/', AprovarMontadorView.as_view(), name='aprovar_montador'),
    path('gerente/montadores/rejeitar/<uuid:pk>/', RejeitarMontadorView.as_view(), name='rejeitar_montador'),
]