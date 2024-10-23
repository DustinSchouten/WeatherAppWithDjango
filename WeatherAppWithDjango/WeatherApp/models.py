from django.db import models

class CityTemperatures(models.Model):
    city_name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=5, null=True)
    country_name = models.CharField(max_length=255, null=True)
    temperature = models.IntegerField()
    api_weather_datetime = models.DateTimeField()
    datetime_created = models.DateTimeField()