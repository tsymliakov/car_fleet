from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

from brand.models import get_brand

from faker import Faker


class Vehicle(models.Model):
    rental_per_hour = models.FloatField()
    total_cost = models.IntegerField()
    mileage = models.IntegerField()
    production_year = models.IntegerField(
        validators=(
            MinValueValidator(1960),
            MaxValueValidator(date.today().year)
            )
        )
    # NOTE: у одного бренда много машин, один ко многим
    brand = models.ForeignKey(to='brand.Brand', on_delete=models.PROTECT)
    # NOTE: у одной компании много машин, один ко многим
    enterprise = models.ForeignKey(to='enterprise.Enterprise', on_delete=models.SET_NULL,
                                   null=True, related_name='vehicle')
    # driver
    # active_driver
    def __str__(self):
        return f'{self.id}, {self.brand.name}'


def get_vehicle():
    fake = Faker()
    rental_per_hour = fake.random_int(min=5, max=50)
    total_cost = fake.random_int(min=5000, max=10000) * fake.random_int(min=5, max=10)
    mileage = fake.random_int(min=5000, max=160000)
    production_year = fake.random_int(min=1960, max=date.today().year)
    brand = get_brand()
    brand.save()

    return Vehicle(rental_per_hour=rental_per_hour,
                   total_cost=total_cost,
                   mileage=mileage,
                   brand=brand,
                   production_year=production_year)
