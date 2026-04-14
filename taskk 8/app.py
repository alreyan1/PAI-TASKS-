import os
import requests
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# API Configuration
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', 'fallback_api_key_here')
OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5'

# Icon mapping to emojis
ICON_MAP = {
    '01d': '☀️',   # clear sky day
    '01n': '🌙',   # clear sky night
    '02d': '⛅',   # few clouds day
    '02n': '☁️',   # few clouds night
    '03d': '☁️',   # scattered clouds day
    '03n': '☁️',   # scattered clouds night
    '04d': '☁️',   # broken clouds day
    '04n': '☁️',   # broken clouds night
    '09d': '🌧️',   # shower rain day
    '09n': '🌧️',   # shower rain night
    '10d': '🌧️',   # rain day
    '10n': '🌧️',   # rain night
    '11d': '⛈️',   # thunderstorm day
    '11n': '⛈️',   # thunderstorm night
    '13d': '❄️',   # snow day
    '13n': '❄️',   # snow night
    '50d': '🌫️',   # mist day
    '50n': '🌫️',   # mist night
}

def get_icon_emoji(icon_code):
    """Map OpenWeatherMap icon code to emoji."""
    return ICON_MAP.get(icon_code, '🌤️')

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/weather')
def get_weather():
    """Get current weather for a city."""
    city = request.args.get('city', '').strip()
    units = request.args.get('units', 'metric')
    
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    
    if units not in ['metric', 'imperial']:
        units = 'metric'
    
    try:
        response = requests.get(
            f'{OPENWEATHER_BASE_URL}/weather',
            params={
                'q': city,
                'units': units,
                'appid': OPENWEATHER_API_KEY
            },
            timeout=10
        )
        
        if response.status_code == 404:
            return jsonify({'error': 'City not found'}), 404
        elif response.status_code == 401:
            return jsonify({'error': 'Invalid API key'}), 401
        
        response.raise_for_status()
        data = response.json()
        
        # Determine unit symbols
        temp_unit = '°C' if units == 'metric' else '°F'
        wind_unit = 'm/s' if units == 'metric' else 'mph'
        
        weather_data = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['main'].title(),
            'icon': get_icon_emoji(data['weather'][0]['icon']),
            'wind_speed': round(data['wind']['speed'], 1),
            'visibility': round(data['visibility'] / 1000, 1),
            'pressure': data['main']['pressure'],
            'temp_unit': temp_unit,
            'wind_unit': wind_unit
        }
        
        return jsonify(weather_data), 200
    
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out. Please try again.'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Connection error. Please check your internet.'}), 503
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/api/forecast')
def get_forecast():
    """Get 5-day forecast for a city."""
    city = request.args.get('city', '').strip()
    units = request.args.get('units', 'metric')
    
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    
    if units not in ['metric', 'imperial']:
        units = 'metric'
    
    try:
        response = requests.get(
            f'{OPENWEATHER_BASE_URL}/forecast',
            params={
                'q': city,
                'units': units,
                'cnt': 40,
                'appid': OPENWEATHER_API_KEY
            },
            timeout=10
        )
        
        if response.status_code == 404:
            return jsonify({'error': 'City not found'}), 404
        elif response.status_code == 401:
            return jsonify({'error': 'Invalid API key'}), 401
        
        response.raise_for_status()
        data = response.json()
        
        # Determine unit symbols
        temp_unit = '°C' if units == 'metric' else '°F'
        
        # Group by date and prefer 12:00 reading
        forecast_by_date = {}
        for item in data['list']:
            dt = datetime.fromtimestamp(item['dt'])
            date_key = dt.strftime('%Y-%m-%d')
            
            if date_key not in forecast_by_date:
                forecast_by_date[date_key] = []
            
            forecast_by_date[date_key].append(item)
        
        # Process each day - prefer 12:00, fallback to available data
        forecast_list = []
        for date_key in sorted(forecast_by_date.keys())[:5]:
            forecasts = forecast_by_date[date_key]
            
            # Try to find 12:00 reading
            preferred = None
            for f in forecasts:
                dt = datetime.fromtimestamp(f['dt'])
                if dt.hour == 12:
                    preferred = f
                    break
            
            # Use preferred or just first available
            item = preferred if preferred else forecasts[0]
            
            # Get all temps for this day to find min/max
            temps = [f['main']['temp'] for f in forecasts]
            
            dt = datetime.fromtimestamp(item['dt'])
            forecast_list.append({
                'date': dt.strftime('%a'),  # e.g., 'Mon'
                'max_temp': round(max(temps)),
                'min_temp': round(min(temps)),
                'description': item['weather'][0]['main'].title(),
                'icon': get_icon_emoji(item['weather'][0]['icon']),
                'humidity': item['main']['humidity'],
                'temp_unit': temp_unit
            })
        
        return jsonify({'forecast': forecast_list}), 200
    
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out. Please try again.'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Connection error. Please check your internet.'}), 503
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
