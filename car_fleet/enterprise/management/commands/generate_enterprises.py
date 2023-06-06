from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generates enterprises and data form them."

    def add_arguments(self, parser):
        parser.add_argument('enterprises_id', type=int, nargs='+',
                            help='ID of enterprises for which data will be generated. If there is \
                                no such ID it will be created and filled with data.')
        parser.add_argument('-c', '--count-vehicle', type=int,
                            help='Count of vehicles generated for every enterprise.')

    def handle(self, *args, **options):
        enterprises_id = options['enterprises_id']
        count = options['count-vehicle']

    '''
    В цикле по айдишникам вызываем get_or_create Enterprise.objects.get_or_create(id=id)
    '''
