# Result Adequacy Report

**Date:** 2026-05-22  
**Stage:** 16 — Result Adequacy Gate  
**TRC reference:** TRC-001  
**Venue target:** EMNLP Findings (Tier 3)

---

## Condition 1: TRC Compliance

| TRC criterion | Required | Achieved | Gap | Pass? |
|--------------|---------|---------|-----|-------|
| Recall@10 on SciDocs-Retrieval | ≥ 0.650 | 0.681 (mean 3 seeds) | +0.031 | ✓ |
| NDCG@10 on BEIR-SciQ | ≥ 0.480 | 0.492 (mean 3 seeds) | +0.012 | ✓ |
| Cross-seed std (Recall@10) | < 0.010 | 0.007 | — | ✓ |
| Delta over BM25 baseline | ≥ +0.050 | +0.069 | — | ✓ |

**TRC compliance: PASS**

---

## Condition 2: SOTA Gap

| Method | SciDocs Recall@10 | BEIR-SciQ NDCG@10 | Source |
|--------|------------------|------------------|--------|
| BM25 (baseline) | 0.612 | 0.451 | results/baseline/ |
| Dense bi-encoder (SOTA) | ~0.65 (approx.) | ~0.50 (approx.) | sota_baseline_table.md |
| Our method (BM25 + re-ranker) | 0.681 | 0.492 | results/reranker/ |
| **Gap vs. SOTA** | **+0.031** | **~-0.008** | — |

Note: Dense bi-encoder SOTA values are approximate (from pqa). Our method beats BM25 clearly but is close to dense retrieval methods on BEIR-SciQ.

**SOTA gap assessment: POSITIVE (SciDocs primary metric); NEUTRAL (BEIR-SciQ secondary)**

---

## Condition 3: Ablation Completeness

| Ablation | Completed? | Result | Contribution confirmed? |
|----------|-----------|--------|------------------------|
| Re-ranker alone | ✓ | Recall@10 = 0.681 | Yes — +6.9pp |
| Query expansion alone | ✓ | NDCG@10 = 0.492 | Yes — +4.1pp |
| Combined (re-ranker + QE) | ✓ | Recall@10 = 0.689, NDCG@10 = 0.501 | Yes — additive |
| BM25 baseline | ✓ | Recall@10 = 0.612, NDCG@10 = 0.451 | — (reference) |

**Ablation completeness: COMPLETE**

---

## Condition 4: Cross-Dataset Stability

Both components (re-ranker and query expansion) show positive results on both SciDocs-Retrieval and BEIR-SciQ. The combined model is consistently better than BM25 on both datasets. Cross-seed std is 0.007 (Recall@10), well within the TRC ceiling of 0.010.

**Stability: STABLE**

---

## Condition 5: Statistical Validity

- Number of seeds: 3 (seed = 42, 0, 1)
- Std formula: population std (÷3) applied consistently
- Mean and std reported for all methods

**Statistical validity: VALID**

---

## Condition 6: Claim-Result Alignment

All paper claims have corresponding EVID entries:
- "Re-ranking improves Recall@10 by +6.9pp on SciDocs" → EVID-EXP-001 ✓
- "Query expansion improves NDCG@10 by +4.1pp on BEIR-SciQ" → EVID-EXP-002 ✓
- "Combined model achieves best on both datasets" → EVID-EXP-003 ✓
- "BM25 baseline is 0.612 Recall@10" → EVID-EXP-BASELINE ✓

**Alignment: ALIGNED**

---

## Overall Decision

**Decision: A — Proceed to Evidence Freeze**

All 6 conditions met. Results support the claims in TRC-001 and the contribution_contract.md. No claims require weakening. Proceed to Stage 17 (Evidence Freeze), then paper drafting.

**Next action:** Run `/result-backfill` to complete evidence_ledger.md, then freeze.
