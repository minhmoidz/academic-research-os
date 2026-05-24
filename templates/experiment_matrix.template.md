# Experiment Matrix

Fill this before running anything. Lock it before running any confirmatory experiment.

---

## Task

[e.g., binary classification via 5-fold cross-validation]

## Datasets

| Dataset | N samples | N classes | Feature extractor | Split protocol | File path |
|---------|-----------|-----------|-------------------|----------------|-----------|
| [Dataset-A] | [N] | [K] ([Class1/Class2]) | [Extractor (Ddim)] | [Patient/Sample]-level [K]-fold seed=[S] | data/[dataset]/ |
| [Dataset-B] | [N] | [K] | [Extractor] | [same protocol] | data/[dataset]/ |

## Baselines

| Method | Code path | Config file | Verified runnable? | Expected runtime |
|--------|-----------|-------------|-------------------|-----------------|
| [BaselineModel] | models/[model]/ | configs/[model].yaml | [✓ / ✗ TODO] | ~[N]h/fold |
| [ComparisonMethod] | models/[method]/ | configs/[method].yaml | [✓ / ✗ TODO] | ~[N]h/fold |

## Proposed Method

| Config | Key hyperparams | Result dir |
|--------|-----------------|-----------|
| [config-name] | [param1=val, param2=val] | results/[method]/ |

## Primary Metric

[e.g., Mean AUC over [K] folds (population std)]

---

## Exploratory Experiments (Type 1 — discovery only, no paper claims)

| Exp ID | Hypothesis | Config change | Dataset | Status |
|--------|-----------|--------------|---------|--------|
| EXP-E1 | [HYP-NNN] | [what changes] | [Dataset] | [PENDING / DONE] |
| EXP-E2 | [HYP-NNN] | [what changes] | [Dataset] | [PENDING / DONE] |

## Diagnostic Experiments (Type 2 — explain failures)

| Exp ID | Purpose | Triggered by | Status |
|--------|---------|-------------|--------|
| EXP-D1 | [Explain why EXP-E1 failed] | [Contradicted hypothesis] | [PENDING / DONE] |

## Confirmatory Experiments (Type 3 — require signed TRC)

| Exp ID | Hypothesis | Config | Datasets | Folds | Status |
|--------|-----------|--------|---------|-------|--------|
| EXP-C1 | [HYP-NNN] | [ProposedMethod full] | [Dataset-A, Dataset-B] | All [K] | [PENDING / DONE] |

## Ablation Designs

| Config | Components active | Purpose |
|--------|-------------------|---------|
| +[ModuleA] only | [ModuleA]=yes, others=no | Isolate [ModuleA] contribution |
| +[ModuleB] only | [ModuleB]=yes, others=no | Isolate [ModuleB] contribution |
| +[ModuleA]+[ModuleB] | Both=yes, [ModuleC]=no | Combined without final component |
| Full model | All components | Full contribution |

---

## Protected Files (Never Modify During Experiments)

- `evaluate.py` (or equivalent evaluation harness)
- `data/` (all dataset files and splits)
- `results/[baselinemodel]/` (baseline results)
