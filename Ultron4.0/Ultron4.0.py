from datetime import datetime
import os
from asyncio import subprocess
from time import time
from voice_input import listen
from nlp_engine import understand
import action_engine as act
from voice_output import speak
from raw_engine import execute_raw
from timer import shutdown_after, cancel_shutdown





speak("ULTRON 4.0 online and ready. Hello. How can I assist you today?")




while True:

    try:

        command = listen()


        if not command:
            continue


        command = command.lower()

        print("You said:", command)



        if "hello" in command:

            speak("Hello. How can I assist you?")


        elif command in [
            "exit",
            "quit",
            "stop",
            "no thanks"
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

            speak(act.screenshot())

        elif "what time is it" in command or "current time" in command:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            print(f"The current time is {current_time}.")
            speak(f"The current time is {current_time}.")

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




        elif command.startswith("close "):

            target = command.replace("close", "", 1).strip()


            speak(act.close_anything(target))




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

            speak(act.open_word())

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

        print("ULTRON ERROR:",e)

        speak("An error occurred while processing your request.")
