from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleIndexAPI(APIView):
    def get(self, request):
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return JsonResponse(serializer.data, safe=False)
