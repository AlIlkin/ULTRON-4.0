import json
from datetime import datetime
import urllib.parse
import urllib.request

DEFAULT_WEATHER_FORMAT = "%l: %c %t %w %m"
DAILY_FORECAST_PARAMS = (
    "temperature_2m_max,temperature_2m_min,weathercode,"
    "windspeed_10m_max,precipitation_probability_max"
)
HOURLY_FORECAST_PARAMS = (
    "temperature_2m,weathercode,windspeed_10m,precipitation_probability"
)


def _call_url(url):
    request = urllib.request.Request(url, headers={"User-Agent": "UltronWeather/1.0"})
    with urllib.request.urlopen(request, timeout=15) as response:
        return response.read().decode("utf-8")


def _short_number(value):
    try:
        return f"{float(value):.2f}"
    except Exception:
        return str(value)


def _geocode_location(location):
    if not location:
        return None

    url_location = urllib.parse.quote_plus(location)
    url = (
        f"https://geocoding-api.open-meteo.com/v1/search?name={url_location}"
        "&count=1&language=en&format=json"
    )
    try:
        body = _call_url(url)
        data = json.loads(body)
        results = data.get("results")
        if not results:
            return None
        return results[0]
    except Exception:
        return None


def _current_weather(latitude, longitude):
    url = (
        "https://api.open-meteo.com/v1/forecast?current_weather=true&timezone=auto"
        f"&latitude={urllib.parse.quote_plus(str(latitude))}"
        f"&longitude={urllib.parse.quote_plus(str(longitude))}"
    )
    try:
        body = _call_url(url)
        data = json.loads(body)
        return data.get("current_weather")
    except Exception:
        return None


def _forecast_weather(latitude, longitude, forecast_days=7):
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"daily={DAILY_FORECAST_PARAMS}&timezone=auto&forecast_days={forecast_days}"
        f"&latitude={urllib.parse.quote_plus(str(latitude))}"
        f"&longitude={urllib.parse.quote_plus(str(longitude))}"
    )
    try:
        body = _call_url(url)
        data = json.loads(body)
        return data.get("daily")
    except Exception:
        return None


def _hourly_weather(latitude, longitude, forecast_hours=24):
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"hourly={HOURLY_FORECAST_PARAMS}&timezone=auto&forecast_hours={forecast_hours}"
        f"&latitude={urllib.parse.quote_plus(str(latitude))}"
        f"&longitude={urllib.parse.quote_plus(str(longitude))}"
    )
    try:
        body = _call_url(url)
        data = json.loads(body)
        return data.get("hourly")
    except Exception:
        return None


def _get_ip_location():
    """Try to get approximate location from the current IP address."""
    try:
        body = _call_url("https://ipapi.co/json/")
        data = json.loads(body)
        lat = data.get("latitude") or data.get("lat")
        lon = data.get("longitude") or data.get("lon")
        city = data.get("city")
        if lat is None or lon is None:
            return None
        return {"latitude": lat, "longitude": lon, "name": city}
    except Exception:
        return None


def _weather_description(code):
    try:
        code = int(code)
    except Exception:
        return "mixed conditions"

    if code == 0:
        return "clear sky"
    if code in (1, 2, 3):
        return "partly cloudy"
    if code in (45, 48):
        return "foggy"
    if code in (51, 53, 55):
        return "light drizzle"
    if code in (61, 63, 65):
        return "rainy"
    if code in (71, 73, 75, 77):
        return "snowy"
    if code in (80, 81, 82):
        return "rain showers"
    if code in (95, 96, 99):
        return "thunderstorms"
    return "mixed conditions"


def _forecast_value(daily, key, index, default="N/A"):
    values = daily.get(key, [])
    try:
        return _short_number(values[index])
    except Exception:
        return default


def _format_tomorrow_forecast(location_name, daily):
    if not daily or not daily.get("time") or len(daily.get("time", [])) < 2:
        return None

    high = _forecast_value(daily, "temperature_2m_max", 1)
    low = _forecast_value(daily, "temperature_2m_min", 1)
    description = _weather_description(daily.get("weathercode", [0])[1])
    windspeed = _forecast_value(daily, "windspeed_10m_max", 1)
    precipitation = _forecast_value(daily, "precipitation_probability_max", 1)

    forecast_text = (
        f"Tomorrow in {location_name}: {description}, "
        f"high {high}°C, low {low}°C, wind up to {windspeed} km/h"
    )
    if precipitation != "N/A":
        forecast_text += f", precipitation chance {precipitation}%"
    forecast_text += "."
    return forecast_text


def _format_weekly_forecast(location_name, daily):
    if not daily or not daily.get("time"):
        return None

    lines = []
    count = min(len(daily.get("time", [])), 7)
    for index in range(count):
        day_value = daily["time"][index]
        try:
            date_obj = datetime.fromisoformat(day_value)
            day_name = date_obj.strftime("%a")
        except Exception:
            day_name = day_value

        description = _weather_description(daily.get("weathercode", [0])[index])
        high = _forecast_value(daily, "temperature_2m_max", index)
        low = _forecast_value(daily, "temperature_2m_min", index)
        precipitation = _forecast_value(daily, "precipitation_probability_max", index)
        windspeed = _forecast_value(daily, "windspeed_10m_max", index)

        line = f"{day_name}: {description}, {high}/{low}°C"
        if precipitation != "N/A":
            line += f", {precipitation}% precip"
        if windspeed != "N/A":
            line += f", wind {windspeed} km/h"
        lines.append(line)

    return f"Weekly forecast for {location_name}:\n" + "\n".join(lines)


def _format_hourly_forecast(location_name, hourly):
    if not hourly or not hourly.get("time"):
        return None

    lines = []
    count = min(len(hourly.get("time", [])), 24)
    for index in range(count):
        time_value = hourly["time"][index]
        try:
            datetime_obj = datetime.fromisoformat(time_value)
            time_str = datetime_obj.strftime("%H:%M")
        except Exception:
            time_str = time_value

        description = _weather_description(hourly.get("weathercode", [0])[index])
        temperature = _forecast_value(hourly, "temperature_2m", index)
        windspeed = _forecast_value(hourly, "windspeed_10m", index)
        precipitation = _forecast_value(hourly, "precipitation_probability", index)

        line = f"{time_str}: {description}, {temperature}°C"
        if windspeed != "N/A":
            line += f", wind {windspeed} km/h"
        if precipitation != "N/A":
            line += f", {precipitation}% precip"
        lines.append(line)

    return f"Hourly forecast for {location_name} (next 24 hours):\n" + "\n".join(lines)


def get_weather(location=None, forecast=False, period=None):
    """Return a short weather summary for a location."""
    if not location:
        if forecast:
            place = _get_ip_location()
            if place:
                daily = _forecast_weather(place["latitude"], place["longitude"])
                if daily:
                    return _format_tomorrow_forecast(place.get("name", "your area"), daily)
            return "I couldn't get the forecast right now."

        # Try IP-based location first to get current local conditions
        place = _get_ip_location()
        if place:
            weather_data = _current_weather(place["latitude"], place["longitude"])
            if weather_data:
                description = _weather_description(weather_data.get("weathercode", 0))
                temperature = _short_number(weather_data.get("temperature", "N/A"))
                windspeed = _short_number(weather_data.get("windspeed", "N/A"))
                return (
                    f"Weather in {place.get('name', 'your area')}: {description}, "
                    f"{temperature}°C, wind {windspeed} km/h."
                )
        # Fallback to wttr.in if IP lookup or API failed
        url_location = ""
        url_format = urllib.parse.quote_plus(DEFAULT_WEATHER_FORMAT)
        url = f"https://wttr.in/{url_location}?format={url_format}"
        try:
            with urllib.request.urlopen(url, timeout=15) as response:
                body = response.read().decode("utf-8").strip()
        except Exception:
            return "I couldn't fetch the weather right now. Please check your internet connection and try again."

        if not body or "unknown location" in body.lower() or "error" in body.lower():
            return "I couldn't get the weather right now."
        return body

    place = _geocode_location(location)
    if not place:
        return "I couldn't find that location. Please try a city name like New York or London."

    if forecast:
        location_name = place.get("name", location)
        normalized_period = (period or "tomorrow").lower()
        
        if "hourly" in normalized_period:
            hourly = _hourly_weather(place["latitude"], place["longitude"])
            if not hourly:
                return "I couldn't fetch the hourly forecast details for that location."
            forecast_text = _format_hourly_forecast(location_name, hourly)
        else:
            daily = _forecast_weather(place["latitude"], place["longitude"])
            if not daily:
                return "I couldn't fetch the forecast details for that location."
            
            if "week" in normalized_period:
                forecast_text = _format_weekly_forecast(location_name, daily)
            else:
                forecast_text = _format_tomorrow_forecast(location_name, daily)

        if forecast_text:
            return forecast_text
        return "I couldn't get the forecast details for that location."

    weather_data = _current_weather(place["latitude"], place["longitude"])
    if not weather_data:
        return "I couldn't fetch the weather details for that location."

    description = _weather_description(weather_data.get("weathercode", 0))
    temperature = _short_number(weather_data.get("temperature", "N/A"))
    windspeed = _short_number(weather_data.get("windspeed", "N/A"))

    return (
        f"Weather in {place.get('name', location)}: {description}, "
        f"{temperature}°C, wind {windspeed} km/h."
    )


def get_weather_coordinates(location=None):
    """Return labeled latitude and longitude values for a location."""
    if not location:
        return "Please specify a location so I can type the latitude and longitude."

    place = _geocode_location(location)
    if not place:
        return "I couldn't find that location. Please try a city name like New York or London."

    latitude = _short_number(place.get("latitude", "N/A"))
    longitude = _short_number(place.get("longitude", "N/A"))
    name = place.get("name", location)

    return (
        f"Location: {name}\n"
        f"Latitude: {latitude}\n"
        f"Longitude: {longitude}"
    )
def get_hourly_forecast(location=None):
    """Return a short hourly weather forecast for a location."""
    if not location:
        place = _get_ip_location()
        if place:
            hourly = _hourly_weather(place["latitude"], place["longitude"])
            if hourly:
                return _format_hourly_forecast(place.get("name", "your area"), hourly)
        return "I couldn't get the hourly forecast right now."

    place = _geocode_location(location)
    if not place:
        return "I couldn't find that location. Please try a city name like New York or London."

    hourly = _hourly_weather(place["latitude"], place["longitude"])
    if not hourly:
        return "I couldn't fetch the hourly forecast details for that location."

    location_name = place.get("name", location)
    forecast_text = _format_hourly_forecast(location_name, hourly)

    if forecast_text:
        return forecast_text
    return "I couldn't get the hourly forecast details for that location."
