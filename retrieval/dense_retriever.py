"""
Dense retrieval module.

HOW TO IMPLEMENT:
=================

Libraries: chromadb, sentence-transformers
Config values: EMBEDDING_MODEL_NAME, TOP_K_DENSE from config.py

1. Define a class: DenseRetriever
   - __init__(self, vector_store):
     - Store a reference to the vector_store (storage.vector_store) instance
     - The vector store already handles ChromaDB collection and embedding

   - retrieve(self, query: str, top_k: int) -> list[dict]:
     - Call vector_store.query(query, n_results=top_k)
     - Return list of dicts: [{"text": "...", "score": 0.95, "metadata": {...}}, ...]
     - ChromaDB returns distances; convert to similarity scores if needed
       (similarity = 1 / (1 + distance) for L2, or just use cosine)

NOTES:
- ChromaDB can compute embeddings internally if configured with a
  SentenceTransformerEmbeddingFunction, so you may not need to embed manually
- The DenseRetriever is used by hybrid_retriever.py alongside the sparse retriever
- Scores should be normalized to [0, 1] range for fair fusion with BM25
"""

from __future__ import annotations

from typing import Any, Dict, List


class DenseRetriever:
    """Calls the vector store for semantic search results."""

    def __init__(self, vector_store) -> None:
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Return top_k chunks from the vector store."""
        return self.vector_store.query(query, n_results=top_k)
    

    
