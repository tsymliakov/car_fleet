import pytz
from rest_framework import serializers
from .models import Route


def get_geoinfo(altitude, logitude):
    """
    Функция обращается к стороннему API, чтобы получить адрес точки.
    """


class RouteSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        timezone = pytz.timezone(instance.vehicle.enterprise.timezone)
        self.fields['start'] = serializers.DateTimeField(default_timezone=timezone)
        self.fields['end'] = serializers.DateTimeField(default_timezone=timezone)
        representation = super().to_representation(instance)

        self.fields['start_point'] = serializers.CharField()
        representation['start_point'] = 'Start'

        self.fields['end_point'] = serializers.CharField()
        representation['end_point'] = 'End'

        return representation

    class Meta:
        model = Route
        fields = ('id', 'vehicle', 'start', 'end')
