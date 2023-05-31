from django.contrib import admin
from .models import Driver
from vehicle.models import Vehicle


@admin.register(Driver)
class AdminDriver(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'salary', 'enterprise', 'vehicles', 'active_vehicle']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["active_vehicle"].queryset = Vehicle.objects.filter(active_driver__isnull=True).filter(driver=obj)
        form.base_fields["vehicle"].queryset = Vehicle.objects.filter(enterprise=obj.enterprise)
        return form

    def enterprise(self, obj):
        return obj.enterprise

    def vehicles(self, obj):
        return tuple(Vehicle.objects.filter(driver=obj))
