# Weather Feature Setup Guide

## Overview

The Farm Decision Support System now includes a fully embedded, dynamic weather feature that provides real-time weather data based on the farmer's location in Uganda. The weather information is seamlessly integrated into the dashboard and helps farmers make informed agricultural decisions.

## Features

✅ **Location-Based Weather**: Automatically displays weather for the farmer's registered location
✅ **Real-Time Updates**: Fetches live weather data from OpenWeatherMap API
✅ **Smart Fallback**: Uses accurate regional defaults if API is unavailable
✅ **Agricultural Advisory**: Provides farming-specific recommendations based on current weather
✅ **Multi-Region Support**: Covers all 20 Ugandan regions with accurate climate data
✅ **No Configuration Required**: Works out-of-the-box with regional defaults; enhanced with optional API

## Installation & Setup

### Option 1: Basic Setup (No API Key - Recommended for Testing)

The system works perfectly without an API key using regional weather defaults for all 20 Ugandan locations. This is ideal for development and testing.

**No additional setup needed!** Just run:

```bash
python manage.py runserver
```

### Option 2: Enhanced Setup (With Real-Time Weather API)

To enable real-time weather data, you'll need an OpenWeatherMap API key.

#### Step 1: Get an API Key

1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Click "Sign Up" and create a free account
3. After verification, go to your account "API keys" section
4. Copy your API key (it usually looks like: `abc123def456ghi789`)

#### Step 2: Configure the API Key

You have three options:

##### Option A: Environment Variable (Recommended for Production)

Add to your `.env` file or system environment:

```bash
WEATHER_API_KEY=your_api_key_here
```

Then in Python, Django will automatically read it from `settings.py`.

##### Option B: Direct Settings (Development Only)

Edit `farm_system/settings.py`:

```python
# Line with WEATHER_API_KEY
WEATHER_API_KEY = 'your_api_key_here'  # Replace with your actual key
```

##### Option C: Docker Environment

If using Docker, add to your `docker-compose.yml`:

```yaml
environment:
  - WEATHER_API_KEY=your_api_key_here
```

#### Step 3: Verify Setup

Run the development server:

```bash
python manage.py runserver
```

Visit: http://localhost:8000

- **Without API Key**: You'll see "Data: default" (regional defaults)
- **With API Key**: You'll see "Data: api" (real-time weather)

## How Weather is Displayed

### 1. Landing Page
Shows current weather for Kampala with an agricultural advisory banner.

### 2. Farmer Dashboard
Displays personalized weather for the farmer's registered location with:
- Current temperature
- Weather condition
- Humidity level
- Rainfall intensity
- Crop forecast
- Farming-specific advisory

### 3. Manager Dashboard
Shows weather data for each region where recommendations were made, helping managers understand regional conditions.

## Weather Data Components

### Temperature (°C)
Real-time temperature data for informed irrigation decisions.

### Condition
Description of current weather (Sunny, Cloudy, Rainy, etc.)

### Humidity (%)
Moisture level in the air - helps predict fungal diseases.

### Rainfall Intensity
- **Heavy**: High precipitation expected
- **Moderate**: Regular rainfall
- **Light**: Dry conditions

### Agricultural Forecast
Crop-specific recommendations based on current conditions:
- "✓ Excellent for irrigation-dependent crops"
- "✓ Good for shade-tolerant crops"
- "⚠ Hot conditions - Use irrigation"
- "⚠ High humidity - Watch for fungal diseases"

## Regional Weather Defaults

The system includes accurate climate data for all 20 Ugandan regions:

| Region | Avg Temp | Typical Condition | Best Crops |
|--------|----------|-------------------|-----------|
| Kampala | 26°C | Partly Cloudy | Most crops |
| Fort Portal | 22°C | Cloudy | Tea (Highland) |
| Kabale | 20°C | Cloudy | Highland crops |
| Mbarara | 23°C | Sunny | Bananas, Coffee |
| Arua | 27°C | Sunny | Requires irrigation |
| Jinja | 25°C | Partly Cloudy | Maize, Beans |
| Mukono | 25°C | Partly Cloudy | Pineapples |

*And 13 more regions with location-specific data...*

## API Usage & Limits

### Free Tier (OpenWeatherMap)

The free tier provides:
- **Calls per minute**: 60 API calls/minute
- **Daily limit**: 1,000 calls/day
- **Data freshness**: Every 10 minutes

This is more than sufficient for a farm management system!

### API Response Time

- **Average**: 200-500ms
- **With fallback**: Instant (if API fails)

## Weather Service Architecture

The weather feature is built on a modular service (`core/weather_service.py`):

```python
# Get weather for a location
from core.weather_service import get_uganda_weather_data, get_weather_advisory

weather = get_uganda_weather_data('Kampala')
advisory = get_weather_advisory(weather)
```

### Available Functions

#### `get_uganda_weather_data(location)`
Returns weather data with automatic API/fallback handling:
```python
{
    'temperature': 26,
    'condition': 'Partly Cloudy',
    'humidity': 75,
    'rainfall': 'moderate',
    'forecast': 'Good for most crops',
    'wind_speed': 10,
    'pressure': 1013,
    'region': 'Central Uganda',
    'source': 'api'  # or 'default'
}
```

#### `get_weather_advisory(weather_data)`
Generates farming-specific recommendations:
```python
"🌡️ Hot conditions - Increase irrigation frequency | 💧 High humidity - Watch for fungal diseases"
```

## Troubleshooting

### Issue: Weather showing "default" instead of real-time

**Cause**: API key not configured or API unreachable

**Solution**:
1. Check your API key is correct
2. Verify internet connection
3. Check OpenWeatherMap API status

### Issue: Weather not updating

**Cause**: API rate limit exceeded or timeout

**Solution**:
1. Wait a few minutes (rate limit resets)
2. Check internet connection
3. Verify API key validity

### Issue: "Cold conditions - Frost risk" showing in summer

**Cause**: Unlikely regional default being used

**Solution**:
1. Set WEATHER_API_KEY for real-time data
2. Or update regional defaults in `core/weather_service.py`

## Development Notes

### Adding New Regions

To add a new region to the defaults, edit `UGANDAN_WEATHER_DEFAULTS` in `core/weather_service.py`:

```python
UGANDAN_WEATHER_DEFAULTS = {
    'NewRegion': {
        'temperature': 25,
        'condition': 'Partly Cloudy',
        'humidity': 70,
        'rainfall': 'moderate',
        'forecast': 'Good for most crops',
        'wind_speed': 9,
        'pressure': 1011,
        'region': 'New Region'
    }
}
```

### Customizing Agricultural Forecasts

Edit `_get_crop_forecast()` function in `core/weather_service.py` to add more agricultural-specific logic.

### API Integration Points

Weather data is fetched in:
- `core/views.py`: `landing()`, `dashboard()`, `manager_dashboard()`
- Templates automatically display with dynamic field names

## Best Practices

✅ **Do**:
- Use environment variables for API keys in production
- Keep regional defaults updated
- Monitor API usage
- Cache weather data for performance

❌ **Don't**:
- Commit API keys to version control
- Hardcode API keys in source code
- Make API calls on every page load (consider caching)

## Support

For issues or questions:
1. Check the debug logs: `debug.log`
2. Verify Django settings: `farm_system/settings.py`
3. Test API key: Visit OpenWeatherMap dashboard
4. Review `core/weather_service.py` documentation

## Future Enhancements

Potential improvements:
- 7-day weather forecast
- Historical weather data
- Weather alerts and notifications
- Seasonal weather patterns analysis
- Integration with soil moisture sensors
- Pest/disease risk assessment based on weather
