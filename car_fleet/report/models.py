from django.db import models

# Create your models here.
class Report(models.Model):
    name = models.TextField()
    start_datetime = models.DateField()
    end_datetime = models.DateField()
    period = models.TextField(choices=('day', 'month', 'year'))
    type = models.TextField()

    class Meta:
        abstract = True

class MonthlyMileage(Report):
    type = models.TextField(default="Пробег автомобиля за период", editable=False)