from django.contrib import admin
from .models import VehicleMileageReport


@admin.register(VehicleMileageReport)
class AdminBrand(admin.ModelAdmin):
    list_display = ['id', 'name']
