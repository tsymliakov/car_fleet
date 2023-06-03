from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponseForbidden
from .models import Enterprise
from .serializers import EnterpriseSerializer
from manager.models import Manager


class EnterpriseIndexAPI(APIView):
    def get(self, request):
        user = request.user

        if user.is_superuser:
            enterprises = Enterprise.objects.all()
            serializer = EnterpriseSerializer(enterprises, many=True)
            return JsonResponse(serializer.data, safe=False)

        if isinstance(getattr(user, 'manager', None), Manager):
            manager = getattr(user, 'manager')
            enterprises = Enterprise.objects.filter(manager=manager)
            serializer = EnterpriseSerializer(enterprises, many=True)
            return JsonResponse(serializer.data, safe=False)

        return HttpResponseForbidden('Доступ запрещен')

