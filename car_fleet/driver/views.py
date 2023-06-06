from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponseForbidden
from .models import Driver
from .serializers import DriverSerializer
from manager.models import Manager


class DriverIndexAPI(APIView):
    def get(self, request):
        user = request.user

        if user.is_superuser:
            drivers = Driver.objects.all()
            serializer = DriverSerializer(drivers, many=True)
            return JsonResponse(serializer.data, safe=False)

        if isinstance(getattr(user, 'manager', None), Manager):
            manager : Manager = getattr(user, 'manager')
            drivers = Driver.objects.filter(enterprise__manager=manager)
            serializer = DriverSerializer(drivers, many=True)
            return JsonResponse(serializer.data, safe=False)

        return HttpResponseForbidden('Доступ запрещен\n')
