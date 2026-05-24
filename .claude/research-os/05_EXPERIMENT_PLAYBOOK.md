# Experiment Playbook

---

## Three Experiment Types

Every experiment must be classified before it runs. The classification determines what can be claimed from its results.

### Type 1: Exploratory Experiments
**Purpose:** Discover what happens when we change something. May produce unexpected findings.  
**Allowed:** Update hypotheses, change direction, generate new ideas.  
**Not allowed:** Produce paper claims directly.  
**Rule:** If exploratory results contradict HYP-NNN, mark hypothesis CONTRADICTED and run `/pivot-decision`.

### Type 2: Diagnostic Experiments
**Purpose:** Explain why something happened. Analyze failure modes, isolate mechanisms, check bugs.  
**When to use:** After a hypothesis is contradicted; after a crash or FAIL; to explain a confounding result.  
**Not allowed:** Produce paper claims directly (diagnostic results support analysis sections only).

### Type 3: Confirmatory Experiments
**Purpose:** Support final paper claims. Must satisfy the Target Result Contract.  
**Requirements:**
- Hypothesis pre-registered in `hypothesis_registry.md`
- Target Result Contract (`target_result_contract.md`) already defined
- All 5 folds (or required seeds) must complete — no partial averaging
- Logged to `results.tsv` with full commit hash and status

**Rule:** Confirmatory experiments must not be designed to confirm the result — they must be designed to test whether the claim is true, which means they must be capable of falsifying it.

**Outcome classification (for every experiment):**
1. `SUPPORTS_HYPOTHESIS` — result matches prediction
2. `PARTIALLY_SUPPORTS` — result in right direction but below threshold
3. `CONTRADICTS_HYPOTHESIS` — result opposite to prediction
4. `UNEXPECTED_POSITIVE` — positive result for a different reason than hypothesized
5. `INCONCLUSIVE` — result too noisy to determine
6. `IMPLEMENTATION_FAILURE` — crash, NaN, metric parse failure

**Decision after classification:**
- KEEP: supports, good signal
- REFINE: partially supports, adjust hypothesis
- DIAGNOSE: contradicts or inconclusive, run diagnostic
- PIVOT: fundamental mismatch with direction
- ABANDON: no signal, no insight
- HOLD: result interesting but not yet classifiable

---

## Core Rule: Lock Before Run, Trace Before Write

1. Lock the experimental setup (datasets, baselines, metrics, splits) BEFORE running experiments.
2. Trace every number in the paper to a specific result file BEFORE writing claims.

---

## Step 1: Experiment Matrix Template

Fill this before running anything. Save as `experiment-matrix.md`.

```markdown
# Experiment Matrix

## Task
[e.g., binary subtype classification via 5-fold cross-validation]

## Datasets
| Dataset | N slides | N classes | Feature extractor | Split protocol | File path |
|---------|----------|-----------|-------------------|----------------|-----------|
| Dataset-A | [N] | 2 (ClassA/ClassB) | [FeatureExtractor (Ddim)] | Patient 5-fold seed=42 | data/dataset-a/ |
| Dataset-B | [N] | 2 (ClassA/ClassB) | [FeatureExtractor (Ddim)] | Patient 5-fold seed=42 | data/dataset-b/ |

## Baselines
| Method | Code path | Config file | Verified runnable? | Expected runtime |
|--------|-----------|-------------|-------------------|-----------------|
| BaselineModel | models/baseline/ | configs/baseline.yaml | ✓ | ~2h/fold |
| ComparisonMethod | models/comparison/ | configs/comparison.yaml | ✓ | ~1h/fold |

## Proposed Method
| Config | Key hyperparams | Result dir |
|--------|-----------------|-----------|
| [your-config-name] | alpha=0.5, beta=0.3, T=2.0, lambda=0.01 | results/ours/ |

## Primary metric
Mean AUC over 5 folds (population std)

## Ablation designs
| Config | Components active | Purpose |
|--------|-------------------|---------|
| +AttentionModule+cls | AttentionModule=yes, ER=no, LS=no | Isolate class token |
| +ER | AttentionModule=no, ER=yes, LS=no | Isolate entropy reweighting |
| +ER+cls | AttentionModule=no, ER=yes, CLS=yes, LS=no | ER + token without AttentionModule |
| +ER+AttentionModule+LS | AttentionModule=yes, ER=yes, LS=yes, CLS=no | All except class token |
| Ours | All components | Full model |
```

---

## Step 2: Dataset Tracking Rules

**Never describe a dataset without verifying:**
- [ ] Dataset exists and is accessible at the stated path
- [ ] N samples matches verified count (`wc -l` or similar)
- [ ] Class distribution verified (not assumed)
- [ ] Split protocol (patient-level vs. slide-level) confirmed
- [ ] Feature extractor version confirmed

If any item is unverified: write `TODO_RESULT_NEEDED: verify [item] for [dataset]`

---

## Step 3: Baseline Tracking Rules

**A baseline is confirmed when:**
- [ ] The code runs without error on the target dataset
- [ ] Results are logged to a file
- [ ] Results are reproducible with the same seed

**Never include a baseline result that came from:**
- Another paper's table (unless explicitly labeled as "reported in [cite]")
- An estimated value
- A partial run (fewer folds than the proposed method)

---

## Step 4: Metric Tracking

**For each result row in the paper:**

```markdown
# Result Record

Method: BaselineModel
Dataset: Dataset-A ([FeatureExtractor (Ddim)])
Metric: Mean AUC ± std (5-fold)
Value: [value] ± [std]
Source file: results/baseline/dataset-a/fold_results.json
Computed by: compute_metrics.py --mode population_std
Verified: ✓ (rechecked YYYY-MM-DD)
```

**Population std vs. sample std:** Decide ONCE before collecting results which std formula to use (÷N or ÷N-1). Apply consistently to ALL methods. Do not mix formulas between rows of the same table.

---

## Step 5: Result File Linking

Create `result-map.md` linking every paper table cell to its source:

```markdown
# Result Map

## Table I (Main Comparison)

| Row | Dataset | Value | Source File |
|-----|---------|-------|-------------|
| BaselineModel | Dataset-A [FeatureExtractor] | [value] ± [std] | results/baseline/dataset-a/summary.json:fold_mean_auc |
| ComparisonMethod | Dataset-A [FeatureExtractor] | [value] ± [std] | results/comparison/dataset-a/summary.json:fold_mean_auc |
| Ours | Dataset-A [FeatureExtractor] | [value] ± [std] | results/ours/[config]/dataset-a/summary.json |

## Table II (Ablation)
...

## Figure 2 (Norm progression)
- After stage 1: results/ours/analysis/norm_progression.json:after_stage1
- After stage 2: results/ours/analysis/norm_progression.json:after_stage2
- After ProposedModule: results/ours/analysis/norm_progression.json:after_proposed
```

---

## Step 6: Reproducibility Checklist

Before writing claims from results:

- [ ] All random seeds documented
- [ ] All hyperparameters logged (not just the final config — include what was tried)
- [ ] Training curves saved (confirm training completed, not crashed early)
- [ ] All 5 folds completed (no partial fold averaging)
- [ ] Std computed with consistent formula (population or sample, not mixed)
- [ ] Hardware and software environment documented (GPU, PyTorch version, CUDA)

---

## Step 7: Rules Against Inventing Results

**Absolutely forbidden:**
- Writing "our method achieves X%" before the experiment runs
- Averaging 3 folds and pretending it's 5-fold
- Using validation AUC instead of test AUC
- "Adjusting" a result to match an expected trend
- Running the proposed method with different data preprocessing than baselines

**If a result is missing:** Write `TODO_RESULT_NEEDED: run [config] on [dataset] for fold [N]` in the draft.

---

## Step 8: Sensitivity Analysis Protocol

For hyperparameter sensitivity tables:
- Test each hyperparameter independently (other params at default)
- Use the SAME fold (fold-0) for all sensitivity comparisons
- Log fold-0 results separately from full 5-fold results
- Never cherry-pick a fold that makes the default look good

---

## Step 10: Bounded Experiment Loop (autoresearch-style)

Use this after the experiment matrix is locked and the baseline is confirmed runnable.
Full details in `20_AUTONOMOUS_EXPERIMENT_LOOP.md`. This is the compressed reference.

### When to use
- You have a runnable baseline with a measurable metric
- You want to explore modifications (architecture, hyperparameters, loss, etc.) systematically
- You need a traceable result record before writing any performance claim

### Setup checklist (complete before running)

- [ ] `experiment-plan.md` exists with: objective, editable files, protected files, metric, budget
- [ ] Evaluation harness is listed in protected files
- [ ] Baseline exists or will be the first run
- [ ] Git is clean (nothing staged or unstaged)
- [ ] A non-main branch is checked out (or will be created)

### Fixed rules (never deviate)

| Rule | Detail |
|------|--------|
| One editable file per experiment (preferred) | Isolates the variable being tested |
| Protected files: never touch | Evaluation harness, data, baseline results |
| Baseline first | Run zero-modification before any EXP-N |
| Commit before running | Commit hash links code to result |
| Log every run | Even crashes — append-only in results.tsv |
| Keep if metric improves; revert if not | Discard = `git revert HEAD` |
| Simplicity tiebreaker | Equal metric: prefer fewer lines |
| Hard budget | max_experiments: user-defined, never exceeded |

### Result log format (results.tsv)

```
exp_id	commit_hash	metric_value	peak_memory_mb	runtime_s	status	description
BASELINE	[hash]	[value]	[mem]	[time]	BASELINE	unmodified baseline
EXP-1	[hash]	[value]	[mem]	[time]	PASS	[hypothesis]
EXP-2	[hash]	NaN	NaN	[time]	CRASH	[hypothesis]
```

Full format spec: `21_EXPERIMENT_LOG_FORMAT.md`.

### Evidence output (required before paper writing)

After the loop:
1. `evidence_ledger.md` — one `EV-EXP-N` entry per PASS run
2. `result_to_claim_map.md` — link each PASS run to the paper claim it supports
3. Phase 8 (Evidence and Result Tracking) uses these artifacts as its inputs

### Invoking the loop

```
/experiment-loop
```

See `.claude/skills/experiment-loop/SKILL.md` for full execution steps.

---

## Step 9 (renumbered): Multi-seed Stability Protocol

If you report multi-seed results:
- Run with ≥ 3 seeds (not 2 — insufficient for variance estimation)
- Report: per-seed mean, inter-seed std
- Compare inter-seed std with cross-fold std explicitly
- Clearly state which result (seed=42 or multi-seed average) is used in the main table
