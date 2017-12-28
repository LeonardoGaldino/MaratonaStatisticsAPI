from celery.task.schedules import crontab
from celery.decorators import periodic_task
from django.core.exceptions import ObjectDoesNotExist

from MaratonaStatistics.celery import celery_app
from MaratonaStatistics import settings
from MaratonaStatistics import Competitors
from API.models import Competitor, Rating

from datetime import datetime
import requests
import json

def create_competitors():
	chain = t_erase_ratings.s() | t_erase_competitors.s() | t_create_competitors.s()
	chain()

@celery_app.task
def t_create_competitors(name='API.celery_tasks.t_create_competitors'):
	competitors = Competitors.competitors
	bulk_insert_list = [Competitor(handle=comp['handle'], name=comp['name']) for comp in competitors]
	Competitor.objects.bulk_create(bulk_insert_list)

@celery_app.task
def t_erase_ratings(name='API.celery_tasks.t_erase_ratings'):
	Rating.objects.all().delete()

@celery_app.task
def t_erase_competitors(name='API.celery_tasks.t_erase_competitors'):
	Competitor.objects.all().delete()

@periodic_task(
    run_every=(crontab('*', '*', '*', '*', '*')),
    name="API.celery_tasks.fetch_competitors_data",
    ignore_result=True
)
def fetch_competitors_data():
    with open('cronjob_log', 'a') as f:
        f.write('executing at ' + str(datetime.now()) + '\n')
    api_url = settings.CF_API_URL
    api_method = 'user.rating'
    competitors = Competitor.objects.all()
    for comp in competitors:
        params = {
            'handle': comp.handle
        }
        req = requests.get(api_url+api_method, params=params)
        data = json.loads(req.content.decode('utf-8'))
        for entry in data['result']:
            date = entry['ratingUpdateTimeSeconds']
            rating = entry['newRating']
            try:
                Rating.objects.get(date=date, competitor=comp)
            except ObjectDoesNotExist:
                Rating.objects.create(rating=rating, date=date, competitor=comp)