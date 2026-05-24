# Target Result Contract (TRC)

## Purpose

The Target Result Contract defines the minimum result requirements that must be specified **before** confirmatory experiments are run. It is the binding agreement between the researcher and the research system about what counts as success, what counts as failure, and what claims are permitted under each outcome.

**Core rule:** The result requirements must be defined before confirmatory experiments are run. Claude must not define pass/fail criteria after seeing results. Any TRC created or modified after confirmatory experiments begin is invalid and must be flagged.

---

## When to Create a TRC

- **Stage 9** (Target Result Contract): before any confirmatory experiment
- **Stage 14** (Confirmatory Experiment Planning): if a pivot changes the claim, a new TRC must be created before re-running experiments
- Never at Stage 15 (Experiment Execution) or later

---

## When a TRC Can Be Modified

A TRC may only be modified before the first confirmatory experiment run. If modification is needed after experiments have begun:

1. Mark the old TRC as `SUPERSEDED` with a timestamp
2. Create a new TRC with a new `contract_id`
3. Log a Decision Entry (DEC) in `decision_log.md`:
   - `DEC-NNN: TRC-NNN superseded by TRC-MMM. Reason: [reason]. Date: [date]. Experiments run before change: [list or "none"].`
4. If any experiments were already run, those results are **exploratory** and cannot be used to evaluate the new TRC's pass/fail condition

---

## TRC Template

Save as: `target_result_contract.md` in the project root.

```markdown
# Target Result Contract

contract_id: TRC-001
date_created: YYYY-MM-DD  # MUST be before confirmatory experiments
stage_created: Stage 9    # Must be Stage 9 or Stage 14
status: ACTIVE            # ACTIVE | SUPERSEDED | EVALUATED

## Venue and Paper Type

target_venue: [full venue name, e.g., "MICCAI 2025"]
venue_tier: [A* | A | B | Workshop]
paper_type: [empirical | method | system | analysis | survey]

## Main Claim

main_claim: >
  [One falsifiable performance claim. Must be specific enough to be testable.
   Example: "The proposed ProposedModule module improves AUC on Dataset-A by at least
   1.0 percentage point over the best BaselineModel baseline under 5-fold CV."]

## Required Baselines

required_baselines:
  - method: BaselineModel
    why: direct backbone; measures contribution of our additions
  - method: ComparisonMethod
    why: prior Mamba-based MIL method on same task
  - method: TransMIL
    why: transformer-based MIL; establishes cross-paradigm comparison
  - method: ACMIL
    why: attention-based MIL; establishes classic baseline
  - method: DSMIL
    why: dual-stream MIL; common benchmark baseline

## Required Datasets

required_datasets:
  - dataset: Dataset-A
    why: primary evaluation; rare cancer, limited prior MIL benchmarks
    split: 5-fold cross-validation, stratified by slide label
  - dataset: Dataset-B ([ClassA]+[ClassB])
    why: secondary evaluation; large, well-benchmarked MIL dataset

## Required Metrics

required_metrics:
  - metric: AUC (Area Under ROC Curve)
    definition: Area under the receiver operating characteristic curve
    formula: "∫ TPR d(FPR) via trapezoidal integration across thresholds"
    report_as: mean ± std across 5 folds
  - metric: Accuracy
    definition: Fraction of correctly classified slides
    formula: "(TP + TN) / (TP + TN + FP + FN)"
    report_as: mean ± std across 5 folds
  - metric: F1-Score (macro)
    definition: Harmonic mean of precision and recall, averaged across classes
    formula: "2 * (P * R) / (P + R), macro-averaged"
    report_as: mean ± std across 5 folds

std_formula: population std (divide by N=5, not N-1)

## Required Seeds / Runs

required_seeds_or_runs:
  minimum: 5-fold cross-validation, single fixed seed per fold
  preferred: 5-fold × 3 seeds (15 total runs) if compute allows
  note: >
    Minimum is 5 folds. Results from fewer folds are exploratory only and
    cannot be used for TRC evaluation. Seed must be fixed and reported.

## Required Ablations

required_ablations:
  - ablation: AttentionModule module removed (backbone only)
    purpose: isolate contribution of cross-granularity attention
  - ablation: CLS module removed
    purpose: isolate contribution of classification head design
  - ablation: ProposedModule module removed
    purpose: isolate contribution of adaptive hypergraph regularization
  - ablation: LS module removed
    purpose: isolate contribution of label smoothing / training strategy
  - ablation: All modules removed (= BaselineModel baseline)
    purpose: verify the ablation baseline matches the reported BaselineModel result

## Required Analysis

required_analysis:
  - type: Attention / saliency visualization
    description: >
      Show which patches the model attends to on at least 2 representative slides
      per dataset. Compare with BaselineModel baseline attention maps.
  - type: Confusion matrix
    description: Per-class error analysis for Dataset-A and Dataset-B
  - type: Convergence curve
    description: Train/val loss curves for one representative fold (to rule out overfitting)

## Required Robustness Checks

required_robustness_checks:
  - check: Cross-dataset consistency
    description: >
      Both Dataset-A and Dataset-B must show positive trends. If one dataset
      shows regression, this must be disclosed and analyzed.
  - check: Sensitivity to hyperparameters
    description: >
      Report results under ±20% variation of the two most important
      hyperparameters (e.g., number of hypergraph neighbors, smoothing factor).
  - check: Stability across folds
    description: >
      Per-fold AUC must not deviate more than 3.0pp from the mean on any fold.
      Outlier folds must be reported, not hidden.

## Minimum Acceptable Results

minimum_acceptable_result:
  primary_metric: AUC
  primary_dataset: Dataset-A
  threshold: "> 0.920"
  note: Mean AUC across 5 folds must exceed 0.920

minimum_acceptable_stability:
  metric: AUC
  max_std: "< 0.010"  # i.e., cross-fold std < 1.0 percentage points
  note: If std ≥ 1.0pp, results are considered unstable and cannot support
        the main performance claim without additional analysis

## Comparison Against Best Prior

comparison_against_best_prior:
  best_prior_method: BaselineModel
  best_prior_value: TODO_RESULT_NEEDED  # fill from verified baseline run
  best_prior_source: our reproduction under identical protocol
  required_gap: ">= +0.5pp AUC on Dataset-A"
  note: >
    The gap must be on the same evaluation protocol (same 5-fold splits,
    same preprocessing). Comparing to numbers from different protocols is forbidden.

## Pass Condition

pass_condition: >
  ALL of the following must be true:
  1. Mean AUC on Dataset-A > 0.920 (5-fold CV, population std)
  2. Cross-fold AUC std < 1.0pp on Dataset-A
  3. AUC gain over BaselineModel baseline >= +0.5pp on Dataset-A
  4. At least 3 of 4 ablation components show individually positive contribution
  5. Results on Dataset-B are non-negative (AUC >= BaselineModel)
  6. All 5 required baselines have been reproduced under identical protocol

## Fail Condition

fail_condition: >
  ANY of the following is true:
  1. Mean AUC on Dataset-A <= 0.920
  2. Cross-fold AUC std >= 1.0pp on Dataset-A
  3. AUC over BaselineModel baseline < +0.5pp on Dataset-A
  4. Fewer than 3 ablation components show individually positive contribution
  5. Results on Dataset-B are significantly worse than BaselineModel (> -1.0pp AUC)
  6. Any required baseline is missing from the comparison

## Fallback Plan

fallback_plan:
  if_fail_by_margin:  # results close but not quite at threshold
    action: RUN_MORE_EXPERIMENTS
    description: >
      Run 3 additional seeds on Dataset-A. If mean improves above threshold,
      report the full set of runs. If not, downgrade claim or venue.

  if_fail_significantly:  # results well below threshold
    action: NARROW_CLAIM
    description: >
      If AUC improvement is < +0.5pp, change the main claim to focus on
      stability improvement (std reduction) if std is meaningfully lower.
      Create new TRC-002 for the narrowed claim.

  if_unstable:  # high variance, low std
    action: PIVOT_ROBUSTNESS
    description: >
      If our method has lower cross-fold std than BaselineModel by >= 30%, frame
      as a robustness contribution. Main claim shifts to stability.
      Create new TRC-002.

  if_negative:  # results worse on both datasets
    action: PIVOT_ANALYSIS or ABANDON
    description: >
      If the method fails on both datasets, analyze failure modes.
      If failure analysis reveals a genuine finding (e.g., hypergraph construction
      degrades on sparse slides), consider an analysis paper.
      If no genuine finding, ABANDON and log decision.

## Claims Allowed If Pass

claim_allowed_if_pass: >
  "The proposed method achieves [AUC value] AUC on Dataset-A, exceeding BaselineModel
  by [gap]pp under 5-fold cross-validation. Ablation experiments confirm that
  [module] contributes the largest individual gain of [value]pp."

## Claims Forbidden If Fail

claim_forbidden_if_fail:
  - "Our method outperforms all baselines"      # if any baseline is not beaten
  - "state-of-the-art results"                   # if best prior is not beaten
  - "significant improvement"                    # if gap < +0.5pp
  - "robust across datasets"                     # if Dataset-B shows regression
  - "our method achieves X AUC"                  # if minimum threshold not met
  - "consistent improvement"                     # if cross-fold std >= 1.0pp
```

---

## Connection to Stage 16 (Result Adequacy Gate)

The TRC is the formal pass/fail criterion evaluated at Stage 16. The Result Adequacy Report (RAR) generated at Stage 16 must reference the active TRC by `contract_id` and evaluate each pass condition individually.

If any pass condition is not met:
- Claude must NOT proceed to Stage 17 (Evidence Freeze)
- Claude must NOT draft abstract, introduction, or contribution list
- Claude must run `/pivot-decision` and log a DEC entry

---

## Example: MIL Paper on GenericBenchmark Datasets

The following illustrates realistic thresholds for a MIL paper comparing against BaselineModel on Dataset-A and Dataset-B:

| Condition | Realistic Threshold | Rationale |
|-----------|-------------------|-----------|
| Mean AUC (Dataset-A) | > 0.920 | Published baseline methods on [Dataset-A] range [X.XX]–[X.XX] |
| Mean AUC (Dataset-B) | > 0.960 | Dataset-B is easier; published range 0.95–0.99 |
| Cross-fold AUC std | < 1.0pp | Dataset-A has moderate size; 1.0pp is reasonable |
| Gain over BaselineModel | >= +0.5pp | Meaningful but achievable with architectural addition |
| Ablation coverage | >= 3 of 4 positive | Redundant modules are acceptable; all 4 is ideal |

These thresholds must be confirmed by the researcher and filled into the TRC **before** running confirmatory experiments. The numbers above are illustrative only — the actual TRC must reflect the specific model and dataset characteristics.

---

## TRC Lifecycle

```
Created (Stage 9)
    │
    ├─── Experiments run (Stage 15)
    │
    ├─── Evaluated (Stage 16 — Result Adequacy Gate)
    │         │
    │         ├── PASS → Stage 17 (Evidence Freeze)
    │         │
    │         └── FAIL → /pivot-decision → new TRC (Stage 14) or ABANDON
    │
    └─── Status updated to EVALUATED or SUPERSEDED
```

---

## Rules for Claude

1. Never accept a TRC created after exploratory experiments have already been run
2. Never modify a TRC's `minimum_acceptable_result` or `pass_condition` after Stage 15 begins
3. If a TRC is superseded, clearly mark both the old and new contracts in `decision_log.md`
4. At Stage 16, evaluate every pass condition individually — a partial pass is a fail
5. Never write "our method achieves X" if the TRC fail condition was triggered
6. If the user requests that Claude lower the TRC bar after seeing results, Claude must refuse and log the request in `decision_log.md`
