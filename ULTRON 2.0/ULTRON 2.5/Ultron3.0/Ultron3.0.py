from voice_input import listen
from nlp_engine import understand
import action_engine as act
from voice_output import speak
from raw_engine import execute_raw
import speech_recognition as sr

authorized_users = ["Ali"]

def register_new_user():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Access restricted. Please state your name for registration.")
        audio = r.listen(source)
    
    try:
        new_name = r.recognize_google(audio).strip().capitalize()
        
        if new_name and new_name not in authorized_users:
            # Add to the active list in memory
            authorized_users.append(new_name)
            
            # Automatically update this script file to save the user permanently
            update_source_file(new_name)
            
            speak(f"User {new_name} has been successfully added to authorized users.")
        else:
            speak(f"Welcome back, {new_name}!")
            
    except Exception as e:
        speak("I couldn't understand the name. Please try again.")

def update_source_file(name):
    filename = "Ultron3.0.py"
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Look for the authorized_users list and inject the new name
    old_target = "authorized_users = ["
    new_replacement = f'authorized_users = [ ... , "{name}" ]' # Or dynamically modify the bracket contents
    
    # A cleaner approach is to find the exact line and rewrite it:
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("authorized_users ="):
            # Insert the new name right before the closing bracket
            updated_line = line.replace("]", f', "{name}"]')
            lines[i] = updated_line
            break
            
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

speak("ULTRON 3.0 online and ready. Hello! How can I assist you today?")

while True:
    command = listen()

    if not command:
        continue

    print("You said:", command)

    if "hello" in command:
        speak("Hello! How can I assist you today?")

    elif "exit" in command:
        speak("Alright. Goodbye.")
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

    elif "delete" in command:
        response = act.delete_words()
        speak(response)

    elif command.startswith("press ") or command.startswith("hold ") or command.startswith("release "):
        response = execute_raw(command)
        speak(response)

    elif "word" in command and "open" in command:
        speak(act.open_word())

    elif "search" in command:
        speak(act.search_web(query))
    
    else:
        # Fallback to NLP Intent Engine
        intent, target = understand(command)
        
        if intent == "open":
            speak(act.open_anything(target))
        elif intent == "close":
            speak(act.close_anything(target))
        elif intent == "minimize":
            speak(act.minimize_anything(target))
        elif intent == "maximize":
            speak(act.maximize_anything(target))
        elif intent == "write" or intent == "type":
            speak(act.write_anything(target))
        elif intent == "search":
            speak(act.search_web(target))
        elif intent == "remove":
            speak(act.remove_words(target, ["remove"]))
        else:
            speak("I didn't understand that command.")
