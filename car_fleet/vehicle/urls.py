from django.urls import path
from .views import VehicleIndexAPI


urlpatterns = [
    path('api/', VehicleIndexAPI.as_view())
]
