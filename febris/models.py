from django.db import models

class countries(models.Model):
    country_key_id = models.CharField(max_length=100, unique=True)
    continent = models.TextField()
    location = models.TextField()
    population = models.IntegerField()
    population_density = models.IntegerField()
    median_age = models.IntegerField()
    aged_65_older = models.IntegerField()
    aged_70_older = models.IntegerField()
    gdp_per_capita = models.IntegerField()
    cardiovasc_death_rate = models.IntegerField()
    diabetes_prevalence = models.IntegerField()
    handwashing_facilities = models.IntegerField()
    hospital_beds_per_thousand = models.IntegerField()
    life_expectancy = models.IntegerField()
    extreme_poverty = models.IntegerField()
    female_smokers = models.IntegerField()
    male_smokers = models.IntegerField()

    def get_country(self):
        return self.location

    def __repr__(self):
        return self.location + ' is added.'

class covid_data_points(models.Model):
    country_key = models.ForeignKey(countries, related_name='data', on_delete=models.CASCADE, null=True, to_field = 'country_key_id')
    # country_key = models.TextField()
    date = models.CharField(max_length=8)
    total_cases = models.IntegerField()
    new_cases = models.IntegerField()
    total_deaths = models.IntegerField()
    new_deaths = models.IntegerField()
    total_cases_per_million = models.IntegerField()
    new_cases_per_million = models.IntegerField()
    total_deaths_per_million = models.IntegerField()
    new_deaths_per_million = models.IntegerField()
    stringency_index = models.IntegerField()

    def get_country(self):
        return self.country_key

    def __repr__(self):
        return self.country_key + ' is added.'

# class Tracker(models.Model):
#     country = models.CharField(max_length=100)
#     population = models.IntegerField()
#
#     def get_country(self):
#         return self.country + ' country: ' + self.country + ' population: ' + self.population
#
#     def __repr__(self):
#         return self.country + ' is added.'
#
#
# class CovidData(models.Model):
#     country = models.ForeignKey(Tracker, related_name='date', on_delete=models.CASCADE, null=True)
#     date = models.CharField(max_length=8)
#     confirmed = models.IntegerField()
#     fatalities = models.IntegerField()
#     recovered = models.IntegerField()
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def get_country(self):
#         return self.date + ' confirmed: ' + self.confirmed + ' fatalities: ' + self.fatalities + 'recovered: ' + self.recovered
#
#     def __repr__(self):
#         return self.date + ' is added.'
