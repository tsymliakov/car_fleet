from django.db import models
from enterprise.models import Enterprise
from django.contrib.auth.models import User


class Manager(User):
    enterprise = models.ManyToManyField(Enterprise, related_name='manager', blank=True)
