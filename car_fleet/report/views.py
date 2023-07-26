from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from rest_framework.views import APIView


class ReportsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='report/reports.html')
    
    def post(self, request, *args, **kwargs):
        return redirect(reverse('reports'))
