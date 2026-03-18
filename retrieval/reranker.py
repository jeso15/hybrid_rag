"""Reranker module."""

# ------------------------------------------------------------------ #
# Step 1 — Imports
# Library: sentence_transformers
# Config values needed: RERANKER_MODEL_NAME, TOP_K_FINAL from config.py
# ------------------------------------------------------------------ #

from sentence_transformers import CrossEncoder
from config import RERANKER_MODEL_NAME, TOP_K_FINAL


# ------------------------------------------------------------------ #
# Step 2 — class Reranker
#
# __init__(self, model_name: str = RERANKER_MODEL_NAME):
#   - Load the CrossEncoder model: self.model = CrossEncoder(model_name)
#   - Note: first load downloads the model (~80MB for ms-marco-MiniLM-L-6-v2)
# ------------------------------------------------------------------ #

class Reranker:
    """Reranks candidate chunks using a CrossEncoder model."""

    def __init__(self, model_name: str = RERANKER_MODEL_NAME):
        self.model = CrossEncoder(model_name)

# ------------------------------------------------------------------ #
# Step 3 — rerank(self, query, candidates, top_k=TOP_K_FINAL) -> list[dict]
#
# - Build input pairs: [(query, candidate["text"]) for candidate in candidates]
# - Score all pairs:   scores = self.model.predict(pairs)
# - Attach scores to candidates and sort descending
# - Return top_k results
# ------------------------------------------------------------------ #

    def rerank(self, query, candidates, top_k=TOP_K_FINAL) -> list[dict]:
        """Rerank candidates based on relevance to the query."""
        if not candidates:
            return []

        # Build (query, text) pairs for the CrossEncoder
        pairs = []
        for c in candidates:
            pairs.append((query, c["text"]))

        # Score each pair
        scores = self.model.predict(pairs)

        # Attach scores back to each candidate
        scored = []
        for i, c in enumerate(candidates):
            result = dict(c)
            result["score"] = float(scores[i])
            scored.append(result)

        # Sort by score descending
        scored.sort(key=lambda x: x["score"], reverse=True)

        return scored[:top_k]


# ------------------------------------------------------------------ #
# Notes
# - CrossEncoder scores each (query, doc) pair independently — more
#   accurate than bi-encoder similarity but slower
# - Use on small candidate sets only (after RRF), not the full corpus
# - Model runs fully locally — no API key needed
# - For better quality (slower): "cross-encoder/ms-marco-TinyBERT-L-2-v2"
# ------------------------------------------------------------------ #
