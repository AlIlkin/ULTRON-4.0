from datetime import datetime
import os
from time import time

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





speak("ULTRON 4.0 online and ready. Hello. How can I assist you today?")


while True:

    try:

        command = listen()


        if not command:
            continue


        command = command.lower()

        print(f"{ANSI_RED}You said:{ANSI_RESET} {command}")



        if "hello" in command:

            speak("Hello. How can I assist you?")


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



        elif "who are you" in command:

            speak("I am ULTRON 4.0, your personal AI assistant.")

        elif "thank you" in command or "thanks" in command:

            speak("You're welcome. Do you need any further assistance?")

        elif "delete" in command:
            response = act.delete_words()
            speak(response)


        elif "shutdown after" in command or "shut down in" in command:
            try:
                words = command.split()
                minutes = None
                for word in words:
                    if word.isdigit():
                        minutes = int(word)
                        break
                if minutes is None:
                    speak("Please specify the time in minutes.")
                else:
                    shutdown_after(minutes)
                    speak(f"Shutting down after {minutes} minutes.")
            except Exception:
                speak("Please specify the time in minutes.")


        elif "shutdown" in command:

            shutdown_end_time = time.time() + 10
            speak("Shutting down in 10 seconds.")


        elif "restart" in command:

            speak("Restarting the system.")

            act.restart_system()
            break

        elif "sleep" in command:
            
            speak("Putting the system to sleep.")

            act.sleep_system()
            break



        # SCREENSHOT

        elif "screenshot" in command:

            speak("act.screenshot()")

        elif "what time is it" in command or "current time" in command:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            print(f"The current time is {current_time}.")
            speak(f"The current time is {current_time}.")

        elif (
            "coordinates" in command
            or "latitude" in command
            or "longitude" in command
        ):
            location = None
            if " in " in command:
                location = command.split(" in ", 1)[1].strip()
            elif "for " in command:
                location = command.split("for ", 1)[1].strip()
            if not location:
                speak("Please tell me the location for the coordinates.")
            else:
                response = act.write_weather_coordinates(location)
                speak(response)

        elif "weather" in command:
            location = None
            if " in " in command:
                location = command.split(" in ", 1)[1].strip()
            print(act.get_weather(location))
            speak(act.get_weather(location))

        # RAW KEYBOARD COMMANDS

        elif (
            command.startswith("press ")
            or command.startswith("hold ")
            or command.startswith("release ")
        ):

            response = execute_raw(command)
            speak(response)




        elif command.startswith("open "):

            target = command.replace("open", "", 1).strip()


            speak(act.open_anything(target))

        elif "play chess" in command:
            
            speak("Opening chess.com in your default web browser.")
            os.system("start https://www.chess.com")

        elif "youtube" in command:

            speak("Opening YouTube in your default web browser.")
            os.system("start https://www.youtube.com")

        elif "instagram" in command:

            speak("Opening Instagram in your default web browser.")
            os.system("start https://www.instagram.com")

        elif "facebook" in command:

            speak("Opening Facebook in your default web browser.")
            os.system("start https://www.facebook.com")

        elif "snapchat" in command:
            speak("Opening Snapchat in your default web browser.")
            os.system("start https://www.snapchat.com")


        elif command.startswith("close "):

            target = command.replace("close", "", 1).strip()
            speak(act.close_system_application(target))

        elif "notification" in command or "notifications" in command:
            
            speak("Opening the notification center.")
            act.check_notification()

        elif "settings" in command or "open settings" in command:
            
            speak("Opening the settings menu.")
            act.open_settings()

        elif command.startswith("search "):

            query = command.replace("search", "" , 1).strip()


            speak(act.search_web(query))


        elif "guessing game" in command or "number guess" in command or "play game" in command:
            speak("Launching the number guessing game.")
            print("\nStarting Number Guessing Game...")
            os.system("java Main")

        elif "convert temperature" in command or "temperature converter" in command:
            speak("Launching your Temperature Converter.")
            print("\nStarting Temperature Converter...")
            os.system("TempConvert.exe")


        elif "open word" in command:

            speak("act.open_word()")

        elif "cancel shutdown" in command or "cancel shut down" in command or "cancel power off" in command:

            cancel_shutdown()


        


        else:

            intent, target = understand(command)


            if intent == "open":

                speak(act.open_anything(target))


            elif intent == "close":

                speak(act.close_anything(target))


            elif intent == "minimize":

                speak(act.minimize_anything(target))


            elif intent == "maximize":

                speak(act.maximize_anything(target))


            elif intent in ["write","type"]:

                speak(act.write_anything(target))


            elif intent == "search":

                speak(act.search_web(target))


            elif intent == "remove":

                speak(act.remove_words(target,["remove"]))


            else:

                speak("I didn't understand that command.")


    except Exception as e:

        print(f"{ANSI_RED}ULTRON ERROR:{ANSI_RESET} {e}")

        speak("An error occurred while processing your request.")