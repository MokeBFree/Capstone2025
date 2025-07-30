
#  Add at least 3 input controls (entry fields, dropdowns, radio buttons, etc.)
#  Display at least 3 weather metrics
#  Implement at least 2 different button functionalities
#  Make the chart update based on user selections
#  Add error handling for edge cases

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import matplotlib as mplt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import requests
import os
from weather_app.core.API_calls import meteo_call

class WeatherDashboard:
	def __init__(self, root):
		self.api_call = meteo_call()

		"""Initialize the Weather Dashboard GUI"""      
		
		self.root = tk.Tk()
		self.root.title("Weather Dashboard")
		self.root.geometry("900x700")
		
		# Ask for User's City
		user_city = simpledialog.askstring("City Input", "Where's your sky?")
		
		if not user_city:
			user_city = "Denver"
		
		self.current_city = user_city
		coords = self.api_call.get_coordinates_for_city(user_city)
		
		if coords:
			lat = coords["lat"]
			lon = coords["lon"]
			default_data = self.api_call.get_weather(lat, lon)

		else: 
			messagebox.showerror("City Error", f"Could not find coordinates for {user_city}.")
								 
		#initialize data                         
		self.weather_data = {self.current_city: [default_data] if default_data else []}
		
		
		# TODO: Add instance variables for storing user selections
		# Example: self.temperature_unit = "F"  # or "C"
		self.temperature_unit = tk.StringVar(value ="F")


		# # Create the GUI
		self.create_widgets()

			# Initialize the display with default data
		self.update_display()



	#             # Compare Cities text entry
		self.city1_entry = tk.Entry(root)
		self.city1_entry.grid(row=3, column=1)

		self.city2_entry = tk.Entry(root)
		self.city2_entry.grid(row=4, column=1)
		
	def create_widgets(self):
		"""Create and arrange all GUI widgets"""

		# Title Frame
		title_frame = ttk.Frame(self.root, padding="10")
		title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))

		title_label = ttk.Label(title_frame, text="Weather Dashboard",
							   font=('Arial', 16, 'bold'))
		title_label.pack()

		# Control Frame (Left Side)
		control_frame = ttk.LabelFrame(self.root, text="Controls", padding="10")
		control_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W, tk.E), padx=10)

		# City entry
		ttk.Label(control_frame, text="City:").grid(row=0, column=0, sticky=tk.W, pady=5)
		self.city_entry = ttk.Entry(control_frame)
		self.city_entry.grid(row=0, column=1, pady=5, sticky=tk.W)
		self.city_entry.insert(0, "Denver")

		# Date range combobox
		ttk.Label(control_frame, text="When?").grid(row=1, column=0, sticky=tk.W, pady=5)
		self.date_range = ttk.Combobox(control_frame, values=["Last 7 Days", "Last 14 Days", "Last 30 Days"], state="readonly")
		self.date_range.grid(row=1, column=1, pady=5, sticky=tk.W)
		self.date_range.set("Last 7 Days")

		# Temperature unit radio buttons
		ttk.Label(control_frame, text="Temperature:").grid(row=2, column=0, sticky=tk.W, pady=5)
		self.temp_radio_f = ttk.Radiobutton(control_frame, text="Fahrenheit", variable=self.temperature_unit, value="F")
		self.temp_radio_f.grid(row=2, column=1, sticky=tk.W)
		self.temp_radio_c = ttk.Radiobutton(control_frame, text="Celsius", variable=self.temperature_unit, value="C")
		self.temp_radio_c.grid(row=2, column=2, sticky=tk.W)

		# # Buttons
		self.update_btn = ttk.Button(control_frame, text="Update", command=self.on_update_clicked)
		self.update_btn.grid(row=3, column=1, pady=10, sticky=tk.W)
		self.clear_btn = ttk.Button(control_frame, text="Clear", command=self.on_clear_clicked)
		self.clear_btn.grid(row=3, column=2, pady=10, sticky=tk.W)

		# Display Frame (Right Side)
		display_frame = ttk.LabelFrame(self.root, text="Current Weather", padding="10")
		display_frame.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.W, tk.E), padx=10)

		self.temp_label = ttk.Label(display_frame, text="Temperature: --")
		self.temp_label.grid(row=0, column=0, sticky=tk.W, pady=5)
		self.humidity_label = ttk.Label(display_frame, text="Humidity: --")
		self.humidity_label.grid(row=1, column=0, sticky=tk.W, pady=5)
		self.precip_label = ttk.Label(display_frame, text="Precipitation: --")
		self.precip_label.grid(row=2, column=0, sticky=tk.W, pady=5)

		# Visualization Frame (Bottom)
		viz_frame = ttk.LabelFrame(self.root, text="Weather Trends", padding="10")
		viz_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

		# Create matplotlib figure - DO NOT MODIFY THIS SECTION
		self.figure = Figure(figsize=(8, 4), dpi=100)
		self.plot = self.figure.add_subplot(111)
		self.canvas = FigureCanvasTkAgg(self.figure, viz_frame)
		self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

		# Configure grid weights for resizing - DO NOT MODIFY
		self.root.columnconfigure(1, weight=1)
		self.root.rowconfigure(2, weight=1)

	

		

		


	# # def get_weather_data(self, city):
	# #     api_key = os.getenv('OPENWEATHER_API_KEY')
	# #     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
	# #     response = requests.get(url)
	
	# #     if response.status_code == 200:
	# #         data = response.json()
	# #         return {
	# #             'temperature': data['main']['temp'],
	# #             'humidity': data['main']['humidity'],
	# #             'precipitation': data.get('rain', {}).get('1h', 0),
	# #             'conditions': data['weather'][0]['description'],
	# #             'wind_speed': data['wind']['speed'],
	# #             'pressure': data['main']['pressure'],
	# #             'date': datetime.now()
	# #     }
	# #     else:
	# #         raise Exception(f"Failed to fetch data: {response.status_code}")

	#     # If the API call is successful, it returns a dictionary with weather data.
	
	def update_display(self):
		"""Update all weather displays with current selections"""
		city = self.city_entry.get().strip()
		date_list = self.get_date_range()
		if city not in self.weather_data:
			messagebox.showerror("City Not Found", f"City '{city}' not found in data.")
			return
		city_data = [d for d in self.weather_data[city] if d is not None]
		# Filter data by date range (dates in date_list)
		filtered = [d for d in city_data 
					if datetime.fromisoformat(d['timestamp']).date() in [dt.date() for dt in date_list]]
		if not filtered:
			self.temp_label.config(text="Temperature: --")
			self.humidity_label.config(text="Humidity: --")
			self.precip_label.config(text="Precipitation: --")
			self.plot.clear()
			self.canvas.draw()
			return
		# Use most recent day for display metrics
		latest = filtered[-1]
		temp = latest['temperature']
		if self.temperature_unit.get() == "C": 
			temp_disp = f"{self.convert_temperature(temp, to_celsius=True)} °C"
		else:
			temp_disp = f"{temp} °F"
		self.temp_label.config(text=f"Temperature: {temp_disp}")
		self.humidity_label.config(text=f"Humidity: {latest['humidity']}%")
		# self.precip_label.config(text=f"Precipitation: {latest['precipitation']} in")
		self.current_city = city
		self.update_chart()
	
	# def update_chart(self):
	#     """Update the matplotlib chart based on current selections"""
	#     self.plot.clear()
	#     city = self.city_entry.get().strip()
	#     date_list = self.get_date_range()
	#     if city not in self.weather_data:
	#         self.canvas.draw()
	#         return
	#     city_data = self.weather_data[city]
	#     filtered = [d for d in city_data 
	#                 if datetime.fromisoformat(d['timestamp']).date() in [dt.date() for dt in date_list]]
	#     if not filtered:
	#         self.canvas.draw()
	#         return
	#     dates = [datetime.fromisoformat(d['timestamp']) for d in filtered]
	#     temps = [d['temperature'] for d in filtered]
	#     if self.temperature_unit.get() == "C":
	#         temps = [self.convert_temperature(t, to_celsius=True) for t in temps]
	#         ylabel = "Temperature (°C)"
	#     else:
	#         ylabel = "Temperature (°F)"
	#     self.plot.plot(dates, temps, marker='o', color='tab:blue')
	#     self.plot.set_title(f"Temperature Trend - {city}")
	#     self.plot.set_ylabel(ylabel)
	#     self.plot.set_xlabel("Date")
	#     self.plot.grid(True, linestyle='--', alpha=0.5)
	#     self.figure.autofmt_xdate()
	#     self.canvas.draw()
	
	def on_update_clicked(self):
		"""Handle update button click"""
		city = self.city_entry.get().strip()
		if not city:
			messagebox.showerror("Input Error", "Please enter a city name.")
			return
		try:
			live_data = self.collector.get_current_weather(city)
			self.weather_data[city] = [live_data]
			self.current_city = city
			self.update_display()
		except Exception as e:
			messagebox.showerror("API Error", str(e))
	   
	   
	# def on_clear_clicked(self):
	#     """Handle clear/reset button click"""
	#     # Reset inputs to defaults
	#     self.city_entry.delete(0, tk.END)
	#     self.city_entry.insert(0, "New York")
	#     self.date_range.set("Last 7 Days")
	#     self.temperature_unit.set("F")
	#     self.current_city = "New York"
	#     self.update_display()

	# # def on_compare_clicked(self):
	# #     """Handle compare button click"""
	# #     city1 = self.city1_entry.get().strip()
	# #     city2 = self.city2_entry.get().strip()

	# #     if not city1 or not city2:
	# #         messagebox.showerror("You need both cities for a comparison.")
	# #         return
		
	# #     try:
	# #         data1 = self.collector.get_current_weather(city1)
	# #         data2 = self.collector.get_current_weather(city2)
	# #     except Exception as e:
	# #         messagebox.showerror("API Error", f"Fetch didn't work: {e}")
	# #         return
		
	# #     self.weather_data[city1] =[data1]  # get most recent entry
	# #     self.weather_data[city2] =[data2]

	# #     self.display_comparison(city1, data1, city2, data2)
	
	# def display_comparison(self, city1, data1, city2, data2):
	#     msg = (
	#         f"Comparing {city1} and {city2}:\n\n"
	#         f"Temperature: {data1['temperature']}°C vs {data2['temperature']}°C\n"
	#         f"Humidity: {data1['humidity']}% vs {data2['humidity']}%\n"
	#         f"Wind Speed: {data1['wind_speed']} km/h vs {data2['wind_speed']} km/h\n"
	#         # f"Conditions: {data1['conditions']} vs {data2['conditions']}"
	#     )
	#     messagebox.showinfo("City Comparison", msg)
	
	# def convert_temperature(self, temp_f, to_celsius=True):
	#     """Helper method to convert between temperature units"""
	#     if to_celsius:
	#         return round((temp_f - 32) * 5 / 9, 1)
	#     else:
	#         return round(temp_f * 9 / 5 + 32, 1)
	
	# def get_date_range(self):
	#     """Helper method to get the selected date range"""
	#     selection = self.date_range.get()
	#     days = 7 if selection == "Last 7 Days" else 14 if selection == "Last 14 Days" else 30
	#     return [datetime.now() - timedelta(days=i) for i in range(days)][::-1]

