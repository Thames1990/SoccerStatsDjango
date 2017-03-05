from django.core.management.base import BaseCommand

from SoccerStats.utils import create_database


class Command(BaseCommand):
    help = 'Creates whole database'

    def handle(self, *args, **options):
        create_database()
