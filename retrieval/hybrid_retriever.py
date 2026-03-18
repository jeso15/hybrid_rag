"""Hybrid retrieval module."""

# ------------------------------------------------------------------ #
# Step 1 — Imports
# Config values needed: TOP_K_DENSE, TOP_K_SPARSE, TOP_K_FINAL, RRF_K
# ------------------------------------------------------------------ #

from retrieval.dense_retriever import DenseRetriever
from retrieval.sparse_retriever import SparseRetriever
from config import TOP_K_DENSE, TOP_K_SPARSE, TOP_K_FINAL, RRF_K


# ------------------------------------------------------------------ #
# Step 2 — reciprocal_rank_fusion(dense_results, sparse_results, k=RRF_K)
#
# RRF formula: score(doc) = sum( 1 / (k + rank) ) across all result lists
# - For each result list, assign rank starting from 1
# - Use chunk_id (or a text hash) as the unique document key
# - Merge scores for documents that appear in both lists
# - Sort by fused score descending and return
#
# Example:
#   fused_scores = {}
#   for rank, result in enumerate(dense_results, start=1):
#       doc_id = result["chunk_id"]
#       fused_scores[doc_id] = fused_scores.get(doc_id, 0) + 1 / (k + rank)
#   for rank, result in enumerate(sparse_results, start=1):
#       doc_id = result["chunk_id"]
#       fused_scores[doc_id] = fused_scores.get(doc_id, 0) + 1 / (k + rank)
# ------------------------------------------------------------------ #

def reciprocal_rank_fusion(dense_results, sparse_results, k=RRF_K):
    """Fuse dense and sparse results using Reciprocal Rank Fusion."""
    def _doc_id(result):
        return str(result.get("chunk_id") or result.get("metadata", {}).get("chunk_id", result["text"][:64]))

    fused_scores = {}
    doc_lookup = {}
    for rank, result in enumerate(dense_results, start=1):
        doc_id = _doc_id(result)
        fused_scores[doc_id] = fused_scores.get(doc_id, 0) + 1 / (k + rank)
        doc_lookup[doc_id] = result
    for rank, result in enumerate(sparse_results, start=1):
        doc_id = _doc_id(result)
        fused_scores[doc_id] = fused_scores.get(doc_id, 0) + 1 / (k + rank)
        doc_lookup.setdefault(doc_id, result)
    # Convert to list of dicts with text and metadata
    fused_results = []
    for doc_id, score in fused_scores.items():
        chunk_dict = doc_lookup.get(doc_id)
        if chunk_dict:
            fused_results.append({
                "text": chunk_dict["text"],
                "metadata": chunk_dict.get("metadata", {}),
                "score": score
            })
    # Sort by fused score descending
    fused_results.sort(key=lambda x: x["score"], reverse=True)
    return fused_results



# ------------------------------------------------------------------ #
# Step 3 — class HybridRetriever
#
# __init__(self, dense_retriever, sparse_retriever, reranker=None):
#   - Store references to dense_retriever, sparse_retriever, reranker
# ------------------------------------------------------------------ #

class HybridRetriever:
    """Combines dense and sparse retrieval with optional reranking."""

    def __init__(self, dense_retriever: DenseRetriever, sparse_retriever: SparseRetriever, reranker=None):
        self.dense = dense_retriever
        self.sparse = sparse_retriever
        self.reranker = reranker

# ------------------------------------------------------------------ #
# Step 4 — retrieve(self, query: str, top_k_final: int) -> list[dict]
#
# - Get dense results:  self.dense.retrieve(query, TOP_K_DENSE)
# - Get sparse results: self.sparse.retrieve(query, TOP_K_SPARSE)
# - Fuse with RRF:      fused = reciprocal_rank_fusion(dense, sparse)
# - Slice to top_k_final candidates
# - If reranker is set: candidates = self.reranker.rerank(query, candidates, top_k_final)
# - Return final candidates
# ------------------------------------------------------------------ #

    def retrieve(self, query: str, top_k_final: int = TOP_K_FINAL) -> list[dict]:
        """Retrieve and fuse results from dense and sparse retrievers."""
        dense_results = self.dense.retrieve(query, TOP_K_DENSE)
        sparse_results = self.sparse.retrieve(query, TOP_K_SPARSE)
        fused_results = reciprocal_rank_fusion(dense_results, sparse_results, k=RRF_K)
        top_candidates = fused_results[:top_k_final]
        if self.reranker:
            top_candidates = self.reranker.rerank(query, top_candidates, top_k_final)
        return top_candidates

# ------------------------------------------------------------------ #
# Notes
# - RRF is preferred over linear score combination because it does not
#   require normalizing scores from two different systems onto the same scale
# - RRF_K=60 is the standard constant from the original paper (Cormack et al.)
# - This is the core orchestration module — it ties together all retrieval components
# ------------------------------------------------------------------ #
