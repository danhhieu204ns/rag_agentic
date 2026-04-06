from __future__ import annotations

from collections.abc import Sequence

from datasets import Dataset
from ragas import evaluate
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import context_precision, context_recall, faithfulness

try:
    from ragas.metrics import answer_relevancy
except ImportError:
    from ragas.metrics import answer_relevance as answer_relevancy


def collect_predictions(
    rag_chain_with_sources,
    questions: Sequence[str],
) -> tuple[list[str], list[list[str]]]:
    """Chay chain de thu ve cau tra loi va context cho nhieu cau hoi.

    Input:
    - rag_chain_with_sources: Chain tra ve dict gom answer/context.
    - questions: Danh sach cau hoi can evaluate.

    Output:
    - Tuple (answers, contexts):
      answers la list[str], contexts la list[list[str]].

    Logic:
    - Lap qua tung query.
    - Invoke chain, lay answer va noi dung page_content cua context.
    - Tra ve du lieu da chuan hoa cho RAGAS.
    """
    answers: list[str] = []
    contexts: list[list[str]] = []

    for query in questions:
        result = rag_chain_with_sources.invoke(query)
        answers.append(result["answer"])
        contexts.append([doc.page_content for doc in result["context"]])

    return answers, contexts


def build_ragas_dataset(
    questions: Sequence[str],
    answers: Sequence[str],
    contexts: Sequence[Sequence[str]],
    ground_truths: Sequence[str],
) -> Dataset:
    """Tao Dataset phu hop schema dau vao cua RAGAS.

    Input:
    - questions: Danh sach cau hoi.
    - answers: Danh sach cau tra loi model.
    - contexts: Danh sach context retrieval theo tung cau hoi.
    - ground_truths: Danh sach dap an tham chieu.

    Output:
    - Dataset (huggingface datasets) voi cac cot question/answer/contexts/ground_truth.

    Logic:
    - Kiem tra do dai cac danh sach phai bang nhau.
    - Chuan hoa ve list va goi Dataset.from_dict.
    """
    if not (len(questions) == len(answers) == len(contexts) == len(ground_truths)):
        raise ValueError("questions, answers, contexts, and ground_truths must have the same length")

    ragas_data = {
        "question": list(questions),
        "answer": list(answers),
        "contexts": [list(c) for c in contexts],
        "ground_truth": list(ground_truths),
    }

    return Dataset.from_dict(ragas_data)


def evaluate_with_ragas(ragas_dataset: Dataset, llm, embeddings):
    """Danh gia chat luong RAG bang bo metric RAGAS.

    Input:
    - ragas_dataset: Dataset da duoc chuan hoa theo schema RAGAS.
    - llm: LLM object de RAGAS su dung trong mot so metric.
    - embeddings: Embedding object de tinh toan metric lien quan retrieval.

    Output:
    - Ket qua evaluate cua RAGAS (co the chuyen sang dataframe).

    Logic:
    - Wrap llm/embeddings sang adapter cua RAGAS.
    - Goi evaluate voi metrics faithfulness, answer relevancy, context precision, context recall.
    """
    ragas_llm = LangchainLLMWrapper(llm)
    ragas_emb = LangchainEmbeddingsWrapper(embeddings)

    return evaluate(
        ragas_dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=ragas_llm,
        embeddings=ragas_emb,
    )
