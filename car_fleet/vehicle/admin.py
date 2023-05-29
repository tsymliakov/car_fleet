from django.contrib import admin
from .models import Vehicle
from brand.models import Brand


@admin.register(Vehicle)
class AdminVehicle(admin.ModelAdmin):
    list_display = ['id', 'total_cost', 'brand_name']

    def brand_name(self, obj):
        return obj.brand.name


@admin.register(Brand)
class AdminBrand(admin.ModelAdmin):
    list_display = ['id', 'name', 'body_type', 'tank_capacity']
