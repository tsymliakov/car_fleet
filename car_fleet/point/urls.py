from django.urls import path
from .views import GetPointsOfVehicle, PointsIndex

urlpatterns = [
    path('<int:id>/', PointsIndex.as_view()),
]
