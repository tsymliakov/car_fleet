from django.db import models
from faker import Faker


class Enterprise(models.Model):
    name = models.TextField()
    location = models.TextField()

    def __str__(self):
        return f'id: {self.id}, {self.name}'


def generate_data_for_enterprise():
    fake = Faker()
    name  = fake.text().split()[-2].capitalize()
    location = fake.city()
    return name, location
