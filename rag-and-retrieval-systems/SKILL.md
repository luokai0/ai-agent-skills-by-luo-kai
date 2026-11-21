---
name: rag-and-retrieval-systems
description: Use when designing, building, evaluating, debugging, or operating retrieval-augmented generation (RAG) pipelines, including document ingestion, chunking, embedding, vector or hybrid search, reranking, grounding of LLM answers, and retrieval quality evaluation.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Rag And Retrieval Systems

## Purpose and boundaries

This skill guides the design and assessment of pipelines that retrieve evidence from a corpus and supply it to a language model for grounded answers. It covers ingestion, parsing, chunking, indexing, query processing, retrieval, reranking, context assembly, answer generation constraints, and evaluation.

In scope: diagnosing poor answers by separating retrieval failures from generation failures; choosing chunking, index, and ranking strategies; building offline evaluation sets; defining grounding and citation rules; operational concerns such as re-indexing, freshness, and access control.

Out of scope: general model training, fine-tuning decisions, prompt engineering unrelated to grounding, and legal or regulatory certification of outputs. Do not claim that a RAG system is compliant, accurate, or safe for a regulated decision without independent validation.

## Inputs and assumptions

Collect before designing:
- Corpus description: source systems, document types, languages, size, update frequency, and expected growth.
- Query profile: sample of real user questions (at least 50 where available), expected answer form, and tolerance for omission.
- Access model: per-document permissions, tenant boundaries, and whether retrieved text may leave the environment.
- Ground truth: any existing question-answer pairs, relevance judgments, or subject matter expert availability.
- Constraints: latency budget, cost per query, hosting limits, and approved model and embedding providers.

Assumptions must be written down. If the corpus is unavailable for inspection, state that all chunking and ranking recommendations are provisional.

## Operating workflow

1. Inspect the corpus. Sample at least 30 documents across types and check parse quality: tables, headers, footnotes, scanned pages, and OCR errors. Record the fraction of content lost in parsing.
2. Define the unit of retrieval. Choose chunk boundaries that follow document structure (section, clause, record, or table row) before falling back to fixed token windows. Typical starting points are 200 to 500 tokens with 10 to 20 percent overlap, adjusted by measurement, not assumed.
3. Attach metadata to every chunk: source identifier, version or effective date, section path, access labels, and language. Metadata drives filtering and citation; retrofitting it is costly.
4. Select the index. Use dense vectors for semantic matching, lexical (BM25-style) search for exact identifiers, codes, and names, and combine them when the corpus contains both. Verify current index and filter syntax against the official documentation of the chosen store, as these change between releases.
5. Build a retrieval pipeline with a candidate depth (for example, retrieve 50 to 100, rerank to 5 to 10). Add a cross-encoder or other reranker only after measuring recall at the candidate stage.
6. Assemble context: deduplicate near-identical chunks, order by relevance or by document logic, respect a token budget, and keep source identifiers attached to each passage.
7. Constrain generation: instruct the model to answer only from supplied passages, to cite passage identifiers, and to state when evidence is insufficient.
8. Evaluate (see Verification) and iterate on one variable at a time.

## Decision gates

Gate A, before indexing: proceed only if parse loss is below 5 percent on the sampled documents, or losses are understood and accepted by the owner.

Gate B, before choosing retrieval method: if exact-match queries (identifiers, part numbers, citations) make up more than 10 percent of the query sample, hybrid retrieval is required.

Gate C, before adding reranking: proceed only if recall at candidate depth is at least 85 percent on the evaluation set and top-k precision is the bottleneck.

Gate D, before production use: require an evaluation set of at least 100 labeled questions with gold source passages, a regression baseline, and documented access-control tests.

Gate E, before any external transfer of corpus text, embeddings, or query logs to a third-party service: obtain explicit approval from the data owner and security reviewer.

## Verification and evidence

Measure retrieval and generation separately.

Retrieval metrics: recall@k against gold passages, mean reciprocal rank, and precision@k. Report them per query category.

Generation metrics: faithfulness (claims supported by retrieved passages), citation accuracy (cited passage actually contains the claim), and answer correctness against reference answers. Use human review on a stratified sample; automated judges must be calibrated against that sample and their agreement reported.

Operational metrics: p95 latency per stage, cost per query, index freshness lag, and failure rate of ingestion jobs.

Access control tests: for a set of test users, confirm that no restricted passage appears in results or context, including through reranking and caching layers.

Record the corpus snapshot identifier, index build version, embedding model identifier, and prompt version with every evaluation run so results are reproducible.

## Failure handling

- Low recall: inspect the failing queries. Common causes are chunks that split an answer across boundaries, missing metadata filters, or vocabulary mismatch. Try structural chunking, query rewriting, or hybrid search before changing models.
- Right passage retrieved but wrong answer: a generation problem. Tighten grounding instructions, reduce context noise, or lower the number of passages.
- Fabricated citations: validate citation identifiers programmatically against the context set and reject answers that fail.
- Stale answers: check ingestion job logs and document version dates; do not silently serve old versions.
- Parse failures on tables or scans: route those documents to a fallback path and flag answers that depend on them.
- If a fix degrades another metric, revert and record the trade-off.

## Deliverable contract

Deliver:
1. Corpus and query assessment summary with parse loss figures and the sample size used.
2. Pipeline specification: chunking rules, metadata schema, index type, retrieval depth, reranking decision, and context budget.
3. Evaluation report: dataset description, metric tables per query category, and reproducibility identifiers.
4. Access control test results.
5. Open risks and unverified items, including any version-sensitive API details that still require confirmation against current official documentation.

Do not present benchmark numbers that were not measured on the user's data. Do not describe the system as accurate, secure, or compliant beyond what the reported evidence shows. Do not send corpus content or user queries to external services without Gate E approval, and do not delete or overwrite existing indexes, snapshots, or evaluation baselines without explicit confirmation.