"""
PDF text extraction module.

HOW TO IMPLEMENT:
=================

Library: PyMuPDF (import fitz)

1. Define a function: parse_pdf(file_path: str) -> list[str]
   - Open the PDF with fitz.open(file_path)
   - Iterate over each page: for page in doc
   - Extract text from each page: page.get_text()
   - Return a list of strings, one per page

2. Optional: extract_pdf_metadata(file_path: str) -> dict
   - Use doc.metadata to get title, author, creation date, etc.
   - Return as a dictionary

NOTES:
- PyMuPDF is imported as 'fitz' (historical naming)
- Handle empty pages gracefully (skip or return empty string)
- Consider adding page numbers to the returned data for source tracking
- This module is called by app.py's /upload endpoint
"""
