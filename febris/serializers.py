from rest_framework import serializers
import datetime
from datetime import timedelta
from .models import countries
from .models import covid_data_points
# from .models import Tracker
# from .models import CovidData

#Serializer 1: Used for the get_all_country_level_data() view
class GetAllCountryKeyIDsSerializer(serializers.ModelSerializer):
    class Meta:
        model = countries
        fields = ('country_key_id', 'location')

#Serializer 2: Used for the get_all_country_level_data() view
class GetAllCountrylevelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = countries
        fields = '__all__'

#Serializer 3: Used for the get_all_data_specific_country() view
class NestedGetAllDataSpecificCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = covid_data_points
        fields = '__all__'
class GetAllDataSpecificCountrySerializer(serializers.ModelSerializer):
    data = NestedGetAllDataSpecificCountrySerializer(read_only=True, many=True)
    class Meta:
        model = countries
        fields = '__all__'

#Serializer 4: Used for the get_latest_data_all_countries() view
class FilterListForNestedGetLatestDataAllCountriesSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        max_date = data.latest('date').date
        data = data.filter(date=max_date)
        return super(FilterListForNestedGetLatestDataAllCountriesSerializer, self).to_representation(data)
class NestedGetLatestDataAllCountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = covid_data_points
        fields = '__all__'
        list_serializer_class = FilterListForNestedGetLatestDataAllCountriesSerializer
class GetLatestDataAllCountriesSerializer(serializers.ModelSerializer):
    data = NestedGetLatestDataAllCountriesSerializer(read_only=True, many=True)
    class Meta:
        model = countries
        fields = '__all__'

#Serializer 5: Used for the get_last_30_days_all_countries() view
class BaseDateFinder():
    def base_date_finder(max_date):
        max_date_in_dt_format = datetime.datetime.fromisoformat(max_date)
        base_date= max_date_in_dt_format - timedelta(days=30)
        return base_date
class FilterListForNestedGetLast30DaysAllCountriesSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        max_date = data.latest('date').date
        base_date = BaseDateFinder.base_date_finder(max_date)
        data = data.filter(date__range=[base_date, max_date])
        return super(FilterListForNestedGetLast30DaysAllCountriesSerializer, self).to_representation(data)
class NestedGetLast30DaysAllCountriesSerializer(serializers.ModelSerializer):
    # data = countryLevelDataSerializer(read_only=True, many=True)
    class Meta:
        model = covid_data_points
        fields = '__all__'
        list_serializer_class = FilterListForNestedGetLast30DaysAllCountriesSerializer
class GetLast30DaysAllCountriesSerializer(serializers.ModelSerializer):
    data = NestedGetLast30DaysAllCountriesSerializer(read_only=True, many=True)
    class Meta:
        model = countries
        fields = '__all__'

#Serializer 6: Used for the get_all_data_all_countries() view
class NestedGetAllDataAllCountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = covid_data_points
        fields = '__all__'
class GetAllDataAllCountriesSerializer(serializers.ModelSerializer):
    data = NestedGetAllDataAllCountriesSerializer(read_only=True, many=True)
    class Meta:
        model = countries
        fields = '__all__'
