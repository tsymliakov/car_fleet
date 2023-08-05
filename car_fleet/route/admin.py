from django.contrib import admin
from .models import Route


@admin.register(Route)
class AdminBrand(admin.ModelAdmin):
    list_display = ['id', 'vehicle', 'start', 'end', 'distance']
