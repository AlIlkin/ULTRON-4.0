import json
import os
import time
import platform
import subprocess
import urllib.error
import urllib.parse
import urllib.request
import pyautogui

import weather
from datetime import datetime, timedelta, timezone
try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None

TIMEZONE_OFFSET_MAP = {
    "Europe/Istanbul": 3,
    "Europe/London": 1,
    "Europe/Moscow": 3,
    "Europe/Paris": 2,
    "Europe/Berlin": 2,
    "Europe/Rome": 2,
    "America/New_York": -4,
    "America/Los_Angeles": -7,
    "America/Chicago": -5,
    "America/Denver": -6,
    "Asia/Tokyo": 9,
    "Asia/Seoul": 9,
    "Asia/Kolkata": 5.5,
    "Asia/Shanghai": 8,
    "Asia/Singapore": 8,
    "Australia/Sydney": 10,
    "Australia/Melbourne": 10,
    "Australia/Perth": 8,
}

pyautogui.FAILSAFE = True

OS_NAME = platform.system()  # "Windows", "Darwin", or "Linux"

# Application name mappings
APP_ALIASES = {
    "powerpoint": ["powerpoint", "ppt", "pptx"],
    "word": ["word", "microsoft word", "document"],
    "excel": ["excel", "spreadsheet", "sheet"],
    "outlook": ["outlook", "email", "mail"],
    "notepad": ["notepad", "notes", "textedit"],
    "paint": ["paint", "drawing", "preview"],
    "calculator": ["calculator", "calc"],
    "google chrome": ["chrome", "google chrome"],
    "settings": ["settings", "system settings"],
    "firefox": ["firefox"],
    "microsoft edge": ["edge", "microsoft edge"],
    "Clock": ["clock"],
    "Zoom": ["zoom"]
}

# Per-OS application/executable names for each canonical key above
APP_NAMES_BY_OS = {
    "Windows": {
        "settings": "settings",
        "powerpoint": "powerpnt",
        "word": "winword",
        "excel": "excel",
        "outlook": "outlook",
        "notepad": "notepad",
        "paint": "mspaint",
        "calculator": "calc",
        "google chrome": "chrome",
        "firefox": "firefox",
        "microsoft edge": "msedge",
        "Clock": "ms-clock:",
        "Zoom": "zoom"
    },
    "Darwin": {
        "settings": "System Settings",
        "powerpoint": "Microsoft PowerPoint",
        "word": "Microsoft Word",
        "excel": "Microsoft Excel",
        "outlook": "Microsoft Outlook",
        "notepad": "TextEdit",
        "paint": "Preview",
        "calculator": "Calculator",
        "google chrome": "Google Chrome",
        "firefox": "Firefox",
        "microsoft edge": "Microsoft Edge",
        "Clock": "Clock",
        "Zoom": "zoom.us"
    },
    "Linux": {
        "settings": "gnome-control-center",
        "powerpoint": "libreoffice --impress",
        "word": "libreoffice --writer",
        "excel": "libreoffice --calc",
        "outlook": "thunderbird",
        "notepad": "gedit",
        "paint": "gimp",
        "calculator": "gnome-calculator",
        "google chrome": "google-chrome",
        "firefox": "firefox",
        "microsoft edge": "microsoft-edge",
        "Clock": "gnome-clocks",
        "Zoom": "zoom"
    },
}

def close_system_application(app_name):
    """Close a system application by name, resolved for the current OS"""
    app_key = get_executable_name(app_name)
    resolved_name = APP_NAMES_BY_OS.get(OS_NAME, {}).get(app_key, app_name)
    try:
        if OS_NAME == "Windows":
            os.system(f'taskkill /IM "{resolved_name}.exe" /F')
        elif OS_NAME == "Darwin":
            subprocess.run(["osascript", "-e", f'tell application "{resolved_name}" to quit'], check=True)
        elif OS_NAME == "Linux":
            subprocess.run(["pkill", "-f", resolved_name], check=True)
        else:
            return f"Unsupported operating system: {OS_NAME}"
        return f"Closed {app_name}"
    except Exception as e:
        return f"Could not close {app_name}. Error: {str(e)}"

def open_settings():
    if OS_NAME == "Windows":
        os.system("start ms-settings:")
    elif OS_NAME == "Darwin":
        subprocess.run(["open", "/System/Applications/System Settings.app"])
    elif OS_NAME == "Linux":
        subprocess.run(["gnome-control-center"])
    else:
        return f"Unsupported operating system: {OS_NAME}"
    return "Opening settings."

def check_notification():
    if OS_NAME == "Windows":
        pyautogui.hotkey("win", "n") # Opening the notification center on Windows
    elif OS_NAME == "Darwin":
        pyautogui.hotkey("fn", "n") # Opening the notification center on macOS
    elif OS_NAME == "Linux":
        pyautogui.hotkey("super", "m") # Opening the notification center on Linux
    else:
        return f"Unsupported operating system: {OS_NAME}"

def close_anything(target):
    if OS_NAME == "Windows":
        import pygetwindow as gw
        wins = gw.getWindowsWithTitle(target)
        if wins:
            wins[0].close()
            return f"Closed {target}"
        return "Window not found"
    elif OS_NAME == "Darwin":
        script = f'tell application "{target}" to quit'
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        return f"Closed {target}" if result.returncode == 0 else "Window not found"
    elif OS_NAME == "Linux":
        result = subprocess.run(["wmctrl", "-c", target], capture_output=True, text=True)
        return f"Closed {target}" if result.returncode == 0 else "Window not found"
    return f"Unsupported operating system: {OS_NAME}"

def delete_words():
    key = "ctrl" if OS_NAME != "Darwin" else "option"
    pyautogui.hotkey(key, "backspace")
    return "Deleted last word."

def get_executable_name(target):
    """Convert user input to canonical app key"""
    target_lower = target.lower().strip()

    for app_name, aliases in APP_ALIASES.items():
        if target_lower in aliases:
            return app_name

    return target


def resolve_windows_app_path(app_key, fallback_name):
    """Return a concrete Windows executable path when a known app is installed."""
    if app_key != "Zoom":
        return fallback_name

    candidates = [
        r"C:\Program Files\Zoom\bin\Zoom.exe",
        r"C:\Program Files (x86)\Zoom\bin\Zoom.exe",
        os.path.expanduser(r"~\AppData\Roaming\Zoom\bin\Zoom.exe"),
    ]

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    return fallback_name


def open_anything(target):
    """Open any application by name, resolved for the current OS"""
    app_key = get_executable_name(target)
    resolved_name = APP_NAMES_BY_OS.get(OS_NAME, {}).get(app_key, target)
    try:
        if OS_NAME == "Windows":
            resolved_name = resolve_windows_app_path(app_key, resolved_name)
            os.system(f'start "" "{resolved_name}"')
        elif OS_NAME == "Darwin":
            subprocess.run(["open", "-a", resolved_name], check=True)
        elif OS_NAME == "Linux":
            subprocess.Popen(resolved_name.split())
        else:
            return f"Unsupported operating system: {OS_NAME}"
        return f"Opening {target}"
    except Exception as e:
        return f"Could not open {target}. Error: {str(e)}"

def open_application(app_name):
    try:
        if OS_NAME == "Windows":
            os.system(f'start "" "{app_name}"')
        elif OS_NAME == "Darwin":
            subprocess.run(["open", "-a", app_name], check=True)
        elif OS_NAME == "Linux":
            subprocess.Popen(app_name.split())
        else:
            return f"Unsupported operating system: {OS_NAME}"
        return f"Opening {app_name}"
    except Exception as e:
        return f"Application {app_name} not found. Error: {str(e)}"

def minimize_anything(target):
    if OS_NAME == "Windows":
        import pygetwindow as gw
        wins = gw.getWindowsWithTitle(target)
        if wins:
            wins[0].minimize()
            return f"Minimized {target}"
        return "Window not found"
    elif OS_NAME == "Darwin":
        script = f'tell application "System Events" to set visible of process "{target}" to false'
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        return f"Minimized {target}" if result.returncode == 0 else "Window not found"
    elif OS_NAME == "Linux":
        result = subprocess.run(["wmctrl", "-r", target, "-b", "add,hidden"], capture_output=True, text=True)
        return f"Minimized {target}" if result.returncode == 0 else "Window not found"
    return f"Unsupported operating system: {OS_NAME}"

def maximize_anything(target):
    if OS_NAME == "Windows":
        import pygetwindow as gw
        wins = gw.getWindowsWithTitle(target)
        if wins:
            wins[0].maximize()
            return f"Maximized {target}"
        return "Window not found"
    elif OS_NAME == "Darwin":
        script = (
            f'tell application "{target}" to activate\n'
            f'tell application "System Events" to tell process "{target}" '
            f'to set value of attribute "AXFullScreen" of window 1 to true'
        )
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        return f"Maximized {target}" if result.returncode == 0 else "Window not found"
    elif OS_NAME == "Linux":
        result = subprocess.run(["wmctrl", "-r", target, "-b", "add,maximized_vert,maximized_horz"], capture_output=True, text=True)
        return f"Maximized {target}" if result.returncode == 0 else "Window not found"
    return f"Unsupported operating system: {OS_NAME}"

def write_anything(text):
    time.sleep(0.5)
    pyautogui.write(text, interval=0.04)
    return "Done"

def shutdown_system():
    if OS_NAME == "Windows":
        os.system("shutdown /s /t 1")
    elif OS_NAME == "Darwin":
        subprocess.run(["osascript", "-e", 'tell app "System Events" to shut down'])
    elif OS_NAME == "Linux":
        subprocess.run(["shutdown", "-h", "now"])
    return

def restart_system():
    if OS_NAME == "Windows":
        os.system("shutdown /r /t 1")
    elif OS_NAME == "Darwin":
        subprocess.run(["osascript", "-e", 'tell app "System Events" to restart'])
    elif OS_NAME == "Linux":
        subprocess.run(["shutdown", "-r", "now"])
    return

def sleep_system():
    if OS_NAME == "Windows":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 1,1,0")
    elif OS_NAME == "Darwin":
        subprocess.run(["pmset", "sleepnow"])
    elif OS_NAME == "Linux":
        subprocess.run(["systemctl", "suspend"])
    return

def screenshot():
    filepath = os.path.join(os.getcwd(), "screenshot.png")
    if OS_NAME == "Darwin":
        try:
            subprocess.run(["screencapture", filepath], check=True)
            return f"Screenshot saved at {filepath}"
        except Exception as e:
            return f"Screenshot failed on macOS: {e}"

    try:
        img = pyautogui.screenshot()
        img.save(filepath)
        return f"Screenshot saved at {filepath}"
    except Exception as e:
        message = str(e)
        if "pyscreeze" in message.lower() or "pillow" in message.lower():
            return (
                "Screenshot failed: PyAutoGUI could not import the screenshot backend. "
                "Install Pillow with `pip install pillow` in your environment."
            )
        return f"Screenshot failed: {message}"


def search_web(query):
    import webbrowser
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searching for {query} on the web"


def get_weather(location=None, forecast=False, period=None):
    try:
        return weather.get_weather(location, forecast=forecast, period=period)
    except Exception:
        return "Weather service is unavailable right now."


def get_time(location=None):
    """Return the local time or the time in a specified location's timezone."""
    try:
        if not location:
            now = datetime.now()
            return f"The current time is {now.strftime('%H:%M')}."

        place = weather._geocode_location(location)
        if not place:
            return "I couldn't find that location. Please try a city name like London or Moscow."

        tz = place.get("timezone")
        name = place.get("name", location)
        if tz and ZoneInfo:
            try:
                now = datetime.now(ZoneInfo(tz))
                return f"Time in {name} ({tz}): {now.strftime('%Y-%m-%d %H:%M:%S')}"
            except Exception:
                # Try an external timezone API (worldtimeapi) as a fallback
                try:
                    body = weather._call_url(f"https://worldtimeapi.org/api/timezone/{tz}")
                    data = json.loads(body)
                    dt = data.get("datetime") or data.get("utc_datetime") or data.get("unixtime")
                    if isinstance(dt, int):
                        # unix time
                        from datetime import datetime as _dt

                        now_utc = _dt.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S')
                        return f"Time in {name} ({tz}): {now_utc} (from worldtimeapi)"
                    if dt:
                        # ISO datetime string
                        return f"Time in {name} ({tz}): {dt} (from worldtimeapi)"
                except Exception:
                    pass

                # Fallback for well-known timezones if external lookup fails
                offset = TIMEZONE_OFFSET_MAP.get(tz)
                if offset is not None:
                    now_utc = datetime.now(timezone.utc)
                    tz_delta = timedelta(hours=offset)
                    now_local = (now_utc + tz_delta).strftime('%Y-%m-%d %H:%M:%S')
                    return f"Time in {name} ({tz}): {now_local} (approximate, using offset {offset:+})"

                # Final fallback: return current UTC time with a note (still includes a colon)
                now_utc = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                return f"Time in {name} ({tz}): {now_utc} (UTC, timezone conversion unavailable)"

        if tz:
            return f"Timezone for {name} is {tz}. Local time unavailable on this system."

        return f"I couldn't determine the timezone for {name}."
    except Exception:
        return "Time service is unavailable right now."


def get_weather_coordinates(location=None):
    try:
        return weather.get_weather_coordinates(location)
    except Exception:
        return "Weather coordinates are unavailable right now."


def write_weather_coordinates(location=None):
    text = get_weather_coordinates(location)
    if text.startswith("I couldn't") or text.startswith("Please specify") or text.startswith("Weather coordinates"):
        return text
    write_anything(text)
    return text


def open_word():
    try:
        if OS_NAME == "Windows":
            for path in (
                "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
                "C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
            ):
                if os.path.exists(path):
                    os.startfile(path)
                    return "Opening Microsoft Word"
            os.system("start winword")
        elif OS_NAME == "Darwin":
            subprocess.run(["open", "-a", "Microsoft Word"], check=True)
        elif OS_NAME == "Linux":
            subprocess.Popen(["libreoffice", "--writer"])
        else:
            return f"Unsupported operating system: {OS_NAME}"
        return "Opening Microsoft Word"
    except Exception as e:
        return f"Could not open Microsoft Word. Error: {str(e)}"