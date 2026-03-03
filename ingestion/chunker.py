"""
Text chunking module.

HOW TO IMPLEMENT:
=================

Config values: CHUNK_SIZE, CHUNK_OVERLAP from config.py

1. Define a function: chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]
   - Use a sliding window approach:
     - Start at position 0
     - Take a slice of length chunk_size
     - Move forward by (chunk_size - chunk_overlap) characters
     - Repeat until you reach the end of the text
   - Return the list of chunk strings

2. Define: chunk_pages(pages: list[str], chunk_size: int, chunk_overlap: int) -> list[dict]
   - Join all pages into one string (or chunk per-page, your choice)
   - Call chunk_text() on the combined text
   - Return list of dicts: [{"text": "...", "chunk_id": 0, "metadata": {...}}, ...]
   - Include metadata like page number, character offset for source tracking

NOTES:
- Try to break at sentence boundaries when possible (find the nearest '.' or '\\n')
- chunk_size is in characters (512 default ≈ 100-130 tokens)
- chunk_overlap ensures context isn't lost between adjacent chunks
- This module is called after pdf_parser.py in the ingestion pipeline
"""


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
      """Chunk a single string of text into overlapping chunks."""
      chunks = []
      start = 0
      text_length = len(text)
   
      while start < text_length:
         end = min(start + chunk_size, text_length)
         chunk = text[start:end]
         chunks.append(chunk)
         start += (chunk_size - chunk_overlap)
   
      return chunks

def chunk_pages(pages: list[str], chunk_size: int, chunk_overlap: int) -> list[dict]:
      """Chunk a list of page texts into a list of chunk dicts with metadata."""
      all_text = "\n".join(pages)
      chunks = chunk_text(all_text, chunk_size, chunk_overlap)
      
      chunk_dicts = []
      char_offset = 0
      
      for i, chunk in enumerate(chunks):
         chunk_dicts.append({
               "text": chunk,
               "chunk_id": i,
               "metadata": {
                  "char_offset": char_offset
               }
         })
         char_offset += (chunk_size - chunk_overlap)
      
      return chunk_dicts

