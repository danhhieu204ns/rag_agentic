from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DEFAULT_PROMPT_TEMPLATE = """
You are a helpful assistant that answers questions based on the provided context.
Use the provided context to answer the question.
Question: {input}
Context: {context}
Answer:
""".strip()


@dataclass(slots=True)
class NaiveRAGConfig:
    """Cau hinh tap trung cho Naive RAG pipeline.

    Input:
    - Cac truong cau hinh duong dan du lieu, tham so chunking, embedding, FAISS, LLM.

    Output:
    - Mot doi tuong config da duoc chuan hoa kieu du lieu (Path cho duong dan).

    Logic:
    - Gom toan bo gia tri mac dinh vao mot dataclass de de override va tai su dung.
    """

    data_path: Path = Path("data/bao_cao.pdf")
    chunk_size: int = 500
    chunk_overlap: int = 50

    # embedding_provider: str = "huggingface"
    # embedding_model_name: str = "AITeamVN/Vietnamese_Embedding_v2"
    embedding_provider: str = "gemini"
    embedding_model_name: str = "models/text-embedding-004"
    embedding_device: str = "cpu"
    embedding_max_seq_length: int = 2048

    faiss_index_dir: Path = Path("faiss_index")
    retriever_k: int = 4

    llm_model: str = "llama-3.3-70b-versatile"
    llm_temperature: float = 0.0
    prompt_template: str = DEFAULT_PROMPT_TEMPLATE

    allow_dangerous_deserialization: bool = True

    def __post_init__(self) -> None:
        """Chuan hoa cac truong duong dan sau khi khoi tao.

        Input:
        - Gia tri data_path va faiss_index_dir co the la str hoac Path.

        Output:
        - Khong tra ve gia tri; cap nhat truc tiep thuoc tinh thanh Path.

        Logic:
        - Ep kieu duong dan ve Path de dong bo khi thao tac file system.
        """
        self.data_path = Path(self.data_path)
        self.faiss_index_dir = Path(self.faiss_index_dir)
