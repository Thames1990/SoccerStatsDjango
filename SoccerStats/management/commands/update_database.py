from django.core.management.base import BaseCommand

from SoccerStats.utils import update_database


class Command(BaseCommand):
    help = 'Updates whole database'

    def handle(self, *args, **options):
        update_database()
