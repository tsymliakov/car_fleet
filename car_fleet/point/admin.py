from django.contrib import admin
from .models import Point


@admin.register(Point)
class AdminBrand(admin.ModelAdmin):
    list_display = ['id', 'point', 'vehicle', 'time']
