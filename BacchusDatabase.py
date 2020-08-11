import sqlite3
from sqlite3 import Error

class BacchusDatabase:
    def __init__(self, db_file, countries, covid_data_points, country_keys, element_keys, covid_data_keys, **kwargs):
        self.db_file = db_file
        self.countries = countries
        self.covid_data_points = covid_data_points
        self.country_keys = country_keys
        self.element_keys = element_keys
        self.covid_data_keys = covid_data_keys

    def create_connection(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            print("Database created and Successfully Connected to SQLite")
            print('SQLITE VERSION: ' + str(sqlite3.version))

        except Error as e:
            print(e)

    def close_connection(self):
        if (self.cursor):
            self.cursor.close()

        if (self.conn):
            self.conn.close()
            print("The SQLite connection is closed")


    def create_tables(self):
        sqlite_countries_table_command = """CREATE TABLE IF NOT EXISTS febris_countries (
                                    id INTEGER,
                                    country_key_id CharField PRIMARY KEY"""
        sqlite_covid_data_points_table_command = """CREATE TABLE IF NOT EXISTS febris_covid_data_points (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    country_key_id CharField"""

        # Looping through element_keys to establish columns for countries table
        for element in self.element_keys:
            sqlite_countries_table_command += (', \n' + element)
        sqlite_countries_table_command += ");"

        # Looping through covid_data_keys to establish columns for covid_data_points table
        for key in self.covid_data_keys:
            sqlite_covid_data_points_table_command += (', \n' + key)
        sqlite_covid_data_points_table_command += ",\nFOREIGN KEY(country_key_id) REFERENCES febris_countries(country_key_id), UNIQUE(country_key_id, date));"

        if (self.conn):
            try:
                cursor = self.conn.cursor()
                cursor.execute(sqlite_countries_table_command)
                cursor.execute(sqlite_covid_data_points_table_command)
            except Error as e:
                print(e)

    def seed_DB(self):
        # Inserting country data
        for country in self.countries:
            sqlite_command_attr_string = '('
            sqlite_command_value_string  = '('
            data_tupple = []

            for attr, value in country.__dict__.items():
                sqlite_command_attr_string += (attr + ', ')
                sqlite_command_value_string += ('?, ')
                data_tupple.append(value)

            sqlite_command_attr_string = (sqlite_command_attr_string[:-2] + ')')
            sqlite_command_value_string = (sqlite_command_value_string[:-2] + ')')
            sqlite_command = "INSERT INTO febris_countries \n" + sqlite_command_attr_string + '\n VALUES\n' + sqlite_command_value_string
            self.cursor.execute(sqlite_command, data_tupple)
            self.conn.commit()

        # Inserting covid_data_points data
        for data_point in self.covid_data_points:
            sqlite_command_attr_string = '('
            sqlite_command_value_string  = '('
            data_tupple = []

            for attr, value in data_point.__dict__.items():
                sqlite_command_attr_string += (attr + ', ')
                sqlite_command_value_string += ('?, ')
                data_tupple.append(value)

            sqlite_command_attr_string = (sqlite_command_attr_string[:-2] + ')')
            sqlite_command_value_string = (sqlite_command_value_string[:-2] + ')')
            sqlite_command = "INSERT INTO febris_covid_data_points \n" + sqlite_command_attr_string + '\n VALUES\n' + sqlite_command_value_string

            self.cursor.execute(sqlite_command, data_tupple)
            self.conn.commit()

            # sqlite_select_Query = "select sqlite_version();"
            # cursor.execute(sqlite_select_Query)
            # record = cursor.fetchall()
            # print("SQLite Database Version is: ", record)

    def update_DB(self):
        # Inserting country data
        for data_point in self.covid_data_points:
            sqlite_command_attr_string = '('
            sqlite_command_value_string  = '('
            data_tupple = []

            for attr, value in data_point.__dict__.items():
                sqlite_command_attr_string += (attr + ', ')
                sqlite_command_value_string += ('?, ')
                data_tupple.append(value)

            sqlite_command_attr_string = (sqlite_command_attr_string[:-2] + ')')
            sqlite_command_value_string = (sqlite_command_value_string[:-2] + ')')
            sqlite_command = "INSERT OR IGNORE INTO covid_data_points \n" + sqlite_command_attr_string + '\n VALUES\n' + sqlite_command_value_string

            try:
                self.cursor.execute(sqlite_command, data_tupple)
                self.conn.commit()
            except Error as e:
                print(e)
                print("DB UPDATE ERROR: An entry for " + self.covid_data_points[i-1].date + " already exists in the DB for " + self.covid_data_points[i-1].country_key)
