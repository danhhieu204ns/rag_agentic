from __future__ import annotations

from collections.abc import Iterable

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    documents: Iterable[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 0,
) -> list[Document]:
    """Chia danh sach Document thanh cac chunk nho.

    Input:
    - documents: Iterable cac Document can tach.
    - chunk_size: Kich thuoc toi da cua moi chunk.
    - chunk_overlap: So ky tu overlap giua 2 chunk lien tiep.

    Output:
    - Danh sach Document da duoc chunk hoa.

    Logic:
    - Tao RecursiveCharacterTextSplitter voi tham so chunking.
    - Chuyen iterable thanh list va thuc hien split_documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return text_splitter.split_documents(list(documents))
