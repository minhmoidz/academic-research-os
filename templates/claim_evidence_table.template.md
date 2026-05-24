# Claim-Evidence Table

Links every paper claim to its evidence ID. Required before Evidence Freeze (Stage 17).

---

| Claim ID | Section | Claim text | Evidence ID | Source file | Status |
|----------|---------|-----------|-------------|-------------|--------|
| C-001 | [e.g., IV.B] | [Exact claim text as it appears in the paper] | EVID-EXP-001 | results/[method]/summary.json | ✓ |
| C-002 | [Section] | [Claim text] | EVID-EXP-002 | results/[method]/summary.json | ✓ |
| C-003 | [Section] | [Claim about dataset size or composition] | EVID-DATA-001 | data/[dataset]/README.md | ✓ |
| C-004 | [Section] | [Claim about prior work] | EVID-LIT-001 | papers/[paper.pdf] | ✓ |
| C-005 | [Section] | [Ablation claim] | EVID-EXP-005 | results/ablation/summary.json | ✓ |
| C-006 | [Section] | [Claim needing evidence] | TODO_RESULT_NEEDED: [run] | — | ✗ BLOCKED |

---

## Rules

- Every row in a paper table must have a corresponding C-NNN entry here
- Every C-NNN entry must point to a valid EVID entry in `evidence_ledger.md`
- EVID entries must point to PASS or BASELINE rows in `results.tsv` (not FAIL or CRASH)
- Claims with status ✗ BLOCKED must be written as `TODO_RESULT_NEEDED:` in the paper
- This table is frozen at Stage 17 — no new claims after the Evidence Freeze

## Evidence ID Types

| ID prefix | Evidence type |
|-----------|--------------|
| EVID-EXP-N | Experiment result from results.tsv |
| EVID-LIT-N | Literature claim from paper-qa |
| EVID-DATA-N | Dataset statistic from verified source |
| EVID-REPO-N | Code or implementation evidence |
