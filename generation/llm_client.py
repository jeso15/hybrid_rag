"""
LLM client module.

HOW TO IMPLEMENT:
=================

Library: openai (from openai import OpenAI)
Config values: OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS from config.py

1. Define a class: LLMClient
   - __init__(self):
     - Initialize the OpenAI client: self.client = OpenAI(api_key=config.OPENAI_API_KEY)

   - generate(self, question: str, context_chunks: list[dict]) -> str:
     - Build messages using prompt_templates.build_messages(question, context_chunks)
     - Call the OpenAI API:
       response = self.client.chat.completions.create(
           model=config.OPENAI_MODEL,
           messages=messages,
           temperature=config.OPENAI_TEMPERATURE,
           max_tokens=config.OPENAI_MAX_TOKENS,
       )
     - Return: response.choices[0].message.content

NOTES:
- Use the openai v1+ SDK (the new client-based API, not the old openai.ChatCompletion)
- Handle API errors gracefully (openai.APIError, openai.RateLimitError)
- Consider adding retry logic with exponential backoff for rate limits
- Token usage is available at response.usage.total_tokens if you want to log costs
- This module is called by app.py's /query endpoint after retrieval
"""
