"""
Text preprocessing module.

HOW TO IMPLEMENT:
=================

1. Define a function: clean_text(text: str) -> str
   - Collapse multiple whitespace/newlines into single spaces
   - Remove or replace special characters that aren't useful (e.g., \x00, \ufeff)
   - Strip leading/trailing whitespace
   - Optionally: normalize unicode (unicodedata.normalize("NFKD", text))

2. Define: preprocess_chunks(chunks: list[dict]) -> list[dict]
   - Apply clean_text() to each chunk's "text" field
   - Filter out chunks that are too short (e.g., < 20 characters)
   - Return the cleaned list of chunk dicts

NOTES:
- Do NOT lowercase the text — embeddings and BM25 both handle case naturally,
  and lowercasing destroys information (acronyms, proper nouns)
- Do NOT remove stopwords — modern embedding models handle them fine,
  and BM25 already downweights them via IDF
- Keep this module simple; heavy NLP preprocessing is usually counterproductive
  for modern retrieval systems
- This module is called after chunker.py in the ingestion pipeline
"""


def clean_text(text: str) -> str:
    """ clean a string of text by collapsing whitespace and removing special characters."""
    import re
    import unicodedata

    # Normalize unicode characters
    text = unicodedata.normalize("NFKD", text)

    # Remove special characters (except basic punctuation)
    text = re.sub(r"[^\w\s.,;:!?()\-]", " ", text)

    # Collapse multiple whitespace/newlines into single spaces
    text = re.sub(r"\s+", " ", text)

    # Strip leading/trailing whitespace
    return text.strip()

def preprocess_chunks(chunks: list[dict]) -> list[dict]:
    """preprocess a list of chunk dicts by cleaning the text and filtering out short chunks."""
    cleaned_chunks = []
    for chunk in chunks:
        cleaned_text = clean_text(chunk["text"])
        if len(cleaned_text) >= 20:  # Filter out chunks that are too short
            cleaned_chunks.append({
                "text": cleaned_text,
                "chunk_id": chunk["chunk_id"],
                "metadata": chunk["metadata"]
            })
    return cleaned_chunks