from django.db import models
from enterprise.models import Enterprise
#from vehicle.models import Vehicle
from datetime import date

from faker import Faker


class Driver(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    salary = models.IntegerField()
    hire_date = models.DateField(default=date.today)

    vehicle = models.ManyToManyField(to='vehicle.Vehicle', blank=True)
    active_vehicle = models.OneToOneField(to='vehicle.Vehicle', blank=True, null=True, on_delete=models.SET_NULL, related_name='active_driver')

    enterprise = models.ForeignKey(to='enterprise.Enterprise', on_delete=models.SET_NULL, blank=True, null=True, related_name='drivers')

    def __str__(self):
        return f'{self.id}, {self.first_name} {self.last_name}'


def get_driver():
    fake = Faker()
    first_name = fake.first_name()
    last_name = fake.last_name()
    salary = fake.random_int(min=1000, max=3000)
    hire_date = fake.date()

    return Driver(first_name=first_name, last_name=last_name, salary=salary, hire_date=hire_date)
