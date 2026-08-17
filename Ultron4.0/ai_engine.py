import os
import re
import json
from urllib import request, error


class LocalAIEngine:
    """A lightweight built-in conversational engine for the assistant."""

    def __init__(self):
        self.name = "ULTRON Local AI"

    def answer(self, prompt):
        cleaned_prompt = self._clean_prompt(prompt)
        if not cleaned_prompt:
            return "I can help explain things. Ask me about a topic or a question."

        if os.getenv("OPENAI_API_KEY"):
            try:
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful assistant. Answer clearly, briefly, and use plain language."
                        },
                        {
                            "role": "user",
                            "content": cleaned_prompt,
                        },
                    ],
                    "temperature": 0.7,
                }
                data = json.dumps(payload).encode("utf-8")
                req = request.Request(
                    "https://api.openai.com/v1/chat/completions",
                    data=data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                    },
                    method="POST",
                )
                with request.urlopen(req, timeout=20) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    if result.get("choices"):
                        return result["choices"][0]["message"]["content"].strip()
            except (error.URLError, error.HTTPError, TimeoutError, ValueError, KeyError):
                pass

        return self._build_local_response(cleaned_prompt)

    def explain_topic(self, topic):
        cleaned_topic = self._clean_topic(topic)
        if not cleaned_topic:
            return "Please tell me what you want explained."

        prompt = f"Explain the topic '{cleaned_topic}' in a clear, simple, and useful way."
        return self.answer(prompt)

    def _clean_prompt(self, prompt):
        if not prompt:
            return ""
        cleaned = prompt.strip().strip("?.,!:")
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned

    def _clean_topic(self, topic):
        if not topic:
            return ""
        cleaned = self._clean_prompt(topic)
        if cleaned.lower().startswith(("explain ", "tell me about ", "what is ", "describe ", "define ", "teach me about ")):
            cleaned = cleaned.split(" ", 1)[1]
        return cleaned.title() if cleaned else ""

    def _build_local_response(self, prompt):
        prompt_text = prompt.strip()
        lower_prompt = prompt_text.lower()

        if "what is" in lower_prompt or "define" in lower_prompt:
            topic = re.sub(r"^(what is|define)\s+", "", prompt_text, flags=re.IGNORECASE).strip(" ?")
            return (
                f"Definition: {topic} is a concept, idea, or thing that can be understood in simple terms. "
                f"In plain language, {topic} means something with a clear purpose, meaning, or set of features. "
                f"A simple example helps make {topic} easier to understand."
            )

        if "how" in lower_prompt or "works" in lower_prompt:
            topic = re.sub(r"^(how does|how do|how)\s+", "", prompt_text, flags=re.IGNORECASE).strip(" ?")
            return (
                f"How it works: {topic} is usually explained by breaking it into smaller steps. "
                f"First, you look at the main idea. Then, you connect it to a simple example. Finally, you see how it is used in real life."
            )

        if lower_prompt.startswith("explain the topic"):
            topic = prompt_text.replace("Explain the topic", "", 1).strip(" '"
)
            return (
                f"Definition: {topic} is a concept that can be explained in simple terms. "
                f"It has a clear meaning, a purpose, and often a practical example. "
                f"In short, {topic} becomes easier to understand when you describe it step by step."
            )

        return (
            f"Answer: {prompt_text}. "
            "I will respond in a simple, direct, and practical way so it is easy to follow."
        )


engine = LocalAIEngine()


def explain_topic(topic, prefer_api=True):
    return engine.explain_topic(topic)


def answer(prompt):
    return engine.answer(prompt)
