from django.core.management.base import BaseCommand, CommandError
from API.celery_tasks import create_competitors
from datetime import datetime

class Command(BaseCommand):
    help = 'Creates competitors to serve data'

    def handle(self, *args, **options):
        try:
            create_competitors()
        except Exception as e:
            with open('errors_log', 'a') as f:
                f.write('at: ' + str(datetime.utcnow()) + e + '\n')