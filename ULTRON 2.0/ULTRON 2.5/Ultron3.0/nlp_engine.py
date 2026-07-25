import spacy

nlp = spacy.load("en_core_web_sm")

def understand(command):
    doc = nlp(command.lower())

    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    nouns = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]

    if any(v in verbs for v in ["open", "launch", "start"]):
        return "open", " ".join(nouns)

    if any(v in verbs for v in ["close", "exit", "quit"]):
        return "close", " ".join(nouns)

    if any(v in verbs for v in ["minimize", "hide"]):
        return "minimize", " ".join(nouns)

    if any(v in verbs for v in ["maximize"]):
        return "maximize", " ".join(nouns)

    if any(v in verbs for v in ["write", "type"]):
        text = command.lower().split("write")[-1].strip()
        return "write", text

    return None, None