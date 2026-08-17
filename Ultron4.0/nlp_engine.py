import re

# Try to import optional dependency
try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=False)
        nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    nlp = None

# Keyword patterns for command parsing (lightweight built-in NLP)
PATTERNS = {
    "open": {
        "keywords": ["open", "launch", "start"],
        "action": "open"
    },
    "close": {
        "keywords": ["close", "exit", "quit", "shut", "shutdown"],
        "action": "close"
    },
    "minimize": {
        "keywords": ["minimize", "hide", "minimize window"],
        "action": "minimize"
    },
    "maximize": {
        "keywords": ["maximize", "expand", "fullscreen"],
        "action": "maximize"
    },
    "write": {
        "keywords": ["write", "type", "input"],
        "action": "write"
    },
    "search": {
        "keywords": ["search", "find", "look for", "google"],
        "action": "search"
    },
    "screenshot": {
        "keywords": ["screenshot", "take screenshot", "snap", "capture"],
        "action": "screenshot"
    },
    "timer": {
        "keywords": ["timer", "set timer", "remind"],
        "action": "timer"
    },
    "weather": {
        "keywords": ["weather", "forecast"],
        "action": "weather"
    }
}

def understand_builtin(command):
    """Lightweight built-in NLP using regex and keyword matching."""
    command = command.lower().strip()
    
    # Try to match patterns
    for pattern_key, pattern_info in PATTERNS.items():
        for keyword in pattern_info["keywords"]:
            if keyword in command:
                action = pattern_info["action"]
                
                # Extract target/argument
                if action in ["open", "close", "minimize", "maximize", "search"]:
                    # Remove the keyword and get the remaining text
                    target = re.sub(r'\b(' + '|'.join(pattern_info["keywords"]) + r')\b', '', command).strip()
                    return action, target
                elif action in ["write", "type"]:
                    # Extract text after "write" or "type"
                    text = re.split(r'\b(write|type)\b', command)[-1].strip()
                    return action, text
                else:
                    return action, ""
    
    return None, None

def understand(command):
    """
    Understands user command using spacy if available, otherwise uses built-in pattern matching.
    """
    if SPACY_AVAILABLE and nlp:
        try:
            # Use spacy for advanced NLP
            doc = nlp(command.lower())
            # Original spacy-based logic can go here if needed
            # For now, we'll use the built-in matching as it's sufficient
            return understand_builtin(command)
        except Exception as e:
            print(f"Spacy error, falling back to built-in NLP: {e}")
            return understand_builtin(command)
    else:
        # Use built-in pattern matching
        return understand_builtin(command)