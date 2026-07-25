from voice_input import listen
from nlp_engine import understand
import action_engine as act
from voice_output import speak
from raw_engine import execute_raw

speak("ULTRON 2.0 online and ready. Hello, Ali! How can I assist you today?")

while True:
    command = listen()

    if not command:
        continue

    print("You said:", command)

    if "hello" in command:
        speak("Hello, Ali! How can I assist you today?")
    
 
    elif "open" in command:
        intent, target = understand(command)
        if intent == "open":
            speak(act.open_anything(target))
        else:
            speak("I didn't understand that command.")

    elif "close" in command:
        intent, target = understand(command)
        if intent == "close":
            speak(act.close_anything(target))
        else:
            speak("I didn't understand that command.")

    elif "minimize" in command:
        intent, target = understand(command)
        if intent == "minimize":
            speak(act.minimize_anything(target))
        else:
            speak("I didn't understand that command.")

    elif "maximize" in command:
        intent, target = understand(command)
        if intent == "maximize":
            speak(act.maximize_anything(target))
        else:
            speak("I didn't understand that command.")

    elif "write" in command:
        intent, target = understand(command)
        if intent == "write":
            speak(act.write_anything(target))
        else:
            speak("I didn't understand that command.")
    elif "press" in command:
        response = execute_raw(command)
        speak(response)
    elif "delete" in command:
        response = act.delete_words()
        speak(response)

    elif "exit" in command:
        speak("Alright, Ali. Goodbye.")
        break

    elif "shut down" in command:
        speak("Shutting down the system. Farewell, Ali.")
        act.shutdown_system()
        break
    elif "restart" in command:
        speak("Restarting the system now.")
        act.restart_system()
        break
    elif "sleep" in command:
        speak("Putting the system to sleep.")
        act.sleep_system()
        break
    elif "screenshot" in command:
        speak(act.screenshot())
    
    elif "search" in command:
        intent, target = understand(command)
        if intent == "search":
            speak(act.search_web(target))
        else:
            speak("I didn't understand that command.")
    elif "remove" in command:
        intent, target = understand(command)
        if intent == "remove":
            speak(act.remove_words(target, ["remove"]))
    elif "word" in command:
        speak(act.open_word())
    elif "type" in command:
        response = act.open_application("Microsoft Word")
        speak(response)
        response = execute_raw(command)
        speak(response)
    else:
        speak("I didn't understand that command.")