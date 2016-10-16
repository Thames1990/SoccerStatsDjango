from django.core.management.base import BaseCommand

from competition.models import CompetitionId
from table.util import get_table


# TODO Figure out how to determine matchday
class Command(BaseCommand):
    help = 'Fetches all cup and league tables'

    def add_arguments(self, parser):
        parser.add_argument('competiton_id', nargs='+', type=CompetitionId)
        parser.add_argument('matchday', nargs='+', type=int)

    def handle(self, *args, **options):
        for competition_id in options['competiton_id']:
            get_table(competition_id, options['matchday'])
