import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    
    # Fetch all available system voices
    voices = engine.getProperty('voices')
    
    # Search for Microsoft David
    for voice in voices:
        if "David" in voice.name:
            engine.setProperty('voice', voice.id)
            break
            
    engine.say(text)
    engine.runAndWait()
