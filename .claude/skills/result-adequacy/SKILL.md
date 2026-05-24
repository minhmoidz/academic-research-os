# SKILL: /result-adequacy
## Purpose
Evaluate whether experimental results are strong enough for the target venue. This is Stage 16 — the gate that must be passed before any paper writing begins. No abstract, introduction, or contributions section may be drafted until this gate returns decision A.

---

## When to Run
- Stage 16 (Result Adequacy Gate) of the research workflow.
- After all planned CONFIRMATORY experiments are complete.
- Before drafting any paper section (abstract, intro, method, results).
- After a pivot, to re-evaluate the new direction's evidence.

---

## Required Inputs
All of the following must exist before this skill can run:

| Input | Source | If Missing |
|-------|--------|------------|
| target_result_contract.md | /target-result-contract | BLOCK — cannot proceed |
| sota_baseline_table.md | /sota-check | BLOCK — cannot proceed |
| results.tsv with CONFIRMATORY rows | experiments | BLOCK — cannot proceed |
| venue_target.md | /venue-target | BLOCK — cannot proceed |
| evidence_ledger.md | /result-backfill or experiment logging | WARN — proceed with caution |

---

## Steps

### Step 1 — Load Gate Reference
Read `.claude/research-os/27_RESULT_ADEQUACY_GATE.md` for decision codes, decision tree, and minimum evidence requirements per venue tier.

### Step 2 — Load the Target Result Contract
Read `target_result_contract.md`. Extract:
- Pass threshold per (dataset, metric).
- Required delta over baseline per dataset.
- Required datasets (all must pass).
- Required baselines (all must be beaten).
- Maximum acceptable std.

### Step 3 — Load Best Confirmed Results
From `results.tsv`, filter: `experiment_type=CONFIRMATORY`, `status=PASS`.
For each (dataset, metric): find the highest-value PASS row.

If no CONFIRMATORY PASS rows exist: assign decision F immediately. Do not continue.

### Step 4 — TRC Compliance Check
For each TRC requirement, evaluate:

| Requirement | Required | Achieved | Pass? |
|-------------|---------|---------|-------|
| Primary metric on Dataset A | [value] | [value] | YES/NO |
| Primary metric on Dataset B | [value] | [value] | YES/NO |
| Delta over [baseline] | [delta] | [delta] | YES/NO |
| Std ≤ max acceptable | [max] | [observed] | YES/NO |
| All required baselines beaten | [list] | [list] | YES/NO |

If ANY required item is NO: the TRC is not fully met.

### Step 5 — SOTA Gap Evaluation
Load `sota_baseline_table.md`. For each (dataset, metric):
```
gap = our_best_confirmed - sota_best
```
Classify:
- `EXCEEDS`: gap > 0 and gap > noise floor
- `COMPETITIVE`: gap is within ±1%
- `BELOW`: gap < 0

If the main claim is "outperforms SOTA" and gap is BELOW for any required dataset: this is a critical failure — assign decision C.

### Step 6 — Ablation Adequacy Check
Read `experiment_matrix.md` and `results.tsv`. Check:
- Are there EXPLORATORY or DIAGNOSTIC runs that isolate each claimed module's contribution?
- Does ablation cover: each component removed individually, baseline without any proposed module?
- Is the number of ablation conditions sufficient for the venue tier?

| Venue Tier | Minimum ablation requirements |
|-----------|------------------------------|
| Tier 1 | Full factorial ablation + interaction effects |
| Tier 2 | Each component individually ablated |
| Tier 3 | At least one ablation condition per main claim |
| Workshop | Any ablation or strong qualitative justification |

### Step 7 — Stability and Variance Check
- Are std values reported across folds/seeds?
- Is the improvement larger than 2× std (signal-to-noise requirement)?
- Are results consistent across datasets (not strong on one and weak on others)?

Signal-to-noise ratio: `delta / std ≥ 2.0` recommended for a confident claim.

### Step 8 — Novelty Support Check
Read `sota_baseline_table.md` and `hypothesis_registry.md`. Confirm:
- No concurrent published paper achieves the same result with the same approach.
- The mechanism claimed (ablation-supported) is distinct from prior methods.

If a concurrent paper reduces novelty: flag and recommend prior-art threat assessment.

### Step 9 — Assign Decision Code
Apply the decision tree from 27_RESULT_ADEQUACY_GATE.md:

| Code | Condition | Action |
|------|-----------|--------|
| **A** | TRC fully met, SOTA gap ≥ 0, ablation complete, std acceptable | PROCEED to Stage 17 (Evidence Freeze) |
| **B** | TRC met on 1 of 2 required datasets | Run /pivot-decision → NARROW_CLAIM or RUN_MORE_EXPERIMENTS |
| **C** | Main claim is "outperforms SOTA" but gap is BELOW on primary dataset | Run /pivot-decision → CHANGE_VENUE or NARROW_CLAIM |
| **D** | TRC threshold not met (below minimum value) | Run /pivot-decision → RUN_MORE_EXPERIMENTS or PIVOT |
| **E** | Ablation insufficient for venue tier | Run more diagnostic experiments; do not write contributions yet |
| **F** | No CONFIRMATORY PASS results | Run /pivot-decision → full pivot required |
| **G** | Std too high (results unstable) | Run more seeds/folds; do not claim until variance is acceptable |

### Step 10 — Write result_adequacy_report.md
```markdown
# Result Adequacy Report

**Date:** [date]
**Decision:** [A/B/C/D/E/F/G]
**Venue:** [name] (Tier [X])

## TRC Compliance
[table from Step 4]

## SOTA Gap
[table from Step 5]

## Ablation Adequacy
[assessment from Step 6]

## Stability
[assessment from Step 7]

## Novelty Support
[assessment from Step 8]

## Decision Rationale
[2–4 sentences]

## Required Next Action
[specific action — or "PROCEED to Stage 17" if decision A]
```

### Step 11 — Log Decision
Append to `decision_log.md`:
```
DEC-[N] | [date] | RESULT_ADEQUACY_GATE | Decision [X]: [summary] | Next: [action]
```

### Step 12 — Update project_state.md
```
result_adequacy_complete: true
result_adequacy_decision: [A-G]
result_adequacy_date: [date]
paper_writing_authorized: [true if A, false otherwise]
```

---

## Output Files
- `result_adequacy_report.md` — created
- `decision_log.md` — appended
- `project_state.md` — updated

---

## Safety Rules (Non-Negotiable)
1. **Never pass this gate if the TRC is not fully met.** TRC existence is required; TRC compliance is required.
2. **Never pass this gate if the main claim is "outperforms" and gap_over_prior is negative** on the primary dataset.
3. **If decision is not A:** Claude must NOT draft abstract, introduction, or contributions section. These sections may only be drafted after decision A.
4. **Decision must be logged in decision_log.md** before any paper writing begins.
5. **Do not allow creative reframing to avoid a gate failure.** If results don't meet the TRC: the gate fails; run /pivot-decision.
6. **Never relax std requirements** because the mean improvement looks good — noisy results are not reliable evidence.
