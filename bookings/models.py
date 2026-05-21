from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from decimal import Decimal

class Suite(models.Model):  
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

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

    def save(self, *args, **kwargs):
        # 1. Calcular la cantidad de noches
        nights = (self.check_out - self.check_in).days
        if nights <= 0:
            nights = 1 
        
        # 2. Traer precios base y multiplicador de temporada
        base = self.suite.base_price
        mult = self.season.multiplier
        
        # --- LÓGICA DE OCUPACIÓN DINÁMICA ---
        active_bookings = Booking.objects.filter(
            suite=self.suite
        ).filter(
            Q(check_in__lt=self.check_out) & Q(check_out__gt=self.check_in)
        )
        
        if self.pk:
            active_bookings = active_bookings.exclude(pk=self.pk)
            
        total_occupied = active_bookings.count()
        total_inventory = 10 
        
        occupancy_rate = (total_occupied / total_inventory) * 100
        
        # CONVERTIMOS LOS FACTORES A DECIMAL ACÁ:
        occupancy_multiplier = Decimal('1.00')
        
        if occupancy_rate >= 90:    # Queda menos del 10% disponible
            occupancy_multiplier = Decimal('1.40')
        elif occupancy_rate >= 70:  # Queda menos del 30% disponible
            occupancy_multiplier = Decimal('1.20')
            
        # 3. La gran ecuación final de Punta Vibe (multiplicamos Decimal con Decimal)
        self.total_price = base * nights * mult * occupancy_multiplier
        
        # 4. Guardar definitivo en la base de datos
        super().save(*args, **kwargs)