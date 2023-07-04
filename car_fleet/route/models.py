from django.contrib.gis.db import models


class Route(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField(auto_now=True)
    duration = models.TimeField()
    vehicle = models.OneToOneField('vehicle.Vehicle', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.id} {self.name}'


class Point(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='point')
    order = models.IntegerField()
    point = models.PointField(dim=2, srid=4326)

    def __str__(self):
        return f"Точка {self.id} в {self.route.name}"
