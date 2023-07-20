from json import load

from django.views import View
from rest_framework.views import APIView

from point.models import Point
from .serializers import RouteSerializer, get_location

import requests

from .models import Route
from django.http import JsonResponse, HttpResponse


class RouteOnMap(View):
    def get(self, request, *args, **kwargs):
        route_id = kwargs['id']
        route = Route.objects.get(id=route_id)

        vehicle_id = route.vehicle.id

        points = Point.objects.filter(vehicle__id=vehicle_id)\
            .filter(time__gte=route.start)\
            .filter(time__lte=route.end)

        with open("settings.json", "r") as settings_file:
            LOCAL_SETTINGS = load(settings_file)

        api_key = LOCAL_SETTINGS.get('api_key')

        point_params = []
        for i, p in enumerate(points):
            latitude = p.point.y
            longitude = p.point.x
            point_params.append(f"{latitude},{longitude}")

        points_for_url = ','.join(point_params)

        url = f"https://static-maps.yandex.ru/1.x/?l=map&pl={points_for_url}&\
        pt={points_for_url[0]},vkbkm&apikey={api_key}"

        r = requests.get(url)

        return HttpResponse(r.content, content_type='image/png')


class RoutesIndex(APIView):
    def get(self, request, *args, **kwargs):
        vehicle_id = kwargs.get('id')
        start_datetime = self.request.GET.get('start_time', None)
        end_datetime = self.request.GET.get('end_time', None)

        if start_datetime is None or end_datetime is None:
            routes = Route.objects.filter(vehicle__id=vehicle_id)
        else:
            routes = Route.objects\
                .filter(start__gte=start_datetime)\
                .filter(end__lte=end_datetime)\
                .filter(vehicle__id=vehicle_id)

        serializer = RouteSerializer(routes, many=True)

        return JsonResponse(serializer.data, safe=False)
