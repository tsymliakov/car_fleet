from django.contrib import admin
from .models import Driver
from vehicle.models import Vehicle


@admin.register(Driver)
class AdminDriver(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'salary', 'enterprise', 'vehicles', 'active_vehicle']

    # TODO: сделать отображение компании, в которой работает водитель
    def enterprise(self, obj):
        return obj.enterprise

    # TODO: сделать отображение id всех автомобилей, к которым прикреплен
    # водитель
    def vehicles(self, obj):
        return tuple(Vehicle.objects.filter(driver=obj))
