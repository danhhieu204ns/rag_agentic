from __future__ import annotations

from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


def build_faiss_vectorstore(documents: list[Document], embeddings) -> FAISS:
    """Tao FAISS vector store tu documents va embeddings.

    Input:
    - documents: Danh sach chunk Document.
    - embeddings: Embedding object co the embed_documents/embed_query.

    Output:
    - Doi tuong FAISS da index xong.

    Logic:
    - Goi FAISS.from_documents de embedding va xay dung index.
    """
    return FAISS.from_documents(documents, embeddings)


def save_faiss_vectorstore(vectorstore: FAISS, index_dir: str | Path) -> None:
    """Luu FAISS index xuong dia.

    Input:
    - vectorstore: Doi tuong FAISS can luu.
    - index_dir: Thu muc dich de luu index.

    Output:
    - Khong tra ve gia tri; tao cap file index tren dia.

    Logic:
    - Tao thu muc neu chua ton tai.
    - Goi save_local cua vectorstore.
    """
    path = Path(index_dir)
    path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(path))


def load_faiss_vectorstore(
    index_dir: str | Path,
    embeddings,
    allow_dangerous_deserialization: bool = True,
) -> FAISS:
    """Tai FAISS index da luu truoc do.

    Input:
    - index_dir: Thu muc chua index FAISS.
    - embeddings: Embedding object dung de map vector query.
    - allow_dangerous_deserialization: Co cho phep deserialize pickle metadata hay khong.

    Output:
    - Doi tuong FAISS da duoc tai len.

    Logic:
    - Kiem tra thu muc index ton tai.
    - Goi FAISS.load_local voi embeddings va co bao mat tuong ung.
    """
    path = Path(index_dir)
    if not path.exists():
        raise FileNotFoundError(f"FAISS index directory does not exist: {path}")

    return FAISS.load_local(
        str(path),
        embeddings,
        allow_dangerous_deserialization=allow_dangerous_deserialization,
    )


def create_retriever(vectorstore: FAISS, k: int = 4):
    """Tao retriever tu FAISS vectorstore.

    Input:
    - vectorstore: Doi tuong FAISS da san sang retrieval.
    - k: So chunk truy van tra ve.

    Output:
    - Retriever object dung cho chain retrieval.

    Logic:
    - Goi as_retriever voi search_kwargs de co top-k mong muon.
    """
    return vectorstore.as_retriever(search_kwargs={"k": k})
