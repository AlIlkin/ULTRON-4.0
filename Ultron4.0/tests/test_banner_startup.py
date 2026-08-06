import importlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ultron_bootstrap = importlib.import_module("ultron_bootstrap")


class BannerStartupTests(unittest.TestCase):
    def test_banner_module_imports_without_voice_dependencies(self):
        self.assertTrue(hasattr(ultron_bootstrap, "print_red_banner"))
        self.assertTrue(hasattr(ultron_bootstrap, "ANSI_RED"))


if __name__ == "__main__":
    unittest.main()
