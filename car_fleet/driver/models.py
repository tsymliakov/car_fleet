from django.db import models
from enterprise.models import Enterprise
from vehicle.models import Vehicle
from datetime import date


class Driver(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    salary = models.IntegerChoices()
    hire_date = models.DateField(default=date.today)
    is_active = models.BooleanField(default=False)

    company = models.ForeignKey(Enterprise, on_delete=models.SET_NULL)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL)
