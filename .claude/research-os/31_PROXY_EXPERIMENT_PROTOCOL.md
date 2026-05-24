# 31 — Proxy Experiment Protocol

**Stage:** 11.5 — Before Exploratory Experiments (Stage 12)  
**Trigger:** Any hypothesis with `validation_status: APPROVED` ready to run  
**Command:** `/proxy-run HYP-NNN --config path/to/config`  
**Blocks:** No full experiment run until PROXY_PASS is logged for the hypothesis.

---

## 1. Core Principle: Never Commit Full Budget Before Seeing a Cheap Signal

Full experiments are expensive in both compute and calendar time. The proxy protocol creates a structured cheap-signal stage that filters hypotheses before committing full resources.

```
Full run  = K folds × E epochs × dataset    = 10–100 GPU-hours
Proxy run = 1 fold  × 0.25E epochs × subset =  0.5–5 GPU-hours

Savings factor = K × 4 = 20–40× cheaper per hypothesis
```

The proxy is not a truncated experiment — it is a **budget signal**. Its purpose is not to produce publishable results but to answer one binary question:

> Does this hypothesis produce a positive training signal within the first quarter of training?

If yes (PROXY_PASS): add to candidate pool, run full experiment.  
If no (PROXY_KILL, PROXY_NAN, PROXY_FAIL): log and abandon — do not retry, do not extend.

---

## 2. The Universal Experiment Interface

The proxy protocol requires a standardized interface between the Research OS and project training code. This interface is defined in `project_profile.md` and must be set up before any experiment runs.

### Required fields in `project_profile.md`

```yaml
# project_profile.md — experiment interface section
train_command: >
  python train.py --config {config} --output {out_dir} --seed 42
  # Placeholders: {config} and {out_dir} are substituted by the OS at runtime.
  # The OS appends --proxy when running a proxy experiment.

eval_command: >
  python eval.py --checkpoint {out_dir}/best.ckpt --output {out_dir}/metrics.json
  # Run after training completes. Writes results to out_dir.

metric_extract: >
  python -c "import json; d=json.load(open('{out_dir}/metric.json')); print(d['primary_metric'])"
  # Must print a single float to stdout. {out_dir} is substituted at runtime.

metric_name: accuracy          # human-readable name of primary_metric
metric_direction: higher       # "higher" or "lower" (is higher better?)
kill_on_nan: true              # abort proxy if metric is NaN?
kill_if: "metric < baseline_metric - 0.02"
  # Python expression. Variables: metric (float), baseline_metric (float from profile).
  # Examples:
  #   "metric < baseline_metric - 0.02"      discriminative tasks
  #   "metric > baseline_metric * 1.5"       generative tasks (FID — lower is better)
  #   "metric < 0"                           RL (reward should be positive)
  #   "metric < baseline_metric * 0.95"      retrieval (recall should be close)
proxy_fraction: 0.25           # fraction of training epochs/steps for proxy run
baseline_metric: null          # MUST be filled before first proxy run (from baseline experiment)
```

### Contract: what the training script must do

The training script is responsible for:
1. Detecting the `--proxy` flag and limiting training to `proxy_fraction` of the full schedule
2. Writing `metric.json` to `{out_dir}` at the end of training:
   ```json
   {"primary_metric": 0.847, "secondary_metrics": {"loss": 0.312}}
   ```
3. Exiting with code `0` on success and code `1` on any failure (NaN loss, OOM crash, missing data)

If the training script does not support `--proxy`, the OS will use `--max_epochs {int(total_epochs * proxy_fraction)}` as a fallback (set `proxy_flag_fallback: true` in `project_profile.md`).

---

## 3. Proxy Run Execution Protocol

Execute these 9 steps in order. Do not skip steps. Log all outcomes.

**Step 1 — Read configuration**  
Read `project_profile.md`. Extract: `train_command`, `eval_command`, `metric_extract`, `kill_on_nan`, `kill_if`, `proxy_fraction`, `baseline_metric`. Verify `baseline_metric` is not null (run baseline experiment first if needed).

**Step 2 — Create output directory**  
```
out_dir = results/proxy/HYP-NNN/[YYYYMMDD-HHMMSS]/
```
Create the directory. Record the path in the experiment log.

**Step 3 — Verify git state**  
Run `git status --short`. If any modified files exist, commit them before proceeding. The commit hash must be recorded — it identifies exactly what code produced this result.

**Step 4 — Execute proxy training**  
Substitute `{config}` and `{out_dir}` in `train_command`. Append `--proxy`.
```bash
{train_command} --proxy
# Example: python train.py --config configs/hyp001.yaml --output results/proxy/HYP-001/20260525-143022/ --seed 42 --proxy
```
Record wall-clock runtime and peak GPU memory.

**Step 5 — Check exit code**  
- Exit code `0`: proceed to step 6
- Exit code non-zero: log `PROXY_FAIL` to `results.tsv`, write crash diagnostic, stop. Do not retry.

**Step 6 — Extract metric**  
Run `metric_extract` with `{out_dir}` substituted. Parse the printed float. If output is not a parseable float, treat as NaN.

**Step 7 — Check kill_on_nan**  
If metric is NaN and `kill_on_nan: true`: log `PROXY_NAN`, stop. This indicates an implementation failure (not a hypothesis failure) — run a diagnostic experiment to find the bug.

**Step 8 — Evaluate kill_if condition**  
Evaluate the `kill_if` expression with `metric` and `baseline_metric` bound to their values.
- Expression is `true` (kill condition met): log `PROXY_KILL`, stop. Hypothesis is abandoned.
- Expression is `false` (kill condition not met): proceed to step 9.

**Step 9 — Log PROXY_PASS**  
Metric passes all filters. Log `PROXY_PASS` to `results.tsv`. Add hypothesis to candidate pool for full run tournament.

---

## 4. `results.tsv` Format

All proxy results are logged as rows in `results.tsv` (tab-separated). One row per proxy run.

```
exp_id          commit_hash  metric_value  peak_memory_mb  runtime_s  status       description
EXP-1-PROXY     a3f2c1d      0.847         4821            1823       PROXY_PASS   HYP-001: cross-attention bottleneck
EXP-2-PROXY     a3f2c1d      NaN           4203            412        PROXY_NAN    HYP-002: gating mechanism (NaN at step 80)
EXP-3-PROXY     b8e1a4f      0.721         4950            1791       PROXY_KILL   HYP-003: label smoothing (below kill threshold: 0.721 < 0.843-0.02)
EXP-4-PROXY     b8e1a4f      —             —               —          PROXY_FAIL   HYP-004: hierarchical pooling (crash: OOM at batch 3)
```

Column definitions:
- `exp_id`: `EXP-N-PROXY` where N matches the HYP-NNN number
- `commit_hash`: 7-char git hash at time of run
- `metric_value`: float from metric_extract, or NaN, or `—` for crash
- `peak_memory_mb`: peak GPU memory in MB (use `nvidia-smi` or equivalent)
- `runtime_s`: wall-clock seconds from start to end of training command
- `status`: one of `PROXY_PASS`, `PROXY_NAN`, `PROXY_KILL`, `PROXY_FAIL`
- `description`: hypothesis description + failure note if applicable

---

## 5. Budget Calculation

Before running proxies, estimate total budget to ensure resources are available.

```
proxy_budget  = N_candidates × avg_proxy_time
full_budget   = N_expected_pass × full_run_time × K_folds
total_budget  = proxy_budget + full_budget
```

**Example calculation:**

```
5 candidate hypotheses × 30 min proxy     = 2.5 hours
Estimated pass rate: 40% → 2 pass proxies
2 hypotheses × 10h full run × 5 folds    = 100 hours

Total = 2.5 + 100 = 102.5 hours

Compare to: 5 × 10h × 5 folds = 250 hours blind (no proxy)
Savings: ~60% compute, ~60% calendar time
```

Track actual vs estimated proxy time per hypothesis. Update estimates after each cycle.

---

## 6. Kill Signal Calibration by Paradigm

The `kill_if` condition must be calibrated to the task paradigm. Use these starting points:

**Discriminative classification / detection:**
```yaml
kill_if: "metric < baseline_metric - 0.02"
# Kill if primary metric is more than 2 points below baseline at proxy checkpoint.
# Rationale: well-behaved classifiers show most of their final performance gain
# by 25% of training. A 2-point deficit at proxy rarely recovers.
```

**Generative models (FID, FVD — lower is better):**
```yaml
kill_if: "metric > baseline_metric * 1.5"
# Kill if FID/FVD is more than 50% worse than baseline at proxy checkpoint.
metric_direction: lower
```

**Reinforcement learning:**
```yaml
kill_if: "metric < 0"
# Kill if mean reward is negative for the last 10% of proxy steps.
# (Modify metric_extract to compute this rolling average.)
```

**Retrieval / ranking (Recall@K, NDCG):**
```yaml
kill_if: "metric < baseline_metric * 0.95"
# Kill if recall is more than 5% relatively below baseline.
```

**Regression / structured prediction (lower RMSE / WER is better):**
```yaml
kill_if: "metric > baseline_metric * 1.1"
metric_direction: lower
# Kill if error is more than 10% relatively worse than baseline.
```

Adjust thresholds based on domain knowledge of how quickly the metric converges for your architecture and dataset size.

---

## 7. Forbidden Patterns

These patterns invalidate the proxy protocol and are explicitly prohibited:

**Pattern 1 — Extending a failed proxy**
> "The results are not good yet but I think it needs more epochs."

FORBIDDEN. If `PROXY_KILL` is triggered, the run is logged and the hypothesis is abandoned. Do not extend the proxy epoch count, do not relax the kill threshold for this hypothesis. The threshold was set before the run and must not change after seeing the result.

**Pattern 2 — Running full experiment first, then retroactively calling it a proxy**
> "I ran the full experiment and it did well, so the proxy would have passed."

FORBIDDEN. The proxy must run before the full experiment. Its purpose is to gate the full run, not to post-hoc justify it.

**Pattern 3 — Modifying config after proxy fail to retry the same hypothesis**
> "I'll just change the learning rate and try again."

FORBIDDEN. A failed proxy with a config change is a different hypothesis. Register it as `HYP-NNN+1` with a new mechanism argument. Log the original as `PROXY_KILL` or `PROXY_FAIL`.

**Pattern 4 — Skipping proxy for "obvious" improvements**
> "This is clearly going to work, the proxy is a formality."

FORBIDDEN. There are no obvious improvements in ML. The proxy exists precisely because intuition is unreliable. No exceptions.

---

## 8. Decision Tree After Proxy

```
Proxy run completes
       │
       ├── Exit code non-zero ──────────────────────────► PROXY_FAIL
       │                                                    Log crash diagnostic
       │                                                    Investigate code, not hypothesis
       │
       ├── Metric = NaN ────────────────────────────────► PROXY_NAN
       │                                                    Log as IMPLEMENTATION_FAILURE
       │                                                    Run diagnostic: small batch, check loss
       │
       ├── kill_if = true ──────────────────────────────► PROXY_KILL
       │                                                    Log hypothesis as abandoned
       │                                                    Do not retry
       │                                                    Move to next candidate
       │
       └── All checks pass ─────────────────────────────► PROXY_PASS
                                                            Add to candidate pool
                                                            Update hypothesis_registry.md
                                                            Schedule full run in tournament
```

**After all candidates have been proxied:** rank `PROXY_PASS` candidates by proxy metric value. Run full experiments in ranked order. If budget allows all, run all; if budget is constrained, run top-K.

---

## 9. Integration with Other Stages

| Stage | Action | Proxy Requirement |
|---|---|---|
| Stage 1.5 | Dialectical Validation | Must pass before proxy |
| **Stage 11.5** | **Proxy Run** | **PROXY_PASS required before full run** |
| Stage 12 | Exploratory Full Run | Uses PROXY_PASS candidates |
| Stage 15 | Ablation Studies | Ablations also require proxy (abbreviated) |
| Stage 16 | Result Adequacy Gate | Full run results only (no proxy results) |

Proxy results (`PROXY_PASS` metric values) must NOT be reported in the paper. Only full run results enter the evidence ledger and appear in tables.

---

*Last updated: 2026-05-25 | Research OS v1.0*
