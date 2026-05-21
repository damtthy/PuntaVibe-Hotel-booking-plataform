from django.contrib import admin
from .models import Suite, Season, Booking

# Register your models here so they appear in the visual dashboard
admin.site.register(Suite)
admin.site.register(Season)
admin.site.register(Booking)