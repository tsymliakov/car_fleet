from rest_framework import serializers
from .models import Driver


class DriverFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('id', 'enterprise', 'vehicle', 'active_vehicle')
