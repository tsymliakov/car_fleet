from django.contrib import admin
from .models import VehicleMileageReport, MileAgeValue


@admin.register(VehicleMileageReport)
class AdminBrand(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(MileAgeValue)
class AdminBrand(admin.ModelAdmin):
    list_display = ['id', 'date_time', 'mileage']
