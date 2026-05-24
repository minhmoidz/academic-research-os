# Autonomous Experiment Loop

Adapted from karpathy/autoresearch. Bounded, evidence-first, metric-driven.

---

## Design Principles (Inherited from autoresearch)

| autoresearch pattern | Our adaptation |
|----------------------|---------------|
| Fixed evaluation harness (`evaluate_bpb()` marked DO NOT CHANGE) | Protected harness files — never editable by the loop |
| One editable file (`train.py`) | One or a small set of explicitly declared editable files |
| Fixed time budget per run (300 s) | User-defined resource budget per run |
| Git branch per session (`autoresearch/mar5`) | Branch per experiment session |
| Result log: TSV with commit hash, metric, status, description | `results.tsv` with experiment ID, commit, metric, status, description |
| Keep if metric improves; revert if not | Keep/discard based on user-defined metric and direction |
| Simplicity criterion: deletion > complexity additions | Prefer improvements from removal or simplification |
| Crash fast on NaN/divergence (exit code 1) | Log crash as FAIL; never present crashed run results |
| Never stop (autoresearch runs until interrupted) | **Bounded**: stop at user-defined experiment budget |

---

## Key Difference from autoresearch

autoresearch is designed to run autonomously overnight without human confirmation.

This adaptation **requires**:
1. A defined experiment budget (N runs max)
2. A user-defined metric and direction (maximize or minimize)
3. A written description for every experiment before it runs
4. A result log entry for every run (pass, fail, or crash)
5. Claim-evidence mapping before any paper claim is made

**The loop is an evidence producer, not a paper writer.**
It fills `evidence_ledger.md` and `experiment_matrix.md` — never `paper.tex` directly.

---

## Pre-Loop Setup (Required Before First Run)

Define these before starting the loop. Write them to `experiment-plan.md`.

### 1. Experiment Objective
One falsifiable sentence:
> "Does [modification] reduce [metric] on [task/dataset] compared to [baseline]?"

### 2. Editable Files
List every file the loop may modify. Anything not on this list is protected.

```
editable:
  - src/model.py
  - configs/train.yaml
```

### 3. Protected Files
Files the loop must never touch.

```
protected:
  - src/evaluate.py        # fixed evaluation harness
  - data/                  # all data files
  - results/baseline/      # baseline result directory
```

### 4. Primary Metric
One metric, one number per run. Must be parseable from stdout or a log file.

```
metric: val_auc
direction: maximize        # or minimize
parse_command: python eval.py | grep "val_auc:" | awk '{print $2}'
```

### 5. Resource Budget
```
budget:
  max_experiments: 20      # hard stop — never run more than this
  max_time_per_run: 600    # seconds (platform-independent comparison)
  crash_threshold: 3       # abort loop after N consecutive crashes
```

---

## The 19-Step Bounded Loop

### Phase A: Initialization

**Step 1 — Confirm objective**
Read `experiment-plan.md`. Confirm metric, editable files, protected list, and budget.
If any is missing: stop and ask the user. Never start the loop without a complete plan.

**Step 2 — Create experiment branch**
```bash
git checkout -b experiment/$(date +%Y%m%d-%H%M%S)
```
All loop commits go on this branch. Never commit loop changes to main.

**Step 3 — Verify protected files**
Run `git diff --name-only HEAD` after each modification.
If any protected file appears in the diff: abort, revert, log as FAIL.

**Step 4 — Run baseline (always first)**
If `results/baseline/` does not exist or `results.tsv` has no BASELINE row:
- Run the experiment with zero modifications (original code)
- Log as experiment ID 0, status BASELINE
- This number is the reference for all keep/discard decisions

Never skip the baseline run. Every keep/discard decision is relative to baseline.

---

### Phase B: Experiment Loop (repeat until budget exhausted)

**Step 5 — Generate experiment description**
Before writing a single line of code, write a hypothesis:
```
EXP-[N]: [what change] because [why it might help] — expected effect on [metric]
```
Log this to `experiment_notes.md`.

**Step 6 — Make one change**
Modify only the declared editable files. One conceptual change per experiment.
- Do not bundle multiple independent changes
- Changes must be traceable to the hypothesis in Step 5
- Prefer the simpler implementation when two options achieve similar results
- A change that removes code is preferred over one that adds code, if both improve the metric equally

**Step 7 — Commit the change**
```bash
git add [editable files only]
git commit -m "EXP-[N]: [description from Step 5]"
```
Record the commit hash. This hash links the code change to the result.

**Step 8 — Run the experiment**
```bash
timeout [max_time_per_run] python train.py 2>&1 | tee logs/exp-[N].log
exit_code=$?
```

**Step 9 — Parse the result**
Extract the metric from the log:
```bash
metric_value=$(grep "val_auc:" logs/exp-[N].log | tail -1 | awk '{print $2}')
```
If parsing fails or exit_code ≠ 0: mark as CRASH.

**Step 10 — Log the result**
Append one row to `results.tsv`:
```
[EXP-N]\t[commit_hash]\t[metric_value]\t[peak_memory_mb]\t[runtime_s]\t[PASS|FAIL|CRASH]\t[description]
```
No experiment may be discussed in the paper without a row in `results.tsv`.

**Step 11 — Keep or discard**

Keep if:
- metric improves over current best (maximize: higher; minimize: lower)
- OR metric is equal AND the change reduces code complexity (lines deleted ≥ lines added)

Discard if:
- metric does not improve
- OR the run crashed
- OR the change modified a protected file

**If keeping:**
- Update `best_result.md` with the new best metric, commit hash, and description
- Update `experiment_matrix.md` with status KEPT

**If discarding:**
```bash
git revert HEAD --no-edit
```
- Log in `failed_runs.md` with reason
- Update `experiment_matrix.md` with status DISCARDED

**Step 12 — Update evidence artifacts**
After every run (keep or discard):
- `experiment_matrix.md`: add/update the row for this experiment
- `evidence_ledger.md`: add evidence entry with experiment ID, metric value, commit hash
- If this result supports a paper claim: add row to `claim_evidence_table.md`

**Step 13 — Check budget**
```
if experiments_run >= max_experiments: STOP
if consecutive_crashes >= crash_threshold: STOP and alert user
```

---

### Phase C: Completion

**Step 14 — Summarize findings**
After the loop ends (budget exhausted or user interrupts):
1. Report best experiment vs. baseline (delta, commit hash)
2. List KEPT experiments in order of metric improvement
3. List DISCARDED experiments with failure reasons
4. Flag any experiment that was KEPT but is inconsistent with another KEPT experiment

**Step 15 — Recommend next experiments**
Based on which changes helped and which failed, suggest:
- The most promising direction for the next loop session
- Any interaction effects between kept changes that should be tested
- Any resource budget increase that is warranted

**Step 16 — Update research-state.md**
Mark the autonomous loop phase as complete.
Record best result pointer in research-state.md for the next session.

---

## Keep/Discard Decision Table

| Metric improves? | Code simpler or equal? | Action |
|-----------------|----------------------|--------|
| Yes | Yes | KEEP |
| Yes | No (added complexity) | KEEP only if delta > complexity cost* |
| No | Yes | DISCARD |
| No | No | DISCARD |
| CRASH | — | DISCARD + log crash |
| Protected file modified | — | ABORT loop, revert, alert |

*Complexity cost: subjective judgment. Default: require ≥ 0.5% metric gain per 10 lines added.

---

## Crash Handling

On crash (exit code ≠ 0 or metric parse failure):
1. Log as CRASH in `results.tsv` with metric value = NaN
2. Log full crash reason in `failed_runs.md`
3. Revert the commit
4. Increment consecutive_crashes counter
5. If consecutive_crashes ≥ crash_threshold: STOP loop and alert user

Never present a CRASH run's partial output as a result.

---

## Simplicity Criterion

Adapted from autoresearch's principle: "improvements from deletion outweigh minor gains from complexity."

When two experiments achieve similar metric values:
- Prefer the one with fewer lines of code
- Prefer the one with fewer hyperparameters
- Prefer the one that removes dependencies over the one that adds them
- Prefer the one that is easier to explain in a methods section

The simplicity criterion does NOT mean choosing a worse metric. It applies only as a tiebreaker between experiments with equivalent metric performance.

---

## What the Loop DOES NOT Do

- Does not write paper prose
- Does not update `references.bib`
- Does not generate figures
- Does not interpret results beyond metric values
- Does not decide which results to report in the paper (that is the user's decision)
- Does not run unbounded — stops at the defined budget
- Does not skip the baseline run
- Does not modify protected files
- Does not present crashed runs as results

---

## Integration with Research OS Phases

| Research OS Phase | Role of the loop |
|-------------------|-----------------|
| Phase 7 (Experiment Planning) | Define `experiment-plan.md` before starting |
| **Phase 7A (This module)** | Run the bounded loop; fill `results.tsv`, `evidence_ledger.md` |
| Phase 8 (Evidence Tracking) | Use `results.tsv` as the authoritative source for claim-evidence table |
| Phase 10 (Section Drafting) | All claims in Method and Experiments sections must have an EXP-N reference |

---

## See Also

- `21_EXPERIMENT_LOG_FORMAT.md` — exact format for all log files
- `18_EVIDENCE_LEDGER.md` — how experiment evidence IDs are managed
- `05_EXPERIMENT_PLAYBOOK.md` — dataset/baseline/metric setup before the loop
- `.claude/skills/experiment-loop/SKILL.md` — how to invoke the loop via `/experiment-loop`
