import os
import time
import pyautogui
import pygetwindow as gw

pyautogui.FAILSAFE = True

# Application name mappings
APP_ALIASES = {
    "powerpoint": ["powerpoint", "ppt", "pptx"],
    "word": ["word", "microsoft word", "document"],
    "excel": ["excel", "spreadsheet", "sheet"],
    "outlook": ["outlook", "email", "mail"],
    "notepad": ["notepad", "notes"],
    "paint": ["paint", "drawing"],
    "calculator": ["calculator", "calc"],
    "chrome": ["chrome", "google chrome"],
    "firefox": ["firefox"],
    "edge": ["edge", "microsoft edge"],
}

def delete_words():
    pyautogui.hotkey("ctrl", "backspace")
    return "Deleted last word."

def get_executable_name(target):
    """Convert user input to proper executable name"""
    target_lower = target.lower().strip()
    
    # Check aliases
    for app_name, aliases in APP_ALIASES.items():
        if target_lower in aliases:
            return app_name
    
    return target

def open_anything(target):
    """Open any application by name"""
    app_name = get_executable_name(target)
    try:
        os.system(f"start {app_name}")
        return f"Opening {target}"
    except Exception as e:
        return f"Could not open {target}. Error: {str(e)}"

def open_application(app_name):
    os.system(f'start "" "{app_name}"')
    if os.path.exists(app_name):
        return f"Opening {app_name}"
    return f"Application {app_name} not found"

def close_anything(target):
    wins = gw.getWindowsWithTitle(target)
    if wins:
        wins[0].close()
        return f"Closed {target}"
    return "Window not found"

def minimize_anything(target):
    wins = gw.getWindowsWithTitle(target)
    if wins:
        wins[0].minimize()
        return f"Minimized {target}"
    return "Window not found"

def maximize_anything(target):
    wins = gw.getWindowsWithTitle(target)
    if wins:
        wins[0].maximize()
        return f"Maximized {target}"
    return "Window not found"

def write_anything(text):
    time.sleep(0.5)
    pyautogui.write(text, interval=0.04)
    return "Done"

def shutdown_system():
    os.system("shutdown /s /t 1")
    return
def restart_system():
    os.system("shutdown /r /t 1")
    return
def sleep_system():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 1,1,0")
    return
def screenshot():
    screenshot = pyautogui.screenshot()
    filepath = os.path.join(os.getcwd(), "screenshot.png")
    screenshot.save(filepath)
    return f"Screenshot saved at {filepath}"
def search_web(query):
    import webbrowser
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searching for {query} on the web"

def open_word():
    try:
        os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE")
        return "Opening Microsoft Word"
    except Exception:
        try:
            os.startfile("C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.EXE")
            return "Opening Microsoft Word"
        except Exception:
            os.system("start winword")
            return "Opening Microsoft Word"