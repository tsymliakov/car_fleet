from django.contrib import admin
from .models import Brand


@admin.register(Brand)
class AdminBrand(admin.ModelAdmin):
    list_display = ['id', 'name', 'body_type', 'tank_capacity']
