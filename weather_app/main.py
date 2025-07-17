from config import Config #needs to import the config file to access the API key and URL
from weather_data_collector import WeatherDataCollector
from weather_database import WeatherDatabase
from weather_dashboard import WeatherDashboard

# from dotenv import load_dotenv
from datetime import datetime
import tkinter as tk
from tkinter import ttk

#points to the db and collects weather data
db = WeatherDatabase(".data/weather.txt")

#processes the data

# #displays the data and runs gui
# uncomment the following lines to run the GUI

# def main():
#     root = tk.Tk()
#     app = WeatherDashboard(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()
