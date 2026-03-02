"""
Tests for the ingestion.chunker module.

HOW TO IMPLEMENT:
=================

Library: pytest

Test cases to write:

1. test_chunk_text_basic:
   - Input: a known string of ~1000 characters, chunk_size=200, overlap=50
   - Assert: the number of chunks is correct (calculate expected count)
   - Assert: each chunk is <= chunk_size characters

2. test_chunk_text_overlap:
   - Input: a known string, chunk_size=100, overlap=30
   - Assert: the end of chunk N overlaps with the start of chunk N+1
   - Verify: chunk[i][-overlap:] == chunk[i+1][:overlap] (approximately)

3. test_chunk_text_short_input:
   - Input: a string shorter than chunk_size
   - Assert: returns exactly 1 chunk containing the full text

4. test_chunk_text_empty_input:
   - Input: empty string ""
   - Assert: returns an empty list (or a list with one empty chunk — decide your behavior)

5. test_chunk_pages:
   - Input: a list of page strings
   - Assert: returns list of dicts with "text", "chunk_id", "metadata" keys

Run: pytest tests/test_chunker.py -v
"""
