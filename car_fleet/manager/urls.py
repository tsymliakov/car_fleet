from django.urls import path
from .views import ViewEnterprise, IndexEnterprises, LoginManager, Menu

urlpatterns = [
    path('login/', LoginManager.as_view(), name='login_manager'),
    path('menu/', Menu.as_view(), name='menu'),
    path('enteprises/', IndexEnterprises.as_view(), name='manager_enterprises'),
    path('enteprises/<str:name>', ViewEnterprise.as_view(), name='enterprise')
]
