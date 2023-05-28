from rest_framework import serializers
from .models import Vehicle, Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Vehicle
        fields = ('id', 'rental_per_hour', 'total_cost', 'mileage', 'production_year', 'brand')