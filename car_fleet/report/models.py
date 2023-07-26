from django.db import models

# Create your models here.
class Report(models.Model):
    name = models.TextField()
    start_datetime = models.DateField()
    end_datetime = models.DateField()
    type = models.TextField(editable=False)

    DAY = 'Дневная'
    MONTH = 'Месячная'
    YEAR = 'Годовая'

    period_choices = (
        (DAY, 'Дневная'),
        (MONTH, 'Месячная'),
        (YEAR, 'Годовая')
    )

    period = models.TextField(choices=period_choices)


class VehicleMileageReport(Report):
    vehicle = models.ForeignKey(to='vehicle.Vehicle', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.type:
            self.type = "Пробег автомобиля за период"

        super().save(*args, **kwargs)


class MileageValue(models.Model):
    date_time = models.DateTimeField()
    mileage = models.IntegerField()

    report = models.ForeignKey(to='report.VehicleMileageReport',
                               on_delete=models.CASCADE,
                               related_name='date_value')
