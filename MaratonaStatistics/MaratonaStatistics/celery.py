from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
import requests
import json

from datetime import datetime

logger = get_task_logger(__name__)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MaratonaStatistics.settings')
app = Celery('MaratonaStatistics')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@periodic_task(
    run_every=(crontab('*', '*', '*', '*', '*')),
    name="fetch_competitors_data",
    ignore_result=True
)
def fetch_competitors_data():
    with open('cronjob_log', 'a') as f:
        f.write('executing at ' + str(datetime.now()) + '\n')
    from API.models import Competitor, Rating
    Competitor.objects.all().delete()
    Rating.objects.all().delete()
    competitors = [{'handle': 'leogaldino',
                    'name': 'Leogal'}, {
                    'handle': 'carnero',
                    'name': 'Diguinho'},
                    {'handle': 'GabrielPessoa',
                    'name': 'GabrielPessoa'}
                  ]
    api_url = settings.CF_API_URL
    api_method = 'user.rating'
    for comp in competitors:
        try:
            Competitor.objects.create(handle=comp['handle'], name=comp['name'])
        except Exception as e:
            with open('errors_log', 'a') as error_logfile:
                error_logfile.write(str(e) + '\n')
        params = {
            'handle': comp['handle']
        }
        req = requests.get(api_url+api_method, params=params)
        data = json.loads(req.content.decode('utf-8'))
        for entry in data['result']:
            date = entry['ratingUpdateTimeSeconds']
            rating = entry['newRating']
            try:
                competitor = Competitor.objects.get(handle=comp['handle'])
                Rating.objects.create(rating=rating, date=date, competitor=competitor)
            except Exception as e:
                with open('errors_log', 'a') as error_logfile:
                    error_logfile.write(str(e) + '\n')