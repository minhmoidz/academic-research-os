# Skill: /proxy-run

**Command:** `/proxy-run HYP-NNN --config path/to/config.yaml`  
**Stage:** 11.5 — Before Exploratory Experiments (Stage 12)  
**Protocol reference:** `.claude/research-os/31_PROXY_EXPERIMENT_PROTOCOL.md`

---

## Purpose

Run one proxy experiment for an approved hypothesis. Execute training at reduced scale (single fold, fraction of epochs), extract the primary metric, evaluate against the kill signal, and log the result to `results.tsv`. Update `hypothesis_registry.md` with the proxy outcome. Report whether to proceed to full run, kill the hypothesis, or diagnose an implementation failure.

---

## Required Inputs

1. `HYP-NNN` — hypothesis ID, must have `validation_status: APPROVED` in `hypothesis_registry.md`
2. `--config path/to/config.yaml` — path to the experiment configuration file
3. `project_profile.md` — must contain all required experiment interface fields
4. Git working tree — must be clean before run (or user must confirm commit)
5. `results.tsv` — must exist (create if this is the first experiment)

---

## Forbidden Actions

- Running proxy without verifying `validation_status: APPROVED` — a PENDING or REJECTED hypothesis must not run
- Proceeding to full run without `PROXY_PASS` logged in `results.tsv`
- Extending proxy duration after a `PROXY_KILL` — no retries, no epoch extensions
- Modifying `kill_if` threshold after seeing the proxy metric — threshold must be set before run
- Writing proxy metric values to the paper, evidence ledger, or any claim-bearing artifact
- Running proxy without recording git commit hash
- Modifying any protected file: `evidence_ledger.md`, `hypothesis_registry.md` claims section (only proxy_result and proxy_metric fields may be updated)

---

## Pre-flight Checklist

Execute all 5 checks before touching the training command. Stop if any check fails.

**Check 1 — Hypothesis approval**
```
hypothesis_registry.md → HYP-NNN → validation_status: APPROVED?
```
If `PENDING`: run `/validate-hypothesis HYP-NNN` first.  
If `REJECTED` or `REVISE`: report status and stop.

**Check 2 — Project profile completeness**
```
project_profile.md must contain:
  train_command     ← not null
  eval_command      ← not null
  metric_extract    ← not null
  metric_name       ← not null
  metric_direction  ← "higher" or "lower"
  kill_on_nan       ← true or false
  kill_if           ← valid Python expression string
  proxy_fraction    ← float between 0.1 and 0.5
  baseline_metric   ← not null (numeric float)
```
If any field is missing or null: report which field and stop.

**Check 3 — Git state**
```bash
git status --short
```
If output is non-empty (modified or untracked files): prompt user to commit, or commit with message `"chore: pre-proxy snapshot for HYP-NNN"`. Do not proceed until git is clean.

**Check 4 — Baseline metric present**
```
project_profile.md → baseline_metric ← must be a float, not null
```
If null: instruct user to run baseline experiment first and record result in `project_profile.md`.

**Check 5 — Config file exists**
```bash
test -f path/to/config.yaml
```
If file does not exist: report path and stop.

---

## Execution Steps

### Step 1 — Read project_profile.md

Extract all experiment interface fields. Bind:
- `train_command`: raw template string with `{config}` and `{out_dir}` placeholders
- `eval_command`: raw template string
- `metric_extract`: raw template string
- `kill_on_nan`: boolean
- `kill_if`: Python expression string
- `proxy_fraction`: float
- `baseline_metric`: float

### Step 2 — Create output directory

```
out_dir = results/proxy/HYP-NNN/[YYYYMMDD-HHMMSS]/
```

Create directory. Record absolute path. This directory will contain `metric.json` and any training logs.

### Step 3 — Get git commit hash

```bash
git rev-parse HEAD
```

Record the 7-character prefix. This hash identifies the exact code version. Log it immediately — do not retrieve it after the run.

### Step 4 — Execute proxy training

Substitute `{config}` → `--config path/to/config.yaml` and `{out_dir}` → `out_dir` in `train_command`. Append `--proxy`.

```bash
# Substituted command example:
python train.py --config path/to/config.yaml --output results/proxy/HYP-NNN/20260525-143022/ --seed 42 --proxy
```

Record:
- Wall-clock start time
- Wall-clock end time → `runtime_s = end - start`
- Peak GPU memory → `peak_memory_mb` (query `nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits` at end of run, or parse from training logs)

### Step 5 — Check exit code

- Exit code `0`: proceed to step 6
- Exit code non-zero: `status = PROXY_FAIL`
  - Append row to `results.tsv` with `—` for metric and memory
  - Write crash note: last 20 lines of stdout/stderr, OOM flag if applicable
  - Report: "PROXY_FAIL — exit code [N]. Investigate code, not hypothesis. See crash note."
  - Stop.

### Step 6 — Extract metric

Run `metric_extract` with `{out_dir}` substituted. Capture stdout. Attempt to parse as float.

If `metric.json` does not exist in `out_dir`: treat as NaN.  
If stdout is not a parseable float: treat as NaN.  
If float parsed successfully: bind to `metric`.

### Step 7 — Check kill_on_nan

If `metric` is NaN and `kill_on_nan = true`:
- `status = PROXY_NAN`
- Append row to `results.tsv`
- Report: "PROXY_NAN — metric.json missing or non-numeric. This is an IMPLEMENTATION_FAILURE, not a hypothesis failure. Recommended diagnostic: run with a minimal batch (2 samples, 5 steps) and inspect loss at each step."
- Stop.

### Step 8 — Evaluate kill_if condition

Evaluate the Python expression from `kill_if` with `metric` and `baseline_metric` bound:

```python
metric = [extracted float]
baseline_metric = [from project_profile.md]
result = eval(kill_if_expression)
```

If `result` is `True` (kill condition met):
- `status = PROXY_KILL`
- Append row to `results.tsv` with note: `[hypothesis — below kill threshold: {metric} vs kill_if: {kill_if}]`
- Update `hypothesis_registry.md`: `proxy_result: KILL`
- Report: "PROXY_KILL — metric {metric} triggered kill condition. Hypothesis abandoned. Do not retry. Move to next candidate."
- Stop.

If `result` is `False` (kill condition not met): proceed to step 9.

### Step 9 — Log PROXY_PASS

`status = PROXY_PASS`

Append row to `results.tsv`:
```
EXP-N-PROXY    [commit_hash]    [metric]    [peak_memory_mb]    [runtime_s]    PROXY_PASS    HYP-NNN: [hypothesis description]
```

Update `hypothesis_registry.md` entry for HYP-NNN:
```yaml
proxy_result: PASS
proxy_metric: [metric value, 3 decimal places]
proxy_date: YYYY-MM-DD
proxy_commit: [commit_hash]
```

### Step 10 — Report result

```
Proxy Run — HYP-NNN
Status: PROXY_PASS
Metric ([metric_name]): [metric] (baseline: [baseline_metric], direction: [metric_direction])
Kill condition: [kill_if expression] → False (did not trigger)
Runtime: [runtime_s]s | Peak memory: [peak_memory_mb] MB
Commit: [commit_hash]

Recommendation: Proceed to full run.
Next: Schedule K-fold full experiment for HYP-NNN.
Note: proxy metric ([metric]) is NOT a reportable result. Full run result goes into evidence ledger.
```

---

## Output Summary

| Artifact | Location | Content |
|---|---|---|
| `results.tsv` | project root or `results/` | One new row: exp_id, hash, metric, memory, runtime, status, description |
| `hypothesis_registry.md` | project root | proxy_result + proxy_metric + proxy_date + proxy_commit added |
| `out_dir/` | `results/proxy/HYP-NNN/[timestamp]/` | metric.json + training logs |
| Skill report | Console | Status, metric, recommendation, next action |

---

## Status Reference

| Status | Meaning | Next Action |
|---|---|---|
| `PROXY_PASS` | Signal detected; metric above kill threshold | Schedule full K-fold run |
| `PROXY_KILL` | Metric triggered kill condition | Abandon hypothesis; log and move on |
| `PROXY_NAN` | metric.json missing or non-numeric | Fix implementation bug; not a hypothesis failure |
| `PROXY_FAIL` | Training script exited non-zero | Fix code crash; check OOM, missing data, config errors |

---

## Budget Accounting

After each proxy, update running budget tally in `project_state.md`:

```
Proxy budget used: [N] × [avg_proxy_time]h = [total]h
Full budget committed: [N_pass] × [full_run_time]h × [K_folds] folds = [total]h
Remaining GPU budget: [total_budget - used]h
```

---

*Research OS v1.0 | Stage 11.5 | See 31_PROXY_EXPERIMENT_PROTOCOL.md for full protocol*
