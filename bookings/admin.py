from django.contrib import admin
from .models import Suite, Room, Booking, Season

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'suite', 'is_active')
    list_filter = ('suite', 'is_active')
    search_fields = ('number',)

admin.site.register(Suite)
admin.site.register(Booking)
admin.site.register(Season)