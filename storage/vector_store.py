"""ChromaDB-backed vector store."""

from __future__ import annotations

from typing import Any, Dict, List

import chromadb
from chromadb.utils import embedding_functions

import config


class VectorStore:
    """Thin wrapper around a persistent ChromaDB collection."""

    def __init__(self, collection_name: str = config.CHROMA_COLLECTION_NAME) -> None:
        # Persist embeddings on disk so they survive restarts
        self.client = chromadb.PersistentClient(path=config.CHROMA_PERSIST_DIR)

        # Embedding model used by Chroma to compute vectors
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=config.EMBEDDING_MODEL_NAME
        )

        # Main collection (creates if missing); cosine similarity space
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(self, chunks: List[Dict[str, Any]]) -> None:
        """Add chunk dicts; Chroma computes embeddings automatically."""
        if not chunks:
            return
        self.collection.add(
            documents=[c["text"] for c in chunks],
            ids=[str(c["chunk_id"]) for c in chunks],
            metadatas=[c.get("metadata", {}) for c in chunks],
        )

    def query(self, query_text: str, n_results: int = 10) -> List[Dict[str, Any]]:
        """Return top results with similarity scores and metadata."""
        n_results = min(n_results, self.collection.count())
        if n_results == 0:
            return []
        results = self.collection.query(query_texts=[query_text], n_results=n_results)
        docs = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        return [
            {
                "text": doc,
                "score": 1 - dist,  # cosine distance -> similarity
                "metadata": meta or {},
            }
            for doc, dist, meta in zip(docs, distances, metadatas)
        ]

    def get_count(self) -> int:
        """Number of stored documents."""
        return self.collection.count()

    def delete_collection(self) -> None:
        """Delete the underlying ChromaDB collection."""
        self.client.delete_collection(self.collection.name)
