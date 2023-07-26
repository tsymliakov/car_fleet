from django.urls import path
from .views import ReportsView, MileageReportREST


urlpatterns = [
    path('', ReportsView.as_view(), name="reports"),
    path('mileage/', MileageReportREST.as_view(), name="get_mileage_report_rest"),
]
