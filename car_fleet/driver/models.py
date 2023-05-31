from django.db import models
from enterprise.models import Enterprise
from vehicle.models import Vehicle
from datetime import date


class Driver(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    salary = models.IntegerField()
    hire_date = models.DateField(default=date.today)

    # NOTE: дополнительная связь- какой автомобиль является активным. Связь один
    # к одному. Может быть null
    active_vehicle = models.OneToOneField(Vehicle, blank=True, null=True, on_delete=models.SET_NULL, related_name='active_driver')

    # NOTE: у одной компании много водителей, один ко многим
    enterprise = models.ForeignKey(Enterprise, on_delete=models.SET_NULL, blank=True, null=True)

    # NOTE: у одной машины много водителей, у одного водителя много машин, многие ко многим
    vehicle = models.ManyToManyField(Vehicle)

    def __str__(self):
        return f'{self.id}, {self.first_name} {self.last_name}'
