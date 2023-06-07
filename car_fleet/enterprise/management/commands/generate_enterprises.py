from django.core.management.base import BaseCommand
from enterprise.models import Enterprise
from vehicle.models import Vehicle, get_vehicle
from driver.models import Driver, get_driver
from random import randint
from faker import Faker


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
        enterprises_id = options['enterprises_id']
        count_vehicles = options['count_vehicle']
        count_drivers = options['count_driver']

        decision = lambda: True if randint(1, 10) == 1 else False

        fake = Faker()

        enterprises = []
        for id in enterprises_id:
            try:
                enterprises.append(Enterprise.objects.get_or_create(id=id,
                                                        name=fake.company(),
                                                        location=fake.city()
                                                        )[0])
            except:
                enterprises.append(Enterprise.objects.get(id=id))

        for ent in enterprises:
            drivers = [get_driver() for _ in range(count_drivers)]
            vehicles = [get_vehicle() for _ in range(count_vehicles)]

            Driver.objects.bulk_create(drivers)
            Vehicle.objects.bulk_create(vehicles)

            for driver in drivers:
                ent.driver.add(driver)
                driver.vehicle.set(vehicles)

            free_drivers = drivers[:]

            for vehicle in vehicles:
                ent.vehicle.add(vehicle)

            ent.save()

            for vehicle in vehicles:
                if decision():
                    vehicle.active_driver=free_drivers.pop()
                    vehicle.active_driver.save()
