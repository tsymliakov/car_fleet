from django.db import models

# Create your models here.
class AbstractReport(models.Model):
    name = models.TextField()
    start_datetime = models.DateField()
    end_datetime = models.DateField()

    DAY = 'DAY'
    MONTH = 'MONTH'
    YEAR = 'YEAR'

    period_choices = (
        (DAY, 'day'),
        (MONTH, 'month'),
        (YEAR, 'year')
    )

    period = models.TextField(choices=period_choices)


class DateValue(models.Model):
    date_time = models.DateTimeField()
    value = models.IntegerField()

    report = models.ForeignKey(to='report.VehicleMileageReport', on_delete=models.CASCADE)


class VehicleMileageReport(AbstractReport):
    type = models.TextField(default="Пробег автомобиля за период", editable=False)
