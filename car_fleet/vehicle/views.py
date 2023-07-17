from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView

from point.models import Point
from vehicle.forms import VehicleForm

from .models import Vehicle
from .serializers import VehicleSerializer
from rest_framework import generics

from route.models import Route
from route.serializers import get_location


class VehicleIndexAPI(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class VehicleUpdateView(View):
    def get(self, request, *args, **kwargs):
        vehicle = Vehicle.objects.get(id=kwargs["id"])
        return render(request, 'vehicle/vehicle_update.html', {'vehicle': vehicle})

    def post(self, request, *args, **kwargs):
        id = kwargs["id"]
        rental = float(request.POST.get('rental'))
        mileage = int(request.POST.get('mileage'))
        vehicle = Vehicle.objects.get(id=id)

        if mileage < 0 or rental < 0:
            return render(request, 'vehicle/vehicle_update.html', {'vehicle': vehicle})

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


class VehicleView(View):
    def get(self, request, *args, **kwargs):
        vehicle_id = kwargs['id']
        start_datetime = request.GET.get('start_datetime')
        end_datetime = request.GET.get('end_datetime')

        routes = []

        if start_datetime and end_datetime:
            routes = Route.objects.filter(vehicle__id=vehicle_id) \
                          .filter(start__gte=start_datetime) \
                          .filter(end__lte=end_datetime)

        for r in routes:
            start_of_route = Point.objects.filter(vehicle__id=vehicle_id) \
                .filter(time__gte=r.start) \
                .order_by('time')[0]
            end_of_route = Point.objects.filter(vehicle__id=vehicle_id) \
                .filter(time__lte=r.end)[0]

            setattr(r, 'start_address', get_location(start_of_route).__str__())
            setattr(r, 'end_address', get_location(end_of_route).__str__())

        return render(request,
                      template_name='vehicle/vehicle.html',
                      context={
                          'routes': routes,
                          'vehicle_id': vehicle_id,
                          'start_datetime': start_datetime,
                          'end_datetime': end_datetime
                      })
