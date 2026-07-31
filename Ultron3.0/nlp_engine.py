import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])

nlp = spacy.load("en_core_web_sm")

def understand(command):
    command = command.lower()
    
    if any(v in command for v in ["open", "launch", "start"]):
        target = command.replace("open", "").replace("launch", "").replace("start", "").strip()
        return "open", target

    if any(v in command for v in ["close", "exit", "quit"]):
        target = command.replace("close", "").replace("exit", "").replace("quit", "").strip()
        return "close", target

    if any(v in command for v in ["minimize", "hide"]):
        target = command.replace("minimize", "").replace("hide", "").strip()
        return "minimize", target

    if "maximize" in command:
        target = command.replace("maximize", "").strip()
        return "maximize", target

    if "write" in command or "type" in command:
        text = command.split("write")[-1].split("type")[-1].strip()
        return "write", text

    if "search" in command:
        target = command.replace("search", "").strip()
        return "search", target

    return None, None