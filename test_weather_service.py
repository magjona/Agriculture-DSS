"""
Weather Service Integration Test
Tests the weather service module for proper functionality
"""

from core.weather_service import (
    get_uganda_weather_data,
    get_weather_advisory,
    get_weather_from_api,
    _get_crop_forecast
)

def test_weather_defaults():
    """Test that regional weather defaults work"""
    print("Testing weather defaults...")
    
    locations = ['Kampala', 'Gulu', 'Entebbe', 'Jinja', 'Mbarara', 'Other']
    
    for location in locations:
        weather = get_uganda_weather_data(location)
        assert weather is not None, f"Weather data for {location} is None"
        assert 'temperature' in weather, f"Missing temperature for {location}"
        assert 'condition' in weather, f"Missing condition for {location}"
        assert 'humidity' in weather, f"Missing humidity for {location}"
        assert 'rainfall' in weather, f"Missing rainfall for {location}"
        assert 'forecast' in weather, f"Missing forecast for {location}"
        print(f"✓ {location}: {weather['temperature']}°C, {weather['condition']}")
    
    print("✓ All weather defaults working!\n")


def test_weather_advisory():
    """Test weather advisory generation"""
    print("Testing weather advisory...")
    
    test_cases = [
        {'temperature': 32, 'humidity': 85, 'rainfall': 'heavy'},
        {'temperature': 15, 'humidity': 45, 'rainfall': 'light'},
        {'temperature': 25, 'humidity': 70, 'rainfall': 'moderate'},
    ]
    
    for weather in test_cases:
        advisory = get_weather_advisory(weather)
        assert advisory, f"No advisory generated for {weather}"
        print(f"✓ Advisory: {advisory[:80]}...")
    
    print("✓ All weather advisories generated!\n")


def test_crop_forecast():
    """Test crop forecast generation"""
    print("Testing crop forecast...")
    
    test_cases = [
        ('rain', 25, 'Excellent'),
        ('cloudy', 25, 'Good'),
        ('sunny', 25, 'Good'),
        ('sunny', 32, 'Hot'),
    ]
    
    for condition, temp, expected_keyword in test_cases:
        forecast = _get_crop_forecast(condition, temp)
        assert expected_keyword.lower() in forecast.lower(), \
            f"Forecast for {condition}/{temp}°C should contain '{expected_keyword}'"
        print(f"✓ {condition} @ {temp}°C: {forecast}")
    
    print("✓ All forecasts generated!\n")


def test_weather_data_structure():
    """Test that weather data has expected structure"""
    print("Testing weather data structure...")
    
    weather = get_uganda_weather_data('Kampala')
    
    required_fields = [
        'temperature',
        'condition',
        'humidity',
        'rainfall',
        'forecast',
        'region',
        'source'
    ]
    
    for field in required_fields:
        assert field in weather, f"Missing required field: {field}"
        print(f"✓ {field}: {weather[field]}")
    
    # Check data types
    assert isinstance(weather['temperature'], int), "Temperature must be int"
    assert isinstance(weather['humidity'], int), "Humidity must be int"
    assert weather['temperature'] > 0, "Temperature must be positive"
    assert 0 <= weather['humidity'] <= 100, "Humidity must be 0-100"
    
    print("✓ All data types correct!\n")


if __name__ == '__main__':
    import os
    import django
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_system.settings')
    django.setup()
    
    print("=" * 60)
    print("WEATHER SERVICE INTEGRATION TEST")
    print("=" * 60 + "\n")
    
    try:
        test_weather_defaults()
        test_weather_data_structure()
        test_weather_advisory()
        test_crop_forecast()
        
        print("=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        exit(1)
