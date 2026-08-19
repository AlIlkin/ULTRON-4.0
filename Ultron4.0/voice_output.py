import subprocess
import platform
import os

# Try to import optional dependency
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

OS_NAME = platform.system()

def speak_with_pyttsx3(text):
    """Uses pyttsx3 for text-to-speech (if available)."""
    try:
        engine = pyttsx3.init()
        
        voices = engine.getProperty('voices')
        
        for voice in voices:
            if "David" in voice.name:
                engine.setProperty('voice', voice.id)
                break
                
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error with pyttsx3: {e}")
        return False
    return True

def speak_windows_builtin(text):
    """Uses Windows built-in text-to-speech via PowerShell."""
    try:
        # Use PowerShell to access Windows SAPI text-to-speech
        ps_script = f"""
        Add-Type -AssemblyName System.Speech
        $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
        $speak.Speak("{text.replace('"', '`"')}")
        """
        subprocess.run(["powershell", "-Command", ps_script], check=True, timeout=30)
        return True
    except Exception as e:
        print(f"Error with Windows TTS: {e}")
        return False

def speak_macos(text):
    """Uses macOS built-in text-to-speech."""
    try:
        subprocess.run(["say", text], check=True, timeout=30)
        return True
    except Exception as e:
        print(f"Error with macOS TTS: {e}")
        return False

def speak_linux(text):
    """Uses espeak for Linux text-to-speech."""
    try:
        subprocess.run(["espeak", text], check=True, timeout=30)
        return True
    except FileNotFoundError:
        print("espeak not found. Install with: sudo apt-get install espeak")
        return False
    except Exception as e:
        print(f"Error with Linux TTS: {e}")
        return False

def speak(text):
    """
    Speaks text using available text-to-speech engine.
    Tries pyttsx3 first, then falls back to OS-specific built-in options.
    """
    if PYTTSX3_AVAILABLE:
        if speak_with_pyttsx3(text):
            return
    
    # Fallback to OS-specific TTS
    if OS_NAME == "Windows":
        speak_windows_builtin(text)
    elif OS_NAME == "Darwin":
        speak_macos(text)
    elif OS_NAME == "Linux":
        speak_linux(text)
    else:
        # Ultimate fallback: just print
        print(f"[SPEAK] {text}")
