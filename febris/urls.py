from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path(
        #URL to retrieve all country key IDs / location names
        'api/v1/country_key_ids/',
        views.get_country_key_ids,
        name='get_country_key_ids'
    ),
        path(
        #URL to retrieve all country level data (but not covid-level data)
        'api/v1/all_country_level_data/',
        views.get_all_country_level_data,
        name='get_all_country_level_data'
    ),
    path(
        #URL to retrieve all data on a specific country
        'api/v1/countries/<slug:country_key_id>/',
        views.get_all_data_specific_country,
        name='get_all_data_specific_country'
    ),
    path(
        #URL to retrieve last date data on all countries
        'api/v1/latest_data_all_countries/',
        views.get_latest_data_all_countries,
        name='get_latest_data_all_countries'
    ),
    path(
        #URL to retrieve last 30 days' data on all countries
        'api/v1/last_30_days_all_countries/',
        views.get_last_30_days_all_countries,
        name='get_last_30_days_all_countries'
    ),
    path(
        #URL to retrieve all data on all countries
        'api/v1/all_data_all_countries/',
        views.get_all_data_all_countries,
        name='get_all_data_all_countries'
    )
]
