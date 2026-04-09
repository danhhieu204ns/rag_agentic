from __future__ import annotations

from collections.abc import Iterable
from typing import Literal

from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter, Language, RecursiveCharacterTextSplitter


ChunkingMethod = Literal["recursive", "character", "markdown", "python"]

MARKDOWN_SEPARATORS = [
    "\n## ",
    "\n### ",
    "\n#### ",
    "\n- ",
    "\n* ",
    "\n",
    " ",
    "",
]


def _build_text_splitter(
    method: ChunkingMethod,
    chunk_size: int,
    chunk_overlap: int,
    separator: str,
):
    if method == "recursive":
        return RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    if method == "character":
        return CharacterTextSplitter(
            separator=separator,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    if method == "markdown":
        return RecursiveCharacterTextSplitter(
            separators=MARKDOWN_SEPARATORS,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    if method == "python":
        return RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    raise ValueError(
        f"Unsupported chunking method: {method}. "
        "Supported methods: recursive, character, markdown, python"
    )


def split_documents(
    documents: Iterable[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 0,
    method: ChunkingMethod = "recursive",
    separator: str = "\n\n",
) -> list[Document]:
    """Chia danh sach Document thanh cac chunk nho theo nhieu chien luoc.

    Input:
    - documents: Iterable cac Document can tach.
    - chunk_size: Kich thuoc toi da cua moi chunk.
    - chunk_overlap: So ky tu overlap giua 2 chunk lien tiep.
    - method: Chien luoc chunking (recursive, character, markdown, python).
    - separator: Ky tu tach khi method=character.

    Output:
    - Danh sach Document da duoc chunk hoa.

    Logic:
    - Tao text splitter theo method duoc chon.
    - Chuyen iterable thanh list va thuc hien split_documents.
    """
    text_splitter = _build_text_splitter(
        method=method,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separator=separator,
    )
    return text_splitter.split_documents(list(documents))
