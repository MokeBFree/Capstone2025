import customtkinter as ctk
from tkinter import messagebox
from weather_app import get_current_weather
import datetime
from utils.geocode import geocode_city
from open_meteo import OpenMeteo
from open_meteo.models import HourlyParameters
import aiohttp
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import asyncio