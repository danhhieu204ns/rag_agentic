from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from rag.config import NaiveRAGConfig
    from rag.pipeline import NaiveRAGPipeline
else:
    from .config import NaiveRAGConfig
    from .pipeline import NaiveRAGPipeline


def parse_args() -> argparse.Namespace:
    """Parse tham so dong lenh cho script Naive RAG.

    Input:
    - Cac tham so CLI (data path, query, index options, embedding, llm, retrieval k).

    Output:
    - argparse.Namespace chua toan bo gia tri cau hinh runtime.

    Logic:
    - Dinh nghia parser va cac argument can thiet.
    - Parse tham so tu command line de su dung trong main.
    """
    parser = argparse.ArgumentParser(description="Run the Naive RAG pipeline from Python modules.")
    parser.add_argument("--data-path", default="data/bao_cao.pdf", help="Path to the source document.")
    parser.add_argument("--query", default="Ten de tai nay la gi?", help="Question to ask the RAG pipeline.")
    parser.add_argument("--index-dir", default="faiss_index", help="Directory to save/load FAISS index.")
    parser.add_argument("--rebuild-index", action="store_true", help="Force re-indexing from raw document.")
    parser.add_argument("--no-save-index", action="store_true", help="Do not persist FAISS index to disk.")

    parser.add_argument("--embedding-model", default="AITeamVN/Vietnamese_Embedding_v2")
    parser.add_argument("--embedding-device", default="cpu")
    parser.add_argument("--max-seq-length", type=int, default=2048)

    parser.add_argument("--llm-model", default="llama-3.3-70b-versatile")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--k", type=int, default=4, help="Top-k chunks from retriever.")
    return parser.parse_args()


def main() -> None:
    """Diem vao script: khoi tao pipeline, truy van va in ket qua.

    Input:
    - Gia tri cau hinh tu parse_args.

    Output:
    - Khong tra ve gia tri; in answer va cac retrieved chunks ra man hinh.

    Logic:
    - Tao NaiveRAGConfig tu tham so CLI.
    - Build/load vectorstore, tao chain.
    - Goi pipeline.ask(with_sources=True) va hien thi ket qua.
    """
    args = parse_args()

    config = NaiveRAGConfig(
        data_path=args.data_path,
        faiss_index_dir=args.index_dir,
        embedding_model_name=args.embedding_model,
        embedding_device=args.embedding_device,
        embedding_max_seq_length=args.max_seq_length,
        llm_model=args.llm_model,
        llm_temperature=args.temperature,
        retriever_k=args.k,
    )

    pipeline = NaiveRAGPipeline(config)
    pipeline.build_or_load_vectorstore(
        force_rebuild=args.rebuild_index,
        persist_index=not args.no_save_index,
    )
    pipeline.build_chains()

    result = pipeline.ask(args.query, with_sources=True)

    print("Answer:")
    print(result["answer"])
    print("\nRetrieved chunks:")
    for i, doc in enumerate(result["context"], start=1):
        print(f"\nChunk {i}")
        print(doc.page_content)


if __name__ == "__main__":
    main()
