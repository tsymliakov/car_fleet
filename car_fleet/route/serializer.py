import pytz
from rest_framework import serializers
from .models import Route


class RouteSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        self.fields['start'] = serializers.DateTimeField(default_timezone=pytz.timezone(instance.vehicle.enterprise.timezone))
        self.fields['end'] = serializers.DateTimeField(default_timezone=pytz.timezone(instance.vehicle.enterprise.timezone))
        return super().to_representation(instance)

    class Meta:
        model = Route
        fields = ('vehicle', 'start', 'end', 'vehicle.point')
