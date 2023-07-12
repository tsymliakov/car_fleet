from datetime import datetime
from dateutil import parser

import pytz
from rest_framework.views import APIView

from point.serializers import PointSerializer

from vehicle.models import Vehicle
from .models import Route
from django.http import HttpResponseNotFound, JsonResponse

from point.models import Point


class RoutesIndex(APIView):
    def get(self, request, *args, **kwargs):
        vehicle_id = kwargs.get('id')
        start_datetime = self.request.GET.get('start_time', None)
        end_datetime = self.request.GET.get('end_time', None)

        if start_datetime is None or end_datetime is None:
            return HttpResponseNotFound('Код 404. Страница не найдена.')

        routes = Route.objects\
            .filter(start__gte=start_datetime)\
            .filter(end__lte=end_datetime)\
            .filter(vehicle__id=vehicle_id)

        # Далее требуется передать это в сериализатор, который добавит лополнительные поля. Такие как
        # адрес начальной и конечной точки.