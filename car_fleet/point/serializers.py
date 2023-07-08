import pytz
from rest_framework import serializers
from .models import Point


class PointSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        self.fields['time'] = serializers.DateTimeField(default_timezone=
                                                        pytz.timezone(instance.vehicle.enterprise.timezone))
        return super().to_representation(instance)

    class Meta:
        model = Point
        fields = ('id', 'point', 'time')
