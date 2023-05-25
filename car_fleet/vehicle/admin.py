from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class AdminVehicle(admin.ModelAdmin):
    list_display = ['id', 'total_cost']
