from django.shortcuts import render
from rest_framework.views import APIView


class MonthlyMileageRESTView(APIView):
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

