"""
Sparse retrieval module (BM25).

HOW TO IMPLEMENT:
=================

Library: rank_bm25 (from rank_bm25 import BM25Okapi)
Config values: TOP_K_SPARSE from config.py

1. Define a class: SparseRetriever
   - __init__(self):
     - self.bm25 = None
     - self.documents = []  # store the original chunk dicts

   - index(self, chunks: list[dict]):
     - Tokenize each chunk's text: text.lower().split() (simple whitespace tokenization)
     - Create BM25 index: self.bm25 = BM25Okapi(tokenized_corpus)
     - Store the original chunks for retrieval

   - retrieve(self, query: str, top_k: int = TOP_K_SPARSE) -> list[dict]:
     - Tokenize the query: query.lower().split()
     - Get scores: self.bm25.get_scores(tokenized_query)
     - Get top-k indices using np.argsort(scores)[::-1][:top_k]
     - Return list of dicts: [{"text": "...", "score": 0.85, "metadata": {...}}, ...]

NOTES:
- BM25 index lives in memory — it needs to be rebuilt when new documents are added
- For production, consider persisting the tokenized corpus to disk
- Tokenization here is intentionally simple; for better results you could use
  nltk.word_tokenize() but the simple split works well enough for most cases
- The SparseRetriever is used by hybrid_retriever.py alongside the dense retriever
"""

from rank_bm25 import BM25Okapi
from config import TOP_K_SPARSE
import numpy as np

class SparseRetriever:
    """Implements BM25 retrieval over the chunk corpus."""

    def __init__(self):
        self.bm25 = None
        self.documents = [] #store the original chunk dicts

    def index(self, chunks: list[dict]):
        """Build BM25 index from chunk texts."""
        if not chunks:
            return
        self.documents = chunks
        tokenized_corpus = [chunk["text"].lower().split() for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def retrieve(self, query: str, top_k: int = TOP_K_SPARSE) -> list[dict]:
        """Return top_k chunks matching the query."""
        if self.bm25 is None or not query:
            return []
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [
            {
                "text": self.documents[i]["text"],
                "score": float(scores[i]),
                "metadata": self.documents[i].get("metadata", {})
            }
            for i in top_indices
        ]