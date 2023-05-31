from django.contrib import admin
from .models import Vehicle
from driver.models import Driver


@admin.register(Vehicle)
class AdminVehicle(admin.ModelAdmin):
    list_display = ['id', 'total_cost', 'brand_name', 'drivers', 'enterprise', 'really_active_driver']

    def brand_name(self, obj : Vehicle):
        return obj.brand.name

    def drivers(self, obj : Vehicle):
        return tuple(Driver.objects.filter(vehicle=obj))

    def enterprise(self, obj : Vehicle):
        return obj.enterprise

    def really_active_driver(self, obj : Vehicle):
        return obj.active_driver

    really_active_driver.short_description = 'Active driver'
