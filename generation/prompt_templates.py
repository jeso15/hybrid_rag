"""Prompt template module."""

# ------------------------------------------------------------------ #
# Step 1 — SYSTEM_PROMPT
# Tells the LLM to answer only from the provided context
# ------------------------------------------------------------------ #

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions based on the provided context. "
    "Only use information from the context below. "
    'If the context does not contain enough information to answer the question, '
    'say "I don\'t have enough information to answer that question."'
)


# ------------------------------------------------------------------ #
# Step 2 — build_user_prompt(question, context_chunks) -> str
# Formats chunks into a numbered context block + the question
# ------------------------------------------------------------------ #

def build_user_prompt(question: str, context_chunks: list[dict]) -> str:
    """Format retrieved chunks and question into a single prompt string."""
    lines = ["Context:"]

    for i, chunk in enumerate(context_chunks, start=1):
        lines.append(f"[{i}] {chunk['text']}")

    lines.append("")
    lines.append(f"Question: {question}")

    return "\n".join(lines)


# ------------------------------------------------------------------ #
# Step 3 — build_messages(question, context_chunks) -> list[dict]
# Returns the full messages list ready for the OpenAI API
# ------------------------------------------------------------------ #

def build_messages(question: str, context_chunks: list[dict]) -> list[dict]:
    """Build the messages list for the OpenAI chat API."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(question, context_chunks)},
    ]


# ------------------------------------------------------------------ #
# Step 4 — build_messages_with_history(question, context_chunks, history)
# Includes prior conversation turns for multi-turn context
# ------------------------------------------------------------------ #

def build_messages_with_history(question: str, context_chunks: list[dict], history: list[dict]) -> list[dict]:
    """Build messages list with prior conversation history for the OpenAI chat API."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Append all prior turns
    for turn in history:
        messages.append({"role": turn["role"], "content": turn["content"]})

    # Append current user question with context
    messages.append({"role": "user", "content": build_user_prompt(question, context_chunks)})

    return messages


# ------------------------------------------------------------------ #
# Notes
# - Keep prompts simple and explicit
# - Chunk numbers ([1], [2]) let the LLM cite sources in its answer
# - build_messages() is called by llm_client.py's generate() method
# - build_messages_with_history() is used for multi-turn conversations
# ------------------------------------------------------------------ #
