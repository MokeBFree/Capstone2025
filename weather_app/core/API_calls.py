import openmeteo_requests
import requests
import os
from typing import Optional, Dict
import pandas as pd
import requests_cache
from retry_requests import retry

class meteo_call:
  def __init__(self):

# Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    self.openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
    self.url = "https://api.open-meteo.com/v1/forecast"

  def get_weather(self, lat, lon) -> dict:

    params = {
	    "latitude": lat,
	    "longitude": lon,
	    "current": ["temperature_2m", "is_day", "precipitation", "relative_humidity_2m", "rain"],     # the order of "current" matters - these must match exact variable names from OpenMeteo
	    "timezone": "America/Denver",
	    "past_days": past_days,
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

# api = meteo_call()
# weather = get_weather(39.7392, -104.9903)   - calls get_weather with coords
# print(f"current temp: {weather['temperature']}")  - returns dictionary value "temperature" for coords

#Makes separate API call to Open Weather to use their geocoding 
  def get_coordinates_for_city(self, city: str) -> Optional[Dict[str, float]]:
      """Convert city name to coordinates using OpenWeatherMap Geocoding API"""
      geocode_url = "http://api.openweathermap.org/geo/1.0/direct"
      params = {
          "q": city,
          "limit": 1,
          "appid": os.getenv("OPENWEATHER_API_KEY")  # Make sure your API key is stored as an environment variable
      }

      try:
          response = requests.get(geocode_url, params=params, timeout=5)
          response.raise_for_status()  # Raises exception if status != 200
          data = response.json()

          if data:
            return {"lat": data[0]["lat"], "lon": data[0]["lon"]}
          else:
              print(f"No data returned for city: {city}")
              return None
      except requests.RequestException as e:
          print(f"Error fetching coordinates: {e}")
          return None