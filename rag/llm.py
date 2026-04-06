from __future__ import annotations

import os

from langchain_groq import ChatGroq


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
