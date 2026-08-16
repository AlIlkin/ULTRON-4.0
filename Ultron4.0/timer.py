import os
import threading
import time
import action_engine as act
from voice_output import speak

shutdown_cancel_event = threading.Event()
active_shutdown_thread = None

def shutdown_after(minutes):
    global active_shutdown_thread
    shutdown_cancel_event.clear()
    
    total_seconds = int(minutes * 60)
    
    def countdown():
        elapsed = 0
        while elapsed < total_seconds:
            if shutdown_cancel_event.is_set():
                return
            
            remaining = total_seconds - elapsed
            mins, secs = divmod(remaining, 60)
            
            print(f"\rTime remaining before shutdown: {mins:02d}:{secs:02d}   ", end="", flush=True)
            
            time.sleep(1)
            elapsed += 1
            
        if not shutdown_cancel_event.is_set():
            print("\nTime is up. Shutting down the system.")
            speak("Time is up. Shutting down the system.")
            act.shutdown_system()

    active_shutdown_thread = threading.Thread(target=countdown)
    active_shutdown_thread.daemon = True
    active_shutdown_thread.start()
    speak(f"System will shut down in {minutes} minutes.")

def cancel_shutdown():
    shutdown_cancel_event.set()
    os.system("shutdown /a")
    print("\nShutdown has been cancelled.")
    speak("Shutdown has been cancelled.")
