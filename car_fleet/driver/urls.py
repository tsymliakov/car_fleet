from django.urls import path
from .views import DriverIndexAPI


urlpatterns = [
    path('api/', DriverIndexAPI.as_view())
]
