from __future__ import annotations

from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_PRESETS = {
    "vi_v2": "AITeamVN/Vietnamese_Embedding_v2",
    "mini_lm": "sentence-transformers/all-MiniLM-L6-v2",
    "mpnet_v2": "sentence-transformers/all-mpnet-base-v2",
}


def create_huggingface_embeddings(
    model_name: str,
    device: str = "cpu",
    max_seq_length: int | None = 2048,
) -> HuggingFaceEmbeddings:
    """Khoi tao HuggingFaceEmbeddings theo cau hinh model.

    Input:
    - model_name: Ten model embedding tren Hugging Face Hub.
    - device: Thiet bi chay model (vi du: "cpu", "cuda").
    - max_seq_length: Gioi han do dai chuoi cho encoder (neu backend ho tro).

    Output:
    - Doi tuong HuggingFaceEmbeddings da san sang de embed query/document.

    Logic:
    - Tao embedding instance.
    - Neu co _client.max_seq_length thi gan gia tri de kiem soat do dai input.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": device},
    )

    if max_seq_length is not None:
        client = getattr(embeddings, "_client", None)
        if client is not None and hasattr(client, "max_seq_length"):
            client.max_seq_length = max_seq_length

    return embeddings


def create_embeddings(
    provider: str,
    model_name: str,
    device: str = "cpu",
    max_seq_length: int | None = 2048,
):
    """Factory tao embedding theo provider.

    Input:
    - provider: Ten nha cung cap embedding (hien ho tro "huggingface").
    - model_name: Ten model embedding.
    - device: Thiet bi suy luan.
    - max_seq_length: Gioi han do dai chuoi.

    Output:
    - Embeddings object tuong ung provider.

    Logic:
    - Chuan hoa provider ve lowercase.
    - Dieu huong den ham tao embedding phu hop.
    - Nem ValueError neu provider chua duoc ho tro.
    """
    provider_normalized = provider.strip().lower()

    if provider_normalized == "huggingface":
        return create_huggingface_embeddings(
            model_name=model_name,
            device=device,
            max_seq_length=max_seq_length,
        )

    raise ValueError(
        f"Unsupported embedding provider: {provider}. Supported providers: huggingface"
    )


def create_embeddings_from_preset(
    preset_name: str,
    device: str = "cpu",
    max_seq_length: int | None = 2048,
) -> HuggingFaceEmbeddings:
    """Khoi tao embedding tu preset ten ngan gon.

    Input:
    - preset_name: Khoa preset (vi du: "vi_v2", "mini_lm").
    - device: Thiet bi suy luan.
    - max_seq_length: Gioi han do dai chuoi.

    Output:
    - Doi tuong HuggingFaceEmbeddings voi model tu preset.

    Logic:
    - Kiem tra preset ton tai trong EMBEDDING_PRESETS.
    - Lay model_name tu bang preset va goi create_huggingface_embeddings.
    """
    key = preset_name.strip().lower()
    if key not in EMBEDDING_PRESETS:
        supported = ", ".join(sorted(EMBEDDING_PRESETS.keys()))
        raise ValueError(f"Unsupported preset: {preset_name}. Available presets: {supported}")

    return create_huggingface_embeddings(
        model_name=EMBEDDING_PRESETS[key],
        device=device,
        max_seq_length=max_seq_length,
    )
