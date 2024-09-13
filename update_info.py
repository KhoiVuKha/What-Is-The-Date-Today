import requests
from lunarcalendar import Converter, Solar
import datetime
import os

# Function to get the current Gregorian date and time
def get_current_date():
    today = datetime.datetime.now()
    return today.strftime("%Y-%m-%d %H:%M:%S")

# Function to get the current Lunar date
def get_lunar_date():
    today = datetime.date.today()
    solar = Solar(today.year, today.month, today.day)
    lunar = Converter.Solar2Lunar(solar)
    return f"{lunar.day}/{lunar.month}/{lunar.year} (Lunar)"

# Function to get weather and air quality data for a specific city
def get_weather_and_air_quality(city):
    # Retrieve API key from environment variable
    API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
    
    # OpenWeatherMap API URLs for weather and air pollution data
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    air_quality_url = f"http://api.openweathermap.org/data/2.5/air_pollution?q={city}&appid={API_KEY}"

    # Fetch the weather and air quality data from the API
    weather_data = requests.get(weather_url).json()
    air_quality_data = requests.get(air_quality_url).json()

    # Extract weather description, temperature, and air quality index
    weather_description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    air_quality_index = air_quality_data['list'][0]['main']['aqi']

    # Return formatted string with the weather and air quality information
    return f"Weather: {weather_description}, Temperature: {temperature}°C, Air Quality Index: {air_quality_index}"

# List of cities to get the weather and air quality data for
cities = ["Hưng Yên", "Hà Nội", "Đà Nẵng", "Ho Chi Minh City"]

# Open the README.md file and append the gathered information
with open("README.md", "a") as f:
    # Write the current Gregorian date and time
    f.write(f"\nCurrent Date: {get_current_date()}\n")
    
    # Write the current Lunar date
    f.write(f"Lunar Date: {get_lunar_date()}\n")
    
    # Write weather and air quality data for each city
    for city in cities:
        f.write(f"{city}:\n{get_weather_and_air_quality(city)}\n")

