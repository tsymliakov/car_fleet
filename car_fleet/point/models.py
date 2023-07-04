from django.contrib.gis.db import models


class Point(models.Model):
    point = models.PointField(dim=2, srid=4326)
    vehicle = models.ManyToManyField('vehicle.Vehicle', related_name='point')
