from django.core.management.base import BaseCommand
from vehicle.models import get_vehicle


class Command(BaseCommand):
    def handle(self, *args, **options):
        print(get_vehicle())
