import unittest
from unittest.mock import patch

import action_engine


class OpenAnythingTests(unittest.TestCase):
    def test_open_zoom_uses_windows_zoom_executable_when_available(self):
        with patch.object(action_engine, "OS_NAME", "Windows"), patch(
            "os.path.exists", side_effect=lambda path: path == r"C:\Program Files\Zoom\bin\Zoom.exe"
        ), patch("os.system") as mock_system:
            result = action_engine.open_anything("zoom")

        self.assertEqual(result, "Opening zoom")
        mock_system.assert_called_once_with(r'start "" "C:\Program Files\Zoom\bin\Zoom.exe"')



if __name__ == "__main__":
    unittest.main()
