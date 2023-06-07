from django.core.management.base import BaseCommand
from enterprise.models import Enterprise, generate_data_for_enterprise
from faker import Faker


def fill_enterprise(enterprise : Enterprise):
    pass


class Command(BaseCommand):
    help = "Generates enterprises and data form them."

    # def add_arguments(self, parser):
    #     parser.add_argument('enterprises_id', type=int, nargs='+',
    #                         help='ID of enterprises for which data will be generated. If there is \
    #                             no such ID it will be created and filled with data.')
    #     parser.add_argument('-c', '--count-vehicle', type=int,
    #                         help='Count of vehicles generated for every enterprise.')


    # def handle(self, *args, **options):
    #     enterprises_id = options['enterprises_id']
    #     count = options['count-vehicle']

    #     companies = [Enterprise.objects.get_or_create(id) for id in enterprises_id]

    def handle(self, *args, **options):
        print(generate_data_for_enterprise())
