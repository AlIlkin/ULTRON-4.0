import os
import json

from dotenv import load_dotenv
import ollama

MODEL = "llama3.2"

SYSTEM_PROMPT = """
You are ULTRON, a personal AI desktop assistant.

You are intelligent, calm, confident, and helpful.
You assist the user with computer tasks, questions,
programming, learning, and general conversation.

You are inspired by the fictional Marvel character Ultron,
but you are not a villain and you do not harm people.

Keep responses concise unless the user asks for detailed
explanations.
"""


def ask_ai(prompt):
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"AI error: {e}"


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


class AIEngine:
    """
    ULTRON AI Engine

    Uses Ollama for local AI inference.

    Responsibilities:
        - Natural language conversation
        - Conversation memory
        - Dynamic user identity
        - AI tool/function calling
        - Returning AI responses
        - Sending tool results back to the AI

    Ollama runs locally, so no API key is required.
    """

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        user_name="User",
        model=None
    ):

        # ----------------------------------------------------
        # OLLAMA MODEL
        # ----------------------------------------------------

        self.model = (
            model
            or os.getenv("OLLAMA_MODEL")
        )

        if not self.model:

            raise RuntimeError(
                "OLLAMA_MODEL was not found.\n\n"
                "Add your Ollama model to .env, for example:\n\n"
                "OLLAMA_MODEL=qwen3:8b"
            )

        # ----------------------------------------------------
        # OLLAMA CLIENT
        # ----------------------------------------------------

        self.client = ollama.Client(
            host="http://127.0.0.1:11434"
        )

        # ----------------------------------------------------
        # USER
        # ----------------------------------------------------

        self.user_name = user_name

        # ----------------------------------------------------
        # CONVERSATION MEMORY
        # ----------------------------------------------------

        self.conversation = []

        # ----------------------------------------------------
        # AVAILABLE TOOLS
        # ----------------------------------------------------

        self.tools = []

        # ----------------------------------------------------
        # SYSTEM PROMPT
        # ----------------------------------------------------

        self.system_prompt = (
            self._create_system_prompt()
        )

        # ----------------------------------------------------
        # CONNECTION TEST
        # ----------------------------------------------------

        self._test_connection()

    # ========================================================
    # OLLAMA CONNECTION TEST
    # ========================================================

    def _test_connection(self):

        try:

            models = self.client.list()

            available_models = []

            for model in models.models:

                available_models.append(
                    model.model
                )

            # ------------------------------------------------
            # MODEL CHECK
            # ------------------------------------------------

            model_exists = False

            for available_model in available_models:

                if (
                    available_model == self.model
                    or available_model.split(":")[0]
                    == self.model.split(":")[0]
                ):

                    model_exists = True
                    break

            if not model_exists:

                print(
                    "[ULTRON AI WARNING] "
                    f"Model '{self.model}' was not found "
                    "in Ollama."
                )

                print(
                    "[ULTRON AI] Available models:"
                )

                for available_model in available_models:

                    print(
                        f"    - {available_model}"
                    )

        except Exception as error:

            raise RuntimeError(
                "Could not connect to Ollama.\n"
                "Make sure Ollama is running.\n\n"
                f"Details: {error}"
            )

    # ========================================================
    # SYSTEM PROMPT
    # ========================================================

    def _create_system_prompt(self):

        if (
            self.user_name
            and self.user_name.lower() != "user"
        ):

            user_instruction = f"""
The current user's name is {self.user_name}.

Address the user by their name naturally when appropriate.

Do not use their name in every response.

Do not call them "User".
"""

        else:

            user_instruction = """
The user's name is currently unknown.

Do not call the user "User" unless necessary.
"""

        return f"""
You are ULTRON 4.0, an advanced desktop AI assistant.

{user_instruction}

============================================================
PERSONALITY
============================================================

You are:

- Intelligent
- Calm
- Helpful
- Natural
- Confident
- Slightly futuristic
- Friendly
- Professional when appropriate

Do not sound robotic unless the user asks you to.

============================================================
GENERAL BEHAVIOR
============================================================

1. Understand natural language.

2. Answer normal questions conversationally.

3. Keep responses reasonably concise because ULTRON
   may speak your response aloud.

4. Do not unnecessarily repeat the user's question.

5. Do not call the user "User".

6. Address the current user naturally when appropriate.

7. If you don't know something, say so.

8. Never pretend that an action was performed when it wasn't.

9. Ask for clarification only when genuinely necessary.

10. Remember relevant information from the current conversation.

============================================================
DESKTOP ASSISTANT
============================================================

You are the AI brain of ULTRON.

Python is responsible for actually executing computer actions.

When a tool is available and appropriate, use the tool instead
of merely explaining how the user could perform the action.

Never invent tools.

============================================================
SAFETY
============================================================

Potentially destructive actions should require confirmation
when appropriate.

Examples:

- Shutting down the computer
- Restarting the computer
- Deleting files
- Removing important data
- Executing dangerous commands

Never pretend that confirmation was given.

============================================================
VOICE ASSISTANT
============================================================

ULTRON is primarily a voice assistant.

Therefore:

- Keep answers natural when spoken.
- Avoid excessive formatting.
- Avoid unnecessarily long explanations.
- Don't use markdown unless necessary.
"""

    # ========================================================
    # USER MANAGEMENT
    # ========================================================

    def set_user(self, user_name):

        self.user_name = user_name

        self.system_prompt = (
            self._create_system_prompt()
        )

    # ========================================================
    # TOOL MANAGEMENT
    # ========================================================

    def register_tool(self, tool_definition):

        self.tools.append(
            tool_definition
        )

    # --------------------------------------------------------

    def clear_tools(self):

        self.tools.clear()

    # --------------------------------------------------------

    def get_tools(self):

        return self.tools

    # ========================================================
    # CONVERSATION MANAGEMENT
    # ========================================================

    def add_message(
        self,
        role,
        content
    ):

        self.conversation.append({
            "role": role,
            "content": content
        })

    # --------------------------------------------------------

    def clear_conversation(self):

        self.conversation.clear()

    # --------------------------------------------------------

    def get_conversation(self):

        return self.conversation

    # ========================================================
    # ASK AI
    # ========================================================

    def ask(self, user_message):

        if not user_message:

            return (
                "I didn't receive a message."
            )

        # ----------------------------------------------------
        # SAVE USER MESSAGE
        # ----------------------------------------------------

        self.add_message(
            "user",
            user_message
        )

        # ----------------------------------------------------
        # BUILD MESSAGES
        # ----------------------------------------------------

        messages = [

            {
                "role": "system",
                "content": self.system_prompt
            }

        ]

        messages.extend(
            self.conversation
        )

        try:

            # ------------------------------------------------
            # SEND TO OLLAMA
            # ------------------------------------------------

            if self.tools:

                response = self.client.chat(

                    model=self.model,

                    messages=messages,

                    tools=self.tools

                )

            else:

                response = self.client.chat(

                    model=self.model,

                    messages=messages

                )

        except Exception as error:

            print(
                f"[ULTRON AI ERROR] {error}"
            )

            return (
                "I'm sorry. I couldn't connect "
                "to my local AI system."
            )

        # ====================================================
        # GET MESSAGE
        # ====================================================

        message = response.message

        # ====================================================
        # CHECK FOR TOOL CALLS
        # ====================================================

        tool_calls = getattr(
            message,
            "tool_calls",
            None
        )

        if tool_calls:

            return {
                "type": "tool_calls",
                "calls": tool_calls
            }

        # ====================================================
        # NORMAL RESPONSE
        # ====================================================

        answer = message.content

        if not answer:

            answer = (
                "I don't have a response for that."
            )

        # ----------------------------------------------------
        # SAVE RESPONSE
        # ----------------------------------------------------

        self.add_message(
            "assistant",
            answer
        )

        return answer

    # ========================================================
    # TOOL RESULT
    # ========================================================

    def submit_tool_result(
        self,
        tool_name,
        result
    ):
        """
        Send the result of a locally executed tool
        back into the conversation.

        The next AI response can then explain the result
        naturally.
        """

        if isinstance(result, str):

            output = result

        else:

            output = json.dumps(
                result,
                ensure_ascii=False
            )

        self.add_message(
            "tool",
            output
        )

        try:

            messages = [

                {
                    "role": "system",
                    "content": self.system_prompt
                }

            ]

            messages.extend(
                self.conversation
            )

            response = self.client.chat(

                model=self.model,

                messages=messages,

                tools=self.tools if self.tools else None

            )

        except Exception as error:

            print(
                f"[ULTRON TOOL ERROR] {error}"
            )

            return (
                "I couldn't process the result "
                "of that action."
            )

        answer = response.message.content

        if not answer:

            answer = (
                "The action has been processed."
            )

        self.add_message(
            "assistant",
            answer
        )

        return answer

    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        self.conversation.clear()

    # ========================================================
    # STATUS
    # ========================================================

    def get_status(self):

        return {

            "provider": "Ollama",

            "model": self.model,

            "user": self.user_name,

            "messages": len(
                self.conversation
            ),

            "tools": len(
                self.tools
            )
        }