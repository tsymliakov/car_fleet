from django.urls import path
from .views import EnterpriseIndexAPI


urlpatterns = [
    path('api/', EnterpriseIndexAPI.as_view())
]
