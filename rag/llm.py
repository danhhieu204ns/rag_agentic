from __future__ import annotations

import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv()

def create_groq_llm(
    model: str = "llama-3.3-70b-versatile",
    temperature: float = 0.0,
) -> ChatGroq:
    """Khoi tao LLM backend ChatGroq.

    Input:
    - model: Ten model tren Groq.
    - temperature: Nhiet do sinh van ban.

    Output:
    - Doi tuong ChatGroq da cau hinh xong.

    Logic:
    - Kiem tra bien moi truong GROQ_API_KEY.
    - Neu thieu key thi nem ValueError, nguoc lai tra ve ChatGroq.
    """
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("Please set GROQ_API_KEY in your environment before running this pipeline.")

    return ChatGroq(model=model, temperature=temperature)


def create_gemini_embedding(
    model: str = "text-embedding-004",
) -> GoogleGenerativeAIEmbeddings:
    """Khoi tao Embedding backend Gemini.

    Input:
    - model: Ten model embedding tren Google GenAI (vd: models/text-embedding-004).

    Output:
    - Doi tuong GoogleGenerativeAIEmbeddings da cau hinh xong.

    Logic:
    - Kiem tra bien moi truong GOOGLE_API_KEY.
    - Neu thieu key thi nem ValueError, nguoc lai tra ve GoogleGenerativeAIEmbeddings.
    """
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Please set GOOGLE_API_KEY in your environment before running this pipeline.")

    normalized_model = model.strip()
    if normalized_model.startswith("models/"):
        normalized_model = normalized_model.split("/", 1)[1]

    return GoogleGenerativeAIEmbeddings(model=normalized_model)
