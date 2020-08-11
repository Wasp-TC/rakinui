import json
import requests
from glob import glob
import os.path
from BacchusDatabase import BacchusDatabase

# Day-by-day covid dataset object to be iterated through when seeding the DB:
class CovidDataPoints():
    def __init__(self, country_key_id, **kwargs):
        self.country_key_id = country_key_id
        for k, v in kwargs.items():
            setattr(self, k, v)

# Country object to be iterated through when seeding the countries DB:
class Country():
    def __init__(self, country_key_id, **kwargs):
        self.country_key_id = country_key_id
        for k, v in kwargs.items():
            #Removing 'data' from the countries object (as 'data' is dealt with separately as a CovidDataPoints object)
            if k != 'data':
                setattr(self, k, v)

# The master class for iterating through the JSON object, pulling out data keys, creating country / covid data objects etc.
class Bacchus():
    data = []
    country_keys = []
    element_keys = []
    covid_data_keys = []
    countries = []
    covid_data_points = []

    def __init__(self):
        pass

    def retrieve_JSON_file(self):
        r = requests.get(url)
        with open('covid_data_source.json','w') as fd:
            fd.write(r.text)

    def read_JSON_file(self):
        #Reading JSON File
        with open('covid_data_source.json') as f:
            self.data.append(json.load(f))

        #Reading country keys and appening to a list of country keys
        for i in self.data[0].keys():
            self.country_keys.append(i)

        # Reading element codes and appening to a list of element keys
        # (the extra for loop / if statement is to cater for the issue that not all countries have the same elements
        # - so the element_keys list iterates through and grabs any unique element it comes across)
        for i in range(0, len(self.country_keys)):
            for line in self.data[0][self.country_keys[i]].keys():
                to_append = True
                if len(self.element_keys) > 0:
                    for element in self.element_keys:
                        if element == line:
                            to_append = False

                #Removing 'data' from the element_keys list so that it isn't iterated through when seeding the DB (as 'data' has its own elements
                # which are dealt with separately below)
                if line == 'data':
                    to_append = False

                if to_append == True:
                    self.element_keys.append(line)

        # Reading covid data codes (i.e. 'data' in the element_keys list) and appening to a list of covid data element keys
        # (as above, the extra for loop / if statement is to cater for the issue that not all covid datasets have the same elements
        # - so the covid_data_keys list iterates through and grabs any unique element it comes across)
        for i in range(0, len(self.country_keys)):
            for x in range(0, len(self.data[0][self.country_keys[i]]['data'])):
                for line in self.data[0][self.country_keys[i]]['data'][x]:
                    to_append = True
                    if len(self.covid_data_keys) > 0:
                        for element in self.covid_data_keys:
                            if element == line:
                                to_append = False
                    if to_append == True:
                        self.covid_data_keys.append(line)

        # Iterating through the country sets and turning the data into Country objects
        for i in range(0, len(self.country_keys)):
            country = Country(self.country_keys[i], **self.data[0][self.country_keys[i]])
            self.countries.append(country)

        # Iterating through the 'data' sets and turning the data into CovidDataPoints objects
        for i in range(0, len(self.country_keys)):
            for x in range(0, len(self.data[0][self.country_keys[i]]['data'])):
                covid_data_point = CovidDataPoints(self.country_keys[i], **self.data[0][self.country_keys[i]]['data'][x])
                self.covid_data_points.append(covid_data_point)

    def output(self):
        pass
        # print(self.country_keys)
        # print(self.element_keys)
        # print(self.covid_data_keys)

# RUN SCRIPTS:
url = "https://covid.ourworldindata.org/data/owid-covid-data.json"
db_creation_sequence_completed = False
# set the boolean below to True if yu don't want to retrieve an new dataset from the net
testing = False

if __name__ == "__main__":
    print("BACCHUS INITIATED")

    # OS LINES
    if (os.path.exists('.\covid_data_source.json') and not testing):
        #Checking if backup file already exists - if so deleting it
        if os.path.exists('.\covid_data_source_BACKUP.json'):
            os.remove('.\covid_data_source_BACKUP.json')
        #Renaming the existing (non-backup) JSON file to a backup
        os.rename('.\covid_data_source.json','.\covid_data_source_BACKUP.json')
    # Checking if the DB alredy exists (if so the update sequence will run - rather than the create new tables / seed DB sequences)
    # if (os.path.exists('.\Bacchus_Database.db')):
    #     db_creation_sequence_completed = True

    # PYTHON LINES
    bacchus = Bacchus()
    if (not testing):
        bacchus.retrieve_JSON_file()
    bacchus.read_JSON_file()
    bacchus.output()

    #SQLITE LINES
    bacchusDatabase = BacchusDatabase('.\db.sqlite3', bacchus.countries, bacchus.covid_data_points, bacchus.country_keys, bacchus.element_keys, bacchus.covid_data_keys)
    bacchusDatabase.create_connection()
    if (db_creation_sequence_completed):
        print("db_creation_sequence_completed = True --> proceeding with update() sequence")
        bacchusDatabase.update_DB()
    else:
        print("db_creation_sequence_completed = False --> proceeding with create_tables() and seed_DB() sequences")
        bacchusDatabase.create_tables()
        bacchusDatabase.seed_DB()
    bacchusDatabase.close_connection()
    print("BACCHUS COMPLETE")
