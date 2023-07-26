from django.db import models
from datetime import datetime, timedelta


class Route(models.Model):
    vehicle = models.OneToOneField(to='vehicle.Vehicle',
                                   on_delete=models.CASCADE,
                                   related_name='route')

    start = models.DateTimeField(default=datetime(2023, 7, 26, 8, 36, 48, 734998))
    end = models.DateTimeField(default=datetime(2023, 7, 26, 3, 36, 48, 734998))
