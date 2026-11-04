class Castle:
    def __init__(self, date, max_temp_c, max_wind_mph):
        self.date = date
        self.max_temp_c = max_temp_c
        self.max_wind_mph = max_wind_mph
    def __str__(self):
        return f"On {self.date}, maximum temp was {self.max_temp_c} and max wind speed was {self.max_wind_mph} mph"