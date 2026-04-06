from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    """Application settings resolved from environment variables."""

    app_name: str
    app_env: str
    base_dir: Path
    storage_dir: Path
    uploads_dir: Path
    index_dir: Path
    database_path: Path
    embedding_model_name: str
    embedding_device: str
    embedding_max_seq_length: int
    chunk_size: int
    chunk_overlap: int
    retriever_k: int
    llm_model: str
    llm_temperature: float



def _int_env(name: str, default: int) -> int:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    return int(raw_value)



def _float_env(name: str, default: float) -> float:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    return float(raw_value)



def get_settings() -> Settings:
    """Create immutable settings object from environment values."""

    base_dir = Path(__file__).resolve().parents[2]
    storage_dir = base_dir / "storage"
    uploads_dir = storage_dir / "uploads"
    index_dir = storage_dir / "indexes" / "global_faiss"

    storage_dir.mkdir(parents=True, exist_ok=True)
    uploads_dir.mkdir(parents=True, exist_ok=True)
    index_dir.parent.mkdir(parents=True, exist_ok=True)

    return Settings(
        app_name=os.getenv("APP_NAME", "RAG App Backend"),
        app_env=os.getenv("APP_ENV", "development"),
        base_dir=base_dir,
        storage_dir=storage_dir,
        uploads_dir=uploads_dir,
        index_dir=index_dir,
        database_path=storage_dir / "app.db",
        embedding_model_name=os.getenv(
            "EMBEDDING_MODEL_NAME", "AITeamVN/Vietnamese_Embedding_v2"
        ),
        embedding_device=os.getenv("EMBEDDING_DEVICE", "cpu"),
        embedding_max_seq_length=_int_env("EMBEDDING_MAX_SEQ_LENGTH", 2048),
        chunk_size=_int_env("CHUNK_SIZE", 500),
        chunk_overlap=_int_env("CHUNK_OVERLAP", 50),
        retriever_k=_int_env("RETRIEVER_K", 4),
        llm_model=os.getenv("LLM_MODEL", "llama-3.3-70b-versatile"),
        llm_temperature=_float_env("LLM_TEMPERATURE", 0.0),
    )


settings = get_settings()
