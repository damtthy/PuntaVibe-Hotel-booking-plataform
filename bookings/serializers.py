from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Suite, Season, Booking  # Asegurate de que estos sean los nombres exactos de tus modelos

# 1. Serializador de Usuarios (para saber quién reserva)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# 2. Serializador de Temporadas
class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'  # Traduce todos los campos de la tabla

# 3. Serializador de Habitaciones / Suites
class SuiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suite
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    suite_details = SuiteSerializer(source='suite', read_only=True)
    season_details = SeasonSerializer(source='season', read_only=True)

    check_in = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d", "iso-8601"])
    check_out = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d", "iso-8601"])

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'user_details', 'suite', 'suite_details', 
            'season', 'season_details', 'check_in', 'check_out', 
            'total_price'
        ]
        read_only_fields = ['total_price']