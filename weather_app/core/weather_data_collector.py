import requests # To make HTTP requests to the weather API.
import time # For delays, rate limiting, and timestamps.
import json # For handling JSON responses (used implicitly).
import logging # For tracking activity, errors, and debugging info.
from datetime import datetime, timedelta #To handle timestamps.
from typing import Dict, List, Optional # Provides type hints like Dict, List, and Optional.
import os # For accessing environment variables (used in related configs).

class WeatherDataCollector:
    """
    A production-ready weather data collector with error handling,
    rate limiting, and robust data validation.

    This class encapsulates everything needed to fetch, validate, and clean 
    weather data from the OpenWeatherMap API in a resilient and reusable way.
    """
    
    def __init__(self, api_key: str, base_url: str = "http://api.openweathermap.org/data/2.5"): 
        # Store API credentials and base URL
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()  # Reuse connections & keeps connections alive
        self.last_request_time = 0
        self.min_request_interval = 60.0  # Minimum seconds between requests
                                        #max amount of requests 60/hr per API limits
        # Set up logging so that warnings and errors can be tracked
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _respect_rate_limit(self):
        """Ensure we don't exceed API rate limits.
        Checks how long it's been since the last API request.
        If not enough time has passed (based on the rate limit), it pauses the program.
        Ensures we don't accidentally get blocked for making too many requests too quickly.
        """
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        self.last_request_time = time.time()
     
    def make_api_request(self, endpoint: str, params: Dict, full_url: str=None) -> Optional[Dict]: #lines 42 - 90 Error Handling
        """
        Make a robust API request with error handling and retries.
        """
        self._respect_rate_limit() #calls rate limit function to ensure we don't exceed API limits.
        if not full_url:
        # Attaches the API key to the query parameters.
        # Constructs the full API URL.
            params['appid'] = self.api_key
            url = f"{self.base_url}/{endpoint}"
        else:
            url = full_url
        # Attempts up to 3 retries if errors occur.
        max_retries = 3
        retry_delays = [1, 2, 4]  # Exponential backoff
        

        """
        200 OK: Success
        429: Too many requests → wait 60 seconds
        401: Invalid key → abort
        Other HTTP codes: Log and retry
        RequestExceptions: Handle connectivity errors, timeouts, etc.
        """
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:  # Rate limited
                    self.logger.warning(f"Rate limited. Waiting before retry...")
                    time.sleep(60)  # Wait 1 minute
                    continue
                elif response.status_code == 401:
                    self.logger.error("Invalid API key")
                    return None
                else:
                    self.logger.warning(f"API returned status {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                
            # Wait before retry (except on last attempt)
            if attempt < max_retries - 1:
                time.sleep(retry_delays[attempt])
        
        self.logger.error(f"Failed to fetch data after {max_retries} attempts")
        # If all attempts fail, it logs a critical error and returns None.
        return None #lines 42 - 90 Error Handling
    
    
    def get_coordinates_for_city(self, city: str) -> Optional[Dict[str, float]]:
        """Convert City name to coordinates using geocoding (for Open Mateo)"""
        geocode_url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": city,
            "limit": 1,
            "appid": self.api_key
        }
        response = self.make_api_request("", params=params, full_url=geocode_url)
        if response and isinstance(response, list) and len(response) > 0:
            return {
                "lat": response[0]["lat"],
                "lon": response[0]["lon"]
            }
        return None
    

    def get_current_weather(self, city: str, country_code: str = None) -> Optional[Dict]:
        """
        Try Open-Meteo first. Fallback to OpenWeatherMap
        """

        #Try Open-Meteo
        data = self.get_open_meteo_weather(city)
        if data:
            self.logger.info("Fetched data from Open-Meteo")
            return data

        "Fall back to OpenWeatherMap"
        location = city
        if country_code:
            location += f",{country_code}"
        # Combines the city and country code into one location string.
                
        params = {
            'q': location,
            'units': 'metric'
        }
        
        raw_data = self.make_api_request('weather', params)
        if raw_data:
            self.logger.info("Fetched data from OpenWeatherMap (fallback)")
            return self._validate_and_clean_current_weather(raw_data)
        return None
    
    def _validate_and_clean_current_weather(self, raw_data: Dict) -> Optional[Dict]:
        """
        Validate and clean the weather data before storage.
        Extracts and reshapes data from the raw API JSON into a cleaner structure.
        Ensures all numeric fields are valid types.
        Handles missing nested fields using .get() with defaults.
        """
        try:
            cleaned_data = {
                'timestamp': datetime.now().isoformat(),
                'city': raw_data['name'],
                'country': raw_data['sys']['country'],
                'temperature': float(raw_data['main']['temp']),
                'feels_like': float(raw_data['main']['feels_like']),
                'humidity': int(raw_data['main']['humidity']),
                'pressure': float(raw_data['main']['pressure']),
                'weather_main': raw_data['weather'][0]['main'],
                'weather_description': raw_data['weather'][0]['description'],
                'wind_speed': float(raw_data.get('wind', {}).get('speed', 0)),
                'wind_direction': int(raw_data.get('wind', {}).get('deg', 0)),
                'cloudiness': int(raw_data['clouds']['all']),
                'visibility': int(raw_data.get('visibility', 10000)),
                'api_timestamp': datetime.fromtimestamp(raw_data['dt']).isoformat()
            }
            
            # Validate reasonable ranges
            if not (-50 <= cleaned_data['temperature'] <= 60):
                self.logger.warning(f"Temperature out of range: {cleaned_data['temperature']}")
                return None
                
            if not (0 <= cleaned_data['humidity'] <= 100):
                self.logger.warning(f"Humidity out of range: {cleaned_data['humidity']}")
                return None
            
            return cleaned_data
            
        except (KeyError, ValueError, TypeError) as e:
            self.logger.error(f"Data validation failed: {e}")
            return None
        
        # If parsing fails (e.g., raw_data['main']['temp'] doesn’t exist or is not a float), the error is logged and the 
        # result is discarded.

def get_open_meteo_weather(self, city: str) -> Optional[Dict]:
    """Try to get current weather from Open-Meteo API."""
    coords = self.get_coordinates_for_city(city)
    if not coords:
        self.logger.warning(f"Could not get coordinates for city: {city}")
        return None
    
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "current_weather": "true"
    }
    response = self.make_api_request("", params=params, full_url="https://api.open-meteo.com/v1/forecast")
    
    if response and "current_weather" in response:
        current = response["current_weather"]
        return {
            'timestamp': datetime.now().isoformat(),
            'city': city,
            'country': "N/A",  # Open-Meteo doesn't return country
            'temperature': float(current["temperature"]),
            'feels_like': float(current["temperature"]),  # Open-Meteo doesn't give this, so use temp
            'humidity': 0,  # Not provided
            'pressure': 0,  # Not provided
            'weather_main': "Unknown",
            'weather_description': "Open-Meteo",
            'wind_speed': float(current["windspeed"]),
            'wind_direction': int(current["winddirection"]),
            'cloudiness': 0,  # Not provided
            'visibility': 10000,  # Assume default
            'api_timestamp': datetime.fromtimestamp(current["time"]).isoformat()
        }
    return None