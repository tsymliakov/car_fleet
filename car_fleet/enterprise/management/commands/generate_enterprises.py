from django.core.management.base import BaseCommand
from enterprise.models import Enterprise, get_enterprise
from vehicle.models import get_vehicle
from driver.models import get_driver
from random import randint, choice
import debugpy


def fill_enterprise(enterprise : Enterprise):
    pass


class Command(BaseCommand):
    help = "Generates enterprises and data for them."

    def add_arguments(self, parser):
        parser.add_argument('enterprises_id', type=int, nargs='+',
                            help='ID of enterprises for which data will be generated. If there is \
                                no such ID it will be created and filled with data.')
        parser.add_argument('--count-vehicle', type=int,
                            help='Count of vehicles generated for every enterprise.')
        parser.add_argument('--count-driver', type=int,
                            help='Count of drivers generated for every enterprise.')


    def handle(self, *args, **options):
        debugpy.listen(('0.0.0.0', 3000))
        debugpy.wait_for_client()
        enterprises_id = options['enterprises_id']
        count_vehicles = options['count_vehicle']
        count_drivers = options['count_driver']

        #decision = lambda: True if randint(1, 10) == 1 else False

        enterprises = [get_enterprise() for _ in range(len(enterprises_id))]

        enterprises = [Enterprise.objects.get_or_create(id) for id in enterprises_id]
        # for ent in enterprises:
        #     drivers = [get_driver() for _ in range(count_drivers)]
        #     vehicles = [get_vehicle() for _ in range(count_vehicles)]

        #     for driver in drivers:
        #         driver.vehicle.set(vehicles)
        #         if decision():
        #             try:
        #                 driver.active_vehicle = choice(vehicles)
        #             except Exception:
        #                 pass

        #     ent.driver.set(drivers)
        #     ent.vehicle.set(vehicles)

        # Enterprise.objects.bulk_create(enterprises)
