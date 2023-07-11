from django.urls import path
from .views import PointsIndex

urlpatterns = [
    path('<int:id>/', PointsIndex.as_view()),
]
