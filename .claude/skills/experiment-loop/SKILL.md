# Skill: /experiment-loop

Run a bounded, autoresearch-inspired experiment loop. Evidence producer only — never writes paper prose.

---

## Trigger

User types `/experiment-loop` or invokes via Skill tool.

---

## Required Input (ask if ALL missing)

If `experiment-plan.md` exists: read it and proceed.  
If it does not exist: ask the user for:

1. Experiment objective (one falsifiable sentence)
2. Editable files (list)
3. Protected files (list — must include the evaluation harness)
4. Primary metric (name + parse command)
5. Improvement direction (maximize or minimize)
6. Max experiments (hard budget)
7. Max time per run (seconds)

Do not start the loop until all 7 items are defined and saved to `experiment-plan.md`.

---

## Pre-Loop Checks (run before first experiment)

### Step 1: Load Research OS rules
```
Read .claude/research-os/20_AUTONOMOUS_EXPERIMENT_LOOP.md
Read .claude/research-os/13_ANTI_HALLUCINATION_RULES.md
Read .claude/research-os/21_EXPERIMENT_LOG_FORMAT.md
```

### Step 2: Load experiment state
```
Read experiment-plan.md        → objective, editable/protected files, metric, budget
Read experiment-matrix.md      → which experiments have run
Read evidence_ledger.md        → which results are already logged
Read results.tsv               → current best metric value
```

### Step 3: Verify critical invariants

- [ ] `experiment-plan.md` exists with all 7 fields filled
- [ ] Protected files list is non-empty (evaluation harness must be listed)
- [ ] Metric parse command is testable: run it on an existing log file to confirm it works
- [ ] `logs/` directory exists (`mkdir -p logs/`)
- [ ] Current branch is NOT main/master (loop runs on a dedicated experiment branch)

If any invariant fails: stop and report. Do not run experiments.

### Step 4: Create experiment branch (if not already on one)
```bash
current_branch=$(git rev-parse --abbrev-ref HEAD)
if [[ "$current_branch" == "main" || "$current_branch" == "master" ]]; then
  git checkout -b experiment/$(date +%Y%m%d-%H%M%S)
fi
```

### Step 5: Run baseline (if missing)
Check `results.tsv` for a `BASELINE` row.  
If missing:
- Confirm no editable files have been modified from the original
- Run with: `timeout [max_time] python [train_script] 2>&1 | tee logs/baseline.log`
- Parse metric from log
- Append to `results.tsv`:  
  `BASELINE\t[commit]\t[value]\t[mem]\t[time]\tBASELINE\tunmodified baseline`
- Set `current_best = baseline_metric`
- Write `best_result.md` with baseline values

Never skip the baseline run.

---

## Main Loop (repeat until budget)

```
for N in 1..max_experiments:
    step_a_hypothesis()
    step_b_modify()
    step_c_commit()
    step_d_run()
    step_e_parse()
    step_f_log()
    step_g_keep_or_discard()
    step_h_update_artifacts()
    if budget_exhausted or consecutive_crashes >= threshold:
        break
```

### step_a_hypothesis
Before writing any code, write to `experiment_notes.md`:
```
## EXP-[N]
Date: [datetime]
Hypothesis: [what change] because [why] — expected effect on [metric]
Files to change: [list]
```

### step_b_modify
Modify ONLY the declared editable files.  
After editing, confirm:
```bash
git diff --name-only
```
If any protected file appears: immediately `git checkout [file]` and do not proceed.

### step_c_commit
```bash
git add [editable files only — explicit, not git add .]
git commit -m "EXP-[N]: [hypothesis summary]"
commit_hash=$(git rev-parse HEAD)
```

### step_d_run
```bash
t_start=$(date +%s)
timeout [max_time_per_run] python [train_script] 2>&1 | tee logs/exp-[N].log
exit_code=${PIPESTATUS[0]}
t_end=$(date +%s)
runtime=$((t_end - t_start))
```

### step_e_parse
```bash
metric_value=$([parse_command applied to logs/exp-[N].log])
```
If exit_code ≠ 0 or metric_value is empty/NaN: mark status=CRASH.

Peak memory: parse from log if available, else `NaN`.

### step_f_log
Append to `results.tsv`:
```
EXP-[N]\t[commit_hash]\t[metric_value]\t[peak_mem]\t[runtime]\t[PASS|FAIL|CRASH]\t[hypothesis]
```
This row is permanent. Never delete it.

### step_g_keep_or_discard

**If CRASH:**
```bash
git revert HEAD --no-edit
```
Increment consecutive_crashes.  
Log to `failed_runs.md`.  
Set status=CRASH.

**If metric does NOT improve (FAIL):**
```bash
git revert HEAD --no-edit
```
Log to `failed_runs.md`.

**If metric improves (PASS):**
Update `current_best = metric_value`.  
Update `best_result.md`.  
Reset consecutive_crashes = 0.

**Simplicity tiebreaker (metric equal to current best):**
- Count lines added/deleted: `git diff HEAD~1 --stat`
- If lines deleted ≥ lines added: PASS (keep)
- Otherwise: FAIL (discard)

### step_h_update_artifacts

After every run (PASS, FAIL, or CRASH):
```
experiment_matrix.md  → add row: EXP-[N], description, status, metric
evidence_ledger.md    → add EV-EXP-[N] entry (even for FAIL/CRASH, marked accordingly)
```

After a PASS:
```
result_to_claim_map.md → add preliminary row if this result supports a contribution claim
```

---

## Budget and Termination

Stop the loop when ANY of:
- `experiments_run >= max_experiments`
- `consecutive_crashes >= crash_threshold` (default 3)
- User sends an interrupt signal

On termination: go to Completion Report.

---

## Completion Report

After the loop ends, output:

```
═══════════════════════════════════════
Experiment Loop Complete
═══════════════════════════════════════
Runs: [N] of [budget]
Best result: [metric_name] = [value] (EXP-[N], commit [hash[:8]])
Delta over baseline: [+/-value] ([%] improvement)

KEPT experiments ([M]):
  EXP-1: [description] → [metric]
  EXP-3: [description] → [metric]
  ...

DISCARDED experiments ([K]):
  EXP-2: FAIL — [reason]
  EXP-4: CRASH — [reason]
  ...

Artifacts updated:
  results.tsv              [N+1 rows including baseline]
  experiment_notes.md      [N entries]
  evidence_ledger.md       [M EV-EXP entries for PASS runs]
  experiment_matrix.md     [N rows]
  best_result.md           [updated to EXP-N]
  failed_runs.md           [K entries]

Recommended next experiments:
  1. [specific direction based on what helped]
  2. [interaction effect to test]
  ...

Next step: /experiment-status to review, then Phase 8 (Evidence Tracking) to map results to claims.
═══════════════════════════════════════
```

---

## Safety Rules

- **Never modify protected files** — not even for a "quick test"
- **Never invent results** — if the log doesn't have a parseable metric, the result is CRASH
- **Never run on main/master branch** — experiments go on a dedicated branch
- **Never write paper prose** — this skill produces evidence, not text
- **Never skip the baseline** — every keep/discard decision requires a baseline reference
- **Never present FAIL or CRASH results as paper claims** — only PASS rows enter the evidence ledger as usable evidence
- **Log every run** — including crashes — before deciding to continue or stop
