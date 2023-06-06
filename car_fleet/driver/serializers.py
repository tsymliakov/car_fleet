from rest_framework import serializers
from .models import Driver
from enterprise.models import Enterprise
from vehicle.models import Vehicle


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('id', 'first_name', 'last_name', 'salary', 'hire_date', 'enterprise', 'vehicle', 'active_vehicle')
