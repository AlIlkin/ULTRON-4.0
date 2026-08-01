from faster_whisper import WhisperModel
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os


# Load Whisper model
# Options: tiny, base, small, medium, large-v3
# small = good balance for assistants
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


def record_audio(duration=3, samplerate=16000):
    """
    Records microphone audio and saves it temporarily.
    """

    print("🎙️ Listening... Speak now")

    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    wav.write(
        temp_file.name,
        samplerate,
        audio
    )

    return temp_file.name

def clean_command(text):
    fillers = [
        "um",
        "uh",
        "hmm",
        "please"
    ]

    for word in fillers:
        text = text.replace(word, "")

    return text.strip().rstrip(".!?,")

def listen():

    audio_file = record_audio()

    try:
        segments, info = model.transcribe(
            audio_file,
            language="en",
            condition_on_previous_text=False,
            vad_filter=True
        )

        text = ""

        for segment in segments:
            text += segment.text

        text = text.strip().lower()

        text = text.rstrip(".!?,")

        print("Action: in process -", text)

        return text


    except Exception as e:
        print("❌ Whisper Error:", e)
        return ""


    finally:
        if os.path.exists(audio_file):
            os.remove(audio_file)