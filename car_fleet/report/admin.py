from django.contrib import admin
from .models import VehicleMileageReport, MileageValue


@admin.register(VehicleMileageReport)
class AdminBrand(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(MileageValue)
class AdminBrand(admin.ModelAdmin):
    list_display = ['id', 'date_time', 'mileage']
