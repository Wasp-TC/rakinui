from django.shortcuts import render
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import countries
from .models import covid_data_points
from .serializers import *

# initialize the APIClient app
client = Client()

#View to retrieve all country key ids / location names on all countries
@api_view(['GET'])
def get_country_key_ids(request):
    if request.method == 'GET':
        countriesData = countries.objects.all()
        serializer = GetAllCountryKeyIDsSerializer(countriesData, many=True)
        return Response(serializer.data)

#View to retrieve all country-level data on all countries
@api_view(['GET'])
def get_all_country_level_data(request):
    if request.method == 'GET':
        countriesData = countries.objects.all()
        serializer = GetAllCountrylevelDataSerializer(countriesData, many=True)
        return Response(serializer.data)

#View to retrieve all data on a specific country (including covid-level data)
@api_view(['GET'])
def get_all_data_specific_country(request, country_key_id):
    try:
        location = countries.objects.get(country_key_id=country_key_id.upper())
    except location.DoesNotExist:
        return Response('status=status.HTTP_404_NOT_FOUND')
    if request.method == 'GET':
        # covid_data = covid_data_points.objects.filter(country_key_id=country_key_id.upper())
        countriesData = countries.objects.filter(country_key_id=country_key_id.upper())
        serializer = GetAllDataSpecificCountrySerializer(countriesData, many=True)
        return Response(serializer.data)

#View to retrieve data on all countries for the latest date in the model (including covid-level data)
@api_view(['GET'])
def get_latest_data_all_countries(request):
    if request.method == 'GET':
        countriesData = countries.objects.all()
        serializer = GetLatestDataAllCountriesSerializer(countriesData, many=True)
        return Response(serializer.data)

#View to retrieve data on all countries for the latest 30 days in the model (including covid-level data)
@api_view(['GET'])
def get_last_30_days_all_countries(request):
    # get covid data for the latest date on all countries
    if request.method == 'GET':
        countriesData = countries.objects.all()
        serializer = GetLast30DaysAllCountriesSerializer(countriesData, many=True)
        return Response(serializer.data)

#View to retrieve all on all countries (including covid-level data)
@api_view(['GET'])
def get_all_data_all_countries(request):
    # get all data on all countries
    if request.method == 'GET':
        countriesData = countries.objects.all()
        serializer = GetAllDataAllCountriesSerializer(countriesData, many=True)
        return Response(serializer.data)
