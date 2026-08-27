from datetime import datetime
import os
from time import time, sleep
from playsong import play_song
from radio import play_radio
from ultron_bootstrap import (
    ANSI_RED,
    ANSI_RESET,
    act,
    cancel_shutdown,
    execute_raw,
    listen,
    print_red_banner,
    shutdown_after,
    speak,
    understand,
)

from ai_engine import AIEngine

import sounddevice as sd
import numpy as np


# ============================================================
# CONFIGURATION
# ============================================================

DEVICE_INDEX = 1


# ============================================================
# AUDIO RECORDING
# ============================================================

def record_audio_clip(
    filename="temp_audio.wav",
    duration=5,
    samplerate=16000
):
    print("\n[ULTRON] Listening through Realtek Microphone...")

    try:
        sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype=np.int16,
            device=DEVICE_INDEX
        )

        sd.wait()

        return filename

    except Exception as e:
        print(f"[ULTRON ERROR] Recording failed: {e}")
        return None


# ============================================================
# AI ENGINE
# ============================================================

try:
    ai = AIEngine()

    print(
        f"{ANSI_RED}[ULTRON AI] AI Engine online.{ANSI_RESET}"
    )

except Exception as e:
    ai = None

    print(
        f"{ANSI_RED}"
        f"[ULTRON AI ERROR] Could not initialize AI Engine: {e}"
        f"{ANSI_RESET}"
    )


# ============================================================
# AI ASSISTANT
# ============================================================

def ask_ai(command):
    """
    Send a command to the AI engine.

    This is used only when ULTRON's normal command system
    cannot understand the user's request.
    """

    if ai is None:
        return "My AI assistant is currently unavailable."

    try:
        response = ai.ask(command)

        # Normal AI response
        if isinstance(response, str):
            return response

        # Tool calls will be handled here later.
        if isinstance(response, dict):
            if response.get("type") == "tool_calls":
                return (
                    "I understood your request, "
                    "but that action is not connected yet."
                )

        return "I couldn't generate a response."

    except Exception as e:
        print(
            f"{ANSI_RED}"
            f"[ULTRON AI ERROR] {e}"
            f"{ANSI_RESET}"
        )

        return (
            "I encountered an error while communicating "
            "with my AI system."
        )


# ============================================================
# STARTUP
# ============================================================

speak(
    "ULTRON 4.0 online and ready. "
    "Hello. How can I assist you today?"
)


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    try:

        # ----------------------------------------------------
        # LISTEN
        # ----------------------------------------------------

        command = listen()

        if not command:
            continue

        command = command.lower().strip()

        print(
            f"{ANSI_RED}You said:{ANSI_RESET} {command}"
        )


        # ====================================================
        # BASIC CONVERSATION
        # ====================================================

        if "hello" in command:

            speak("Hello. How can I assist you?")


        # ====================================================
        # EXIT
        # ====================================================

        elif command in [
            "exit",
            "quit",
            "stop",
            "no, thanks",
            "goodbye",
            "bye"
        ]:

            speak("Goodbye.")
            break


        # ====================================================
        # IDENTITY
        # ====================================================

        elif "who are you" in command:

            speak(
                "I am ULTRON 4.0, your personal AI assistant."
            )


        # ====================================================
        # THANK YOU
        # ====================================================

        elif (
            "thank you" in command
            or "thanks" in command
        ):

            speak(
                "You're welcome. "
                "Do you need any further assistance?"
            )


        # ====================================================
        # CREATOR
        # ====================================================

        elif (
            "who made you" in command
            or "who created you" in command
        ):

            speak(
                "I was created by AI and a developer "
                "named Ali Gurbanov."
            )

            print(
                f"{ANSI_RED}"
                "I was created by a developer named "
                "Ali Gurbanov."
                f"{ANSI_RESET}"
            )

            act.search_web("Ali Ilkinoglu")

            speak(
                "I have opened a search for "
                "Ali Ilkinoglu, the developer who created me."
            )


        # ====================================================
        # DELETE
        # ====================================================

        elif "delete" in command:

            response = act.delete_words()
            speak(response)


        # ====================================================
        # MUSIC
        # ====================================================

        elif "watch" in command or "sing" in command:

            play_song(command)


        # ====================================================
        # CAMERA
        # ====================================================

        elif (
            "take a photo" in command
            or "capture a photo" in command
            or "take a picture" in command
        ):

            from camera import take_photo

            photo_path = take_photo()

            if photo_path:
                print(
                    f"{ANSI_RED}"
                    f"Photo captured successfully and "
                    f"saved as '{photo_path}'!"
                    f"{ANSI_RESET}"
                )
            else:
                speak("Failed to capture photo.")


        # ====================================================
        # SHUTDOWN AFTER
        # ====================================================

        elif (
            "shutdown after" in command
            or "shut down in" in command
        ):

            try:

                words = command.split()
                minutes = None

                for word in words:
                    if word.isdigit():
                        minutes = int(word)
                        break

                if minutes is None:

                    speak(
                        "Please specify the time in minutes."
                    )

                else:

                    shutdown_after(minutes)

                    speak(
                        f"Shutting down after "
                        f"{minutes} minutes."
                    )

            except Exception:

                speak(
                    "Please specify the time in minutes."
                )


        # ====================================================
        # SHUTDOWN
        # ====================================================

        elif "shutdown" in command:

            shutdown_end_time = time() + 10

            speak("Shutting down in 10 seconds.")


        # ====================================================
        # RESTART
        # ====================================================

        elif "restart" in command:

            speak("Restarting the system.")

            act.restart_system()

            break


        # ====================================================
        # SLEEP
        # ====================================================

        elif "sleep" in command:

            speak("Putting the system to sleep.")

            act.sleep_system()

            break


        # ====================================================
        # SCREENSHOT
        # ====================================================

        elif "screenshot" in command:

            if "cut" in command:

                act.pyautogui.hotkey(
                    "win",
                    "shift",
                    "s"
                )

            elif "full" in command:

                speak(f"{act.screenshot()}")

            else:

                speak("Taking a full screenshot.")

                speak(f"{act.screenshot()}")


        # ====================================================
        # TIME
        # ====================================================

        elif (
            "what time is it" in command
            or "what is the time" in command
            or "current time" in command
            or "time in " in command
            or command.startswith("time ")
        ):

            if " in " in command:

                location = command.split(
                    " in ",
                    1
                )[1].strip()

                time_text = act.get_time(location)

                print(
                    f"{ANSI_RED}"
                    f"{time_text}"
                    f"{ANSI_RESET}"
                )

                speak(time_text)

            else:

                current_time = datetime.now().strftime("%H:%M")

                print(
                    f"The current time is "
                    f"{ANSI_RED}"
                    f"{current_time}"
                    f"{ANSI_RESET}."
                )

                speak(
                    f"The current time is {current_time}."
                )


        # ====================================================
        # COORDINATES
        # ====================================================

        elif (
            "coordinates" in command
            or "latitude" in command
            or "longitude" in command
        ):

            location = None

            if " in " in command:

                location = command.split(
                    " in ",
                    1
                )[1].strip()

            elif "for " in command:

                location = command.split(
                    "for ",
                    1
                )[1].strip()

            if not location:

                speak(
                    "Please tell me the location "
                    "for the coordinates."
                )

            else:

                response = act.write_weather_coordinates(
                    location
                )

                speak(response)


        # ====================================================
        # WEATHER
        # ====================================================

        elif "weather" in command:

            location = None

            if " in " in command:

                location = command.split(
                    " in ",
                    1
                )[1].strip()

            if (
                " tomorrow " in command
                or command.startswith("weather tomorrow")
            ):

                forecast_text = act.get_weather(
                    location,
                    forecast=True,
                    period="tomorrow"
                )

                print(
                    f"{ANSI_RED}"
                    f"{forecast_text}"
                    f"{ANSI_RESET}"
                )

                speak(forecast_text)

            elif (
                " weekly" in command
                or "this week" in command
            ):

                forecast_text = act.get_weather(
                    location,
                    forecast=True,
                    period="week"
                )

                print(
                    f"{ANSI_RED}"
                    f"{forecast_text}"
                    f"{ANSI_RESET}"
                )

                speak(forecast_text)

            elif (
                " this hour" in command
                or "hourly" in command
            ):

                forecast_text = act.get_weather(
                    location,
                    forecast=True,
                    period="hourly"
                )

                print(
                    f"{ANSI_RED}"
                    f"{forecast_text}"
                    f"{ANSI_RESET}"
                )

                speak(forecast_text)

            else:

                current_text = act.get_weather(location)

                print(
                    f"{ANSI_RED}"
                    f"{current_text}"
                    f"{ANSI_RESET}"
                )

                speak(current_text)


        # ====================================================
        # RAW KEYBOARD COMMANDS
        # ====================================================

        elif (
            command.startswith("press ")
            or command.startswith("hold ")
            or command.startswith("release ")
        ):

            response = execute_raw(command)

            speak(response)


        # ====================================================
        # OPEN
        # ====================================================

        elif command.startswith("open "):

            target = command.replace(
                "open",
                "",
                1
            ).strip()

            speak(act.open_anything(target))


        # ====================================================
        # CHESS
        # ====================================================

        elif "play chess" in command:

            speak("Opening chess.com.")

            os.system(
                "start https://www.chess.com"
            )


        # ====================================================
        # YOUTUBE
        # ====================================================

        elif "youtube" in command:

            speak("Opening YouTube.")

            os.system(
                "start https://www.youtube.com"
            )


        # ====================================================
        # INSTAGRAM
        # ====================================================

        elif "instagram" in command:

            speak("Opening Instagram.")

            os.system(
                "start https://www.instagram.com"
            )


        # ====================================================
        # FACEBOOK
        # ====================================================

        elif "facebook" in command:

            speak("Opening Facebook.")

            os.system(
                "start https://www.facebook.com"
            )


        # ====================================================
        # SNAPCHAT
        # ====================================================

        elif "snapchat" in command:

            speak("Opening Snapchat.")

            os.system(
                "start https://www.snapchat.com"
            )


        # ====================================================
        # RADIO
        # ====================================================

        elif (
            "radio" in command
            or "listen to radio" in command
        ):

            play_radio(
                speak,
                listen_func=listen
            )


        # ====================================================
        # CLOSE
        # ====================================================

        elif command.startswith("close "):

            target = command.replace(
                "close",
                "",
                1
            ).strip()

            speak(
                act.close_system_application(target)
            )


        # ====================================================
        # NOTIFICATIONS
        # ====================================================

        elif (
            "notification" in command
            or "notifications" in command
        ):

            speak(
                "Opening the notification center."
            )

            act.check_notification()


        # ====================================================
        # SETTINGS
        # ====================================================

        elif (
            "settings" in command
            or "open settings" in command
        ):

            speak(
                "Opening the settings menu."
            )

            act.open_settings()


        # ====================================================
        # SEARCH
        # ====================================================

        elif command.startswith("search "):

            query = command.replace(
                "search",
                "",
                1
            ).strip()

            speak(
                act.search_web(query)
            )


        # ====================================================
        # GUESSING GAME
        # ====================================================

        elif (
            "guessing game" in command
            or "number guess" in command
            or "play game" in command
        ):

            speak(
                "Launching the number guessing game."
            )

            print(
                "\nStarting Number Guessing Game..."
            )

            os.system("java Main")


        # ====================================================
        # TEMPERATURE CONVERTER
        # ====================================================

        elif (
            "convert temperature" in command
            or "temperature converter" in command
        ):

            speak(
                "Launching the Temperature Converter."
            )

            print(
                "\nStarting Temperature Converter..."
            )

            os.system("TempConvert.exe")


        # ====================================================
        # WORD
        # ====================================================

        elif "open word" in command:

            speak("Opening Microsoft Word.")

            speak(
                act.open_anything("word")
            )


        # ====================================================
        # CANCEL SHUTDOWN
        # ====================================================

        elif (
            "cancel shutdown" in command
            or "cancel shut down" in command
            or "cancel power off" in command
        ):

            cancel_shutdown()


        # ====================================================
        # EXISTING NLP ENGINE
        # ====================================================

        else:

            intent, target = understand(command)

            if intent == "open":

                speak(
                    act.open_anything(target)
                )

            elif intent == "close":

                speak(
                    act.close_anything(target)
                )

            elif intent == "minimize":

                speak(
                    act.minimize_anything(target)
                )

            elif intent == "maximize":

                speak(
                    act.maximize_anything(target)
                )

            elif intent in ["write", "type"]:

                speak(
                    act.write_anything(target)
                )

            elif intent == "search":

                speak(
                    act.search_web(target)
                )

            elif intent == "remove":

                speak(
                    act.remove_words(
                        target,
                        ["remove"]
                    )
                )

            # =================================================
            # AI FALLBACK
            # =================================================

            else:

                ai_response = ask_ai(command)

                print(
                    f"{ANSI_RED}"
                    f"ULTRON: {ai_response}"
                    f"{ANSI_RESET}"
                )

                speak(ai_response)


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        print(
            f"{ANSI_RED}"
            f"ULTRON ERROR:"
            f"{ANSI_RESET} {e}"
        )

        speak(
            "An error occurred while processing "
            "your request."
        )