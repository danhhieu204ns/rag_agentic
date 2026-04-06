# Advanced + Agentic RAG Cookbooks👨🏻‍💻
Welcome to the comprehensive collection of advanced + agentic Retrieval-Augmented Generation (RAG) techniques.

## Introduction🚀
RAG is a popular method that improves accuracy and relevance by finding the right information from reliable sources and transforming it into useful answers. This repository covers the most effective advanced + agentic RAG techniques with clear implementations and explanations.

The main goal of this repository is to provide a helpful resource for researchers and developers looking to use advanced RAG techniques in their projects. Building these techniques from scratch takes time, and finding proper evaluation methods can be challenging. This repository simplifies the process by offering ready-to-use implementations and guidance on how to evaluate them.
>[!NOTE]
>This repository starts with naive RAG as a foundation and progresses to advanced and agentic techniques. It also includes research papers/references for each RAG technique, which you can explore for further reading.

## Introduction to RAG💡
Large Language Models are trained on a fixed dataset, which limits their ability to handle private or recent information. They can sometimes "hallucinate", providing incorrect yet believable answers. Fine-tuning can help but it is expensive and not ideal for retraining again and again on new data. The Retrieval-Augmented Generation (RAG) framework addresses this issue by using external documents to improve the LLM's responses through in-context learning. RAG ensures that the information provided by the LLM is not only contextually relevant but also accurate and up-to-date.

![final diagram](https://github.com/user-attachments/assets/508b3a87-ac46-4bf7-b849-145c5465a6c0)

There are four main components in RAG:

**Indexing:** First, documents (in any format) are split into chunks, and embeddings for these chunks are created. These embeddings are then added to a vector store.

**Retriever:** Then, the retriever finds the most relevant documents based on the user's query, using techniques like vector similarity from the vector store.

**Augment:** After that, the Augment part combines the user's query with the retrieved context into a prompt, ensuring the LLM has the information needed to generate accurate responses.

**Generate:** Finally, the combined query and prompt are passed to the model, which then generates the final response to the user's query.

These components of RAG allow the model to access up-to-date, accurate information and generate responses based on external knowledge. However, to ensure RAG systems are functioning effectively, it’s essential to evaluate their performance.

## RAG Evaluation📊
To ensure the reliability and accuracy of RAG systems, it is essential to evaluate both the retrieval and generation components. A popular and effective framework for this is **Ragas** (Retrieval Augmented Generation Assessment).

Ragas provides a suite of metrics designed to evaluate RAG pipelines objectively:
- **Faithfulness:** Measures if the generated answer is strictly grounded in the retrieved context, penalizing hallucinations.
- **Answer Relevance:** Evaluates how well the generated answer addresses the user's initial prompt or query.
- **Context Precision:** Checks whether the most relevant context chunks are ranked highest by the retriever.
- **Context Recall:** Measures whether the retrieved context contains all the necessary information required to answer the query accurately.

By automating the evaluation across these metrics, you can systematically compare different RAG techniques and optimize your pipelines for better performance.

## Advanced RAG Techniques⚙️
Here are the details of all the Advanced RAG techniques covered in this repository (ordered from easiest to hardest).

| Technique | Description |
| :--- | :--- |
| **Naive RAG** | The simplest RAG implementation consisting of indexing, retrieval, and generation. |
| **Rewrite-Retrieve-Read** | Refines the retrieval process by using an LLM to rewrite and improve the user's query before searching. |
| **HyDE RAG** | Uses Hypothetical Document Embeddings by generating a mock answer to guide the retrieval of relevant documents. |
| **Contextual RAG** | Improves relevance and cost-efficiency by compressing retrieved documents to keep only query-specific information. |
| **Hybrid RAG** | Combines the semantic understanding of vector search with the precise keyword matching of BM25. |
| **RAG Fusion** | Enhances retrieval by generating sub-queries and reranking documents using Reciprocal Rank Fusion (RRF). |
| **Parent Document Retriever** | Indexes small "child" chunks for precise matching but retrieves larger "parent" documents for richer context. |
| **Unstructured RAG** | Handles documents with text, tables, and images using `unstructured.io`, preventing table fragmentation. |

## Agent Techniques⚙️
Here are the details of all the Agent techniques covered in this repository (ordered from easiest to hardest).

| Technique | Description |
| :--- | :--- |
| **ReAct (Reasoning and Action)** | Interleaves reasoning and tool actions step by step to solve tasks with external information.|
| **ReWOO (Reasoning WithOut Observation)** | Separates planning, tool execution, and final synthesis (Planner-Worker-Solver) to improve efficiency and control.|
| **Reflexion** | Uses self-reflection and memory feedback loops so the agent can learn from prior mistakes and iteratively improve outputs.|

## Agentic RAG Techniques⚙️
Here are the details of all the Agentic RAG techniques covered in this repository (ordered from easiest to hardest).

| Technique | Description |
| :--- | :--- |
| **Basic Agentic RAG** | Combines generative models with AI agents that use tools (like VectorStore and WebSearch) to dynamically retrieve information. |
| **Adaptive RAG** | Adjusts retrieval strategy dynamically based on query complexity (e.g., self-corrective vs web search). |
| **Corrective RAG** | Improves accuracy by evaluating, refining, or discarding retrieved documents, optionally falling back to web search before generation. |
| **Self RAG** | Improves generated text accuracy by allowing the model to reflect on its own output and retrieval usage via reflection tokens. |
| **Agentic RAG with DeepSeek** | An implementation of Agentic RAG using DeepSeek, Qdrant, and LangChain for retrieval and task planning. |

## Getting Started🛠️
First, clone this repository by using the following command:
```bash
git clone https://github.com/athina-ai/rag-cookbooks.git
```
Next, navigate to the project directory:
```bash
cd rag-cookbooks
```
Once you are in the 'rag-cookbooks' directory, follow the detailed implementation for each technique.

## Fullstack RAG App (FastAPI + React)

This repository now also includes a fullstack application:

- Backend: `app-backend` (FastAPI)
- Frontend: `app-frontend` (React + Vite)

### Features

- Chat UI for question answering with chat memory
- Document management UI for upload, edit metadata, embedding, delete
- Global FAISS index built from embedded document chunks

### Run Backend

```bash
pip install -r app-backend/requirements.txt
uvicorn app.main:app --reload --app-dir app-backend
```

Required environment variable:

- `GROQ_API_KEY`

### Run Frontend

```bash
cd app-frontend
npm install
npm run dev
```

Frontend default API target is `http://localhost:8000/api`.






