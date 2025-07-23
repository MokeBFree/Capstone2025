from core.config import Config #needs to import the config file to access the API key and URL
from core.weather_data_collector import WeatherDataCollector
from core.weather_dashboard import WeatherDashboard
from core.storage import save_last_city, load_last_city, log_weather_data

from dotenv import load_dotenv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import requests
import os
from tkinter import ttk



def main():
    root = tk.Tk()
    app = WeatherDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()