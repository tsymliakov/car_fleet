from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponseForbidden
from vehicle.forms import VehicleForm

from enterprise.models import Enterprise
from .models import Vehicle
from .serializers import VehicleSerializer
from manager.models import Manager
from rest_framework.response import Response
from rest_framework import generics



class VehicleIndexAPI(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class VehicleUpdateView(View):
    def get(self, request, *args, **kwargs):
        vehicle = Vehicle.objects.get(id=kwargs["id"])
        return render(request, 'vehicle/vehicle.html', {'vehicle': vehicle})

    def post(self, request, *args, **kwargs):
        id = kwargs["id"]
        rental = float(request.POST.get('rental'))
        mileage = int(request.POST.get('mileage'))
        vehicle = Vehicle.objects.get(id=id)

        if mileage < 0 or rental < 0:
            return render(request, 'vehicle/vehicle.html', {'vehicle': vehicle})

        vehicle.rental_per_hour = rental
        vehicle.mileage = mileage

        vehicle.save()

        return redirect('enterprise', name=vehicle.enterprise.name)


class DeleteVehicle(View):
    def get(self, request, *args, **kwargs):
        vehicle = Vehicle.objects.get(id=kwargs["id"])
        return render(request, 'vehicle/delete.html', {'vehicle': vehicle})

    def post(self, request, *args, **kwargs):
        vehicle = Vehicle.objects.get(id=kwargs["id"])
        name = vehicle.enterprise.name
        vehicle.delete()

        return redirect('enterprise', name=name)


class VehicleCreateView(CreateView):
    form_class = VehicleForm
    template_name = 'vehicle/vehicle_form.html'

    def get_form_kwargs(self):
        kwargs = super(VehicleCreateView, self).get_form_kwargs()
        kwargs['manager_id'] = DeleteVehicle.manager_id
        return kwargs

    def get(self, request, *args, **kwargs):
        DeleteVehicle.manager_id = request.user.id
        return super().get(request, *args, **kwargs)
