#needs to import the config file to access the API key and URL
#accesses the database
from weather_database import WeatherDatabase


db = WeatherDatabase("data/weather.db")
#collects weather data
#processes the data
#displays the data and runs gui