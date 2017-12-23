from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from API.models import Competitor, Rating

import json

# Create your views here.

def v_get_competitors(request):
    competitors = Competitor.objects.all()
    ret = []
    for competitor in competitors:
        ret.append({
            'name': competitor.name,
            'handle': competitor.handle,
            'rating': competitor.get_current_rating().rating
        })
    return JsonResponse({'error': False, 'content': ret})

def v_get_competitor(request, **kwargs):
    handle = kwargs['handle']
    try:
        comp = Competitor.objects.get(handle=handle)
    except ObjectDoesNotExist:
        return JsonResponse({'error': True, 
                            'errorMessage': 'Competitor ' + handle + ' does not exists.'})
    return JsonResponse({'error': False, 'content': {
        'name': comp.name,
        'handle': comp.handle,
        'rating': comp.get_current_rating().rating
    }})

def v_get_ratings(request):
    ratings = Rating.objects.all()
    temp = [{'rating': rating.rating, 
            'date': rating.date, 
            'competitor': rating.competitor.handle}
            for rating in ratings]
    return JsonResponse({'error': False, 'content': temp})

def v_get_competitor_ratings(request, **kwargs):
    handle = kwargs['handle']
    try:
        comp = Competitor.objects.get(handle=handle)
    except ObjectDoesNotExist:
        return JsonResponse({'error': True, 
                            'errorMessage': 'Competitor ' + handle + ' does not exists.'})
    comp_ratings = list(comp.rating_set.all().values('rating', 'date'))
    return JsonResponse({'error': False, 'content': comp_ratings})