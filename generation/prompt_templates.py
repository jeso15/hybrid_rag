"""
Prompt template module.

HOW TO IMPLEMENT:
=================

1. Define a SYSTEM_PROMPT string:
   - Tell the LLM it's a helpful assistant that answers questions based on
     provided context
   - Instruct it to only use information from the context, and say "I don't know"
     if the context doesn't contain the answer
   - Example:
     SYSTEM_PROMPT = '''You are a helpful assistant that answers questions based
     on the provided context. Only use information from the context below.
     If the context does not contain enough information to answer the question,
     say "I don't have enough information to answer that question."'''

2. Define a function: build_user_prompt(question: str, context_chunks: list[dict]) -> str
   - Format the retrieved chunks into a numbered context block:
     Context:
     [1] chunk_text_1
     [2] chunk_text_2
     ...
   - Append the user's question:
     Question: {question}
   - Return the formatted string

3. Optional: build_messages(question: str, context_chunks: list[dict]) -> list[dict]
   - Return the full messages list ready for the OpenAI API:
     [
       {"role": "system", "content": SYSTEM_PROMPT},
       {"role": "user", "content": build_user_prompt(question, context_chunks)}
     ]

NOTES:
- Keep prompts simple and explicit — complex prompt engineering rarely helps
- Including chunk numbers ([1], [2]) lets the LLM cite sources in its answer
- This module is used by llm_client.py to prepare the final prompt
"""
