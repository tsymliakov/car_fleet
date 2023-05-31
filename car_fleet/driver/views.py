from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Driver
from .serializers import DriverSerializer


class DriverIndexAPI(APIView):
    def get(self, request):
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return JsonResponse(serializer.data, safe=False)
