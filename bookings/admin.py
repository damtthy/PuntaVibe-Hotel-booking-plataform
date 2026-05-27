from django.contrib import admin
from .models import Suite, Room, Booking, Season

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'suite', 'is_active')
    list_filter = ('suite', 'is_active')
    search_fields = ('number',)

# No olvides registrar los demás si no lo habías hecho
admin.site.register(Suite)
admin.site.register(Booking)
admin.site.register(Season)