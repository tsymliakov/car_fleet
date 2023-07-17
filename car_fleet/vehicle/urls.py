from django.urls import path
from .views import VehicleCreateView, VehicleUpdateView, DeleteVehicle, VehicleIndexAPI, VehicleView


urlpatterns = [
    path('api/', VehicleIndexAPI.as_view()),
    path('<int:id>/', VehicleView.as_view(), name="vehicle"),
    path('<int:id>/update', VehicleUpdateView.as_view(), name="change_vehicle"),
    path('<int:id>/delete/', DeleteVehicle.as_view(), name="delete_vehicle"),
    path('create/', VehicleCreateView.as_view(), name="create_vehicle"),
]
