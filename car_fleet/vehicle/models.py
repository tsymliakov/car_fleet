from django.db import models


class Brand(models.Model):
    name = models.TextField()
    class BodyType(models.TextChoices):
        CARGO = "CARG", "Cargo"
        BUS = "BUS", "Bus"
        PICKUP = "PICK", "Pickup"
        SEDAN = "SEDA", "Sedan"
        CABRIOLET = "CABR", "Cabriolet"

    body_type = models.CharField(
        max_length=4,
        choices=BodyType.choices,
        default=BodyType.SEDAN
    )
    tank_capacity = models.IntegerField()
    passanger_seat_count = models.IntegerField()

    def __str__(self):
        return f'{self.name}'


class Vehicle(models.Model):
    rental_per_hour = models.FloatField()
    total_cost = models.IntegerField()
    mileage = models.IntegerField()
    production_year = models.DateField()

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
