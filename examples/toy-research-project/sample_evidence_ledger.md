# Evidence Ledger

All evidence entries for the toy research project. Frozen at Stage 17.

---

## EVID-EXP-001

**Type:** EXP (experiment result)  
**Experiment ID:** EXP-001  
**Commit hash:** a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0  
**Date logged:** 2026-05-14  
**Method:** BM25 + cross-encoder re-ranker (top-50 → top-10)  
**Dataset:** SciDocs-Retrieval (500 papers, full eval set)  
**Metric:** Recall@10  
**Value:** 0.681 (seed=42)  
**Status:** PASS  
**Source file:** results/reranker/scidocs/fold_results.json  
**Computed by:** evaluate.py --dataset scidocs --metric recall@10  
**Supports hypothesis:** HYP-001  
**Supports claim:** "Cross-encoder re-ranking improves Recall@10 on SciDocs-Retrieval from 0.612 to 0.681 (+6.9pp)"  
**Paper location:** Table I, row "BM25 + Re-ranker", column "SciDocs Recall@10"

---

## EVID-EXP-BASELINE

**Type:** EXP (baseline result)  
**Experiment ID:** BASELINE  
**Commit hash:** 0f1e2d3c4b5a6f7e8d9c0b1a2f3e4d5c6b7a8f9e  
**Date logged:** 2026-05-13  
**Method:** BM25 (no re-ranking, no query expansion)  
**Dataset:** SciDocs-Retrieval (500 papers)  
**Metric:** Recall@10  
**Value:** 0.612 (seed=42)  
**Status:** BASELINE  
**Source file:** results/baseline/scidocs/fold_results.json  
**Computed by:** evaluate.py --dataset scidocs --metric recall@10  
**Supports claim:** "BM25 baseline achieves Recall@10 = 0.612 on SciDocs-Retrieval"  
**Paper location:** Table I, row "BM25", column "SciDocs Recall@10"

---

## EVID-DATA-001

**Type:** DATA (dataset statistic)  
**Date verified:** 2026-05-09  
**Dataset:** SciDocs-Retrieval  
**Claim:** SciDocs-Retrieval evaluation set contains 500 scientific papers with query-relevance annotations  
**Source:** data/scidocs/README.md (line 12) + official SciDocs paper  
**Verified by:** `wc -l data/scidocs/queries.jsonl` → 500  
**Supports claim:** "We evaluate on SciDocs-Retrieval (500 documents)"  
**Paper location:** Section III (Experimental Setup), dataset description paragraph

---

## EVID-LIT-001

**Type:** LIT (literature evidence)  
**Date verified:** 2026-05-10  
**Query used:** `pqa ask "BM25 baseline Recall@10 SciDocs"`  
**Claim supported:** "BM25 achieves approximately 60% Recall@10 on SciDocs, consistent with prior work"  
**Source:** [Paper D] — pqa response: "Paper D reports BM25 Recall@10 of approximately 0.60 on SciDocs"  
**Confidence:** Medium (pqa found approximate value; exact value in paper may vary)  
**Paper location:** Section III, Related Work paragraph on BM25 baselines
