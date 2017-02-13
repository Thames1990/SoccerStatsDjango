import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Shows specific log file dependant on DEBUG'

    def handle(self, *args, **options):
        if settings.DEBUG:
            os.system('tail -f -n +1 /var/log/SoccerStats/debug.log')
        else:
            os.system('tail -f -n +1 /var/log/SoccerStats/production.log')
