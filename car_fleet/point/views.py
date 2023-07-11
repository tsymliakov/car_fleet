from datetime import datetime
from dateutil import parser

import pytz

from django.http import JsonResponse, HttpResponse
from rest_framework import generics

from point.models import Point
from vehicle.models import Vehicle
from point.serializers import PointSerializer
from rest_framework.views import APIView

from django.core.serializers import serialize


class GetPointsOfVehicle(generics.ListCreateAPIView):
    serializer_class = PointSerializer

    def get_queryset(self):
        vehicle_id = self.kwargs['id']

        start_datetime = self.request.GET.get('start_time',
                                              datetime.utcnow().replace(hour=0,
                                                                        minute=0,
                                                                        second=0,
                                                                        microsecond=0))
        end_datetime = self.request.GET.get('end_time', datetime.utcnow())

        return Point.objects.filter(vehicle__id=vehicle_id).filter(time__lte=end_datetime).filter(time__gte=start_datetime)


class PointsIndex(APIView):
    def get(self, request, *args, **kwargs):
        vehicle_id = self.kwargs['id']
        tz = pytz.timezone(Vehicle.objects.get(id=vehicle_id).enterprise.timezone)

        start_datetime = self.request.GET.get('start_time', None)
        if not start_datetime:
            start_datetime = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            start_datetime = parser.parse(start_datetime)

        start_datetime = datetime(start_datetime.year, start_datetime.month, start_datetime.day, start_datetime.hour,
                 start_datetime.minute, start_datetime.second, tzinfo=tz)

        end_datetime = self.request.GET.get('end_time', None)
        if not end_datetime:
            end_datetime = datetime.utcnow()
        else:
            end_datetime = parser.parse(end_datetime)

        end_datetime = datetime(end_datetime.year, end_datetime.month, end_datetime.day, end_datetime.hour,
                 end_datetime.minute, end_datetime.second, tzinfo=tz)

        points_queryset = Point.objects.filter(vehicle__id=vehicle_id).filter(time__lte=end_datetime).filter(time__gte=start_datetime)

        serializator = PointSerializer(points_queryset, many=True)

        geojson_format = self.request.GET.get('geojson', '0')

        if geojson_format == '1':
            return JsonResponse(serialize("geojson", points_queryset), safe=False)

        return JsonResponse(serializator.data, safe=False)
