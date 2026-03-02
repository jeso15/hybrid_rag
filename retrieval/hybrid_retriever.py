"""
Hybrid retrieval module.

HOW TO IMPLEMENT:
=================

Config values: TOP_K_DENSE, TOP_K_SPARSE, TOP_K_FINAL, RRF_K from config.py

1. Define a function: reciprocal_rank_fusion(
       dense_results: list[dict],
       sparse_results: list[dict],
       k: int = RRF_K
   ) -> list[dict]:
   - RRF formula: score(doc) = sum( 1 / (k + rank) ) across all result lists
   - For each result list, assign rank starting from 1
   - Merge scores for documents appearing in both lists
   - Sort by fused score descending
   - Return top TOP_K_FINAL results

   Example RRF implementation:
     fused_scores = {}
     for rank, result in enumerate(dense_results, start=1):
         doc_id = result["chunk_id"]  # or use text hash as key
         fused_scores[doc_id] = fused_scores.get(doc_id, 0) + 1 / (k + rank)
     for rank, result in enumerate(sparse_results, start=1):
         doc_id = result["chunk_id"]
         fused_scores[doc_id] = fused_scores.get(doc_id, 0) + 1 / (k + rank)
     # Sort by score, return top results

2. Define a class: HybridRetriever
   - __init__(self, dense_retriever, sparse_retriever, reranker=None):
     - Store references to all three components

   - retrieve(self, query: str) -> list[dict]:
     - Get dense results: dense_retriever.retrieve(query, TOP_K_DENSE)
     - Get sparse results: sparse_retriever.retrieve(query, TOP_K_SPARSE)
     - Fuse with RRF: fused = reciprocal_rank_fusion(dense, sparse)
     - If reranker is provided: fused = reranker.rerank(query, fused)
     - Return top TOP_K_FINAL results

NOTES:
- RRF is preferred over linear score combination because it doesn't require
  normalizing scores from two different systems onto the same scale
- RRF_K=60 is the standard constant from the original paper (Cormack et al.)
- This is the core orchestration module — it ties together all retrieval components
"""
