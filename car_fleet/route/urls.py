from django.urls import path
from .views import RoutesIndex



urlpatterns = [
    path('<int:id>', RoutesIndex.as_view()),
]
