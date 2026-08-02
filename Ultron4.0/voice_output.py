import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    
    voices = engine.getProperty('voices')
    
    for voice in voices:
        if "David" in voice.name:
            engine.setProperty('voice', voice.id)
            break
            
    engine.say(text)
    engine.runAndWait()
