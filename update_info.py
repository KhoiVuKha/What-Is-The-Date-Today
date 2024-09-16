import requests
from lunarcalendar import Converter, Solar
import datetime
import os
import pytz

# Function to get the current Gregorian date and time in both UTC and Vietnam time
def get_current_date():
    now_utc = datetime.datetime.now(pytz.utc)
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now_vietnam = now_utc.astimezone(vietnam_tz)
    
    return now_utc.strftime("%Y-%m-%d %H:%M:%S (UTC)"), now_vietnam.strftime("%Y-%m-%d %H:%M:%S (UTC+7)")

# Function to get the current Lunar date
def get_lunar_date():
    today = datetime.date.today()
    solar = Solar(today.year, today.month, today.day)
    lunar = Converter.Solar2Lunar(solar)
    return f"{lunar.day}/{lunar.month}/{lunar.year} (Lunar)"

# Function to get weather data for a specific city using OpenWeatherMap's API
def get_weather_data(city):
    # Retrieve API key from environment variable
    API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
    
    # OpenWeatherMap API URL for weather data
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    # Fetch the weather data from the API
    response = requests.get(weather_url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description'].capitalize()
        temperature = data['main']['temp']
    else:
        weather_description = "Unavailable"
        temperature = "Unavailable"
    
    return weather_description, temperature

# Function to get air quality data for a specific city using OpenWeatherMap's API
def get_air_quality_data(lat, lon):
    # Retrieve API key from environment variable
    API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
    
    # OpenWeatherMap API URL for air quality data
    air_quality_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    
    # Fetch the air quality data from the API
    response = requests.get(air_quality_url)
    if response.status_code == 200:
        data = response.json()
        air_quality_index = data['list'][0]['main']['aqi']
        # Return the AQI description based on the index
        return air_quality_index, get_aqi_description(air_quality_index)
    else:
        return "Unavailable", "Unavailable"

# Function to get description for the Air Quality Index
def get_aqi_description(aqi):
    descriptions = {
        1: "Good: Air quality is considered satisfactory, and air pollution poses little or no risk.",
        2: "Fair: Air quality is acceptable; however, there may be a risk for some people.",
        3: "Moderate: Air quality is acceptable; however, there may be a risk for some people, especially those with respiratory or heart conditions.",
        4: "Poor: Air quality is poor and poses a health risk for everyone, especially those with respiratory or heart conditions.",
        5: "Very Poor: Air quality is very poor, and everyone is likely to be affected, with significant health effects."
    }
    return descriptions.get(aqi, "Unavailable")

# Coordinates for the cities
cities = {
    "Hung Yen": {"lat": 20.6514, "lon": 106.0764},
    "Hanoi": {"lat": 21.0285, "lon": 105.8542},
    "Da Nang": {"lat": 16.0544, "lon": 108.2022},
    "Ho Chi Minh City": {"lat": 10.8231, "lon": 106.6297}
}

# Open the README.md file in write mode ("w") to overwrite the content
with open("README.md", "w") as f:
    # Write the current Gregorian date and time
    f.write("# Daily Report\n")
    f.write("## Date Information\n")
    
    # Get both UTC and Vietnam times
    utc_time, vietnam_time = get_current_date()
    f.write(f"- **Current UTC Time**: {utc_time}\n")
    f.write(f"- **Current Vietnam Time**: {vietnam_time}\n")
    
    # Lunar date
    f.write(f"- **Lunar Date**: {get_lunar_date()}\n")
    
    # Add a separator for readability
    f.write("\n## Weather and Air Quality Information\n")
    
    # Write weather and air quality data for each city in a well-formatted way
    for city, coords in cities.items():
        weather_description, temperature = get_weather_data(city)
        air_quality_index, air_quality_description = get_air_quality_data(coords['lat'], coords['lon'])
        
        f.write(f"\n### {city}:\n")
        f.write(f"- Weather: {weather_description}, Temperature: {temperature}°C\n")
        f.write(f"- Air Quality Index: {air_quality_index} ({air_quality_description})\n")
