from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Driver
from .serializers import DriverFullSerializer


class DriverIndexAPI(APIView):
    def get(self, request):
        drivers = Driver.objects.all()
        serializer = DriverFullSerializer(drivers, many=True)
        return JsonResponse(serializer.data, safe=False)
