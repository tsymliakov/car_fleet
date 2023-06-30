import pytz
from rest_framework import serializers
from brand.serializers import BrandSerializer
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    def to_representation(self, instance):
        self.fields['buy_datetime'] = serializers.DateTimeField(default_timezone=pytz.timezone(instance.enterprise.timezone))
        return super().to_representation(instance)

    class Meta:
        model = Vehicle
        fields = ('id', 'rental_per_hour', 'total_cost', 'mileage', 'production_year', 'brand',
                  'enterprise', 'active_driver', 'buy_datetime')
