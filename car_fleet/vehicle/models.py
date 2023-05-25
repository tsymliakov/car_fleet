from django.db import models

# Create your models here.
class Vehicle(models.Model):
    rental_per_hour = models.FloatField()
    total_cost = models.IntegerField()
    mileage = models.IntegerField()
    production_year = models.DateField()
