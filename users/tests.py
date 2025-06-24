from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import SystemUser
from rest_framework import status
from django.core import mail

class UserFlowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.gerente_data = {
            "email": "gerente@test.com",
            "full_name": "Gerente Teste",
            "phone": "11999999999",
            "cpf": "123.456.789-00",
            "city": "São Paulo",
            "state": "SP",
            "password": "senha123"
        }
        self.montador_data = {
            "email": "montador@test.com",
            "full_name": "Montador Teste",
            "phone": "11988888888",
            "cpf": "987.654.321-00",
            "city": "Campinas",
            "state": "SP",
            "region_lat": -22.90,
            "region_lng": -47.06,
            "password": "senha123"
        }

    def test_cadastro_gerente(self):
        res = self.client.post(reverse('register_gerente'), self.gerente_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(SystemUser.objects.filter(email=self.gerente_data['email'], is_active=True).exists())

    def test_cadastro_montador(self):
        res = self.client.post(reverse('register_montador'), self.montador_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = SystemUser.objects.get(email=self.montador_data['email'])
        self.assertFalse(user.is_active)
        self.assertEqual(user.user_type, 'assembler')
        self.assertEqual(len(mail.outbox), 1)  # Confirma que e-mail foi enviado

    def test_login_gerente(self):
        SystemUser.objects.create_user(username='g1', is_active=True, user_type='manager', **self.gerente_data)
        res = self.client.post(reverse('token_obtain_pair'), {
            "email": self.gerente_data['email'],
            "password": self.gerente_data['password']
        }, format='json')
        self.assertIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_montador_inativo_falha(self):
        SystemUser.objects.create_user(username='m1', is_active=False, user_type='assembler', **self.montador_data)
        res = self.client.post(reverse('token_obtain_pair'), {
            "email": self.montador_data['email'],
            "password": self.montador_data['password']
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def autenticar_gerente(self):
        user = SystemUser.objects.create_user(username='g1', is_active=True, user_type='manager', **self.gerente_data)
        res = self.client.post(reverse('token_obtain_pair'), {
            "email": self.gerente_data['email'],
            "password": self.gerente_data['password']
        }, format='json')
        token = res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return user

    def test_listar_montadores_pendentes(self):
        self.autenticar_gerente()
        SystemUser.objects.create_user(username='m1', is_active=False, user_type='assembler', **self.montador_data)
        res = self.client.get(reverse('listar_montadores'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_aprovar_montador(self):
        self.autenticar_gerente()
        montador = SystemUser.objects.create_user(username='m1', is_active=False, user_type='assembler', **self.montador_data)
        url = reverse('aprovar_montador', kwargs={'pk': montador.pk})
        res = self.client.put(url)
        montador.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(montador.is_active)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('aprovado', mail.outbox[0].subject.lower())

    def test_rejeitar_montador(self):
        self.autenticar_gerente()
        montador = SystemUser.objects.create_user(username='m1', is_active=False, user_type='assembler', **self.montador_data)
        url = reverse('rejeitar_montador', kwargs={'pk': montador.pk})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(SystemUser.objects.filter(pk=montador.pk).exists())
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('recusado', mail.outbox[0].subject.lower())
