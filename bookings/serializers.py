from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Suite, Season, Booking  # Asegurate de que estos sean los nombres exactos de tus modelos

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # Definimos la contraseña como "solo escritura" para que no se devuelva nunca en el JSON
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        # Usamos estrictamente create_user para que Django encripte la contraseña en la BD
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly', 
        # Permite ver suites/disponibilidad sin loguearse (Visitor), 
        # pero exige login para reservar (Customer).
    )
}