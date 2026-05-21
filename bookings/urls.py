from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SuiteViewSet, SeasonViewSet, BookingViewSet

# Creamos el enrutador automático de la API
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'suites', SuiteViewSet)
router.register(r'seasons', SeasonViewSet)
router.register(r'bookings', BookingViewSet)

# Las URLs de la app se generan solas gracias al router
urlpatterns = [
    path('', include(router.urls)),
]