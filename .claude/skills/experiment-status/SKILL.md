# SKILL: /experiment-status
## Purpose
Report the current state of all experiments in the project. Provides a concise, factual summary of experiment counts, best results, hypothesis status, and budget usage. Recommends the next action.

---

## When to Run
- Any time during Stage 8–16 (active experimentation phases).
- At the start of a new session to restore context.
- Before running /result-adequacy to get a pre-check.
- When the user asks "where are we?" or "what experiments have been run?"

---

## Required Inputs
None required. Reads from existing project files.

---

## Steps

### Step 1 — Read results.tsv
Location: `results.tsv` in project root.
Format: tab-separated with columns:
```
run_id | timestamp | commit_hash | experiment_type | hypothesis_id | dataset | metric | value | direction | baseline_comparison | status | evidence_id | notes
```

If the file does not exist or is empty: report "No experiments run yet" and stop.

Parse all rows. For status values:
- `PASS` — experiment met its pass criterion
- `FAIL` — experiment ran but did not meet criterion
- `CRASH` — experiment did not complete (error, OOM, timeout)
- `BASELINE` — reference run (no hypothesis)
- `PARTIAL` — incomplete (missing folds, etc.)

### Step 2 — Count Experiments by Status
```
Total runs: N
  BASELINE: [count]
  PASS:     [count]
  FAIL:     [count]
  CRASH:    [count]
  PARTIAL:  [count]
```
Also break down by experiment_type:
```
  EXPLORATORY:  [count]
  DIAGNOSTIC:   [count]
  CONFIRMATORY: [count]
```

### Step 3 — Extract Best Result
For each (dataset, metric) pair:
1. Filter rows where status=PASS.
2. Find the row with the best value (highest for AUC/Accuracy; lowest for loss/error).
3. Compute delta over baseline:
   - Find the BASELINE row for the same (dataset, metric).
   - delta = best_value - baseline_value (absolute).
   - delta_pct = (delta / baseline_value) * 100.

Format:
```
Best result: [metric]=[value] on [dataset]
  Experiment: [run_id] | [experiment_type] | [hypothesis_id]
  Delta over baseline: +[X.XX] ([+X.XX%])
  Evidence ID: [evidence_id]
  Commit: [commit_hash]
```

If no PASS results exist: "No PASS results yet."

### Step 4 — Check Hypothesis Status
Read `hypothesis_registry.md`. For each hypothesis, determine status:
- **PENDING:** No experiments with this hypothesis_id completed yet.
- **EXPLORATORY_ONLY:** Only EXPLORATORY experiments run (no confirmatory yet).
- **SUPPORTED:** At least one CONFIRMATORY PASS result linked to this hypothesis.
- **CONTRADICTED:** CONFIRMATORY FAIL result for this hypothesis with no alternative explanation.
- **INCONCLUSIVE:** Mixed results (some PASS, some FAIL) across datasets/seeds.

Format:
```
Hypothesis status:
  HYP-001: [status] — [brief reason]
  HYP-002: [status] — [brief reason]
```

### Step 5 — Check Budget Usage
Read `experiment_matrix.md` for budget limits. Compare to actual run count.

```
Budget:
  Experiments run:    [N] / [max_N] ([pct]% used)
  Time consumed:      [estimate from timestamps if available]
  Crash rate:         [crash_count] / [total] = [pct]%
  Budget status:      NORMAL / WARNING (>70% used) / CRITICAL (>90% used) / EXHAUSTED
```

If experiment_matrix.md does not exist: "No experiment plan found. Run /plan-experiments."

### Step 6 — Recommend Next Action
Apply the following decision logic:

| Condition | Recommendation |
|-----------|---------------|
| No experiments run | Run baseline experiment first; then /plan-experiments |
| Only EXPLORATORY runs | Refine hypotheses based on findings; run DIAGNOSTIC if unexpected results |
| All CONFIRMATORY pass | Run /result-adequacy |
| Any CONFIRMATORY FAIL | Run /pivot-decision |
| Crash rate > 30% | Stop and run DIAGNOSTIC; do not continue CONFIRMATORY |
| Budget > 90% used, no PASS | Run /pivot-decision immediately |
| All hypotheses SUPPORTED, TRC met | Proceed to /result-adequacy → Stage 16 |

### Step 7 — Output the Status Report
```
=== EXPERIMENT STATUS REPORT ===
Generated: [timestamp]
Project: [project name from research_direction.md or directory name]

--- Run Counts ---
Total runs: [N]
  BASELINE: [N] | PASS: [N] | FAIL: [N] | CRASH: [N] | PARTIAL: [N]
  EXPLORATORY: [N] | DIAGNOSTIC: [N] | CONFIRMATORY: [N]

--- Best Result ---
[best result block, per Step 3]

--- Hypothesis Status ---
[hypothesis block, per Step 4]

--- Budget ---
[budget block, per Step 5]

--- Recommendation ---
[recommendation from Step 6]
================================
```

---

## Output
Printed to terminal. No files written by this skill (read-only diagnostic).

---

## Safety Rules
1. **Report only from actual log files.** Never summarize results from memory or prior conversation turns.
2. **If results.tsv is missing or empty:** report exactly "No experiments run yet" — do not speculate.
3. **Do not mark a hypothesis SUPPORTED** unless there is at least one CONFIRMATORY PASS result linked to it (EXPLORATORY support is insufficient).
4. **Do not recommend "proceed to paper writing"** if any of the following are true:
   - No CONFIRMATORY PASS results exist.
   - Budget is EXHAUSTED with no PASS.
   - Crash rate > 30%.
   - Any CONTRADICTED hypothesis has not been addressed by a pivot.
5. **Crash diagnosis takes priority.** If crash rate is > 20%, the recommendation must include "diagnose crashes before continuing."
