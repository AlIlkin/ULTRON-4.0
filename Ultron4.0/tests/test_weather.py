import unittest
from unittest.mock import patch

import weather


class WeatherForecastTests(unittest.TestCase):
    def setUp(self):
        self.daily_data = {
            "time": ["2026-08-11", "2026-08-12", "2026-08-13"],
            "temperature_2m_max": [30, 32, 31],
            "temperature_2m_min": [20, 22, 21],
            "weathercode": [1, 3, 61],
            "windspeed_10m_max": [10, 12, 14],
            "precipitation_probability_max": [5, 15, 40],
        }

    @patch("weather._geocode_location")
    @patch("weather._forecast_weather")
    def test_get_weather_tomorrow_forecast(self, mock_forecast, mock_geocode):
        mock_geocode.return_value = {"latitude": 40.4093, "longitude": 49.8671, "name": "Baku"}
        mock_forecast.return_value = self.daily_data

        response = weather.get_weather("Baku", forecast=True, period="tomorrow")

        self.assertIn("Tomorrow in Baku", response)
        self.assertIn("high 32.00°C", response)
        self.assertIn("low 22.00°C", response)
        self.assertIn("precipitation chance 15.00%", response)

    @patch("weather._geocode_location")
    @patch("weather._forecast_weather")
    def test_get_weather_weekly_forecast(self, mock_forecast, mock_geocode):
        mock_geocode.return_value = {"latitude": 40.4093, "longitude": 49.8671, "name": "Baku"}
        mock_forecast.return_value = self.daily_data

        response = weather.get_weather("Baku", forecast=True, period="week")

        self.assertTrue(response.startswith("Weekly forecast for Baku:"))
        self.assertIn("Wed: partly cloudy, 30.00/20.00°C", response)
        self.assertIn("Thu: partly cloudy, 32.00/22.00°C", response)
        self.assertIn("Fri: rainy, 31.00/21.00°C", response)


if __name__ == "__main__":
    unittest.main()
