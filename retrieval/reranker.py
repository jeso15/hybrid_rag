"""
Reranker module.

HOW TO IMPLEMENT:
=================

Library: sentence_transformers (from sentence_transformers import CrossEncoder)
Config values: RERANKER_MODEL_NAME, TOP_K_FINAL from config.py

1. Define a class: Reranker
   - __init__(self, model_name: str = RERANKER_MODEL_NAME):
     - Load the CrossEncoder model:
       self.model = CrossEncoder(model_name)
     - Note: first load downloads the model (~80MB for ms-marco-MiniLM-L-6-v2)

   - rerank(self, query: str, candidates: list[dict], top_k: int = TOP_K_FINAL) -> list[dict]:
     - Create input pairs: [(query, candidate["text"]) for candidate in candidates]
     - Get scores: self.model.predict(pairs)
     - Attach scores to candidates
     - Sort by score descending
     - Return top_k results

NOTES:
- The CrossEncoder scores each (query, document) pair independently — this is
  more accurate than bi-encoder similarity but slower (hence used on a small
  candidate set, not the full corpus)
- Model: "cross-encoder/ms-marco-MiniLM-L-6-v2" is small and fast (~100ms
  for 10 candidates on CPU)
- For better quality at the cost of speed, consider "cross-encoder/ms-marco-TinyBERT-L-2-v2"
- No API key needed — everything runs locally
- This module is optionally called by hybrid_retriever.py after RRF fusion
"""
