---
name: analytics-vector-retrieval
description: Use when designing, indexing, querying, or evaluating vector retrieval over analytical datasets (embeddings stored alongside tabular or warehouse data), including choosing embedding dimensions, index types, metadata filters, hybrid search, and recall or latency tradeoffs.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Analytics Vector Retrieval

## Purpose and boundaries

This skill guides an agent through building and assessing nearest-neighbor retrieval over analytical data: event logs, product catalogs, support tickets, documents with structured attributes, and similar corpora that are queried with both semantic similarity and SQL-style filters. It covers embedding storage layout, index selection, filtered search, hybrid lexical-plus-vector ranking, recall measurement, and capacity planning.

It does not cover: training or fine-tuning embedding models, general OLAP modeling unrelated to similarity search, generative answer synthesis, or production cluster provisioning. Those require separate skills or human owners.

## Inputs and assumptions

Collect before designing anything:

- Corpus size now and at 12 months; daily ingest rate; update and delete rate.
- Embedding model name, output dimension, normalization behavior, and license terms (verify against the model provider's current documentation).
- Query patterns: top-k value, required filters (tenant, date range, category), latency budget at p95, freshness requirement (seconds, minutes, or daily batch).
- Target store: state whether the platform is a dedicated vector database, a warehouse vector feature, or a relational extension. Capabilities differ by version; mark every index option as "verify against current official documentation" until confirmed.
- A labeled or judged evaluation set: at least 200 query-result pairs with relevance grades, or a documented proxy such as click-through with known bias.

If any of these are missing, state the gap and proceed only with explicitly labeled assumptions.

## Operating workflow

1. **Define the retrieval contract.** Write one sentence per query type: what is returned, ranked by what, under which filters, within what latency.
2. **Fix the embedding space.** Record model, dimension, distance metric (cosine, dot product, or L2), and whether vectors are normalized. Mixing models or metrics within one column is a defect; reject it.
3. **Design the table layout.** Keep one row per embeddable entity with a stable primary key, a vector column, a model-version column, and filterable scalar columns. Store the model version so re-embedding can run as a parallel backfill.
4. **Select the index.** Compare approximate indexes (graph-based, inverted-file with quantization) against exact scan. For corpora under roughly tens of thousands of rows, exact scan is often sufficient; measure before adding an index. Record build time, memory, and update cost for each candidate.
5. **Plan filtered search.** Restrictive filters (selectivity below about 1 percent) can collapse approximate recall. Test pre-filtering versus post-filtering with the actual predicate distribution. Partition by tenant or time when the filter is always present.
6. **Design hybrid ranking if needed.** Combine lexical score and vector score with reciprocal rank fusion or a weighted sum over normalized scores. Tune on the evaluation set, not by intuition.
7. **Run a baseline.** Compute exact top-k as ground truth for a sample of queries, then compare approximate results at each index parameter setting.
8. **Document the plan** using the deliverable contract below.

## Decision gates

- **Gate A (Model and metric):** Proceed only if the query and document embeddings come from the same model version and the metric matches how the model was trained to be used.
- **Gate B (Index):** Adopt an approximate index only if recall@k against exact search meets the agreed threshold (default target: 0.95 at k=10, unless the owner specifies otherwise) at the required latency.
- **Gate C (Filters):** Adopt a filter strategy only if recall holds across the 10 most common filter values and across the least common values that carry real traffic.
- **Gate D (Freshness):** If updates must appear within a stated window, verify the index insert path meets that window under peak ingest. Batch rebuilds are acceptable only when the owner accepts the lag.
- **Gate E (Data movement):** Copying customer or personal data into an external embedding service, or into a new storage location, requires explicit approval from the data owner.

## Verification and evidence

Report these measurements with the exact configuration used:

- Recall@k versus exact search on at least 500 sampled queries, with confidence bounds if sample variance is high.
- Latency at p50, p95, and p99 under concurrency matching expected peak.
- Index build time, memory footprint, and rebuild duration at target scale.
- Filter selectivity histogram and recall by filter bucket.
- For hybrid ranking, relevance metric (nDCG@10 or precision@10) against the baseline lexical ranker, with the judged-set size stated.

Do not state a result without its configuration, sample size, and date. Do not extrapolate scale results from small tests without labeling them as projections.

## Failure handling

- **Low recall:** Increase search breadth parameters one step at a time, re-measure, and stop when returns flatten. If recall remains low, check for embedding drift, mixed models, or normalization mismatch before changing the index.
- **Latency breach:** Profile whether time goes to filter evaluation, candidate fetch, or distance computation. Reduce candidate count or add partitioning before lowering recall targets.
- **Ingest backlog:** Switch to batched upserts and report the freshness gap to the owner. Do not silently drop writes.
- **Unexpected empty results:** Check filter types (string versus integer, timezone handling) before concluding the index is wrong.
- **Version uncertainty:** When a parameter name, index type, or limit is not confirmed in current documentation, label it unverified and do not present it as fact.

## Deliverable contract

Produce a single document containing:

1. Retrieval contract (per query type).
2. Embedding specification: model, dimension, metric, normalization, version field.
3. Schema and index plan with rationale and rejected alternatives.
4. Filter strategy with selectivity analysis.
5. Evaluation results table: configuration, recall@k, latency percentiles, build cost, sample size.
6. Open risks, unverified platform details, and required approvals (including any data movement under Gate E).
7. Rollback path: how to revert to exact search or the prior index without data loss.

Do not:

- Deploy schema changes, drop indexes, or re-embed production tables without written approval.
- Send raw records to external embedding APIs without approval under Gate E.
- Claim compliance, privacy, or security guarantees for any service.
- Report benchmark numbers that were not measured in this engagement.
- Specify exact parameter names or limits without verification against current official documentation.

## Ultron routing contract

**Choose this skill when:** the problem is the retrieval layer over analytical or structured corpora: embedding/index layout, nearest-neighbor search, hybrid lexical/vector retrieval, metadata filters, query latency, recall, capacity, and SQL-style constraints.

**Choose `rag-and-retrieval-systems` when:** retrieved material is being assembled into a language-model context and the full grounded-answer pipeline must be designed or evaluated, including parsing, chunking, reranking, citation, generation constraints, and answer quality.

**Handoff contract:** this skill returns index and query contracts, recall/latency measurements, filter semantics, source identifiers, and candidate ranking behavior. The RAG skill defines how those candidates become traceable evidence and how generated answers must cite and abstain. Do not use answer quality alone to diagnose an index problem; isolate retrieval metrics first.

**Why the boundary exists:** vector search is a retrieval engine capability; RAG is the broader evidence-to-answer system that may use it.
