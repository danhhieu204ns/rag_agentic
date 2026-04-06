from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from .chain import build_prompt, build_rag_chain, build_rag_chain_with_sources
from .config import NaiveRAGConfig
from .embeddings import create_embeddings
from .evaluation import build_ragas_dataset, collect_predictions, evaluate_with_ragas
from .llm import create_groq_llm
from .loaders import load_documents
from .splitter import split_documents
from .vectorstore import (
    build_faiss_vectorstore,
    create_retriever,
    load_faiss_vectorstore,
    save_faiss_vectorstore,
)


class NaiveRAGPipeline:
    """Pipeline dieu phoi day du cac buoc Naive RAG.

    Input:
    - config: NaiveRAGConfig (co the truyen vao hoac dung mac dinh).

    Output:
    - Mot object giu trang thai embeddings/vectorstore/retriever/chain trong qua trinh chay.

    Logic:
    - Cung cap cac method rieng cho index, build chain, ask, evaluate.
    - Tai su dung cac module con trong rag de code gon va de test.
    """

    def __init__(self, config: NaiveRAGConfig | None = None) -> None:
        """Khoi tao pipeline va cac bien trang thai.

        Input:
        - config: Cau hinh runtime cho pipeline.

        Output:
        - Khong tra ve gia tri; gan config va dat cac component ve None.

        Logic:
        - Neu config khong duoc truyen vao thi dung gia tri mac dinh.
        """
        self.config = config or NaiveRAGConfig()
        self.embeddings = None
        self.vectorstore = None
        self.retriever = None
        self.llm = None
        self.prompt = None
        self.rag_chain = None
        self.rag_chain_with_sources = None

    def build_embeddings(self):
        """Khoi tao embedding component theo config.

        Input:
        - Doc tham so embedding provider/model/device/max_seq_length tu self.config.

        Output:
        - Embeddings object duoc luu vao self.embeddings va duoc tra ve.

        Logic:
        - Goi factory create_embeddings de tao embedding backend tu config.
        """
        self.embeddings = create_embeddings(
            provider=self.config.embedding_provider,
            model_name=self.config.embedding_model_name,
            device=self.config.embedding_device,
            max_seq_length=self.config.embedding_max_seq_length,
        )
        return self.embeddings

    def build_or_load_vectorstore(
        self,
        force_rebuild: bool = False,
        persist_index: bool = True,
    ):
        """Build index moi hoac load FAISS index da ton tai.

        Input:
        - force_rebuild: True de bo qua index cu va index lai tu raw document.
        - persist_index: True de luu index vua build xuong dia.

        Output:
        - Doi tuong vectorstore (FAISS), dong thoi cap nhat self.retriever.

        Logic:
        - Dam bao embeddings da duoc tao.
        - Neu co index va khong force_rebuild thi load tu dia.
        - Nguoc lai: load documents -> split -> build FAISS -> save (neu bat).
        - Tao retriever voi top-k tu config.
        """
        embeddings = self.embeddings or self.build_embeddings()
        index_dir = Path(self.config.faiss_index_dir)

        if index_dir.exists() and not force_rebuild:
            self.vectorstore = load_faiss_vectorstore(
                index_dir=index_dir,
                embeddings=embeddings,
                allow_dangerous_deserialization=self.config.allow_dangerous_deserialization,
            )
        else:
            documents = load_documents(self.config.data_path)
            split_docs = split_documents(
                documents,
                chunk_size=self.config.chunk_size,
                chunk_overlap=self.config.chunk_overlap,
            )

            self.vectorstore = build_faiss_vectorstore(split_docs, embeddings)
            if persist_index:
                save_faiss_vectorstore(self.vectorstore, index_dir)

        self.retriever = create_retriever(self.vectorstore, k=self.config.retriever_k)
        return self.vectorstore

    def build_chains(self):
        """Khoi tao prompt, LLM va cac RAG chain can dung.

        Input:
        - Su dung self.retriever da co san tu buoc index/load.

        Output:
        - Tuple (rag_chain, rag_chain_with_sources).

        Logic:
        - Kiem tra retriever ton tai.
        - Tao llm, prompt.
        - Build 2 chain: chain tra text va chain tra answer kem context.
        """
        if self.retriever is None:
            raise RuntimeError("Retriever is not initialized. Run build_or_load_vectorstore first.")

        self.llm = create_groq_llm(
            model=self.config.llm_model,
            temperature=self.config.llm_temperature,
        )
        self.prompt = build_prompt(self.config.prompt_template)
        self.rag_chain = build_rag_chain(self.retriever, self.llm, self.prompt)
        self.rag_chain_with_sources = build_rag_chain_with_sources(
            self.retriever,
            self.llm,
            self.prompt,
        )

        return self.rag_chain, self.rag_chain_with_sources

    def ask(self, query: str, with_sources: bool = False):
        """Thuc thi truy van hoi dap tren RAG pipeline.

        Input:
        - query: Cau hoi nguoi dung.
        - with_sources: True de tra ve answer kem context retrieved.

        Output:
        - Neu with_sources=False: string answer.
        - Neu with_sources=True: dict co answer va context.

        Logic:
        - Tu dong build chain neu chua co.
        - Chon chain phu hop theo with_sources va invoke voi query.
        """
        if with_sources:
            if self.rag_chain_with_sources is None:
                self.build_chains()
            return self.rag_chain_with_sources.invoke(query)

        if self.rag_chain is None:
            self.build_chains()
        return self.rag_chain.invoke(query)

    def evaluate(
        self,
        questions: Sequence[str],
        ground_truths: Sequence[str],
    ):
        """Danh gia pipeline tren tap cau hoi bang RAGAS.

        Input:
        - questions: Danh sach cau hoi test.
        - ground_truths: Danh sach dap an tham chieu tuong ung.

        Output:
        - Tuple (ragas_result, dataframe_ket_qua).

        Logic:
        - Dam bao chain, embeddings, llm da duoc khoi tao.
        - Chay collect_predictions.
        - Tao ragas_dataset va goi evaluate_with_ragas.
        - Tra ve ket qua goc va bang pandas de de quan sat.
        """
        if self.rag_chain_with_sources is None:
            self.build_chains()
        if self.embeddings is None:
            self.build_embeddings()
        if self.llm is None:
            self.llm = create_groq_llm(
                model=self.config.llm_model,
                temperature=self.config.llm_temperature,
            )

        answers, contexts = collect_predictions(self.rag_chain_with_sources, questions)
        ragas_dataset = build_ragas_dataset(
            questions=questions,
            answers=answers,
            contexts=contexts,
            ground_truths=ground_truths,
        )

        ragas_result = evaluate_with_ragas(
            ragas_dataset=ragas_dataset,
            llm=self.llm,
            embeddings=self.embeddings,
        )

        return ragas_result, ragas_result.to_pandas()
