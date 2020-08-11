from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Tracker
from ..serializers import TrackerSerializer


# initialize the APIClient app
client = Client()

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_country(request, pk):
    try:
        country = Tracker.objects.get(pk=pk)
    except Tracker.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single country
    if request.method == 'GET':
        return Response({})
    # delete a single country
    elif request.method == 'DELETE':
        return Response({})
    # update details of a single country
    elif request.method == 'PUT':
        return Response({})


@api_view(['GET', 'POST'])
def get_post_countries(request):
    # get all countries
    if request.method == 'GET':
        return Response({})
    # insert a new record for a country
    elif request.method == 'POST':
        return Response({})
