from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Suite, Season, Booking
from .serializers import UserSerializer, SuiteSerializer, SeasonSerializer, BookingSerializer, RegisterSerializer

from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

User = get_user_model()

# 1. Ventanilla para manejar Usuarios
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 2. Ventanilla para manejar Temporadas
class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

# 3. Ventanilla para manejar Habitaciones (Suites)
class SuiteViewSet(viewsets.ModelViewSet):
    queryset = Suite.objects.all()
    serializer_class = SuiteSerializer

# 4. Ventanilla para manejar las Reservas (Bookings)
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        """
        Opcional: Si en el futuro querés que el usuario que está logueado 
        se asigne automáticamente a la reserva, se puede manejar acá.
        Por ahora, dejamos que DRF use la lógica estándar.
        """
        serializer.save()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny] # Permiso abierto: cualquiera puede registrarse sin estar logueado
    serializer_class = RegisterSerializer