#!/usr/bin/env python
"""Simple weather service test"""
import sys
import os
import django

sys.path.insert(0, r'c:\Users\MAGADA\Desktop\MJR\vscode')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_system.settings')
django.setup()

from core.weather_service import get_uganda_weather_data, get_weather_advisory

# Test weather for Kampala
print("="*60)
print("Weather Service Quick Test")
print("="*60)

weather = get_uganda_weather_data('Kampala')
print(f"\nLocation: {weather['region']}")
print(f"Temperature: {weather['temperature']}°C")
print(f"Condition: {weather['condition']}")
print(f"Humidity: {weather['humidity']}%")
print(f"Rainfall: {weather['rainfall']}")
print(f"Forecast: {weather['forecast']}")
print(f"Data Source: {weather['source']}")

advisory = get_weather_advisory(weather)
print(f"\nAdvisory: {advisory}")

# Test multiple locations
print("\n" + "="*60)
print("Testing Multiple Locations")
print("="*60)

locations = ['Gulu', 'Entebbe', 'Jinja', 'Mbarara', 'Fort Portal']
for loc in locations:
    w = get_uganda_weather_data(loc)
    print(f"\n{loc}: {w['temperature']}°C, {w['condition']}, {w['forecast'][:30]}...")

print("\n" + "="*60)
print("✓ WEATHER SERVICE WORKING!")
print("="*60)
