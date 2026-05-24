# Experiment Matrix

Locked on: 2026-05-12 (after TRC-001 signed)

---

## Task

Retrieval evaluation via Recall@10 and NDCG@10 on scientific QA datasets.

## Datasets

| Dataset | N samples | N classes | Feature type | Split protocol | File path |
|---------|-----------|-----------|-------------|----------------|-----------|
| SciDocs-Retrieval | 500 | — (ranking) | TF-IDF / BM25 | Single eval set, seed=42 | data/scidocs/ |
| BEIR-SciQ | 1000 | — (ranking) | TF-IDF / BM25 | Single eval set, seed=42 | data/beir-sciq/ |

## Baselines

| Method | Code path | Config file | Verified runnable? | Expected runtime |
|--------|-----------|-------------|-------------------|-----------------|
| BM25 | retrieval/bm25.py | configs/bm25.yaml | ✓ | ~5 min |
| Dense bi-encoder | retrieval/biencoder.py | configs/biencoder.yaml | ✓ | ~30 min |

## Proposed Method

| Config | Key components | Result dir |
|--------|---------------|-----------|
| bm25_rerank | BM25 + cross-encoder re-ranker (top-50 → top-10) | results/reranker/ |
| bm25_qe | BM25 + query expansion | results/qexpansion/ |
| bm25_qe_rerank | BM25 + query expansion + re-ranker | results/combined/ |

## Primary Metric

Recall@10 on SciDocs-Retrieval (primary); NDCG@10 on BEIR-SciQ (secondary)

---

## Exploratory Experiments (Type 1)

| Exp ID | Hypothesis | Config change | Dataset | Status | Result |
|--------|-----------|--------------|---------|--------|--------|
| BASELINE | — | BM25 only | SciDocs | DONE | Recall@10 = 0.612 |
| EXP-001 | HYP-001 | + re-ranker | SciDocs | DONE (PASS) | Recall@10 = 0.681 |
| EXP-002 | HYP-002 | + query expansion | BEIR-SciQ | PENDING | — |

## Confirmatory Experiments (Type 3 — require TRC-001)

| Exp ID | Hypothesis | Config | Datasets | Seeds | Status |
|--------|-----------|--------|---------|-------|--------|
| EXP-C1 | HYP-001 | bm25_rerank | SciDocs + BEIR-SciQ | 42, 0, 1 | PENDING |
| EXP-C2 | HYP-002 (if supported) | bm25_qe | SciDocs + BEIR-SciQ | 42, 0, 1 | PENDING |
| EXP-C3 | Combined | bm25_qe_rerank | SciDocs + BEIR-SciQ | 42, 0, 1 | PENDING |

## Ablation Designs

| Config | Components active | Purpose |
|--------|------------------|---------|
| BM25 only | Neither | Baseline |
| + re-ranker | Re-ranker only | Isolate re-ranker contribution |
| + query expansion | QE only | Isolate QE contribution |
| + both | Both | Full model |

---

## Protected Files (Never Modify)

- `evaluate.py` — evaluation harness
- `data/` — all dataset files and splits
- `results/baseline/` — BM25 baseline results
