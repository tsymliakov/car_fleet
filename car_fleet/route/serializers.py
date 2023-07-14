import pytz
from rest_framework import serializers
from .models import Route
from point.models import Point
from geopy.geocoders import Nominatim


def get_location(point):
    latitude = point.point.y
    longitude = point.point.x

    geolocator = Nominatim(user_agent="pls_dont_ban_my_home_proj")
    location = geolocator.reverse((latitude,longitude))

    if location is not None:
        return location

    return (latitude, longitude)


class RouteSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        timezone = pytz.timezone(instance.vehicle.enterprise.timezone)
        # self.fields['start'] = serializers.DateTimeField(default_timezone=timezone)
        # self.fields['end'] = serializers.DateTimeField(default_timezone=timezone)
        representation = super().to_representation(instance)

        self.fields['route_start_location'] = serializers.CharField()

        self.fields['route_end_location'] = serializers.CharField()

        start_point = Point.objects.filter(vehicle__id=representation['vehicle'])\
                                   .filter(time__gte=representation['start']).order_by('time')[0]

        end_point = Point.objects.filter(vehicle__id=representation['vehicle'])\
                                   .filter(time__lte=representation['end'])[0]

        start_location = get_location(start_point)
        end_location = get_location(end_point)

        representation['route_start_location'] = start_location.__str__()
        representation['route_end_location'] = end_location.__str__()

        return representation

    class Meta:
        model = Route
        fields = ('id', 'vehicle', 'start', 'end')
