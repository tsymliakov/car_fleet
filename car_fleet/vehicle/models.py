from django.db import models
from brand.models import Brand
from enterprise.models import Enterprise


class Vehicle(models.Model):
    rental_per_hour = models.FloatField()
    total_cost = models.IntegerField()
    mileage = models.IntegerField()
    production_year = models.DateField()

    # NOTE: у одного бренда много машин, один ко многим
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    # NOTE: у одной компании много машин, один ко многим
    enterprise = models.ForeignKey(Enterprise, on_delete=models.SET_NULL, null=True, related_name='vehicles')

    def __str__(self):
        return f'{self.id}, {self.brand.name}'
