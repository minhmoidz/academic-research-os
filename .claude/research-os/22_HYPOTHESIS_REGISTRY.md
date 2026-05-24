# 22 — Hypothesis Registry

**Purpose:** Pre-register all research hypotheses before experiments run. This prevents post-hoc
rationalization — the practice of inventing a "story" around results after seeing them, rather
than testing a genuine prediction. Every claim in the final paper must trace back to a registered
hypothesis that was written before the experiment that tests it.

---

## Core Principle

> A hypothesis is a falsifiable prediction written in ignorance of its outcome.
> If you already know the result when you write the hypothesis, it is not a hypothesis — it is a
> description. Descriptions do not constitute scientific contribution.

**Anti-hallucination enforcement:** Claude must never update a hypothesis `status` field until the
experiment that tests it has produced a real logged result in the experiment log
(`experiment_log.md`). Changing a hypothesis status without evidence is a protocol violation.

---

## When to Register Hypotheses

Hypotheses are registered at specific stages of the research workflow:

| Stage | When to Register |
|-------|-----------------|
| Stage 2 | Initial research idea → first hypothesis from intuition |
| Stage 4 | After literature review → refined hypotheses based on gaps found |
| Stage 8 | After pilot experiments → new hypotheses from unexpected findings |
| Stage 12 | Confirmatory experiments → hypotheses about ablation components |
| Stage 13 | After direction update → hypotheses for the revised framing |

**Rule:** If an experiment reveals an unexpected finding, that finding becomes a new hypothesis
(HYP-NNN), not an immediate claim. The new hypothesis must be tested by a subsequent confirmatory
experiment before being stated as a contribution.

---

## Hypothesis ID Format

```
HYP-001, HYP-002, HYP-003, ...
```

IDs are assigned sequentially regardless of stage. Once assigned, an ID is never reused, even if
the hypothesis is abandoned.

---

## Status Transition Diagram

```
[pending]
    |
    | (experiment started)
    v
[testing]
    |
    +-------> [supported]            — metric exceeds success_criterion
    |
    +-------> [partially_supported]  — metric moves in predicted direction
    |                                  but does not reach success_criterion
    +-------> [contradicted]         — metric moves opposite to prediction,
    |                                  or success_criterion definitively not met
    +-------> [inconclusive]         — experiment result is noisy, invalid,
                                       or underpowered to decide
```

**Transitions are one-way.** A hypothesis cannot be moved back from `contradicted` to `pending`.
If the researcher believes a new experiment could re-test, they must register a new hypothesis
(e.g., HYP-007 as a refinement of HYP-002).

**Abandoned hypotheses:** If a hypothesis is dropped without testing (e.g., because the research
direction pivots), mark it `abandoned` and log a DEC entry in `decision_log.md`.

---

## Hypothesis Registry Template

Create this file at the project root: **`hypothesis_registry.md`**

```markdown
# Hypothesis Registry

Project: [Project name]
Last updated: [YYYY-MM-DD]
Total hypotheses: [N]
Supported: [N] | Partially supported: [N] | Contradicted: [N] |
Inconclusive: [N] | Pending: [N] | Testing: [N] | Abandoned: [N]

---

## HYP-001

- **hypothesis_id:** HYP-001
- **date_registered:** YYYY-MM-DD  ← must be BEFORE experiment
- **stage_registered:** 2
- **hypothesis_text:** >
    If [intervention X] is applied to [model/system Y] under [condition Z], then [outcome metric]
    will [increase/decrease] by at least [delta] compared to [baseline].
- **motivation:** >
    [2-3 sentences explaining why this is expected based on prior work or domain knowledge.
    No result values may be cited here — only reasoning.]
- **expected_observation:** >
    [Metric name] on [dataset] will [increase/decrease] from approximately [baseline value] to
    at least [target value] when comparing [ablated model A] vs [ablated model B].
- **experiment_assigned:** EXP-001
- **metric:** [e.g., val_auc, test_acc, macro_f1]
- **success_criterion:** [e.g., "val_auc ≥ 0.90 averaged across 5 folds"]
- **failure_criterion:** [e.g., "val_auc < 0.87, or no improvement over baseline in 3/5 folds"]
- **possible_outcomes:**
    - supports: metric meets success_criterion
    - partially_supports: metric improves but does not reach threshold
    - contradicts: metric degrades or shows no effect
    - inconclusive: high variance across folds, experiment error, or confound found
- **current_status:** pending
- **evidence:** none yet
- **decision:** none yet
- **next_action:** Run EXP-001; do not update status until experiment log entry exists.
```

---

## Example Registry: Three Hypotheses with Different Outcomes

### HYP-001 — Supported

```markdown
## HYP-001

- **hypothesis_id:** HYP-001
- **date_registered:** 2025-03-10
- **stage_registered:** 2
- **hypothesis_text:** >
    If an [AttentionModule] is added to [BaselineModel] before patch aggregation, then the
    5-fold mean AUC on [Dataset-A] will increase by at least 1.5 percentage points compared
    to the vanilla [BaselineModel] baseline.
- **motivation:** >
    [BaselineModel] aggregates patch features with equal weighting across the sequence.
    Pathological or complex features in input data are often spatially heterogeneous, so a
    gating mechanism should suppress irrelevant patches. Prior work on attention-gating in
    similar settings shows consistent gains on comparable datasets. We expect the gain to be
    larger on [Dataset-A] than [Dataset-B] due to higher intra-sample heterogeneity.
- **expected_observation:** >
    val_auc on [Dataset-A] will increase from approximately 0.855 ([BaselineModel] baseline)
    to at least 0.870 with [AttentionModule] added.
- **experiment_assigned:** EXP-003
- **metric:** val_auc (5-fold mean ± std)
- **success_criterion:** val_auc ≥ 0.870 on [Dataset-A]
- **failure_criterion:** val_auc < 0.860 or no statistically meaningful gap from baseline
- **possible_outcomes:**
    - supports: val_auc ≥ 0.870
    - partially_supports: 0.860 ≤ val_auc < 0.870
    - contradicts: val_auc < 0.860 or degrades
    - inconclusive: fold variance > 0.030, masking true effect
- **current_status:** supported
- **evidence:** EXP-003 → val_auc = 0.8823 ± 0.0091 ([Dataset-A], 5-fold); logged 2025-04-02
- **decision:** KEEP — HYP-001 becomes contribution candidate CC-01 in contribution_contract.md
- **next_action:** Proceed to ablation to confirm [AttentionModule] contributes independently of other modules.
```

---

### HYP-002 — Contradicted

```markdown
## HYP-002

- **hypothesis_id:** HYP-002
- **date_registered:** 2025-03-12
- **stage_registered:** 2
- **hypothesis_text:** >
    If a learnable sequence (LS) positional token is prepended to the input sequence in
    [BaselineModel], then the 5-fold mean AUC on [Dataset-B] will increase by at least
    1.0 percentage point over [BaselineModel] without LS.
- **motivation:** >
    [BaselineModel] processes inputs as an unordered set. Ordering along the scan or
    processing path may contain structural information. Prepending a learnable positional
    token, similar to the CLS token in ViT, could anchor global context for the sequence model.
- **expected_observation:** >
    val_auc on [Dataset-B] will increase from approximately 0.948 ([BaselineModel]) to
    at least 0.958 with LS token.
- **experiment_assigned:** EXP-005
- **metric:** val_auc (5-fold mean)
- **success_criterion:** val_auc ≥ 0.958 on [Dataset-B]
- **failure_criterion:** val_auc < 0.948 (degradation) or no meaningful change
- **possible_outcomes:**
    - supports: val_auc ≥ 0.958
    - partially_supports: 0.948 ≤ val_auc < 0.958
    - contradicts: val_auc < 0.948
    - inconclusive: high fold variance
- **current_status:** contradicted
- **evidence:** EXP-005 → val_auc = 0.9421 ± 0.0114 ([Dataset-B], 5-fold); degraded from
    baseline 0.948; logged 2025-04-08
- **decision:** DIAGNOSE — investigate whether LS token disrupts sequence length assumptions.
- **next_action:** Run EXP-006 (LS with position normalization); if still degrading, ABANDON LS
    as standalone module. Do NOT claim LS as a positive contribution. Log DEC-003 in decision_log.md.
    See 23_RESEARCH_DIRECTION_UPDATE.md for direction update protocol.
```

---

### HYP-003 — Inconclusive

```markdown
## HYP-003

- **hypothesis_id:** HYP-003
- **date_registered:** 2025-03-15
- **stage_registered:** 4
- **hypothesis_text:** >
    If the [ProposedModule] is appended after the [BaselineModel] encoder, then the 5-fold
    macro-F1 on [Dataset-A] will increase by at least 2 percentage points compared to
    [BaselineModel] without [ProposedModule].
- **motivation:** >
    Input instances often share regional or structural context. Graph-based or hierarchical
    reasoning over instance neighborhoods has been shown to capture structure missed by
    linear sequence models. [ProposedModule] adds local-global reasoning at adaptive scales,
    potentially capturing context missed by the base encoder.
- **expected_observation:** >
    macro_f1 on [Dataset-A] will increase from approximately 0.79 ([BaselineModel]) to
    at least 0.81 with [ProposedModule].
- **experiment_assigned:** EXP-007
- **metric:** macro_f1 (5-fold mean)
- **success_criterion:** macro_f1 ≥ 0.81 on [Dataset-A]
- **failure_criterion:** macro_f1 < 0.79 or fold std > 0.040
- **possible_outcomes:**
    - supports: macro_f1 ≥ 0.81
    - partially_supports: 0.79 ≤ macro_f1 < 0.81
    - contradicts: macro_f1 < 0.79
    - inconclusive: fold std > 0.040 masking effect
- **current_status:** inconclusive
- **evidence:** EXP-007 → macro_f1 = 0.8071 ± 0.0431 ([Dataset-A], 5-fold); std too high to
    conclude; logged 2025-04-15
- **decision:** REFINE — insufficient evidence. Increase seed count from 5 to 10; check for
    data imbalance in fold splits.
- **next_action:** Register HYP-008 with larger evaluation budget. Do not claim [ProposedModule]
    as a confirmed contribution until HYP-008 resolves.
```

---

## Operational Rules

1. **Write before run.** The `date_registered` must predate the experiment start date in
   `experiment_log.md`. Claude must verify this before updating status.

2. **No quiet drops.** If a hypothesis is contradicted, it must be logged as `contradicted`.
   Deleting or silently overwriting a contradicted hypothesis is a protocol violation equivalent
   to data fabrication.

3. **Supported → contribution candidate.** A `supported` hypothesis is the only pathway to
   making a contribution claim in the paper. Update `contribution_contract.md` with the
   evidence pointer.

4. **Abandoned → decision log.** Any hypothesis marked `abandoned` requires a DEC entry in
   `decision_log.md` explaining why it was not tested.

5. **Unexpected findings → new hypothesis.** If an experiment shows an unexpected result
   (positive or negative) that was not the subject of any registered hypothesis, register it as
   a new hypothesis and design a confirmatory experiment before claiming it in the paper.

6. **Claude must not fill `evidence` with plausible-sounding values.** Every value in the
   `evidence` field must trace to an experiment log entry with a real timestamp.

---

## Link to Direction Updates

If a hypothesis is `contradicted` or `inconclusive`, refer to
**`23_RESEARCH_DIRECTION_UPDATE.md`** for the protocol on how this affects the research direction,
contribution contract, and venue targeting.
