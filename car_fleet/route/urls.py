from django.urls import path
from .views import RouteIndex

urlpatterns = [
    path('<int:id>/', RouteIndex.as_view()),
]
