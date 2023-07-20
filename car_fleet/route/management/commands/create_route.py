from django.core.management.base import BaseCommand
from enterprise.models import Enterprise
from vehicle.models import Vehicle, get_vehicle
from driver.models import Driver, get_driver
from random import randint
from faker import Faker


class Command(BaseCommand):
    help = "Generates route for given vehicle."

    def add_arguments(self, parser):
        parser.add_argument('--id', type=int)
        parser.add_argument('--length', type=int)
        parser.add_argument('--max-speed', type=int)
        parser.add_argument('--max-acceleration', type=int)
        parser.add_argument('--between-points', type=int)

    def handle(self, *args, **options):
        vehicle_id = options['id']
        length = options['length']
        max_speed = options['max-speed']
        max_acceleration = options['max_acceleration']
        between_points = options['between-points']

        # Суть такова. Функция в бесконечном цикле генерирурет точку и сохраняет
        # ёё в базе. Ждет 10 секунд, после чего опять генерирует точку.
        # Как учесть максимальную скорость и ускорение?


