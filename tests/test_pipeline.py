"""
End-to-end pipeline tests: ingest -> retrieve -> generate.

HOW TO IMPLEMENT:
=================

Libraries: pytest, httpx, fastapi.testclient

Test cases to write:

1. test_health_endpoint:
   - Use TestClient(app) from fastapi.testclient
   - GET /health
   - Assert: status 200, body == {"status": "ok"}

2. test_upload_pdf:
   - Create a small test PDF (or use a fixture)
   - POST /upload with the PDF file
   - Assert: status 200, response contains "num_chunks" > 0

3. test_query_after_upload:
   - Upload a test PDF first
   - POST /query with {"question": "What is this document about?"}
   - Assert: status 200, response contains "answer" and "sources"

4. test_query_without_upload:
   - POST /query without uploading anything first
   - Assert: appropriate error or empty response

NOTES:
- Use pytest fixtures to share the TestClient across tests
- For test PDFs, you can create one programmatically with fitz (PyMuPDF):
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Test content here")
    doc.save("test.pdf")
- Mock the OpenAI API call in test_query_after_upload to avoid real API costs

Run: pytest tests/test_pipeline.py -v
"""
