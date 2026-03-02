"""
PDF text extraction module.

HOW TO IMPLEMENT:
=================

Library: pdfplumber (import pdfplumber)

1. Define a function: parse_pdf(file_path: str) -> list[str]
   - Open the PDF with pdfplumber.open(file_path) as a context manager:
     with pdfplumber.open(file_path) as pdf:
   - Iterate over each page: for page in pdf.pages
   - Extract text from each page: page.extract_text()
   - Return a list of strings, one per page

2. Optional: extract_pdf_metadata(file_path: str) -> dict
   - Use pdf.metadata to get title, author, creation date, etc.
   - Return as a dictionary

3. Optional: extract_tables(file_path: str) -> list[list[list[str]]]
   - Use page.extract_tables() to get structured table data
   - pdfplumber excels at table extraction compared to other PDF libraries
   - Returns a list of tables per page, each table is a list of rows

NOTES:
- pdfplumber.open() should be used as a context manager (with statement)
- page.extract_text() returns None for pages with no extractable text — handle this
  with: text = page.extract_text() or ""
- Consider adding page numbers to the returned data for source tracking
- pdfplumber is built on top of pdfminer.six and is great for both text and tables
- This module is called by app.py's /upload endpoint
"""


import pdfplumber

def parse_pdf(file_path: str) -> list[str]:
    """Extract text from a PDF file, returning a list of page texts."""
    page_texts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            page_texts.append(text)
    return page_texts


def extract_pdf_metadata(file_path: str) -> dict:
    """Extract metadata from a PDF file, returning a dictionary of metadata."""
    with pdfplumber.open(file_path) as pdf:
        return pdf.metadata


def extract_tables(file_path: str) -> list[list[list[str]]]:
    """Extract tables from a PDF file, returning a list of tables per page."""
    tables = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            tables.append(page_tables)
    return tables

