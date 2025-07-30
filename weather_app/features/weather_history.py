# Initialize data storage

        


        self.current_city = "Denver"  # Default city
        default_data = self.collector.get_current_weather(self.current_city)
        self.weather_data = {self.current_city: [default_data] if default_data else []}