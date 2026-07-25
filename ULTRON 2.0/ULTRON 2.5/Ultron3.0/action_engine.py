import os
import time
import platform
import subprocess
import pyautogui

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
    "firefox": ["firefox"],
    "microsoft edge": ["edge", "microsoft edge"],
}

# Per-OS application/executable names for each canonical key above
APP_NAMES_BY_OS = {
    "Windows": {
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
    },
    "Darwin": {
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
    },
    "Linux": {
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
    },
}

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

def open_anything(target):
    """Open any application by name, resolved for the current OS"""
    app_key = get_executable_name(target)
    resolved_name = APP_NAMES_BY_OS.get(OS_NAME, {}).get(app_key, target)
    try:
        if OS_NAME == "Windows":
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
        subprocess.run(["screencapture", filepath])
    else:
        img = pyautogui.screenshot()
        img.save(filepath)
    return f"Screenshot saved at {filepath}"

def search_web(query):
    import webbrowser
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searching for {query} on the web"

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
