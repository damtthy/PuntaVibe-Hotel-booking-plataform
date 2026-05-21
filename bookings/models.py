from django.db import models
from django.contrib.auth.models import User

class Suite(models.Model):
    """
    Represents the premium rooms available in the boutique hotel.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.IntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=150.00)

    def __str__(self):
        return self.name

class Season(models.Model):
    """
    Defines calendar ranges (High, Mid, Low seasons) and their price multipliers.
    """
    name = models.CharField(max_length=50)  # e.g., 'High Season', 'Low Season'
    start_date = models.DateField()
    end_date = models.DateField()
    price_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)

    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"

class Booking(models.Model):
    """
    The core transactional model linking a User to a Suite for specific dates.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.user.username} ({self.suite.name})"

