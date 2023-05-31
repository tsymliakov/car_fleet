from django.contrib import admin
from .models import Enterprise
from vehicle.models import Vehicle
from driver.models import Driver


@admin.register(Enterprise)
class AdminEnterprise(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'vehicles', 'drivers']

    def vehicles(self, obj):
        return tuple(Vehicle.objects.filter(enterprise=obj))

    def drivers(self, obj):
        return tuple(Driver.objects.filter(enterprise=obj))
