from django.contrib import admin
from django.urls import path

from API import views

urlpatterns = [
    path('competitors', views.v_get_competitors),
    path('competitors/<str:handle>', views.v_get_competitor),
    path('ratings', views.v_get_ratings),
    path('ratings/<str:handle>', views.v_get_competitor_ratings),
]
