import unittest
from unittest.mock import patch

import action_engine as act


class TimeTests(unittest.TestCase):
    @patch("weather._geocode_location")
    def test_get_time_for_location(self, mock_geocode):
        mock_geocode.return_value = {"latitude": 55.7558, "longitude": 37.6173, "name": "Moscow", "timezone": "Europe/Moscow"}

        response = act.get_time("Moscow")

        self.assertIsInstance(response, str)
        self.assertIn("Moscow", response)
        self.assertIn(":", response)


if __name__ == "__main__":
    unittest.main()
