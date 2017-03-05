import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Clears specific log file dependant on DEBUG'

    def handle(self, *args, **options):
        if settings.DEBUG:
            os.system('truncate -s0 /var/log/SoccerStats/debug.log')
        else:
            os.system('truncate -s0 /var/log/SoccerStats/production.log')
