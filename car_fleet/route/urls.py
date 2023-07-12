from django.urls import path
from views import RoutesIndex



urlpatterns = [
    path('/', RoutesIndex.as_view()),
]
