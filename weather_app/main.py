from core.config import Config #needs to import the config file to access the API key and URL
from core.weather_data_collector import WeatherDataCollector
from core.storage import save_last_city, load_last_city, log_weather_data

from dotenv import load_dotenv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import requests
import os
from tkinter import ttk

load_dotenv() # Load API key from .env file
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    collector = WeatherDataCollector(API_KEY)
    weather = collector.get_current_weather(city)
    save_last_city(city)  # Save the last city for future reference
   
    if weather is None:
        result_label.config(text="Error fetching data.")
    else:
        description = weather["weather_description"]
        temp = weather["temperature"]
        result_label.config(text=f"{description.capitalize()}, {temp}°C")
        log_weather_data(city, temp, description)



#processes the data

# #displays the data and runs gui

root = tk.Tk()
root.title("Weather App")
root.geometry("300x200")
city_entry = tk.Entry(root, width=25)
city_entry.pack(pady=10)
city_entry.insert(0, "Enter city")
get_button = tk.Button(root, text="Get Weather", command=get_weather)
get_button.pack(pady=5)
result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.pack(pady=10)
root.mainloop()