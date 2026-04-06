# RAG Python Modules

This folder contains a modular Python implementation of the Naive RAG pipeline from the notebook.

## Structure

- `config.py`: Centralized runtime configuration.
- `loaders.py`: Document loaders (`.pdf`, `.txt`, `.md`).
- `splitter.py`: Chunking logic.
- `embeddings.py`: Embedding model builders and presets.
- `vectorstore.py`: FAISS create/save/load/retriever helpers.
- `llm.py`: Groq LLM builder.
- `chain.py`: RAG chain and source-aware chain.
- `evaluation.py`: RAGAS dataset and metrics helpers.
- `pipeline.py`: End-to-end orchestration class.
- `run_naive_rag.py`: CLI example for indexing and querying.

## Quick Run

Run from repository root:

```bash
python -m rag.run_naive_rag --data-path data/bao_cao.pdf --query "Ten de tai nay la gi?"
```

Make sure `GROQ_API_KEY` is set in your environment before running.

## CLI Parameters

The CLI entrypoint is in `run_naive_rag.py`.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--data-path` | string | `data/bao_cao.pdf` | Path to the input document for indexing. |
| `--query` | string | `Ten de tai nay la gi?` | User question sent to the RAG pipeline. |
| `--index-dir` | string | `faiss_index` | Directory used to save/load the FAISS index. |
| `--rebuild-index` | flag | `False` | Force a full rebuild from source documents instead of loading existing index. |
| `--no-save-index` | flag | `False` | Build index in memory only (skip saving index to disk). |
| `--embedding-model` | string | `AITeamVN/Vietnamese_Embedding_v2` | Embedding model name used by HuggingFace embeddings. |
| `--embedding-device` | string | `cpu` | Device for embedding inference (`cpu`, `cuda`, etc.). |
| `--max-seq-length` | int | `2048` | Maximum sequence length for embedding model backend (when supported). |
| `--llm-model` | string | `llama-3.3-70b-versatile` | Groq chat model used for answer generation. |
| `--temperature` | float | `0.0` | Sampling temperature for the LLM. |
| `--k` | int | `4` | Number of retrieved chunks per query. |

## Config Parameters (`NaiveRAGConfig`)

These fields are defined in `config.py` and used by `NaiveRAGPipeline`.

| Field | Default | Meaning |
| :--- | :--- | :--- |
| `data_path` | `data/bao_cao.pdf` | Source document path. |
| `chunk_size` | `500` | Chunk size for text splitting. |
| `chunk_overlap` | `50` | Overlap between adjacent chunks. |
| `embedding_provider` | `huggingface` | Embedding backend selector. |
| `embedding_model_name` | `AITeamVN/Vietnamese_Embedding_v2` | Model identifier for embeddings. |
| `embedding_device` | `cpu` | Device used by embedding model. |
| `embedding_max_seq_length` | `2048` | Max token/sequence length for embedding backend. |
| `faiss_index_dir` | `faiss_index` | Directory for persisted FAISS index. |
| `retriever_k` | `4` | Top-k chunks returned by retriever. |
| `llm_model` | `llama-3.3-70b-versatile` | Groq model name for generation. |
| `llm_temperature` | `0.0` | Generation temperature. |
| `prompt_template` | default prompt | Prompt template for RAG answer synthesis. |
| `allow_dangerous_deserialization` | `True` | Controls FAISS metadata deserialization behavior when loading local index. |

## Common Command Examples

Rebuild FAISS index from scratch:

```bash
python -m rag.run_naive_rag --data-path data/bao_cao.pdf --rebuild-index
```

Run with a different embedding model and top-k:

```bash
python -m rag.run_naive_rag --embedding-model sentence-transformers/all-MiniLM-L6-v2 --k 6
```

Run without persisting index files:

```bash
python -m rag.run_naive_rag --no-save-index
```
