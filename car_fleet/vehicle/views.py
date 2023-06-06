from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponseForbidden
from .models import Vehicle
from .serializers import VehicleSerializer
from manager.models import Manager
from enterprise.models import Enterprise


class VehicleIndexAPI(APIView):
    def get(self, request):
        user = request.user

        if user.is_superuser:
            enterprises = Vehicle.objects.all()
            serializer = VehicleSerializer(enterprises, many=True)
            return JsonResponse(serializer.data, safe=False)

        if isinstance(getattr(user, 'manager', None), Manager):
            manager : Manager = getattr(user, 'manager')
            vehicles = Vehicle.objects.filter(enterprise__manager=manager)
            serializer = VehicleSerializer(vehicles, many=True)
            return JsonResponse(serializer.data, safe=False)

        return HttpResponseForbidden('Доступ запрещен\n')