from __future__ import annotations

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


def _validate_file(file_path: Path) -> None:
    """Kiem tra file dau vao hop le truoc khi load.

    Input:
    - file_path: Duong dan file can kiem tra.

    Output:
    - Khong tra ve gia tri.

    Logic:
    - Nem FileNotFoundError neu file khong ton tai.
    - Nem ValueError neu duong dan khong phai file.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File does not exist: {file_path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")


def load_pdf_documents(file_path: str | Path) -> list[Document]:
    """Doc tai lieu PDF thanh danh sach Document.

    Input:
    - file_path: Duong dan den file PDF.

    Output:
    - Danh sach Document do PyPDFLoader tra ve.

    Logic:
    - Chuan hoa path, validate file, sau do load bang PyPDFLoader.
    """
    path = Path(file_path)
    _validate_file(path)
    return PyPDFLoader(str(path)).load()


def load_text_documents(file_path: str | Path, encoding: str = "utf-8") -> list[Document]:
    """Doc file text/markdown thanh danh sach Document.

    Input:
    - file_path: Duong dan file text.
    - encoding: Bang ma ky tu khi doc file.

    Output:
    - Danh sach Document do TextLoader tra ve.

    Logic:
    - Chuan hoa path, validate file, va load noi dung bang TextLoader.
    """
    path = Path(file_path)
    _validate_file(path)
    return TextLoader(str(path), encoding=encoding).load()


def load_documents(file_path: str | Path) -> list[Document]:
    """Router chon loader theo phan mo rong file.

    Input:
    - file_path: Duong dan toi tai lieu can nap.

    Output:
    - Danh sach Document da duoc parse.

    Logic:
    - Neu la .pdf thi goi load_pdf_documents.
    - Neu la .txt/.md thi goi load_text_documents.
    - Nem ValueError voi dinh dang chua ho tro.
    """
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return load_pdf_documents(path)
    if suffix in {".txt", ".md"}:
        return load_text_documents(path)

    raise ValueError(
        f"Unsupported file extension: {suffix}. Supported: .pdf, .txt, .md"
    )
