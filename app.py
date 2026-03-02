"""
Main entry point for the Hybrid RAG FastAPI application.

HOW TO IMPLEMENT:
=================

1. Import FastAPI, CORSMiddleware, UploadFile, and File from fastapi.
2. Import config values from config.py (CORS_ORIGINS, APP_HOST, APP_PORT, UPLOAD_DIR).
3. Create a FastAPI app instance with title="Hybrid RAG API".

4. Add CORS middleware:
   - allow_origins = config.CORS_ORIGINS  (defaults to ["http://localhost:5173"])
   - allow_methods = ["*"]
   - allow_credentials = True
   - allow_headers = ["*"]

5. Create a startup event (or lifespan) to:
   - Ensure UPLOAD_DIR exists (os.makedirs)
   - Optionally pre-load the embedding model and reranker to avoid cold-start

6. Define these API routes:

   GET /health
     - Returns {"status": "ok"} for health checks

   POST /upload
     - Accepts a PDF file via UploadFile
     - Save to UPLOAD_DIR
     - Call ingestion pipeline: pdf_parser -> chunker -> preprocessor
     - Store chunks in vector store (storage.vector_store)
     - Build BM25 index (retrieval.sparse_retriever)
     - Return {"message": "...", "num_chunks": N}

   POST /query
     - Accepts JSON body: {"question": "..."}
     - Call hybrid_retriever.retrieve(question) to get top-k chunks
     - Call llm_client.generate(question, chunks) to get the answer
     - Return {"answer": "...", "sources": [...]}

7. Add an __main__ block:
   if __name__ == "__main__":
       import uvicorn
       uvicorn.run("app:app", host=config.APP_HOST, port=config.APP_PORT, reload=True)
"""
