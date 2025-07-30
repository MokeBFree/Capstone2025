import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

class API_call:
  def __init__(self):

# Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
    self.url = "https://api.open-meteo.com/v1/forecast"

  def get_weather(self, lat, lon) -> dict:

    params = {
	    "latitude": lat,
	    "longitude": lon,
	    "current": ["temperature_2m", "is_day", "precipitation", "relative_humidity_2m", "rain"],     # the order of "current" matters - these must match exact variable names from OpenMeteo
	    "timezone": "America/Denver",
	    "past_days": 7,
	    "wind_speed_unit": "mph",
	    "temperature_unit": "fahrenheit",
	    "precipitation_unit": "inch",
    }
    responses = self.openmeteo.weather_api(self.url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

# # debugging print statements
# print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
# print(f"Elevation: {response.Elevation()} m asl")
# print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
# print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# current.Variables(index) corresponds to params "current" request. Must be in order.
    current = response.Current()
    temp = current.Variables(0).Value()
    is_day = current.Variables(1).Value()
    precipitation = current.Variables(2).Value()
    relative_humidity = current.Variables(3).Value()
    rain = current.Variables(4).Value()

    return {
            "temperature" : temp,
            "is_day" : is_day,
            "precipitation" : precipitation,
            "relative_humidity" : relative_humidity,
            "rain" : rain,
            "timestamp" : current.Time()

    }

# # debugging print statements

# weather = get_weather(39.7392, -104.9903)   - calls get_weather with coords
# print(f"current temp: {weather['temperature']}")  - returns dictionary value "temperature" for coords