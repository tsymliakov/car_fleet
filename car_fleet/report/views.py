from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from datetime import datetime
from rest_framework.views import APIView
from report.models import VehicleMileageReport, MileageValue



class ReportsView(View):
    def get(self, request, *args, **kwargs):
        str_start_date = request.GET.get('start_date')
        str_end_date = request.GET.get('end_date')
        layout = request.GET.get('layout')
        manager = request.user

        if not str_start_date or not str_end_date or not layout:
            reports = VehicleMileageReport.objects.all()
            return render(request,
                          template_name='report/reports.html',
                          context={'reports': reports,
                                   'mileage_report_type': 'Пробег автомобиля за период'})
        if not manager:
            return HttpResponseNotAllowed()

        date_start = datetime.strptime(str_start_date, "%d/%m/%Y").date()
        date_end = datetime.strptime(str_end_date, "%d/%m/%Y").date()

        queryset_reports = VehicleMileageReport.objects.filter(start_datetime__gte=date_start)\
                                                       .filter(end_datetime__lte=date_end)\
                                                       .filter(period=layout)

        return render(request,
                      template_name='report/reports.html',
                      context={
                          'reports':queryset_reports,
                          'mileage_report_type': 'Пробег автомобиля за период'
                          })
    
    def post(self, request, *args, **kwargs):
        layout = request.POST['layout']
        str_start_date = request.POST['daterange'].split()[0]
        str_end_date = request.POST['daterange'].split()[-1]

        return redirect(f"{reverse('reports')}?start_date={str_start_date}&end_date={str_end_date}&layout={layout}")


class MileageReportREST(APIView):
    def get(self, request, *args, **kwargs):
        str_start_date = request.GET.get('start_date')
        str_end_date = request.GET.get('end_date')
        vehicle_id = request.GET.get('vehicle_id')

        try:
           start_date = datetime.strptime(str_start_date, "%B %d, %Y").date()
           end_date = datetime.strptime(str_end_date, "%B %d, %Y").date()
        except ValueError:
            try:
                start_date = datetime.strptime(str_start_date, "%d-%m-%Y").date()
                end_date = datetime.strptime(str_end_date, "%d-%m-%Y").date()
            except ValueError:
                return HttpResponseNotFound("Неверное время.")

        period = request.GET.get('period')
        manager = request.user

        if not manager:
            return HttpResponseNotAllowed("Требуется аутентификация.")
        
        if not all((str_start_date, str_end_date, period, vehicle_id)):
            return HttpResponseBadRequest("Не хватает одного или нескольких query- параметров")

        reports_query = VehicleMileageReport.objects.filter(vehicle__id=vehicle_id)\
                                                    .filter(start_datetime__gte=start_date)\
                                                    .filter(end_datetime__lte=end_date)
        
        values = MileageValue.objects.filter(report__in=reports_query)

        