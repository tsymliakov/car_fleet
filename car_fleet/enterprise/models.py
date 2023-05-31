from django.db import models


class Enterprise(models.Model):
    name = models.TextField()
    location = models.TextField()

    def __str__(self):
        return f'id: {self.id}, {self.name}'