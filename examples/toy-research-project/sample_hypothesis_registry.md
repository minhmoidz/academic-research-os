# Hypothesis Registry

All hypotheses must be registered here before any experiment tests them. Status transitions: pending → testing → supported / partially_supported / contradicted / inconclusive.

---

## HYP-001

- **id:** HYP-001
- **registered:** 2026-05-08
- **status:** supported
- **type:** performance
- **claim:** If a cross-encoder re-ranker is applied to the top-50 BM25 candidates, then Recall@10 on SciDocs-Retrieval will increase by at least 5 percentage points compared to BM25 alone.
- **rationale:** BM25 retrieves by term overlap without semantic understanding. A cross-encoder can score query-document relevance using bidirectional attention, which should reorder candidates more accurately. The 5pp threshold is chosen because it exceeds the measurement noise (estimated ±1pp based on prior work with the same dataset).
- **prediction:** Recall@10 will increase from ~0.60 (BM25) to ≥ 0.65 with re-ranking.
- **success_criterion:** Recall@10 ≥ 0.65 on SciDocs-Retrieval (seed=42, full eval set)
- **experiment:** EXP-001
- **evidence:** EXP-001 → Recall@10 = 0.681 (SciDocs-Retrieval); logged 2026-05-14
- **conclusion:** HYP-001 SUPPORTED. Re-ranker improves Recall@10 by +6.9pp (0.612 → 0.681), exceeding the 5pp threshold.

---

## HYP-002

- **id:** HYP-002
- **registered:** 2026-05-08
- **status:** pending
- **type:** performance
- **claim:** If query expansion using synonyms from a scientific vocabulary is applied before BM25 retrieval, then NDCG@10 on BEIR-SciQ will increase by at least 3 percentage points compared to unexpanded BM25.
- **rationale:** Scientific queries often use precise terminology that may not match document vocabulary. Expanding queries with synonyms (e.g., "neural network" → "deep learning", "artificial neural network") increases recall. BEIR-SciQ contains questions with both formal and informal phrasing.
- **prediction:** NDCG@10 will increase from ~0.45 (BM25) to ≥ 0.48 with query expansion.
- **success_criterion:** NDCG@10 ≥ 0.48 on BEIR-SciQ (seed=42)
- **experiment:** EXP-002 (NOT YET RUN — TODO_RESULT_NEEDED: run EXP-002)
- **evidence:** none yet
- **conclusion:** n/a
