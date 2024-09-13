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

    # Fetch the weather data from the API
    weather_response = requests.get(weather_url)
    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        weather_description = weather_data['weather'][0]['description'].capitalize()
        temperature = weather_data['main']['temp']
    else:
        weather_description = "Unavailable"
        temperature = "Unavailable"
    
    # Fetch the air quality data from the API
    air_quality_response = requests.get(air_quality_url)
    if air_quality_response.status_code == 200:
        air_quality_data = air_quality_response.json()
        if 'list' in air_quality_data and len(air_quality_data['list']) > 0:
            air_quality_index = air_quality_data['list'][0]['main']['aqi']
        else:
            air_quality_index = "Unavailable"
    else:
        air_quality_index = "Unavailable"

    # Return formatted string with the weather and air quality information
    return f"Weather: {weather_description}, Temperature: {temperature}°C, Air Quality Index: {air_quality_index}"

# List of cities to get the weather and air quality data for
cities = ["Hưng Yên", "Hà Nội", "Đà Nẵng", "Ho Chi Minh City"]

# Open the README.md file and append the gathered information
with open("README.md", "a") as f:
    # Write the current Gregorian date and time
    f.write("\n## Date Information\n")
    f.write(f"- **Current Date**: {get_current_date()}\n")
    f.write(f"- **Lunar Date**: {get_lunar_date()}\n")
    
    # Add a separator for readability
    f.write("\n## Weather and Air Quality Information\n")
    
    # Write weather and air quality data for each city in a well-formatted way
    for city in cities:
        f.write(f"\n### {city}:\n")
        f.write(f"- {get_weather_and_air_quality(city)}\n")
