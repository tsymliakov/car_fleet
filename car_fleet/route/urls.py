from django.urls import path
from .views import RoutesIndex, RouteOnMap

urlpatterns = [
    path('api/<int:id>/', RoutesIndex.as_view(), name='route'),
    path('<int:id>', RouteOnMap.as_view(), name='route_on_map')
]
