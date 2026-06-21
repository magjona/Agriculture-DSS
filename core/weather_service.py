"""
Weather Service Module
Provides dynamic weather data based on farmer location in Uganda.
Integrates with OpenWeatherMap API with fallback to regional defaults.
"""

import logging
import requests
from django.conf import settings
from datetime import datetime
import urllib3

if not getattr(settings, 'VERIFY_SSL', True):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

# Uganda Regional Weather Defaults with realistic climate data
UGANDAN_WEATHER_DEFAULTS = {
    'Kampala': {
        'temperature': 26,
        'condition': 'Partly Cloudy',
        'humidity': 75,
        'rainfall': 'moderate',
        'forecast': 'Good for most crops',
        'wind_speed': 10,
        'pressure': 1013,
        'region': 'Central Uganda'
    },
    'Gulu': {
        'temperature': 24,
        'condition': 'Sunny',
        'humidity': 65,
        'rainfall': 'light',
        'forecast': 'Irrigation recommended',
        'wind_speed': 8,
        'pressure': 1011,
        'region': 'Northern Uganda'
    },
    'Entebbe': {
        'temperature': 25,
        'condition': 'Cloudy',
        'humidity': 80,
        'rainfall': 'moderate',
        'forecast': 'Favorable for water-loving crops',
        'wind_speed': 12,
        'pressure': 1012,
        'region': 'Central Uganda (Lake Region)'
    },
    'Jinja': {
        'temperature': 25,
        'condition': 'Partly Cloudy',
        'humidity': 70,
        'rainfall': 'moderate',
        'forecast': 'Good for maize and beans',
        'wind_speed': 9,
        'pressure': 1012,
        'region': 'Eastern Uganda'
    },
    'Mbarara': {
        'temperature': 23,
        'condition': 'Sunny',
        'humidity': 60,
        'rainfall': 'light',
        'forecast': 'Great for bananas and coffee',
        'wind_speed': 7,
        'pressure': 1010,
        'region': 'Southwestern Uganda'
    },
    'Masaka': {
        'temperature': 24,
        'condition': 'Cloudy',
        'humidity': 72,
        'rainfall': 'moderate',
        'forecast': 'Good for matooke',
        'wind_speed': 8,
        'pressure': 1012,
        'region': 'Central Uganda'
    },
    'Mbale': {
        'temperature': 25,
        'condition': 'Partly Cloudy',
        'humidity': 70,
        'rainfall': 'moderate',
        'forecast': 'Favorable for crops',
        'wind_speed': 9,
        'pressure': 1011,
        'region': 'Eastern Uganda'
    },
    'Arua': {
        'temperature': 27,
        'condition': 'Sunny',
        'humidity': 55,
        'rainfall': 'light',
        'forecast': 'Irrigation needed for most crops',
        'wind_speed': 10,
        'pressure': 1010,
        'region': 'Northwestern Uganda'
    },
    'Lira': {
        'temperature': 24,
        'condition': 'Partly Cloudy',
        'humidity': 65,
        'rainfall': 'moderate',
        'forecast': 'Good for sorghum',
        'wind_speed': 8,
        'pressure': 1011,
        'region': 'Northern Uganda'
    },
    'Fort Portal': {
        'temperature': 22,
        'condition': 'Cloudy',
        'humidity': 80,
        'rainfall': 'heavy',
        'forecast': 'Perfect for tea cultivation',
        'wind_speed': 6,
        'pressure': 1009,
        'region': 'Western Uganda (Highland)'
    },
    'Mukono': {
        'temperature': 25,
        'condition': 'Partly Cloudy',
        'humidity': 75,
        'rainfall': 'moderate',
        'forecast': 'Excellent for pineapples',
        'wind_speed': 9,
        'pressure': 1012,
        'region': 'Central Uganda (Lake Region)'
    },
    'Soroti': {
        'temperature': 26,
        'condition': 'Sunny',
        'humidity': 60,
        'rainfall': 'light',
        'forecast': 'Good for millet production',
        'wind_speed': 11,
        'pressure': 1010,
        'region': 'Eastern Uganda'
    },
    'Hoima': {
        'temperature': 25,
        'condition': 'Cloudy',
        'humidity': 70,
        'rainfall': 'moderate',
        'forecast': 'Favorable for sunflower',
        'wind_speed': 8,
        'pressure': 1011,
        'region': 'Western Uganda'
    },
    'Kitgum': {
        'temperature': 24,
        'condition': 'Partly Cloudy',
        'humidity': 65,
        'rainfall': 'light',
        'forecast': 'Good for sesame cultivation',
        'wind_speed': 9,
        'pressure': 1010,
        'region': 'Northern Uganda'
    },
    'Mubende': {
        'temperature': 24,
        'condition': 'Sunny',
        'humidity': 68,
        'rainfall': 'moderate',
        'forecast': 'Perfect for maize cultivation',
        'wind_speed': 8,
        'pressure': 1011,
        'region': 'Central Uganda'
    },
    'Kabale': {
        'temperature': 20,
        'condition': 'Cloudy',
        'humidity': 78,
        'rainfall': 'heavy',
        'forecast': 'Ideal for highland crops',
        'wind_speed': 7,
        'pressure': 1008,
        'region': 'Southwestern Uganda (Highland)'
    },
    'Kasese': {
        'temperature': 24,
        'condition': 'Sunny',
        'humidity': 65,
        'rainfall': 'light',
        'forecast': 'Good for range of crops',
        'wind_speed': 9,
        'pressure': 1010,
        'region': 'Western Uganda (Mountain Region)'
    },
    'Iganga': {
        'temperature': 25,
        'condition': 'Partly Cloudy',
        'humidity': 72,
        'rainfall': 'moderate',
        'forecast': 'Good for rice and cotton',
        'wind_speed': 8,
        'pressure': 1012,
        'region': 'Eastern Uganda'
    },
    'Other': {
        'temperature': 25,
        'condition': 'Partly Cloudy',
        'humidity': 70,
        'rainfall': 'moderate',
        'forecast': 'Favorable for most crops',
        'wind_speed': 9,
        'pressure': 1011,
        'region': 'Uganda'
    }
}


def get_weather_from_api(location="Kampala"):
    """
    Fetch real-time weather data from OpenWeatherMap API.
    
    Args:
        location: Uganda location name
        
    Returns:
        dict: Weather data with temperature, condition, humidity, etc.
    """
    api_key = getattr(settings, 'WEATHER_API_KEY', None)
    
    if not api_key:
        logger.debug(f"No WEATHER_API_KEY configured, using regional defaults for {location}")
        return None
    
    try:
        # OpenWeatherMap API endpoint
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': f"{location},UG",
            'appid': api_key,
            'units': 'metric'
        }
        
        verify_ssl = getattr(settings, 'VERIFY_SSL', True)
        response = requests.get(url, params=params, timeout=5, verify=verify_ssl)
        
        if response.status_code == 200:
            data = response.json()
            main_data = data.get('main', {})
            weather_data = data.get('weather', [{}])[0]
            wind_data = data.get('wind', {})
            
            weather_info = {
                'temperature': round(main_data.get('temp', 25)),
                'condition': weather_data.get('description', 'Unknown').title(),
                'humidity': main_data.get('humidity', 70),
                'pressure': main_data.get('pressure', 1013),
                'wind_speed': round(wind_data.get('speed', 0) * 3.6),  # Convert m/s to km/h
                'rainfall': 'heavy' if 'rain' in weather_data.get('description', '').lower() else 'light',
                'forecast': _get_crop_forecast(weather_data.get('description', ''), main_data.get('temp', 25)),
                'region': location,
                'source': 'api'
            }
            logger.info(f"Successfully fetched weather for {location} from API")
            return weather_info
        else:
            logger.warning(f"Weather API returned status {response.status_code} for {location}")
            return None
            
    except requests.exceptions.Timeout:
        logger.warning(f"Weather API timeout for {location}")
        return None
    except requests.exceptions.RequestException as e:
        logger.warning(f"Weather API error for {location}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching weather for {location}: {str(e)}")
        return None


def _get_crop_forecast(condition, temperature):
    """
    Generate crop-specific forecast based on weather condition and temperature.
    
    Args:
        condition: Weather condition description
        temperature: Current temperature in Celsius
        
    Returns:
        str: Agricultural forecast recommendation
    """
    condition_lower = condition.lower()
    
    if 'rain' in condition_lower or 'drizzle' in condition_lower:
        return '✓ Excellent for irrigation-dependent crops'
    elif 'cloud' in condition_lower:
        return '✓ Good for shade-tolerant crops'
    elif 'clear' in condition_lower or 'sunny' in condition_lower:
        if temperature > 28:
            return '⚠ Hot conditions - Use irrigation'
        return '✓ Good for most crops'
    elif 'fog' in condition_lower or 'mist' in condition_lower:
        return '⚠ Low visibility - Reduce operations'
    else:
        return '✓ Conditions suitable for farming'


def get_uganda_weather_data(location="Kampala"):
    """
    Get weather data for Ugandan locations.
    Attempts to fetch from API first, falls back to regional defaults.
    
    Args:
        location: Uganda location name
        
    Returns:
        dict: Weather data including temperature, condition, humidity, etc.
    """
    # Try to get fresh API data first
    api_weather = get_weather_from_api(location)
    if api_weather:
        return api_weather
    
    # Fallback to regional defaults
    default_weather = UGANDAN_WEATHER_DEFAULTS.get(location, UGANDAN_WEATHER_DEFAULTS['Other']).copy()
    default_weather['source'] = 'default'
    default_weather['updated_at'] = datetime.now().isoformat()
    
    return default_weather


def get_weather_advisory(weather_data):
    """
    Generate farming-specific advisory based on weather data.
    
    Args:
        weather_data: dict from get_uganda_weather_data
        
    Returns:
        str: Agricultural advisory
    """
    if not weather_data:
        return "Check weather conditions before planning farm activities."
    
    temp = weather_data.get('temperature', 25)
    humidity = weather_data.get('humidity', 70)
    rainfall = weather_data.get('rainfall', 'light')
    
    advisories = []
    
    # Temperature-based advisories
    if temp > 30:
        advisories.append("🌡️ Hot conditions - Increase irrigation frequency")
    elif temp < 15:
        advisories.append("❄️ Cool conditions - Frost risk present, protect seedlings")
    
    # Humidity-based advisories
    if humidity > 80:
        advisories.append("💧 High humidity - Watch for fungal diseases")
    elif humidity < 40:
        advisories.append("🌵 Low humidity - Boost irrigation to prevent crop stress")
    
    # Rainfall-based advisories
    if rainfall == 'heavy':
        advisories.append("🌧️ Heavy rainfall expected - Ensure proper drainage")
    elif rainfall == 'light':
        advisories.append("☀️ Dry conditions - Plan irrigation schedule")
    
    return " | ".join(advisories) if advisories else weather_data.get('forecast', 'Farm operations normal')
