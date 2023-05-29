from django.db import models


class Enterprise(models.Model):
    name = models.TextField()
    location = models.TextField()
