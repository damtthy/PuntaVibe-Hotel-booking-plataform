from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationJWTTests(APITestCase):

    def setUp(self):
        self.user_data = {
            "username": "thiago_vibe",
            "email": "thiago@puntavibe.com",
            "password": "PasswordSeguro123"
        }

    def test_flujo_completo_jwt(self):
        """Prueba de diagnóstico para ver dónde se interrumpe el flujo"""
        
        # 1. Diagnóstico de Registro
        response_reg = self.client.post('/api/auth/register/', self.user_data, format='json')
        print("\n=== DEBUG REGISTRO ===")
        print(f"Status esperado: 201 | Status real: {response_reg.status_code}")
        print(f"Datos devueltos: {response_reg.data}")
        self.assertEqual(response_reg.status_code, status.HTTP_201_CREATED)
        
        # 2. Diagnóstico de Login
        login_data = {"username": "thiago_vibe", "password": "PasswordSeguro123"}
        response_log = self.client.post('/api/auth/login/', login_data, format='json')
        print("\n=== DEBUG LOGIN ===")
        print(f"Status esperado: 200 | Status real: {response_log.status_code}")
        print(f"Datos devueltos: {response_log.data}")
        self.assertEqual(response_log.status_code, status.HTTP_200_OK)
        
        # 3. Diagnóstico de Ruta Protegida
        token = response_log.data.get('access')
        if token:
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response_protected = self.client.get('/api/bookings/')
        print("\n=== DEBUG ACCESO PROTEGIDO ===")
        print(f"Status esperado: 200 | Status real: {response_protected.status_code}")
        print(f"Datos devueltos: {response_protected.data}\n")
        self.assertEqual(response_protected.status_code, status.HTTP_200_OK)