# models.py
import pandas as pd
from geopy.geocoders import Nominatim
import swisseph as swe
import datetime
from . import calculations as calc


class NatalChart:
    def __init__(self, name, date, time, location):
        self.name = name
        self.date = date
        self.time = time
        self.location = location
        self.timezone = None
        self.longitude = None
        self.latitude = None
        self.planets_pos = None
        self.houses_pos = None
        self.aspects_matrix = None

    def calculate_all(self):
        # Parse date and time considering timezone
        input_date = self.parseInputDateTime(self.date, self.time, self.location)
        # Calculate positions
        self.planet_positions = calc.get_planets_pos(input_date, self.longitude, self.latitude)
        self.house_positions = calc.get_house_cusps(input_date, self.longitude, self.latitude)
        self.aspect_matrix = calc.aspects_calc(self.planet_positions, self.house_positions)

    def parseInputDateTime(self, date, time, location):
        ## Input Format
        input_date = date ## self.date
        input_time = time     ## self.time
        input_location = location  ## self.location
        
        ## Get Lat, Long and Tz from location
        geolocator = Nominatim(user_agent="astroPy")
        location = geolocator.geocode(input_location)
        latitude = location.latitude
        longitude = location.longitude
        timezone = 1  ## timedelta from UTC+0 ---> Guess from Locale or Ask to user o internet
        self.timezone = timezone
        self.longitude = longitude
        self.latitude = latitude
        
        ## Proly on local time so ----> to UTC  and then ------> Julian Day
        local_dt = datetime.datetime.strptime(f"{input_date} {input_time}","%d/%m/%y %H:%M")   ## '31/01/22 23:59' 
        ## En ESP somos GMT+1 es decr que para volver a utc es -1
        utc_dt = local_dt - datetime.timedelta(hours=timezone)  
        julian_day = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60)
        return julian_day
    

    def get_planet_positions(self):
        return self.planet_positions

    def get_house_positions(self):
        return self.house_positions

    def get_aspect_matrix(self):
        return self.aspect_matrix

