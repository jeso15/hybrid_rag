"""In-memory thread store — manages per-thread retrieval state and chat history."""

import uuid
from datetime import datetime, timezone

from storage.vector_store import VectorStore
from retrieval.dense_retriever import DenseRetriever
from retrieval.sparse_retriever import SparseRetriever
from retrieval.hybrid_retriever import HybridRetriever


# Global dict keyed by thread_id
_threads: dict[str, dict] = {}


def create_thread(reranker) -> dict:
    """Create a new thread with its own vector store, BM25 index, and empty history."""
    thread_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    # Each thread gets its own ChromaDB collection
    vector_store = VectorStore(collection_name=f"thread_{thread_id}")
    sparse_retriever = SparseRetriever()
    dense_retriever = DenseRetriever(vector_store)
    hybrid_retriever = HybridRetriever(dense_retriever, sparse_retriever, reranker)

    thread = {
        "thread_id": thread_id,
        "title": "New Chat",
        "created_at": created_at,
        "corpus_chunks": [],
        "next_chunk_id": 0,
        "history": [],
        "files": [],  # list of {"filename": str, "path": str, "uploaded_at": str}
        "vector_store": vector_store,
        "sparse_retriever": sparse_retriever,
        "dense_retriever": dense_retriever,
        "hybrid_retriever": hybrid_retriever,
    }

    _threads[thread_id] = thread
    return thread


def get_thread(thread_id: str) -> dict | None:
    """Return thread by ID or None if not found."""
    return _threads.get(thread_id)


def list_threads() -> list[dict]:
    """Return lightweight metadata for all threads, newest first."""
    result = []
    for t in _threads.values():
        result.append({
            "thread_id": t["thread_id"],
            "title": t["title"],
            "created_at": t["created_at"],
        })
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return result


def delete_thread(thread_id: str) -> bool:
    """Delete a thread and its ChromaDB collection. Returns True if found."""
    thread = _threads.pop(thread_id, None)
    if thread is None:
        return False
    thread["vector_store"].delete_collection()
    return True


def append_history(thread_id: str, role: str, content: str) -> None:
    """Append a message turn to the thread's conversation history."""
    thread = _threads.get(thread_id)
    if thread is not None:
        thread["history"].append({"role": role, "content": content})


def set_title(thread_id: str, content: str) -> None:
    """Set the thread title from the first user message (truncated to 50 chars)."""
    thread = _threads.get(thread_id)
    if thread is not None and thread["title"] == "New Chat":
        thread["title"] = content[:50]


def add_file(thread_id: str, filename: str, path: str) -> None:
    """Record an uploaded file for a thread."""
    thread = _threads.get(thread_id)
    if thread is not None:
        uploaded_at = datetime.now(timezone.utc).isoformat()
        thread["files"].append({"filename": filename, "path": path, "uploaded_at": uploaded_at})


def list_files(thread_id: str) -> list[dict]:
    """Return uploaded file metadata for a thread."""
    thread = _threads.get(thread_id)
    if thread is None:
        return []
    return [{"filename": f["filename"], "uploaded_at": f["uploaded_at"]} for f in thread["files"]]
