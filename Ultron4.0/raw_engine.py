import subprocess
from click import command
import pyautogui
import os
import subprocess


def execute_raw(command):
    command = command.lower()

    if command.startswith("type "):
        text = command.replace("type ", "")
        pyautogui.write(text, interval=0.02)
        return "Typed."

    if command.startswith("press "):
        key = command.replace("press ", "")
        pyautogui.press(key)
        return f"Pressed {key}"

    if "close" in command:
        pyautogui.hotkey("alt", "f4")
        return "Closed window."

    if "minimize" in command:
        pyautogui.hotkey("win", "down")
        return "Minimized."

    if "maximize" in command:
        pyautogui.hotkey("win", "up")
        return "Maximized."
    
    if command.startswith("open "):
        app = command.replace("open ", "")
        os.system(f'start "" "{app}"')
        return f"Opening {app}"
    if command.startswith("hold "):
        key = command.replace("hold ", "")
        pyautogui.keyDown(key)
        return f"Holding {key}"
    if command.startswith("release "):
        key = command.replace("release ", "")
        pyautogui.keyUp(key)
        return f"Released {key}"

    return "Command executed."
