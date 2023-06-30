from django.db import models
from faker import Faker


class Enterprise(models.Model):
    name = models.TextField()
    location = models.TextField()

    TIMEZONES = [
        ('Etc/GMT+12', 'GMT+12'),
        ('Etc/GMT+11', 'GMT+11'),
        ('Etc/GMT+10', 'GMT+10'),
        ('Etc/GMT+9', 'GMT+9'),
        ('Etc/GMT+8', 'GMT+8'),
        ('Etc/GMT+7', 'GMT+7'),
        ('Etc/GMT+6', 'GMT+6'),
        ('Etc/GMT+5', 'GMT+5'),
        ('Etc/GMT+4', 'GMT+4'),
        ('Etc/GMT+3', 'GMT+3'),
        ('Etc/GMT+2', 'GMT+2'),
        ('Etc/GMT+1', 'GMT+1'),
        ('Etc/GMT+0', 'GMT+0'),
        ('Etc/GMT-0', 'GMT-0'),
        ('Etc/GMT-1', 'GMT-1'),
        ('Etc/GMT-2', 'GMT-2'),
        ('Etc/GMT-3', 'GMT-3'),
        ('Etc/GMT-4', 'GMT-4'),
        ('Etc/GMT-5', 'GMT-5'),
        ('Etc/GMT-6', 'GMT-6'),
        ('Etc/GMT-7', 'GMT-7'),
        ('Etc/GMT-8', 'GMT-8'),
        ('Etc/GMT-9', 'GMT-9'),
        ('Etc/GMT-10', 'GMT-10'),
        ('Etc/GMT-11', 'GMT-11'),
        ('Etc/GMT-12', 'GMT-12'),
        ('Etc/GMT-13', 'GMT-13'),
        ('Etc/GMT-14', 'GMT-14')
    ]

    timezone = models.TextField(choices=TIMEZONES, default='GMT-0')

    def __str__(self):
        return f'id: {self.id}, {self.name}, {self.location}'


def get_enterprise():
    fake = Faker()
    name = fake.company()
    location = fake.city()
    return Enterprise(name=name, location=location)
