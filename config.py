"""
Central configuration for the Hybrid RAG application.

All tuneable constants are defined here. Secrets (API keys) are loaded
from environment variables via python-dotenv; everything else has a
sensible default that can be overridden.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # reads .env file in project root

# ── OpenAI ────────────────────────────────────────────────────
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))
OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "1024"))

# ── Embedding Model ──────────────────────────────────────────
EMBEDDING_MODEL_NAME: str = os.getenv(
    "EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2"
)

# ── Reranker (local CrossEncoder) ────────────────────────────
RERANKER_MODEL_NAME: str = os.getenv(
    "RERANKER_MODEL_NAME", "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

# ── ChromaDB ─────────────────────────────────────────────────
CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
CHROMA_COLLECTION_NAME: str = os.getenv(
    "CHROMA_COLLECTION_NAME", "hybrid_rag_docs"
)

# ── Chunking ─────────────────────────────────────────────────
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "512"))
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "64"))

# ── Retrieval ────────────────────────────────────────────────
TOP_K_DENSE: int = int(os.getenv("TOP_K_DENSE", "10"))
TOP_K_SPARSE: int = int(os.getenv("TOP_K_SPARSE", "10"))
TOP_K_FINAL: int = int(os.getenv("TOP_K_FINAL", "5"))
RRF_K: int = int(os.getenv("RRF_K", "60"))  # RRF constant

# ── FastAPI / Server ─────────────────────────────────────────
APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
CORS_ORIGINS: list[str] = os.getenv(
    "CORS_ORIGINS", "http://localhost:5173"  # Vite default
).split(",")

# ── Upload ───────────────────────────────────────────────────
UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
