from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Enterprise
from .serializers import EnterpriseSerializer


class EnterpriseIndexAPI(APIView):
    def get(self, request):
        enterprises = Enterprise.objects.all()
        serializer = EnterpriseSerializer(enterprises, many=True)
        return JsonResponse(serializer.data, safe=False)
