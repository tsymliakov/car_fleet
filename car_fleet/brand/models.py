from django.db import models
from faker import Faker


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
        return f'{self.id}, {self.name}'


def get_brand():
    fake = Faker()
    name = fake.text().split()[-2].capitalize()
    body_type = "SEDA"
    tank_capacity = fake.random_int(min=70, max=100)
    passanger_seat_count = fake.random_int(min=1, max=6)

    return Brand(name=name,
                 body_type=body_type,
                 tank_capacity=tank_capacity,
                 passanger_seat_count=passanger_seat_count)
