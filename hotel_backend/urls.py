# hotel_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from bookings.views import RegisterView # Importamos la vista de registro que creaste recién

urlpatterns = [
    path('admin/', admin.site.admin_view),
    
    # Endpoints de Autenticación Unificados
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', RegisterView.as_view(), name='auth_register'),
    
    # Tus otras rutas existentes de la app bookings (suites, reservas, etc.)
    path('api/', include('bookings.urls')),
]