"""
Weather MCP - Open-Meteo API Integration (No API Key Required)

This module provides MCP tools for fetching weather data from Open-Meteo API.
Open-Meteo is a free, open-source weather API that requires NO API key.

Tools:
- get_current_weather: Get current weather conditions
- get_weather_forecast: Get multi-day weather forecast
- get_air_quality: Get air quality index and pollutant levels

API Documentation: https://open-meteo.com/en/docs
"""

import json
import logging
import httpx
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# Open-Meteo API base URLs (No API key required!)
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
AIR_QUALITY_API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


def _get_coordinates(location: str) -> tuple:
    """Get latitude and longitude for a location using Open-Meteo Geocoding API."""
    try:
        response = httpx.get(
            GEOCODING_API_URL,
            params={"name": location, "count": 1, "language": "en", "format": "json"},
            timeout=10.0
        )
        data = response.json()
        
        if data.get("results"):
            result = data["results"][0]
            return (
                result["latitude"],
                result["longitude"],
                result.get("name", location),
                result.get("country", "")
            )
        return None, None, location, ""
    except Exception as e:
        logger.error(f"Geocoding error: {e}")
        return None, None, location, ""


def _get_weather_description(code: int) -> str:
    """Convert WMO weather code to description."""
    codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return codes.get(code, "Unknown")


@tool
def get_current_weather(location: str) -> str:
    """
    Get current weather conditions for a location using Open-Meteo API (FREE, no API key).
    
    Args:
        location: City name or location (e.g., "London", "New York", "Tokyo")
    
    Returns:
        Current weather data including temperature, humidity, conditions
    """
    try:
        # Get coordinates
        lat, lon, name, country = _get_coordinates(location)
        if lat is None:
            return f"Error: Could not find location '{location}'"
        
        # Get current weather
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,surface_pressure",
            "timezone": "auto"
        }
        
        response = httpx.get(WEATHER_API_URL, params=params, timeout=10.0)
        data = response.json()
        
        if response.status_code == 200 and "current" in data:
            current = data["current"]
            weather = {
                "location": f"{name}, {country}" if country else name,
                "temperature": f"{current['temperature_2m']}°C",
                "feels_like": f"{current['apparent_temperature']}°C",
                "humidity": f"{current['relative_humidity_2m']}%",
                "conditions": _get_weather_description(current['weather_code']),
                "wind_speed": f"{current['wind_speed_10m']} km/h",
                "pressure": f"{current['surface_pressure']} hPa",
                "coordinates": {"lat": lat, "lon": lon}
            }
            return json.dumps(weather, indent=2)
        else:
            return f"Error: Unable to fetch weather data for {location}"
    except Exception as e:
        logger.error(f"Weather API error: {e}")
        return f"Error fetching weather: {str(e)}"


@tool
def get_weather_forecast(location: str, days: int = 5) -> str:
    """
    Get weather forecast for a location using Open-Meteo API (FREE, no API key).
    
    Args:
        location: City name or location (e.g., "London", "New York", "Tokyo")
        days: Number of days to forecast (1-7, default 5)
    
    Returns:
        Weather forecast data for the specified days
    """
    try:
        # Get coordinates
        lat, lon, name, country = _get_coordinates(location)
        if lat is None:
            return f"Error: Could not find location '{location}'"
        
        # Get forecast
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max,wind_speed_10m_max",
            "timezone": "auto",
            "forecast_days": min(days, 7)
        }
        
        response = httpx.get(WEATHER_API_URL, params=params, timeout=10.0)
        data = response.json()
        
        if response.status_code == 200 and "daily" in data:
            daily = data["daily"]
            forecasts = []
            
            for i in range(min(days, len(daily["time"]))):
                forecasts.append({
                    "date": daily["time"][i],
                    "temp_high": f"{daily['temperature_2m_max'][i]}°C",
                    "temp_low": f"{daily['temperature_2m_min'][i]}°C",
                    "conditions": _get_weather_description(daily['weather_code'][i]),
                    "precipitation_chance": f"{daily['precipitation_probability_max'][i]}%",
                    "wind_speed": f"{daily['wind_speed_10m_max'][i]} km/h"
                })
            
            return json.dumps({
                "location": f"{name}, {country}" if country else name,
                "forecast_days": len(forecasts),
                "forecast": forecasts
            }, indent=2)
        else:
            return f"Error: Unable to fetch forecast for {location}"
    except Exception as e:
        logger.error(f"Forecast API error: {e}")
        return f"Error fetching forecast: {str(e)}"


@tool
def get_air_quality(location: str) -> str:
    """
    Get air quality data for a location using Open-Meteo API (FREE, no API key).
    
    Args:
        location: City name or location (e.g., "London", "New York", "Tokyo")
    
    Returns:
        Air quality index and pollutant levels
    """
    try:
        # Get coordinates
        lat, lon, name, country = _get_coordinates(location)
        if lat is None:
            return f"Error: Could not find location '{location}'"
        
        # Get air quality
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone",
            "timezone": "auto"
        }
        
        response = httpx.get(AIR_QUALITY_API_URL, params=params, timeout=10.0)
        data = response.json()
        
        if response.status_code == 200 and "current" in data:
            current = data["current"]
            aqi = current.get('us_aqi', 0)
            
            # AQI level classification
            if aqi <= 50:
                aqi_level = "Good"
            elif aqi <= 100:
                aqi_level = "Moderate"
            elif aqi <= 150:
                aqi_level = "Unhealthy for Sensitive Groups"
            elif aqi <= 200:
                aqi_level = "Unhealthy"
            elif aqi <= 300:
                aqi_level = "Very Unhealthy"
            else:
                aqi_level = "Hazardous"
            
            return json.dumps({
                "location": f"{name}, {country}" if country else name,
                "aqi": aqi,
                "aqi_level": aqi_level,
                "pollutants": {
                    "PM2.5": f"{current.get('pm2_5', 'N/A')} μg/m³",
                    "PM10": f"{current.get('pm10', 'N/A')} μg/m³",
                    "Ozone (O3)": f"{current.get('ozone', 'N/A')} μg/m³",
                    "NO2": f"{current.get('nitrogen_dioxide', 'N/A')} μg/m³",
                    "CO": f"{current.get('carbon_monoxide', 'N/A')} μg/m³"
                }
            }, indent=2)
        else:
            return f"Error: Unable to fetch air quality for {location}"
    except Exception as e:
        logger.error(f"Air Quality API error: {e}")
        return f"Error fetching air quality: {str(e)}"


# Export all weather tools
WEATHER_TOOLS = [
    get_current_weather,
    get_weather_forecast,
    get_air_quality
]
