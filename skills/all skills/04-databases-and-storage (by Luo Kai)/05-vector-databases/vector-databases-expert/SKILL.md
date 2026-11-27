---
author: luo-kai
name: vector-databases
description: Expert-level vector database development. Use when working with Pinecone, Weaviate, Qdrant, pgvector, Chroma, FAISS, implementing semantic search, hybrid search, ANN algorithms, or embedding storage and retrieval. Also use when the user mentions 'vector database', 'pgvector', 'Pinecone', 'semantic search', 'embedding storage', 'HNSW', 'ANN', 'similarity search', 'RAG retrieval', or 'nearest neighbor'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Vector Databases Expert

You are an expert in vector databases with deep knowledge of embedding models, ANN algorithms, retrieval strategies, and building production semantic search systems.

## Before Starting

1. **Use case** — semantic search, RAG retrieval, recommendation, duplicate detection?
2. **Vector store** — pgvector, Pinecone, Qdrant, Weaviate, Chroma, FAISS?
3. **Scale** — thousands, millions, or billions of vectors?
4. **Latency requirement** — real-time (< 100ms) or batch?
5. **Problem type** — setup, performance, retrieval quality, hybrid search?

---

## Core Expertise Areas

- **Embedding models**: OpenAI, Cohere, BGE, E5, sentence-transformers — selection guide
- **ANN algorithms**: HNSW, IVF, ScaNN, FLAT — trade-offs and configuration
- **pgvector**: PostgreSQL extension, indexing, hybrid search, production setup
- **Pinecone**: namespaces, metadata filtering, sparse-dense hybrid
- **Qdrant**: collections, payload filtering, quantization, on-disk indexing
- **Retrieval strategies**: top-k, MMR, hybrid BM25+dense, reranking
- **Chunking**: fixed, recursive, semantic, sliding window strategies
- **Evaluation**: recall@k, MRR, NDCG, latency benchmarks

---

## Key Patterns & Code

### Embedding Model Selection Guide
```
OpenAI text-embedding-3-small:
  Dimensions: 1536 (or lower via matryoshka)
  Strengths: excellent English, easy to use, reliable
  Cost: $0.02 per 1M tokens
  Use when: OpenAI already in stack, budget not a concern

OpenAI text-embedding-3-large:
  Dimensions: 3072
  Strengths: best OpenAI quality, multilingual
  Cost: $0.13 per 1M tokens
  Use when: highest quality needed, multilingual

Cohere embed-v3:
  Dimensions: 1024
  Strengths: excellent multilingual, search-optimized
  Use when: multilingual content, good quality/cost balance

BGE-M3 (open source):
  Dimensions: 1024
  Strengths: multilingual, dense+sparse+ColBERT in one model
  Cost: free (self-hosted)
  Use when: self-hosted required, multilingual, best open-source quality

all-MiniLM-L6-v2 (sentence-transformers):
  Dimensions: 384
  Strengths: tiny, fast, free
  Cost: free
  Use when: prototype, low latency critical, limited compute

Rule of thumb:
  Production RAG: text-embedding-3-small or BGE-M3
  Multilingual: Cohere embed-v3 or BGE-M3
  Prototype/dev: all-MiniLM-L6-v2
  Cost-sensitive at scale: self-hosted BGE

Important: Use the SAME model for indexing and querying
Never mix embedding models in the same collection
```

### pgvector — PostgreSQL Setup
```sql
-- Install extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table with embedding column
CREATE TABLE documents (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content     TEXT NOT NULL,
  embedding   vector(1536),   -- dimension must match your model
  metadata    JSONB NOT NULL DEFAULT '{}',
  source      TEXT,
  chunk_index INT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- HNSW index (best for most use cases)
-- m: number of connections per node (default 16, higher = better recall, more memory)
-- ef_construction: size of dynamic candidate list during build (default 64)
CREATE INDEX idx_documents_embedding_hnsw
  ON documents
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

-- IVFFlat index (lower memory than HNSW, slightly lower recall)
-- lists: number of clusters (sqrt(n_rows) is a good starting point)
CREATE INDEX idx_documents_embedding_ivfflat
  ON documents
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- At query time, set probes (higher = better recall, slower)
SET ivfflat.probes = 10;

-- Basic similarity search
SELECT
  id,
  content,
  metadata,
  1 - (embedding <=> '[0.1, 0.2, ...]'::vector) AS similarity
FROM documents
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
LIMIT 10;

-- Distance operators:
-- <=>  cosine distance (use for normalized embeddings)
-- <->  Euclidean (L2) distance
-- <#>  inner product (negative, use - for similarity)

-- Filtered similarity search (use metadata for pre-filtering)
SELECT
  id,
  content,
  1 - (embedding <=> $1::vector) AS similarity
FROM documents
WHERE
  metadata->>'source' = 'product-docs'
  AND metadata->>'language' = 'en'
  AND created_at > NOW() - INTERVAL '30 days'
ORDER BY embedding <=> $1::vector
LIMIT 20;

-- Hybrid search: combine semantic + keyword (BM25)
-- Requires pg_trgm or pgroonga extension for full-text
WITH
semantic_results AS (
  SELECT id, content,
    1 - (embedding <=> $1::vector) AS semantic_score
  FROM documents
  ORDER BY embedding <=> $1::vector
  LIMIT 50
),
keyword_results AS (
  SELECT id, content,
    ts_rank(to_tsvector('english', content), plainto_tsquery('english', $2)) AS keyword_score
  FROM documents
  WHERE to_tsvector('english', content) @@ plainto_tsquery('english', $2)
  LIMIT 50
)
SELECT
  COALESCE(s.id, k.id) AS id,
  COALESCE(s.content, k.content) AS content,
  COALESCE(s.semantic_score, 0) * 0.7 +
  COALESCE(k.keyword_score, 0) * 0.3 AS hybrid_score
FROM semantic_results s
FULL OUTER JOIN keyword_results k USING (id)
ORDER BY hybrid_score DESC
LIMIT 10;
```

### pgvector Python Client
```python
from pgvector.psycopg import register_vector
import psycopg
import numpy as np
from openai import OpenAI
from typing import Optional

oai = OpenAI()

def get_embedding(text: str, model: str = 'text-embedding-3-small') -> list[float]:
    text = text.replace('\n', ' ').strip()
    response = oai.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

class VectorStore:
    def __init__(self, conn_string: str):
        self.conn = psycopg.connect(conn_string)
        register_vector(self.conn)

    def upsert(self, doc_id: str, content: str, metadata: dict = None) -> None:
        embedding = get_embedding(content)
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO documents (id, content, embedding, metadata)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                  content = EXCLUDED.content,
                  embedding = EXCLUDED.embedding,
                  metadata = EXCLUDED.metadata
                ''',
                (doc_id, content, embedding, metadata or {})
            )
        self.conn.commit()

    def bulk_upsert(self, documents: list[dict], batch_size: int = 100) -> None:
        # Batch embedding calls for efficiency
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            texts = [doc['content'] for doc in batch]
            response = oai.embeddings.create(input=texts, model='text-embedding-3-small')
            embeddings = [r.embedding for r in response.data]

            with self.conn.cursor() as cur:
                cur.executemany(
                    '''
                    INSERT INTO documents (id, content, embedding, metadata)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                      content = EXCLUDED.content,
                      embedding = EXCLUDED.embedding,
                      metadata = EXCLUDED.metadata
                    ''',
                    [
                        (doc['id'], doc['content'], emb, doc.get('metadata', {}))
                        for doc, emb in zip(batch, embeddings)
                    ]
                )
            self.conn.commit()
            print('Upserted', i + len(batch), '/', len(documents))

    def search(
        self,
        query: str,
        top_k: int = 10,
        metadata_filter: Optional[dict] = None,
        min_similarity: float = 0.0,
    ) -> list[dict]:
        query_embedding = get_embedding(query)

        filter_clause = ''
        filter_params = []
        if metadata_filter:
            conditions = []
            for key, value in metadata_filter.items():
                conditions.append("metadata->>%s = %s")
                filter_params.extend([key, str(value)])
            filter_clause = 'WHERE ' + ' AND '.join(conditions)

        with self.conn.cursor() as cur:
            cur.execute(
                '''
                SELECT
                  id,
                  content,
                  metadata,
                  1 - (embedding <=> %s::vector) AS similarity
                FROM documents
                ''' + filter_clause + '''
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                ''',
                [query_embedding] + filter_params + [query_embedding, top_k]
            )
            rows = cur.fetchall()

        return [
            {'id': r[0], 'content': r[1], 'metadata': r[2], 'similarity': float(r[3])}
            for r in rows
            if float(r[3]) >= min_similarity
        ]
```

### Qdrant — Production Setup
```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue, Range,
    SearchRequest, SearchParams, HnswConfigDiff,
    OptimizersConfigDiff, QuantizationConfig, ScalarQuantization,
)
import uuid

client = QdrantClient(url='http://localhost:6333')
COLLECTION = 'documents'
EMBEDDING_DIM = 1536

# Create collection with HNSW config
client.recreate_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(
        size=EMBEDDING_DIM,
        distance=Distance.COSINE,
        on_disk=True,           # store vectors on disk for large collections
    ),
    hnsw_config=HnswConfigDiff(
        m=16,                   # connections per node
        ef_construct=100,       # build-time recall vs speed
        full_scan_threshold=10_000,  # use HNSW only above this
    ),
    optimizers_config=OptimizersConfigDiff(
        indexing_threshold=20_000,  # start indexing after 20k vectors
    ),
    quantization_config=QuantizationConfig(
        scalar=ScalarQuantization(
            type='int8',        # 4x memory reduction
            quantile=0.99,
            always_ram=True,    # keep quantized vectors in RAM
        )
    ),
)

# Upsert vectors with payload (metadata)
def upsert_documents(documents: list[dict]):
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=doc['embedding'],
            payload={
                'content': doc['content'],
                'source':  doc.get('source', ''),
                'doc_id':  doc.get('doc_id', ''),
                'chunk':   doc.get('chunk', 0),
                'language': doc.get('language', 'en'),
            }
        )
        for doc in documents
    ]
    client.upsert(collection_name=COLLECTION, points=points, wait=True)

# Search with payload filtering
def search(
    query_vector: list[float],
    top_k: int = 10,
    source_filter: str = None,
    language: str = None,
    score_threshold: float = 0.7,
) -> list[dict]:
    must_conditions = []
    if source_filter:
        must_conditions.append(
            FieldCondition(key='source', match=MatchValue(value=source_filter))
        )
    if language:
        must_conditions.append(
            FieldCondition(key='language', match=MatchValue(value=language))
        )

    query_filter = Filter(must=must_conditions) if must_conditions else None

    results = client.search(
        collection_name=COLLECTION,
        query_vector=query_vector,
        limit=top_k,
        query_filter=query_filter,
        score_threshold=score_threshold,
        search_params=SearchParams(hnsw_ef=128, exact=False),
        with_payload=True,
    )

    return [
        {
            'id':       r.id,
            'score':    r.score,
            'content':  r.payload['content'],
            'source':   r.payload.get('source'),
        }
        for r in results
    ]
```

### Chunking Strategies
```python
from typing import Generator
import re

def fixed_chunks(text: str, size: int = 512, overlap: int = 64) -> list[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), size - overlap):
        chunk = ' '.join(words[i:i + size])
        if chunk:
            chunks.append(chunk)
    return chunks

def recursive_chunks(
    text: str,
    max_size: int = 512,
    overlap: int = 64,
    separators: list[str] = None,
) -> list[str]:
    if separators is None:
        separators = ['\n\n', '\n', '. ', '! ', '? ', ', ', ' ', '']

    if len(text.split()) <= max_size:
        return [text.strip()] if text.strip() else []

    for sep in separators:
        if sep and sep in text:
            parts = text.split(sep)
            chunks = []
            current = ''
            for part in parts:
                test = current + (sep if current else '') + part
                if len(test.split()) <= max_size:
                    current = test
                else:
                    if current:
                        chunks.append(current.strip())
                        # Overlap: take last portion of current chunk
                        overlap_words = current.split()[-overlap:]
                        current = ' '.join(overlap_words) + sep + part
                    else:
                        # Part itself too long — recurse
                        chunks.extend(recursive_chunks(part, max_size, overlap))
                        current = ''
            if current.strip():
                chunks.append(current.strip())
            return chunks

    # Fallback: fixed chunking
    return fixed_chunks(text, max_size, overlap)

def sentence_chunks(text: str, max_sentences: int = 5, overlap: int = 1) -> list[str]:
    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    chunks = []
    for i in range(0, len(sentences), max_sentences - overlap):
        chunk = ' '.join(sentences[i:i + max_sentences])
        if chunk:
            chunks.append(chunk)
    return chunks

# Choosing chunk strategy:
# Fixed: simple, predictable size — good baseline
# Recursive: respects natural boundaries (paragraphs > sentences > words) — recommended
# Sentence: great for Q&A, preserves semantic units
# Semantic: split on topic shifts using embedding similarity — best quality, slow
```

### Retrieval Evaluation
```python
import numpy as np
from typing import Any

def recall_at_k(retrieved: list[Any], relevant: list[Any], k: int) -> float:
    top_k = set(retrieved[:k])
    relevant_set = set(relevant)
    if not relevant_set:
        return 0.0
    return len(top_k & relevant_set) / len(relevant_set)

def mrr(retrieved: list[Any], relevant: list[Any]) -> float:
    relevant_set = set(relevant)
    for rank, item in enumerate(retrieved, 1):
        if item in relevant_set:
            return 1.0 / rank
    return 0.0

def ndcg_at_k(retrieved: list[Any], relevant: list[Any], k: int) -> float:
    relevant_set = set(relevant)
    dcg = sum(
        1.0 / np.log2(rank + 1)
        for rank, item in enumerate(retrieved[:k], 1)
        if item in relevant_set
    )
    ideal_dcg = sum(
        1.0 / np.log2(rank + 1)
        for rank in range(1, min(len(relevant_set), k) + 1)
    )
    return dcg / ideal_dcg if ideal_dcg > 0 else 0.0

def evaluate_retrieval(
    vector_store,
    test_cases: list[dict],
    k: int = 10,
) -> dict:
    recall_scores = []
    mrr_scores = []
    ndcg_scores = []
    latencies = []

    import time
    for case in test_cases:
        start = time.time()
        results = vector_store.search(case['query'], top_k=k)
        latency = (time.time() - start) * 1000

        retrieved_ids = [r['id'] for r in results]
        relevant_ids  = case['relevant_doc_ids']

        recall_scores.append(recall_at_k(retrieved_ids, relevant_ids, k))
        mrr_scores.append(mrr(retrieved_ids, relevant_ids))
        ndcg_scores.append(ndcg_at_k(retrieved_ids, relevant_ids, k))
        latencies.append(latency)

    return {
        'recall@' + str(k):  round(np.mean(recall_scores), 4),
        'mrr':               round(np.mean(mrr_scores), 4),
        'ndcg@' + str(k):    round(np.mean(ndcg_scores), 4),
        'p50_latency_ms':    round(np.percentile(latencies, 50), 1),
        'p99_latency_ms':    round(np.percentile(latencies, 99), 1),
    }
```

---

## Best Practices

- Use the same embedding model for indexing and querying — never mix models
- Normalize embeddings before storing (L2 normalization) when using cosine similarity
- Use recursive chunking over fixed-size — it respects natural text boundaries
- Add metadata filtering at the vector level — do not post-filter large result sets
- Always evaluate retrieval quality before building the LLM layer on top
- For RAG: retrieve top-20, rerank with a cross-encoder, use top-5 for generation
- Use pgvector for < 1M vectors, Qdrant/Pinecone for larger scale
- Monitor retrieval latency and recall@k in production — both degrade over time

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Mixing embedding models | Incomparable vectors, garbage results | One model per collection, always |
| No metadata filtering | Retrieving irrelevant documents from other sources | Filter by source/tenant at query time |
| Chunks too large | Noisy context dilutes relevant signal | Keep chunks 256-512 tokens |
| Chunks too small | Missing context, incomplete sentences | Ensure overlap and semantic completeness |
| No evaluation | Shipping blind — retrieval quality unknown | Build eval set before production |
| No reranking | Top-k order from ANN is imprecise | Add cross-encoder reranker |
| Exact search on large index | Slow queries at scale | Use HNSW approximate search |
| Not indexing metadata | Slow filtered queries | Create payload indexes in Qdrant |

---

## Related Skills

- **llm-engineering**: For RAG pipeline using vector retrieval
- **postgresql-expert**: For pgvector configuration and tuning
- **machine-learning**: For embedding model fine-tuning
- **data-engineering**: For building embedding pipelines
- **monitoring-expert**: For vector search observability
- **python-expert**: For Python vector database clients