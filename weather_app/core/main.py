from config import Config #needs to import the config file to access the API key and URL
from weather_data_collector import WeatherDataCollector
from weather_database import WeatherDatabase

# from dotenv import load_dotenv
from datetime import datetime
import tkinter as tk
from tkinter import ttk

#accesses the database
from weather_database import WeatherDatabase


db = WeatherDatabase("data/weather.db")
#collects weather data
#processes the data

#displays the data and runs gui
def main():
    root = tk.Tk()
    app = WeatherDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
