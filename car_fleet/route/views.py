from datetime import datetime
from dateutil import parser

import pytz
from rest_framework.views import APIView

from .serializer import RouteSerializer
from point.serializers import PointSerializer

from vehicle.models import Vehicle
from .models import Route
from django.http import HttpResponseNotFound, JsonResponse

from point.models import Point


class RouteIndex(APIView):
    def get(self, request, *args, **kwargs):
        # Получаем id машинки
        vehicle_id = kwargs.get('id')

        tz = pytz.timezone(Vehicle.objects.get(id=vehicle_id).enterprise.timezone)

        start_datetime = self.request.GET.get('start_time', None)
        end_datetime = self.request.GET.get('end_time', None)

        if start_datetime is None or end_datetime is None:
            return HttpResponseNotFound('Код 404. Страница не найдена.')

        start_datetime = parser.parse(start_datetime)
        end_datetime = parser.parse(end_datetime)

        start_datetime = datetime(start_datetime.year,
                                  start_datetime.month,
                                  start_datetime.day,
                                  start_datetime.hour,
                                  start_datetime.minute,
                                  start_datetime.second,
                                  tzinfo=tz)

        end_datetime = datetime(end_datetime.year,
                                end_datetime.month,
                                end_datetime.day,
                                end_datetime.hour,
                                end_datetime.minute,
                                end_datetime.second,
                                tzinfo=tz)

        routes = Route.objects.filter(vehicle__id=vehicle_id) \
            .filter(start__gte=start_datetime) \
            .filter(end__lte=end_datetime)

        if len(routes) == 0:
            return JsonResponse([], safe=False)

        absolute_start = routes[0].start
        absolute_end = routes[len(routes) - 1].end

        points = Point.objects.filter(vehicle__id=vehicle_id).filter(time__lte=absolute_end).filter(
            time__gte=absolute_start)

        serializer = PointSerializer(points, many=True)
        return JsonResponse(serializer.data, safe=False)
