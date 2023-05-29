from django.db import models
from brand.models import Brand
from enterprise.models import Enterprise


class Vehicle(models.Model):
    rental_per_hour = models.FloatField()
    total_cost = models.IntegerField()
    mileage = models.IntegerField()
    production_year = models.DateField()

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    company = models.ForeignKey(Enterprise, on_delete=models.SET_NULL)
