from django.urls import path
from .views import PointsIndex, GetPointsInRoutes

urlpatterns = [
    path('<int:id>/', PointsIndex.as_view()),
    path('route_points/<int:id>/', GetPointsInRoutes.as_view()),
]
