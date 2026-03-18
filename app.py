"""Main entry point for the Hybrid RAG FastAPI application."""

import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import config
from config import CORS_ORIGINS, APP_HOST, APP_PORT, UPLOAD_DIR
from ingestion import pdf_parser, chunker, preprocessor
from ingestion import docx_parser
from retrieval.reranker import Reranker
from generation.llm_client import LLMClient
import threads.thread_store as thread_store

# ------------------------------------------------------------------ #
# App setup
# ------------------------------------------------------------------ #

@asynccontextmanager
async def lifespan(_app: FastAPI):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    yield

app = FastAPI(title="Hybrid RAG API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

# ------------------------------------------------------------------ #
# Global singletons (stateless — shared across all threads)
# ------------------------------------------------------------------ #

reranker = Reranker()
llm_client = LLMClient()


# ------------------------------------------------------------------ #
# Request / Response models
# ------------------------------------------------------------------ #

class QueryRequest(BaseModel):
    thread_id: str
    question: str


# ------------------------------------------------------------------ #
# Routes — health
# ------------------------------------------------------------------ #

@app.get("/health")
async def health_check():
    return {"status": "ok"}


# ------------------------------------------------------------------ #
# Routes — thread management
# ------------------------------------------------------------------ #

@app.post("/threads")
async def create_thread():
    """Create a new chat thread."""
    thread = thread_store.create_thread(reranker)
    return {
        "thread_id": thread["thread_id"],
        "title": thread["title"],
        "created_at": thread["created_at"],
    }


@app.get("/threads")
async def list_threads():
    """List all threads (newest first)."""
    return thread_store.list_threads()


@app.delete("/threads/{thread_id}")
async def delete_thread(thread_id: str):
    """Delete a thread and its documents."""
    deleted = thread_store.delete_thread(thread_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Thread not found.")
    return {"deleted": True}


# ------------------------------------------------------------------ #
# Routes — document upload (per thread)
# ------------------------------------------------------------------ #

@app.post("/threads/{thread_id}/upload")
async def upload_file(thread_id: str, file: UploadFile = File(...)):
    """Upload a PDF or Word document to a specific thread."""
    thread = thread_store.get_thread(thread_id)
    if thread is None:
        raise HTTPException(status_code=404, detail="Thread not found.")

    filename = file.filename.lower()
    if not (filename.endswith(".pdf") or filename.endswith(".docx")):
        raise HTTPException(status_code=400, detail="Only PDF and Word (.docx) files are supported.")

    # Save to disk
    dest_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(dest_path, "wb") as f:
        f.write(await file.read())

    # Parse based on file type
    if filename.endswith(".pdf"):
        pages = pdf_parser.parse_pdf(dest_path)
    else:
        pages = docx_parser.parse_docx(dest_path)

    # Chunk and preprocess
    raw_chunks = chunker.chunk_pages(pages, config.CHUNK_SIZE, config.CHUNK_OVERLAP)

    for chunk in raw_chunks:
        chunk["chunk_id"] = thread["next_chunk_id"]
        chunk.setdefault("metadata", {})
        chunk["metadata"]["source_file"] = file.filename
        thread["next_chunk_id"] += 1

    cleaned_chunks = preprocessor.preprocess_chunks(raw_chunks)
    thread["corpus_chunks"] += cleaned_chunks

    # Index into this thread's vector store and BM25
    thread["vector_store"].add_documents(cleaned_chunks)
    thread["sparse_retriever"].index(thread["corpus_chunks"])

    # Track file for this thread
    thread_store.add_file(thread_id, file.filename, dest_path)

    return {"message": "Ingestion complete", "num_chunks": len(cleaned_chunks)}


# ------------------------------------------------------------------ #
# Routes — file listing and download (per thread)
# ------------------------------------------------------------------ #

@app.get("/threads/{thread_id}/files")
async def list_files(thread_id: str):
    """List all uploaded files for a thread."""
    if thread_store.get_thread(thread_id) is None:
        raise HTTPException(status_code=404, detail="Thread not found.")
    return thread_store.list_files(thread_id)


@app.get("/files/{filename}")
async def download_file(filename: str):
    """Download an uploaded file by filename."""
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(path=file_path, filename=filename)


# ------------------------------------------------------------------ #
# Routes — query (per thread, with history)
# ------------------------------------------------------------------ #

@app.post("/query")
async def query_rag(body: QueryRequest):
    """Retrieve relevant chunks and generate an answer within a thread."""
    thread = thread_store.get_thread(body.thread_id)
    if thread is None:
        raise HTTPException(status_code=404, detail="Thread not found.")

    if thread["vector_store"].get_count() == 0:
        raise HTTPException(status_code=400, detail="No documents ingested yet. Please upload a file first.")

    # Set thread title from first question
    thread_store.set_title(body.thread_id, body.question)

    # Retrieve and generate
    candidates = thread["hybrid_retriever"].retrieve(body.question, top_k_final=config.TOP_K_FINAL)
    answer = llm_client.generate_with_history(body.question, candidates, thread["history"])

    # Save turns to history
    thread_store.append_history(body.thread_id, "user", body.question)
    thread_store.append_history(body.thread_id, "assistant", answer)

    sources = []
    for c in candidates:
        sources.append({
            "text": c.get("text"),
            "metadata": c.get("metadata", {}),
            "score": c.get("score"),
        })

    return {
        "answer": answer,
        "sources": sources,
        "thread_id": body.thread_id,
    }


# ------------------------------------------------------------------ #
# Entry point
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    uvicorn.run("app:app", host=APP_HOST, port=APP_PORT, reload=True)
