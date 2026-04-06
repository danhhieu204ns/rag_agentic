from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


def build_prompt(template: str) -> ChatPromptTemplate:
    """Tao prompt template cho chain.

    Input:
    - template: Chuoi template co placeholder nhu {input}, {context}.

    Output:
    - ChatPromptTemplate da compile.

    Logic:
    - Goi ChatPromptTemplate.from_template de tao prompt object.
    """
    return ChatPromptTemplate.from_template(template)


def build_rag_chain(retriever, llm, prompt: ChatPromptTemplate):
    """Xay dung chuoi Naive RAG tra ve cau tra loi text.

    Input:
    - retriever: Retriever lay context lien quan.
    - llm: Chat model dung de sinh cau tra loi.
    - prompt: Prompt template cho pha augment.

    Output:
    - Runnable chain nhan query va tra ve string answer.

    Logic:
    - Tao dict dau vao gom context tu retriever va input tu RunnablePassthrough.
    - Truyen qua prompt -> llm -> StrOutputParser.
    """
    return (
        {"context": retriever, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )


def build_rag_chain_with_sources(retriever, llm, prompt: ChatPromptTemplate):
    """Xay dung RAG chain giu lai ca answer va context da retrieve.

    Input:
    - retriever: Retriever lay tai lieu lien quan.
    - llm: Chat model.
    - prompt: Prompt template.

    Output:
    - Runnable tra ve dict co it nhat "answer" va "context".

    Logic:
    - Tao retrieval_setup de dong goi context va input.
    - Dung assign de bo sung truong answer duoc sinh tu prompt|llm|parser.
    """
    retrieval_setup = RunnableParallel(
        {"context": retriever, "input": RunnablePassthrough()}
    )

    return retrieval_setup.assign(
        answer=(
            prompt
            | llm
            | StrOutputParser()
        )
    )
