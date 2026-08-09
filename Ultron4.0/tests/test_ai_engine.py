import unittest

from ai_engine import explain_topic


class ExplainTopicTests(unittest.TestCase):
    def test_explain_topic_returns_a_detailed_response(self):
        explanation = explain_topic("python")

        self.assertIsInstance(explanation, str)
        self.assertGreater(len(explanation), 40)
        self.assertIn("Python", explanation)


if __name__ == "__main__":
    unittest.main()
