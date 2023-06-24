from django.urls import path
from .views import Companies


urlpatterns = [
    path('companies/', Companies.as_view(), name='manager_companies'),
]
