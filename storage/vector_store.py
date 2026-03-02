"""
Vector store module.

HOW TO IMPLEMENT:
=================

Library: chromadb
Config values: CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME, EMBEDDING_MODEL_NAME from config.py

1. Define a class: VectorStore
   - __init__(self):
     - Create a persistent ChromaDB client:
       self.client = chromadb.PersistentClient(path=config.CHROMA_PERSIST_DIR)
     - Set up the embedding function:
       from chromadb.utils import embedding_functions
       self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
           model_name=config.EMBEDDING_MODEL_NAME
       )
     - Get or create the collection:
       self.collection = self.client.get_or_create_collection(
           name=config.CHROMA_COLLECTION_NAME,
           embedding_function=self.embedding_fn,
           metadata={"hnsw:space": "cosine"}  # use cosine similarity
       )

   - add_documents(self, chunks: list[dict]):
     - Extract texts, ids, and metadatas from chunks
     - Call self.collection.add(
           documents=[c["text"] for c in chunks],
           ids=[str(c["chunk_id"]) for c in chunks],
           metadatas=[c.get("metadata", {}) for c in chunks]
       )
     - ChromaDB computes embeddings automatically via the embedding_function

   - query(self, query_text: str, n_results: int = 10) -> list[dict]:
     - Call results = self.collection.query(
           query_texts=[query_text],
           n_results=n_results
       )
     - Parse results into list of dicts:
       [{"text": doc, "score": dist, "metadata": meta}, ...]
     - Note: results["distances"][0] contains distance values;
       for cosine space, similarity = 1 - distance

   - get_count(self) -> int:
     - Return self.collection.count()

NOTES:
- ChromaDB handles embedding computation internally when an embedding_function
  is provided — no need to embed manually
- PersistentClient stores data at CHROMA_PERSIST_DIR (./chroma_data by default)
- The collection persists across restarts — data is not lost when the server stops
- "hnsw:space": "cosine" ensures cosine similarity is used (not L2 distance)
- This module is used by dense_retriever.py for querying and by app.py for indexing
"""
