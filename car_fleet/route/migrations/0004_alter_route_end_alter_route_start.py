# Generated by Django 4.2.1 on 2023-07-26 08:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('route', '0003_alter_route_end_alter_route_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 26, 8, 29, 13, 372131)),
        ),
        migrations.AlterField(
            model_name='route',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 26, 3, 29, 13, 372109)),
        ),
    ]
