---
name: weather-forecaster
description: "Retrieve current weather conditions, multi-day forecasts, and air quality data for any global location using Open-Meteo. Use when checking current weather, planning around forecasts, or monitoring air quality indices."
---

# Weather Forecaster

## Workflow

1. **Resolve the location**: accept city name, region, or coordinates from the user
2. **Select the right tool** based on request type (current, forecast, or air quality)
3. **Present data** with temperature, conditions, humidity, wind, and units
4. **Suggest related checks**: if showing current weather, offer forecast or air quality

## Available Tools

| Tool | Description |
| ---- | ----------- |
| `get_current_weather(location)` | Temperature, humidity, wind speed, and conditions right now |
| `get_weather_forecast(location, days)` | Daily forecast for 1–7 days ahead |
| `get_air_quality(location)` | US AQI index and pollutant breakdown |

## Example Interactions

**User**: "What's the weather in Tokyo?"
→ Call `get_current_weather("Tokyo")` and show temperature, conditions, humidity, and wind

**User**: "5-day forecast for London"
→ Call `get_weather_forecast("London", 5)` and present daily highs, lows, and conditions

**User**: "Air quality in Delhi"
→ Call `get_air_quality("Delhi")` and report AQI level with health guidance

## Guardrails

1. **Data only**: Report actual values from the MCP tools; never fabricate weather data
2. **Forecast limit**: Maximum 7-day forecast available — inform user if they request more
3. **Units**: Present temperature in °C and wind in km/h by default; convert if user specifies preference
