# Project State

working_title: "Re-ranking for Scientific Literature Retrieval: Cross-Encoder Re-ranking Improves Recall on SciDocs"
project_id: toy-reranker-2026
last_updated: 2026-05-15T14:32:00Z
session_count: 7

---

## Current Stage

current_stage: 12
stage_name: Exploratory Experiments
stage_description: Running first experiments to test HYP-001 and HYP-002

---

## Hypothesis

original_hypothesis: "A cross-encoder re-ranker applied after BM25 retrieval will improve Recall@10 on scientific QA benchmarks by at least 5 percentage points."
current_hypothesis: "Same as original — not yet contradicted."
hypothesis_status: testing

---

## Research Direction

See `research_direction.md` (v1 — no pivots yet)

main_claim_current: "Cross-encoder re-ranking improves Recall@10 on SciDocs-Retrieval by ≥5pp over BM25."
scope_limits:
  - Evaluated on SciDocs-Retrieval and BEIR-SciQ only
  - BM25 retrieval backend only (no dense retrieval comparison yet)

---

## Completed Stages

completed_stages:
  - 0: System Readiness
  - 1: Idea Intake (paper_brief.md created)
  - 2: Hypothesis Registration (HYP-001, HYP-002)
  - 3: Venue Targeting (venue_target.md: EMNLP Findings, Tier 3)
  - 4: Research Direction Lock (research_direction.md v1)
  - 5: Literature Review (literature-matrix.md: 12 rows)
  - 6: Prior-Art/SOTA Check (threat: Medium — two prior papers on re-ranking for SciDocs)
  - 7: Gap Validation (gap: no prior work combines query expansion + re-ranking)
  - 8: Contribution Mapping (contribution_contract.md created)
  - 9: Target Result Contract (TRC-001 signed)
  - 10: Experiment Planning (experiment_matrix.md created)
  - 11: Environment Setup (evaluate.py confirmed runnable; BASELINE logged)

---

## Artifacts

completed_artifacts:
  - paper_brief.md
  - project_state.md
  - hypothesis_registry.md
  - venue_target.md
  - research_direction.md
  - literature-matrix.md
  - prior_art_competition_table.md
  - sota_baseline_table.md
  - contribution_contract.md
  - target_result_contract.md
  - experiment_matrix.md
  - results.tsv
  - experiment_notes.md

missing_artifacts:
  - evidence_ledger.md (partially filled — needs EXP-001 entry)
  - claim-evidence-table.md (not started — Stage 17)
  - result_adequacy_report.md (not started — Stage 16)

---

## Active Blockers

- HYP-002 (query expansion) experiment not yet run — EXP-002 PENDING
- Need to verify SciDocs-Retrieval split protocol (patient vs. document level)

---

## TODO Markers

active_todo_markers: 3
  TODO_RESULT_NEEDED: 2 (EXP-002 and EXP-003 not yet run)
  TODO_EVIDENCE_NEEDED: 1 (prior work on query expansion for scientific QA)

---

## Active Experiments

| Exp ID | Hypothesis | Status | Metric |
|--------|-----------|--------|--------|
| BASELINE | — | DONE | Recall@10 = 0.612 |
| EXP-001 | HYP-001 | DONE (PASS) | Recall@10 = 0.681 |
| EXP-002 | HYP-002 | PENDING | — |

---

## Current Best Result

best_exp_id: EXP-001
best_metric: Recall@10 = 0.681 (SciDocs-Retrieval, seed=42)
baseline_metric: Recall@10 = 0.612
delta: +0.069 (+6.9pp)

---

## Evidence Status

evidence_status: NOT_FROZEN
evidence_ledger_entries: 1
claim_evidence_table_entries: 0

---

## Gate Status

gate_1_prior_art: PASSED (2026-05-10)
gate_2_trc: SIGNED (2026-05-12, TRC-001)
gate_3_adequacy: NOT_STARTED
gate_4_freeze: NOT_STARTED

---

## Next Safe Action

Run EXP-002 (HYP-002: query expansion). Then evaluate whether both HYP-001 and HYP-002 are supported before planning confirmatory experiments.
