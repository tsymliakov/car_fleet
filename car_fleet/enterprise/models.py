from django.db import models
from faker import Faker


class Enterprise(models.Model):
    name = models.TextField()
    location = models.TextField()

    def __str__(self):
        return f'id: {self.id}, {self.name}, {self.location}'


def get_enterprise():
    fake = Faker()
    name  = fake.company()
    location = fake.city()
    return Enterprise(name=name, location=location)
