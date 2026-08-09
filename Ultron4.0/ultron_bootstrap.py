import importlib
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ANSI_RED = "\033[91m"
ANSI_BOLD = "\033[1m"
ANSI_RESET = "\033[0m"


def print_red_banner():
    print(f"{ANSI_BOLD}{ANSI_RED}")
    print("╔══════════════════════════════════════════════════════╗")
    print("║                    ULTRON 4.0                        ║")
    print("║             Ready to serve and assist                ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(ANSI_RESET)


if os.name == "nt":
    os.system("title ULTRON 4.0")

print_red_banner()


def safe_import(module_name, default=None):
    try:
        return importlib.import_module(module_name)
    except Exception as exc:
        print(f"{ANSI_RED}{module_name} unavailable:{ANSI_RESET} {exc}")
        return default


voice_input = safe_import("voice_input")
voice_output = safe_import("voice_output")
nlp_engine = safe_import("nlp_engine")
action_engine = safe_import("action_engine")
raw_engine = safe_import("raw_engine")
timer = safe_import("timer")

listen = getattr(voice_input, "listen", None)
if listen is None:
    def listen():
        return ""

speak = getattr(voice_output, "speak", None)
if speak is None:
    def speak(text):
        print(text)

understand = getattr(nlp_engine, "understand", None)
if understand is None:
    def understand(command):
        return "", ""

act = action_engine
if act is None:
    class _FallbackActionEngine:
        def delete_words(self):
            return "Delete action unavailable."

        def restart_system(self):
            return None

        def sleep_system(self):
            return None

        def screenshot(self):
            return "Screenshot unavailable."

        def open_anything(self, target):
            return f"Opening {target} is unavailable."

        def close_system_application(self, target):
            return f"Closing {target} is unavailable."

        def check_notification(self):
            return "Notifications unavailable."

        def open_settings(self):
            return "Settings unavailable."

        def search_web(self, query):
            return f"Search unavailable for {query}."

        def open_word(self):
            return "Word opening unavailable."

        def close_anything(self, target):
            return f"Closing {target} is unavailable."

        def minimize_anything(self, target):
            return f"Minimizing {target} is unavailable."

        def maximize_anything(self, target):
            return f"Maximizing {target} is unavailable."

        def write_anything(self, target):
            return f"Typing {target} is unavailable."

        def remove_words(self, target, words):
            return "Remove action unavailable."

    act = _FallbackActionEngine()

execute_raw = getattr(raw_engine, "execute_raw", None)
if execute_raw is None:
    def execute_raw(command):
        return "Raw command support unavailable."

shutdown_after = getattr(timer, "shutdown_after", None)
cancel_shutdown = getattr(timer, "cancel_shutdown", None)
if shutdown_after is None:
    def shutdown_after(minutes):
        print(f"Shutdown after {minutes} minutes is unavailable.")
if cancel_shutdown is None:
    def cancel_shutdown():
        print("Shutdown cancel is unavailable.")
