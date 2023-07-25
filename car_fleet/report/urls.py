from django.urls import path
from .views import MonthlyMileageRESTView

urlpatterns = [
    path('mounthlymileage/<int:id>', MonthlyMileageRESTView.as_view(), name='monthlymilage_report')
]
