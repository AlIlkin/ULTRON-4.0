from voice_input import listen
from voice_output import speak
from nlp_engine import understand
import action_engine as act

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

    elif "exit" in command or "shutdown" in command:
        speak("Shutting down. Goodbye, Ali.")
        break

    else:
        speak("I did not understand that command.")
