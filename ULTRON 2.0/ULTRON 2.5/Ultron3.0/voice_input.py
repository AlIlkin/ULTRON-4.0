import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("🎙️ Listening... Speak now")
        recognizer.adjust_for_ambient_noise(source, duration=1.0)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Action: in process - ", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError as e:
        print("❌ API error:", e)
        return ""
