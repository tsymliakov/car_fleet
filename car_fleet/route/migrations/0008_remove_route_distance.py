# Generated by Django 4.2.1 on 2023-08-05 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('route', '0007_alter_route_vehicle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='distance',
        ),
    ]
