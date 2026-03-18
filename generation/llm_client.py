"""LLM client module."""

# ------------------------------------------------------------------ #
# Step 1 — Imports
# Libraries: openai (from openai import OpenAI, APIError, RateLimitError)
# Config values needed: OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE,
#                       OPENAI_MAX_TOKENS from config.py
# Also import: build_messages from generation.prompt_templates
# ------------------------------------------------------------------ #

from generation.prompt_templates import build_messages, build_messages_with_history
from openai import OpenAI, APIError, RateLimitError
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS  


# ------------------------------------------------------------------ #
# Step 2 — class LLMClient
#
# __init__(self):
#   - Initialize the OpenAI client:
#     self.client = OpenAI(api_key=config.OPENAI_API_KEY)
# ------------------------------------------------------------------ #

class LLMClient:
    """Client for interacting with the OpenAI API."""
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)



# ------------------------------------------------------------------ #
# Step 3 — generate(self, question: str, context_chunks: list[dict]) -> str
#
# - Build messages: messages = build_messages(question, context_chunks)
# - Call the OpenAI API:
#     response = self.client.chat.completions.create(
#         model=OPENAI_MODEL,
#         messages=messages,
#         temperature=OPENAI_TEMPERATURE,
#         max_tokens=OPENAI_MAX_TOKENS,
#     )
# - Return: response.choices[0].message.content
# ------------------------------------------------------------------ #


    def generate(self, question: str, context_chunks: list[dict]) -> str:
        """Generate an answer from the LLM based on the question and context."""
        messages = build_messages(question, context_chunks)
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=OPENAI_TEMPERATURE,
                max_tokens=OPENAI_MAX_TOKENS,
            )
            return response.choices[0].message.content
        except APIError as e:
            return f"API error: {e}"
        except RateLimitError:
            return "Rate limit reached. Try again later."

    def generate_with_history(self, question: str, context_chunks: list[dict], history: list[dict]) -> str:
        """Generate an answer with prior conversation history for multi-turn context."""
        messages = build_messages_with_history(question, context_chunks, history)
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=OPENAI_TEMPERATURE,
                max_tokens=OPENAI_MAX_TOKENS,
            )
            return response.choices[0].message.content
        except APIError as e:
            return f"API error: {e}"
        except RateLimitError:
            return "Rate limit reached. Try again later."


# ------------------------------------------------------------------ #
# Notes
# - Use the openai v1+ SDK (client-based, not the old openai.ChatCompletion)
# - Token usage is at response.usage.total_tokens if you want to log costs
# - This module is called by app.py's /query endpoint after retrieval
# ------------------------------------------------------------------ #

