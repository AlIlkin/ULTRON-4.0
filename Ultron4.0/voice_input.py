import os
import tempfile
import subprocess
import platform

# Try to import optional dependencies
try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    import sounddevice as sd
    import scipy.io.wavfile as wav
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

if WHISPER_AVAILABLE:
    model = WhisperModel(
        "small",
        device="cpu",
        compute_type="int8"
    )

def record_audio_advanced(duration=3, samplerate=16000):
    """
    Records microphone audio using sounddevice and scipy.
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

def record_audio_windows(duration=3):
    """
    Records audio using Windows built-in recorder via command line.
    """
    print("🎙️ Listening... Speak now")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_path = temp_file.name
    temp_file.close()
    
    try:
        # Use PowerShell to record audio
        script = f"""
        $audioFile = '{temp_path}'
        Add-Type -AssemblyName System.Speech
        $recorder = New-Object System.Media.SoundRecorder
        $recorder.Start()
        Start-Sleep -Seconds 3
        $recorder.Stop()
        """
        subprocess.run(["powershell", "-Command", script], check=False, timeout=10)
        return temp_path
    except Exception as e:
        print(f"Could not record audio: {e}")
        return None

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
    """
    Listens for user input. Uses Whisper if available, otherwise falls back to text input.
    """
    if WHISPER_AVAILABLE and AUDIO_AVAILABLE:
        try:
            audio_file = record_audio_advanced()
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

            if os.path.exists(audio_file):
                os.remove(audio_file)
                
            return text

        except Exception as e:
            print(f"❌ Whisper Error: {e}")
            return ""
    else:
        # Fallback: use text input
        print("🎙️ Listening... (text input mode - voice unavailable)")
        text = input("Enter command: ").strip().lower()
        return text.rstrip(".!?,") if text else ""