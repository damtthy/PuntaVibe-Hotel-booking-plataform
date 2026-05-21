from django.db import models
from django.contrib.auth.models import User

class Suite(models.Model):  # <-- Corregido acá (models.Model)
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

class Booking(models.Model):  # <-- Corregido acá también
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Reserva de {self.user.username} - {self.suite.name}"

    def save(self, *args, **kwargs):
        # 1. Calcular noches
        nights = (self.check_out - self.check_in).days
        if nights <= 0:
            nights = 1 
        
        # 2. Traer valores
        base = self.suite.base_price
        mult = self.season.multiplier
        
        # 3. Calcular total
        self.total_price = base * nights * mult
        
        # 4. Guardar real
        super().save(*args, **kwargs)