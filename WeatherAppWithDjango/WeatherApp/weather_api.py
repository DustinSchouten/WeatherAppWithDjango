import os
import requests
from babel import Locale
import datetime
from .models import CityTemperatures
from decouple import config


class WeatherDataHandler():
    API_KEY = config("API_KEY")
    API_BASE_URL = config("API_BASE_URL")

    def __init__(self, city):
        self.city = city
        self.URL = f"{WeatherDataHandler.API_BASE_URL}?q={city}&appid={WeatherDataHandler.API_KEY}&units=metric&lang=nl";
        print(self.URL)

    def fetch_data(self):
        try:
            self.response = requests.get(self.URL)
        except:
            self.response = None

    def get_status_code(self):
        return self.response.status_code

    def parse_data(self):
        response_data = self.response.json()
        # Collect all data to store into the database
        city_name = response_data['name']
        country_code = response_data['sys'].get('country', None)
        country_name = None
        if country_code is not None:
            country_name = Locale('nl').territories[country_code.upper()]
            country_code = country_code.lower()
        temperature = round(response_data['main']['temp'])
        api_weather_timestamp = response_data['dt']

        api_weather_datetime = datetime.datetime.fromtimestamp(api_weather_timestamp)
        datetime_created = datetime.datetime.now()
        return {'city_name':city_name,
                'country_code':country_code,
                'country_name':country_name,
                'temperature':temperature,
                'api_weather_datetime':api_weather_datetime,
                'datetime_created':datetime_created,
                }

    def write_to_db(self, data_object):
        data_record = CityTemperatures(**data_object)
        data_record.save()