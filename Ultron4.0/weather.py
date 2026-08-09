import json
import urllib.parse
import urllib.request

DEFAULT_WEATHER_FORMAT = "%l: %c %t %w %m"


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


def get_weather(location=None):
    """Return a short weather summary for a location."""
    if not location:
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
