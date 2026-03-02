# Hybrid RAG (Retrieval-Augmented Generation)

A hybrid retrieval-augmented generation system that combines **dense retrieval**
(ChromaDB + sentence-transformers), **sparse retrieval** (BM25), and a
**CrossEncoder reranker** to provide high-quality context to **GPT-4** for
answer generation. PDFs are ingested, chunked, and indexed automatically.

## Architecture

```
User (React) --> FastAPI --> Hybrid Retriever --> GPT-4 --> Answer
                               |
                    +----------+----------+
                    |                     |
              Dense (ChromaDB)     Sparse (BM25)
                    |                     |
                    +----------+----------+
                               |
                         CrossEncoder
                          Reranker
```

## Project Structure

```
hybrid_rag/
├── app.py                     # FastAPI entry point, routes, CORS
├── config.py                  # All configuration constants
├── requirements.txt           # Python dependencies
├── .env.example               # Template for environment variables
│
├── ingestion/                 # PDF ingestion pipeline
│   ├── pdf_parser.py          #   Extract text from PDFs (PyMuPDF)
│   ├── chunker.py             #   Split text into overlapping chunks
│   └── preprocessor.py        #   Clean and normalize text
│
├── retrieval/                 # Retrieval layer
│   ├── dense_retriever.py     #   Semantic search via ChromaDB
│   ├── sparse_retriever.py    #   Keyword search via BM25
│   ├── hybrid_retriever.py    #   Reciprocal Rank Fusion of both
│   └── reranker.py            #   CrossEncoder reranking
│
├── generation/                # Answer generation
│   ├── prompt_templates.py    #   System and user prompt templates
│   └── llm_client.py         #   OpenAI GPT-4 client wrapper
│
├── storage/                   # Persistence
│   └── vector_store.py        #   ChromaDB collection management
│
├── frontend/                  # React app (Vite + TypeScript)
│
└── tests/                     # Test suite
    ├── test_chunker.py
    ├── test_retrieval.py
    └── test_pipeline.py
```

## Quick Start

### Backend

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 4. Run the server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Opens at http://localhost:5173
```

## Configuration

All settings live in `config.py` and can be overridden via environment
variables in `.env`. Key settings:

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | (required) | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4` | LLM model to use |
| `EMBEDDING_MODEL_NAME` | `all-MiniLM-L6-v2` | Sentence-transformer model |
| `RERANKER_MODEL_NAME` | `cross-encoder/ms-marco-MiniLM-L-6-v2` | CrossEncoder model |
| `CHUNK_SIZE` | `512` | Characters per chunk |
| `CHUNK_OVERLAP` | `64` | Overlap between chunks |
| `TOP_K_FINAL` | `5` | Chunks sent to LLM |

## Tech Stack

- **Backend**: FastAPI + Uvicorn
- **Frontend**: React + Vite + TypeScript
- **Vector Store**: ChromaDB
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Sparse Retrieval**: rank-bm25
- **Reranker**: CrossEncoder (ms-marco-MiniLM-L-6-v2)
- **LLM**: OpenAI GPT-4
- **PDF Parsing**: PyMuPDF
