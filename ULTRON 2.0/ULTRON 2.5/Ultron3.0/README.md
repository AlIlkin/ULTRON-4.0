# ULTRON 2.5 / 3.0 — AI-Powered Desktop Voice Assistant

An advanced, modular desktop automation and voice assistant built in Python. Ultron combines speech recognition, text-to-speech synthesis, natural language understanding (`spaCy`), and system-level automation (`pyautogui`, `pyscreeze`) to give you hands-free control over your Windows environment.

---

## 🚀 Key Features

* **Voice Command Processing:** Listens to user voice inputs via microphone and executes mapped actions.
* **Text-to-Speech Engine:** Custom audio output supporting Windows SAPI5 system voices (e.g., Microsoft David).
* **Desktop Automation:** Capable of capturing screenshots, manipulating windows, typing text, and managing system states.
* **Natural Language Parsing:** Uses `spaCy` to process and understand user intents locally.
* **Isolated Environment:** Fully self-contained virtual environment configuration to avoid dependency conflicts.

---

## 📁 Project Structure

```text
Ultron3.0/
│
├── .venv/                  # Python Virtual Environment
├── Ultron3.0.py            # Main application entry point
├── action_engine.py        # System automation & pyautogui scripts
├── nlp_engine.py           # Natural language processing (spaCy)
├── voice_output.py         # Text-to-speech configuration (pyttsx3)
├── voice_input.py          # Microphone input & speech recognition
└── run_ultron.bat          # Standalone launcher batch script
```

---

## 🛠️ Prerequisites & Dependencies

Ensure you have **Python 3.12** installed on Windows. Ultron relies on several key Python packages:

* `spacy` — Natural language understanding
* `pyautogui` & `pyscreeze` — Screen capture and GUI automation
* `pyttsx3` — Offline text-to-speech synthesis
* `SpeechRecognition` & `PyAudio` — Microphone input and audio processing
* `pywin32` — Windows API integration

---

## ⚙️ Installation & Setup

1. **Clone or Open the Project Directory** in your terminal:
   ```powershell
   cd "c:\Users\alilk\OneDrive\Desktop\ULTRON 2.0\ULTRON 2.5\Ultron3.0\"
   ```

2. **Create and Activate the Virtual Environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install Required Dependencies**:
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install spacy pyautogui pyscreeze pillow pyttsx3 SpeechRecognition pyaudio pywin32
   ```

---

## 🚀 Running Ultron

### Method 1: Using the Standalone Batch Script (Recommended)
To run Ultron independently in its own dedicated window without needing VS Code:
1. Double-click the **`run_ultron.bat`** file located in your project folder.
2. The script will automatically activate the virtual environment and boot up Ultron.

### Method 2: Via PowerShell
If you prefer running it manually through your terminal:
```powershell
.\.venv\Scripts\python.exe "Ultron3.0.py"
```

---

## 🎙️ Customizing Voice Options
Ultron utilizes Windows SAPI5 voices. To configure a specific voice like **Microsoft David**, ensure the voice pack is installed via Windows Settings (`Time & Language` > `Speech`), and verify it in your `voice_output.py` configuration.
