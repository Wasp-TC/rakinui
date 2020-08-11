from django.contrib import admin

# from .models import countries, CovidData
from .models import countries
from .models import covid_data_points
# from .models import CovidData
# from .models import Tracker
# Register your models here.

# admin.site.register(Tracker)
# admin.site.register(CovidData)
admin.site.register(countries)
admin.site.register(covid_data_points)
