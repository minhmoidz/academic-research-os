# SKILL: /plan-experiments
## Purpose
Design the full experiment matrix before running any experiments. Covers all three experiment types: exploratory, diagnostic, and confirmatory. Ensures every experiment has a clear hypothesis, pass/fail criterion, and budget before execution begins.

---

## When to Run
- Stage 8 (Experiment Planning) of the research workflow.
- Before running any EXPLORATORY or CONFIRMATORY experiments.
- After hypothesis_registry.md is populated with at least one active hypothesis.
- May be re-run after a pivot to update the plan.

---

## Required Inputs
| Input | Source |
|-------|--------|
| Active hypotheses | hypothesis_registry.md |
| Venue and evidence requirements | venue_target.md |
| Pass/fail thresholds | target_result_contract.md (if CONFIRMATORY planning) |
| Available compute budget | User |

---

## Experiment Types

### EXPLORATORY
- **Purpose:** Discover what happens. Test assumptions. May contradict the hypothesis.
- **Allowed outcome:** Contradicting result is valid and valuable; update hypothesis accordingly.
- **TRC coverage:** Not covered — cannot be used as primary confirmatory evidence.
- **Logging:** Must be logged in results.tsv with `experiment_type=EXPLORATORY`.

### DIAGNOSTIC
- **Purpose:** Explain why something happened. Isolate a specific mechanism or rule out a bug.
- **Trigger:** After a FAIL or unexpected result from an EXPLORATORY experiment.
- **Allowed outcome:** Result may not be reportable in the paper; goal is understanding.
- **Logging:** Must be logged in results.tsv with `experiment_type=DIAGNOSTIC`.

### CONFIRMATORY
- **Purpose:** Support final paper claims. Must follow TRC. Must be pre-registered.
- **Requirement:** TRC must exist before this type is run.
- **Logging:** Must be logged in results.tsv with `experiment_type=CONFIRMATORY` and linked to `evidence_id`.

---

## Steps

### Step 1 — Load Reference Documents
1. Read `.claude/research-os/05_EXPERIMENT_PLAYBOOK.md`.
2. Read `hypothesis_registry.md` — list all active hypotheses (HYP-NNN).
3. Read `venue_target.md` — get required datasets, baselines, and evidence requirements.
4. Read `target_result_contract.md` if it exists (confirmatory requirements).

### Step 2 — Design a Falsifying Experiment for Each Hypothesis
For each hypothesis HYP-NNN, design one experiment that could FALSIFY it:
- Ask: "What result would prove this hypothesis WRONG?"
- Design the experiment so that failure is informative, not just an absence of signal.
- Record: what the falsifying result would look like.

**Example:**
```
HYP-001: [AttentionModule] improves metric over baseline [BaselineModel].
Falsifying result: Metric with [AttentionModule] ≤ metric without [AttentionModule] on [Dataset-A].
Experiment: Run [BaselineModel] + [AttentionModule] vs. [BaselineModel] (no [AttentionModule]), same seeds, same config.
```

### Step 3 — Fill the Experiment Matrix
Create or update `experiment_matrix.md` with the following structure for each experiment:

```markdown
## EXP-[N]: [short name]

| Field | Value |
|-------|-------|
| Type | EXPLORATORY / DIAGNOSTIC / CONFIRMATORY |
| Hypothesis | HYP-NNN |
| Dataset | [name] |
| Primary metric | [metric] |
| Method variant | [description] |
| Config file | [path] |
| Baseline | [method to compare against] |
| Pass criterion | [specific value or delta] |
| Fail criterion | [what constitutes failure] |
| Editable files | [list of files that may be modified] |
| Protected files | [PROTECTED: evaluation harness, data split files] |
| Expected runtime | [estimate] |
| Expected output file | [path] |
| Budget: max runs | [N] |
| Budget: max time | [hours] |
| Crash threshold | [e.g., "abort if >2 consecutive CRASH"] |
| Notes | |
```

### Step 4 — Mark Protected Files
Protected files are those that define evaluation fairness and must not be modified during experimentation:
- Data split files (e.g., `splits/fold_*.csv`)
- Evaluation harness scripts (e.g., `eval.py`, `metrics.py`)
- Baseline config files used for comparison

Mark each as:
```
PROTECTED: [filename] — reason: [evaluation fairness / baseline reproducibility]
```
These files must not be modified after experiments begin. Any modification voids the comparison.

### Step 5 — Set Global Experiment Budget
Define the global budget for this planning session:

```markdown
## Global Budget

| Resource | Limit |
|----------|-------|
| Total experiments (all types) | [N] |
| Confirmatory experiments | [N] |
| Max time for any single run | [hours] |
| Compute environment | [GPU type, memory] |
| Crash threshold (project-level) | [e.g., "pause and diagnose if 3 consecutive crashes"] |
| Budget exhaustion action | [e.g., "run /pivot-decision"] |
```

### Step 6 — Sequence the Experiments
Order experiments logically:
1. EXPLORATORY first (understand the landscape).
2. DIAGNOSTIC after any unexpected EXPLORATORY result.
3. CONFIRMATORY last (after hypotheses are refined and TRC is signed).

Output the sequence as a numbered list with estimated completion date.

### Step 7 — Present Plan for User Review
Present the full experiment matrix and budget to the user BEFORE any experiment begins.
Ask: "Do you approve this experiment plan? (yes / modify / cancel)"
Do NOT begin any experiment until the user approves.

### Step 8 — Update project_state.md
```
experiment_plan_complete: true
experiment_plan_date: [date]
total_experiments_planned: [N]
experiments_run: 0
```

---

## Output Files
- `experiment_matrix.md` — created or updated
- `project_state.md` — updated

---

## Safety Rules
1. **Design experiments to test hypotheses, not to confirm them.** Every experiment must have a condition under which it would count as a failure.
2. **Never start a CONFIRMATORY experiment without a signed TRC.**
3. **Every experiment must have an explicit pass/fail criterion** stated before running — not determined after seeing the result.
4. **Budget must be defined before running.** If budget is exhausted with no PASS result: run /pivot-decision, do not extend budget without a DEC entry.
5. **Never modify protected files** after experiments begin. If a bug is found in the evaluation harness: log as DIAGNOSTIC, freeze current results, fix, re-run all affected experiments with new evidence IDs.
6. **Log every run in results.tsv** — even exploratory and failed runs. Selective reporting is a protocol violation.
7. **Do not reorder experiment types** to produce a more favorable narrative (e.g., running confirmatory first to see if the hypothesis holds, then running exploratory to "explain" it).
