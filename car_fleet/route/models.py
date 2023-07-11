from django.db import models
from datetime import datetime, timedelta


class Route(models.Model):
    vehicle = models.OneToOneField(to='vehicle.Vehicle',
                                   on_delete=models.CASCADE,
                                   related_name='route')

    start = models.DateTimeField(default=datetime.now() - timedelta(hours=5))
    end = models.DateTimeField(default=datetime.now())
