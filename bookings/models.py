from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from decimal import Decimal
from datetime import date, datetime
from django.core.exceptions import ValidationError

class Suite(models.Model):  
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)  # Número o código de habitación
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE, related_name='rooms')
    is_active = models.BooleanField(default=True)  # Por si la habitación entra en mantenimiento/reparación

    def __str__(self):
        return f"Habitación {self.number} ({self.suite.name})"

class Season(models.Model):  # <-- Corregido acá también
    name = models.CharField(max_length=50)  
    multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)

    def __str__(self):
        return f"{self.name} (x{self.multiplier})"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Reserva de {self.user.username} - {self.suite.name}"
    
    def clean(self):
        if isinstance(self.check_in, str):
            self.check_in = datetime.datetime.strptime(self.check_in, "%Y-%m-%d").date()
        if isinstance(self.check_out, str):
            self.check_out = datetime.datetime.strptime(self.check_out, "%Y-%m-%d").date()

        # Si alguna fecha falta, no continuamos con las validaciones cruzadas
        if not self.check_in or not self.check_out:
            raise ValidationError("Ambas fechas (Check-in y Check-out) son obligatorias.")

        # 2. Validación Cronológica: Salida antes que la entrada
        if self.check_out <= self.check_in:
            raise ValidationError({
                'check_out': "La fecha de salida (Check-out) debe ser posterior a la fecha de entrada (Check-in)."
            })

        # 3. Validación de Pasado: Evitar que reserven en días que ya ocurrieron
        today = datetime.date.today()
        if self.check_in < today:
            raise ValidationError({
                'check_in': "No se pueden realizar reservas con una fecha de entrada en el pasado."
            })

        # 4. FILTRO ANTI-OVERBOOKING (Validación de disponibilidad por inventario)
        # Buscamos todas las reservas que colisionen temporalmente con el rango solicitado
        overlapping_bookings = Booking.objects.filter(
            suite=self.suite
        ).filter(
            Q(check_in__lt=self.check_out) & Q(check_out__gt=self.check_in)
        )

        # Si el usuario está modificando una reserva que ya existe, la excluimos para no chocar con sí misma
        if self.pk:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)

        total_occupied = overlapping_bookings.count()
        total_inventory = 10  # Capacidad máxima simulada de este tipo de suite en el hotel

        # Si ya se alcanzó el límite de habitaciones ocupadas para esas fechas, lanzamos el error
        if total_occupied >= total_inventory:
            raise ValidationError(
                f"Lo sentimos, no hay disponibilidad para la suite '{self.suite.name}' en el rango seleccionado. "
                f"Todas las unidades disponibles ({total_inventory}) ya están reservadas."
            )


    def save(self, *args, **kwargs):

        self.clean()

        # --- BLINDAJE DE FECHAS PARA LA API ---
        # Si las fechas entran como string (JSON de la API), las convertimos a objetos date
        if isinstance(self.check_in, str):
            self.check_in = datetime.strptime(self.check_in, "%Y-%m-%d").date()
        if isinstance(self.check_out, str):
            self.check_out = datetime.strptime(self.check_out, "%Y-%m-%d").date()

        # 1. Calcular la cantidad de noches (ahora 100% seguro de que son objetos date)
        nights = (self.check_out - self.check_in).days
        if nights <= 0:
            raise ValidationError("La fecha de salida (Check-out) debe ser posterior a la fecha de entrada (Check-in).")
    
        # 2. Traer precios base y multiplicador de temporada
        base = self.suite.base_price
        season_multiplier = self.season.multiplier
        
        # --- LÓGICA DE OCUPACIÓN DINÁMICA ---
        active_bookings = Booking.objects.filter(
            suite=self.suite
        ).filter(
            Q(check_in__lt=self.check_out) & Q(check_out__gt=self.check_in)
        )
        
        if self.pk:
            active_bookings = active_bookings.exclude(pk=self.pk)
            
        total_occupied = active_bookings.count()
        total_inventory = self.suite.rooms.filter(is_active=True).count()

        if total_inventory == 0:
            raise ValidationError(f"La categoría '{self.suite.name}' no tiene habitaciones físicas habilitadas en el hotel.")
        
        occupancy_rate = (total_occupied / total_inventory) * 100
        
        # CONVERTIMOS LOS FACTORES A DECIMAL ACÁ:
        occupancy_multiplier = Decimal('1.00')
        
        if occupancy_rate >= 90:    # Queda menos del 10% disponible
            occupancy_multiplier = Decimal('1.40')
        elif occupancy_rate >= 70:  # Queda menos del 30% disponible
            occupancy_multiplier = Decimal('1.20')
        elif occupancy_rate < 30:
        # Descuento comercial: Más del 70% disponible (Ocupación < 30%) -> -10% para impulsar ventas
            occupancy_multiplier = Decimal('0.90')

        # 3. La gran ecuación final de Punta Vibe
        self.total_price = base * nights * season_multiplier * occupancy_multiplier
        
        # 4. Guardar definitivo en la base de datos
        super().save(*args, **kwargs)

