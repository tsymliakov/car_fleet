from rest_framework import serializers
from .models import Vehicle
from brand.serializers import BrandSerializer


class VehicleSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Vehicle
        fields = ('id', 'rental_per_hour', 'total_cost', 'mileage', 'production_year', 'brand', 'enterprise')
