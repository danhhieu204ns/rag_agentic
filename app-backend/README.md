# RAG App Backend (FastAPI)

## Features

- Document CRUD and upload API
- Embedding/chunking pipeline for uploaded documents
- Global FAISS index rebuild and retrieval
- Chat query endpoint with persistent chat memory

## Run

Install dependencies:

```bash
pip install -r app-backend/requirements.txt
```

Run server from repository root:

```bash
uvicorn app.main:app --reload --app-dir app-backend
```

Alternative: run from app-backend folder:

```bash
cd app-backend
uvicorn app.main:app --reload
```

## Environment

Required:

- `GROQ_API_KEY`: API key for answer generation.

Optional tuning:

- `EMBEDDING_PROVIDER` (`huggingface` or `gemini`)
- `EMBEDDING_MODEL_NAME`
- `EMBEDDING_DEVICE`
- `EMBEDDING_MAX_SEQ_LENGTH`
- `GEMINI_API_KEY` (or `GOOGLE_API_KEY` when using Gemini embeddings)
- `CHUNK_SIZE`
- `CHUNK_OVERLAP`
- `CHUNKING_METHOD` (`recursive`, `character`, `markdown`, `python`)
- `RETRIEVER_K`
- `LLM_MODEL`
- `LLM_TEMPERATURE`
