---
name: rag-systems-expert
version: 1.0.0
description: Build production-grade Retrieval Augmented Generation systems. Covers chunking, embedding, vector search, reranking, evaluation, and RAG pipelines.
author: luo-kai
tags: [rag, retrieval, embeddings, vector-search, llm, production, langchain]
---

# RAG Systems Expert

## Before Starting
1. What documents are you indexing — PDFs, web pages, code, structured data?
2. Query type — factual lookup, summarization, multi-hop reasoning?
3. Latency requirements — real-time or batch acceptable?

## Core Expertise Areas

### Document Processing and Chunking
Chunking strategy determines retrieval quality more than model choice.
Fixed-size: simple but breaks context mid-sentence.
Sentence-based: cleaner but variable size.
Semantic: chunk by topic shift — highest quality, highest cost.
Recursive character splitting: best general-purpose approach.
Overlap: 10 to 20 percent overlap between chunks prevents context loss at boundaries.

### Embedding Models
OpenAI text-embedding-3-small: 1536 dims, cheap, strong general performance.
OpenAI text-embedding-3-large: 3072 dims, better for complex semantic queries.
Cohere embed-v3: strong multilingual, good for diverse document types.
Sentence-transformers: free open-source, good for on-premise or zero-budget.
Embed queries and documents with the same model — never mix.

### Vector Databases
Pinecone: managed, fast, production-ready, free tier available.
Weaviate: open-source option, good hybrid search.
Chroma: lightweight, runs locally, perfect for development and small scale.
pgvector: Postgres extension — use if already on Postgres.
Qdrant: fast, open-source, good filtering support.

### Retrieval and Reranking
Semantic search: cosine similarity on embeddings — good baseline.
Hybrid search: semantic + BM25 keyword — better for factual queries.
Reranking: use Cohere Rerank or cross-encoder after initial retrieval.
Top-k: retrieve 10 to 20 candidates, rerank to top 3 to 5.
MMR (Maximal Marginal Relevance): reduces redundancy in multi-doc retrieval.

### RAG Pipeline Evaluation
Faithfulness: does the answer reflect the retrieved context?
Answer relevance: does the answer address the question?
Context relevance: are the retrieved chunks actually relevant?
Tools: RAGAS framework, Trulens, DeepEval.
Baseline: run 50 golden QA pairs before and after changes.

## Key Patterns

### Basic RAG Pipeline
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# 1. Load and chunk documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)
chunks = splitter.split_documents(documents)

# 2. Embed and store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(chunks, embeddings)

# 3. Retrieve and generate
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

response = qa_chain.run("What are the main topics covered?")
```

### Hybrid Search with Reranking
```python
import cohere
from langchain.retrievers import BM25Retriever, EnsembleRetriever

# Sparse retriever (BM25 keyword search)
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 10

# Dense retriever (semantic)
dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# Ensemble: combine both
ensemble = EnsembleRetriever(
    retrievers=[bm25_retriever, dense_retriever],
    weights=[0.4, 0.6]
)

# Rerank top results
co = cohere.Client()
docs = ensemble.get_relevant_documents(query)
reranked = co.rerank(
    query=query,
    documents=[d.page_content for d in docs],
    top_n=3,
    model="rerank-english-v3.0"
)
```

### RAG Evaluation with RAGAS
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_relevancy

# Build evaluation dataset
from datasets import Dataset
eval_data = Dataset.from_dict({
    "question": questions,
    "answer": generated_answers,
    "contexts": retrieved_contexts,
    "ground_truth": golden_answers
})

# Run evaluation
results = evaluate(eval_data, metrics=[
    faithfulness,
    answer_relevancy,
    context_relevancy
])
print(results)
# Target: faithfulness > 0.85, answer_relevancy > 0.80
```

## Best Practices
- Start with recursive character splitting — it beats fixed size in most cases
- Always include chunk overlap — prevents context loss at boundaries
- Retrieve more than you need then rerank — quality beats raw retrieval count
- Evaluate before and after every pipeline change — track regression
- Add metadata to chunks — enables filtered retrieval and better context

## Common Pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Chunks too large | Diluted retrieval relevance | Keep chunks 500 to 1500 tokens |
| Chunks too small | Missing context, incoherent answers | Minimum 200 tokens with overlap |
| No reranking | Top-k not actually most relevant | Add reranker after initial retrieval |
| No evaluation | Regressions go undetected | Run RAGAS on 50+ golden pairs |
| Embedding model mismatch | Poor similarity scores | Always embed queries and docs with same model |

## Related Skills
- llm-engineering-expert
- vector-databases-expert
- deep-learning-expert
- agent-memory-expert
