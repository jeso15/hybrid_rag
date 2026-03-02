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
