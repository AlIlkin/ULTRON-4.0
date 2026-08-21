import unittest
from unittest.mock import patch

import timer

class ShutdownTimerTests(unittest.TestCase):
    def test_shutdown_after_announces_countdown_and_triggers_shutdown(self):
        spoken_messages = []

        def fake_speak(message):
            spoken_messages.append(message)

        with patch("timer.speak", side_effect=fake_speak), patch(
            "timer.act.shutdown_system", side_effect=lambda: spoken_messages.append("shutdown")
        ), patch("timer.time.sleep", side_effect=lambda _: None):
            timer.shutdown_after(1)
            if timer.active_shutdown_thread is not None:
                timer.active_shutdown_thread.join(timeout=2)

        self.assertTrue(any("minute" in message.lower() for message in spoken_messages))
        self.assertTrue(any("shutting down" in message.lower() for message in spoken_messages))
        self.assertIn("shutdown", spoken_messages)



if __name__ == "__main__":
    unittest.main()
