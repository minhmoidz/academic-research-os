# Skill: /hypothesis-tournament

**Command:** `/hypothesis-tournament`  
**Purpose:** Run a Successive Halving tournament across multiple APPROVED hypothesis candidates to identify the best one using a fraction of the compute required to run all candidates fully.  
**Stage:** 11.5 (after Stage 10 Proxy Protocol, before Stage 12 Exploratory Experiments)  
**Protocol file:** `.claude/research-os/32_HYPOTHESIS_TOURNAMENT.md`

---

## When This Skill Is Invoked

- User has ≥ 3 hypothesis candidates with `validation_status: APPROVED` in `hypothesis_registry.md`
- User explicitly types `/hypothesis-tournament`
- Gap Scout (`/gap-scout`) returned multiple candidates and user chose "Approve all"
- Research OS routing from Stage 10 suggests tournament (multiple candidates survived proxy individually)

---

## Required Inputs

| Input | Source | Required |
|-------|--------|----------|
| List of HYP-NNN IDs to include | User provides or auto-detected from hypothesis_registry.md | Yes |
| `project_profile.md` | Project root | Yes — must contain train_command, metric_extract, proxy_time, full_run_time, protocol, k, seed |
| `hypothesis_registry.md` | Project root | Yes — all listed HYP-NNN must have validation_status: APPROVED |
| `experiment_matrix.md` | Project root | Yes — must exist (created at Stage 7) |
| `results.tsv` | Project root | Yes — baseline_metric must be recorded |
| Git working tree | Project | Yes — must be clean (no uncommitted changes) |

---

## Precondition Checks (run before any experiment)

1. Verify git status is clean: `git status --short` must return empty output
2. Read `hypothesis_registry.md` — confirm all listed HYP-NNN have `validation_status: APPROVED`
3. Read `project_profile.md` — confirm all required fields exist
4. Read `results.tsv` — confirm baseline row exists with a numeric metric value
5. Confirm `experiment_matrix.md` exists
6. If any check fails: report the specific failure and stop — do not start experiments

---

## Execution Steps

### Step 1 — Read configuration
Read `project_profile.md`. Extract:
- `train_command`: command template with `{config}`, `{fold}`, `{seed}` placeholders
- `metric_extract`: shell command or regex to extract primary_metric from stdout/log
- `proxy_time`: estimated runtime per candidate for proxy run
- `full_run_time`: estimated runtime per fold for full run
- `k`: number of folds in full protocol
- `seed`: fixed random seed

### Step 2 — Identify candidates
Read `hypothesis_registry.md`. List all HYP-NNN entries with `validation_status: APPROVED`. If user specified a subset, use only those. Confirm count ≥ 3 (if <3, abort: "Tournament requires ≥3 APPROVED candidates. Run individual proxy-to-full pipeline instead.").

### Step 3 — Compute and display budget
Using the formula from Section 4 of `32_HYPOTHESIS_TOURNAMENT.md`:
```
N   = candidate count
proxy_budget   = N × proxy_time
round1_budget  = ceil(N/2) × full_run_time × 1
round2_budget  = ceil(N/4) × full_run_time × 3  [0 if ceil(N/2)==1]
full_budget    = 1 × full_run_time × k

total = proxy_budget + round1_budget + round2_budget + full_budget
naive = N × full_run_time × k
savings = (1 - total/naive) × 100
```
Display the budget table clearly.

### Step 4 — Human Checkpoint 2 (REQUIRED — do not skip)
```
Tournament budget: [X.X] h total ([Y]% savings vs naive [Z] h)
  Round 0 (proxy, all N candidates):  [X] h
  Round 1 (1-fold, top 50%):          [X] h
  Round 2 (3-fold, top 25%):          [X] h  [or "skipped if 1 survivor"]
  Round 3 (K-fold, winner):           [X] h

Proceed with tournament? (y/n)
```
**Do not run any experiments until user confirms.**

### Step 5 — Round 0: PROXY (all candidates)
For each candidate in parallel (or sequentially if parallel not possible):
- Substitute candidate's config into `train_command` proxy variant
- Fix: fold=0, seed from project_profile
- Run and capture output
- Extract metric using `metric_extract`
- Log to `results.tsv` as `HYP-NNN-ROUND0-PROXY` with status `PROXY_PASS`, `PROXY_NAN`, or `PROXY_OOM`
- If run fails: log as `PROXY_NAN` with note, do not re-run

After all Round 0 runs complete:
- Sort candidates by proxy metric descending
- Kill bottom 50% (round down survivors: e.g., N=5 → keep 3, N=4 → keep 2)
- Display Round 0 results table with survivors and eliminated candidates clearly labeled

### Step 6 — Round 1: 1-FOLD FULL (survivors)
For each surviving candidate:
- Run full training on fold-0 with same seed
- Log to `results.tsv` as `HYP-NNN-ROUND1`
- Extract metric

After all Round 1 runs:
- Sort survivors by Round 1 metric
- Kill bottom 50%
- Display Round 1 results table

### Step 7 — Round 2: 3-FOLD (survivors, if >1)
If only 1 survivor after Round 1: skip to Step 8.
For each surviving candidate:
- Run full training on folds 0, 1, 2 with same seed
- Log to `results.tsv` as `HYP-NNN-ROUND2` (one entry per fold, or aggregated)
- Compute mean metric over 3 folds

After all Round 2 runs:
- Sort by mean metric
- Kill bottom 50%
- Display Round 2 results table

### Step 8 — Round 3: K-FOLD CONFIRMATORY (winner)
The single surviving candidate is the tournament winner.
- Run full K-fold training (all folds from project_profile.k)
- Same seed
- Log each fold to `results.tsv` as `HYP-NNN-FOLD[k]`
- Log aggregate as `HYP-NNN-CONFIRMATORY`
- Compute mean ± std over K folds

### Step 9 — Declare winner
Compare winner's confirmatory metric against `baseline_metric` in `results.tsv`.

If winner > baseline:
```
TOURNAMENT COMPLETE
Winner: HYP-NNN — [hypothesis short title]
Confirmatory metric: [value] ± [std] (baseline: [baseline_value], delta: +[Δ])
Next step: Stage 16 Result Adequacy Gate
```

If winner ≤ baseline:
```
TOURNAMENT COMPLETE — ALL CANDIDATES FAIL TO BEAT BASELINE
Winner: HYP-NNN (best in tournament but below baseline)
Confirmatory metric: [value] ± [std] (baseline: [baseline_value])
Action required: Run /pivot-decision
Do NOT draft paper claiming improvement.
```

### Step 10 — Human Checkpoint 3 (REQUIRED)
Present the full tournament ranking table:

```
| Rank | ID      | Round 0 | Round 1 | Round 2 | Confirmatory | Status      |
|------|---------|---------|---------|---------|--------------|-------------|
| 1    | HYP-003 | 0.724   | 0.739   | 0.731   | 0.738 ±0.011 | WINNER      |
| 2    | HYP-001 | 0.681   | 0.701   | —       | —            | ELIMINATED  |
| 3    | HYP-002 | 0.612   | —       | —       | —            | ELIMINATED  |
| 4    | HYP-004 | NaN     | —       | —       | —            | PROXY_NAN   |
```

Ask: "Confirm winner and proceed to Stage 16? (y/n)"

### Step 11 — Update registries
After user confirms:
- Update `hypothesis_registry.md`: winner → `CONFIRMED`, others → `TOURNAMENT_ELIMINATED` with rank and elimination round
- Record confirmatory result in `evidence_ledger.md` as CONFIRMATORY evidence
- Update `project_state.md` to Stage 12 / 16 as appropriate

---

## Output Artifacts

| Artifact | Location | Description |
|----------|----------|-------------|
| `results.tsv` | Project root | All tournament run entries appended |
| `hypothesis_registry.md` | Project root | Winner CONFIRMED, others TOURNAMENT_ELIMINATED |
| `evidence_ledger.md` | Project root | Confirmatory evidence entry for winner |
| `project_state.md` | Project root | Stage advanced |

---

## Forbidden Actions

- Running tournament with any candidate having `validation_status` other than `APPROVED`
- Starting Round 1 before all Round 0 results are collected
- Changing any config parameter for a candidate between tournament rounds
- Assigning different folds to different candidates within the same round
- Extending a losing candidate with "just one more fold" outside the halving schedule
- Running confirmatory (K-fold) on any candidate other than the single tournament winner
- Skipping Human Checkpoint 2 (budget approval) before starting experiments
- Skipping Human Checkpoint 3 (winner confirmation) before updating registries
- Reporting only the winner's metrics without the full tournament log

---

## Error Conditions

| Condition | Response |
|-----------|----------|
| <3 APPROVED candidates | "Tournament requires ≥3 APPROVED candidates. Use individual proxy-to-full pipeline." |
| Git tree not clean | "Working tree has uncommitted changes. Commit or stash before running tournament." |
| project_profile.md missing fields | List the missing fields and stop. |
| baseline_metric not in results.tsv | "Baseline metric not found. Run baseline experiment and log it before tournament." |
| All Round 0 runs return NaN | "All candidates failed proxy. Check implementations before re-running." |
| experiment_matrix.md missing | "experiment_matrix.md not found. Complete Stage 7 before running tournament." |
