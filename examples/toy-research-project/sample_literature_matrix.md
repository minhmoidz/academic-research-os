# Literature Matrix

Built from paper-qa index on 2026-05-10. Only cells verified via paper-qa queries are filled.
Cells marked `?` require manual verification or additional pqa queries.

---

## Query log

```bash
pqa ask "What methods improve retrieval for scientific literature?"
pqa ask "Cross-encoder re-ranking information retrieval 2022 2023"
pqa ask "Query expansion scientific QA benchmark results"
pqa ask "BM25 baseline Recall@10 SciDocs benchmark"
pqa ask "BEIR benchmark dense vs sparse retrieval comparison"
```

---

## Matrix

| # | Paper (placeholder — fill with pqa results) | Year | Method | Dataset | Metric | Value | Gap vs. ours | Notes |
|---|---------------------------------------------|------|--------|---------|--------|-------|-------------|-------|
| 1 | [Paper A — dense retrieval for scientific QA] | 2023 | Dense bi-encoder | SciDocs | Recall@10 | ? | TODO_SOTA_NEEDED | pqa found paper but AUC not extracted |
| 2 | [Paper B — cross-encoder re-ranking survey] | 2022 | Cross-encoder ensemble | BEIR | NDCG@10 | ? | TODO_SOTA_NEEDED | survey paper; no single-model number |
| 3 | [Paper C — query expansion with domain vocab] | 2023 | Vocabulary expansion | BEIR-SciQ | NDCG@10 | ~0.47 | +0.01pp | pqa: "around 47% NDCG@10 reported" |
| 4 | [Paper D — BM25 baseline characterization] | 2021 | BM25 | SciDocs | Recall@10 | ~0.60 | -0.07pp (ours better) | pqa confirmed value |
| 5 | [Paper E — hybrid retrieval scientific domain] | 2024 | BM25 + bi-encoder hybrid | SciDocs | Recall@10 | ? | TODO_SOTA_NEEDED | most recent; need pqa re-query |

---

## Gap Statement

Based on the literature matrix:
- BM25 baseline on SciDocs Recall@10 is ~0.60 (confirmed via Paper D)
- Query expansion (Paper C) achieves ~0.47 NDCG@10 on BEIR-SciQ
- No paper combines cross-encoder re-ranking WITH query expansion for scientific QA
- The gap: our contribution (re-ranking alone; re-ranking + query expansion) has not been directly compared on both benchmarks in a single study

**Remaining TODOs:**
- TODO_SOTA_NEEDED: confirm best Recall@10 on SciDocs (Papers A, E)
- TODO_EVIDENCE_NEEDED: prior work combining query expansion + re-ranking
