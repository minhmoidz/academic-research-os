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
- **dialectical_score:** [0-10 | null]
  # Aggregate score từ /validate-hypothesis. null = chưa validate.
  # Chỉ hypotheses với score ≥ 6 được chạy experiment.
- **validation_status:** [PENDING | APPROVED | REJECTED | REVISE]
  # PENDING = chưa validate
  # APPROVED = dialectical_score ≥ 6 AND no fatal_flaw → có thể chạy proxy
  # REJECTED = score < 6 OR fatal_flaw detected → không chạy experiment
  # REVISE = cần viết lại argument trước khi validate lại
- **proxy_status:** [NOT_RUN | PROXY_PASS | PROXY_KILL | PROXY_NAN | PROXY_FAIL]
  # NOT_RUN = proxy chưa chạy
  # PROXY_PASS = passed kill_if check → proceed to full run
  # PROXY_KILL = failed kill_if → abandoned
  # PROXY_NAN = NaN encountered → investigate
  # PROXY_FAIL = crash/error → fix code
- **proxy_metric:** [float | null]
  # Primary metric value sau proxy run. null nếu NOT_RUN.
- **tournament_round:** [null | 0 | 1 | 2 | WINNER | ELIMINATED]
  # null = single hypothesis (not in tournament)
  # 0 = competed in proxy round
  # 1 = survived to 1-fold round
  # 2 = survived to 3-fold round
  # WINNER = tournament winner
  # ELIMINATED = eliminated in tournament round N
- **max_gpu_hours:** [float | null]
  # Hard cap trên compute budget cho hypothesis này (GPU-hours)
  # Experiment tự động kill nếu vượt quá. null = no cap.
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
    If a cross-attention gating (CGA) module is added to the GMMamba backbone before patch
    aggregation, then the 5-fold mean AUC on TCGA-ESCA will increase by at least 1.5 percentage
    points compared to the vanilla GMMamba baseline.
- **motivation:** >
    GMMamba aggregates patch features with equal weighting across the sequence. Pathological
    features in WSIs are spatially heterogeneous, so a gating mechanism should suppress irrelevant
    patches. Prior work on attention-gating in MIL (ABMIL, TransMIL) shows consistent gains on
    TCGA datasets. We expect the gain to be larger on ESCA than Lung due to higher intra-slide
    heterogeneity in ESCA.
- **expected_observation:** >
    val_auc on TCGA-ESCA will increase from ~0.855 (GMMamba baseline) to ≥ 0.870 with CGA added.
- **experiment_assigned:** EXP-003
- **metric:** val_auc (5-fold mean ± std)
- **success_criterion:** val_auc ≥ 0.870 on TCGA-ESCA
- **failure_criterion:** val_auc < 0.860 or no statistically meaningful gap from baseline
- **possible_outcomes:**
    - supports: val_auc ≥ 0.870
    - partially_supports: 0.860 ≤ val_auc < 0.870
    - contradicts: val_auc < 0.860 or degrades
    - inconclusive: fold variance > 0.030, masking true effect
- **current_status:** supported
- **evidence:** EXP-003 → val_auc = 0.8823 ± 0.0091 (TCGA-ESCA, 5-fold); logged 2025-04-02
- **decision:** KEEP — HYP-001 becomes contribution candidate CC-01 in contribution_contract.md
- **next_action:** Proceed to ablation to confirm CGA contributes independently of other modules.
```

---

### HYP-002 — Contradicted

```markdown
## HYP-002

- **hypothesis_id:** HYP-002
- **date_registered:** 2025-03-12
- **stage_registered:** 2
- **hypothesis_text:** >
    If a learnable sequence (LS) positional token is prepended to the patch sequence in GMMamba,
    then the 5-fold mean AUC on TCGA-Lung will increase by at least 1.0 percentage point over
    GMMamba without LS.
- **motivation:** >
    GMMamba processes patches as an unordered set. WSI patch ordering along the tissue scan path
    may contain structural information. Prepending a learnable positional token, similar to the
    CLS token in ViT, could anchor global context for the Mamba sequence model.
- **expected_observation:** >
    val_auc on TCGA-Lung will increase from ~0.948 (GMMamba) to ≥ 0.958 with LS token.
- **experiment_assigned:** EXP-005
- **metric:** val_auc (5-fold mean)
- **success_criterion:** val_auc ≥ 0.958 on TCGA-Lung
- **failure_criterion:** val_auc < 0.948 (degradation) or no meaningful change
- **possible_outcomes:**
    - supports: val_auc ≥ 0.958
    - partially_supports: 0.948 ≤ val_auc < 0.958
    - contradicts: val_auc < 0.948
    - inconclusive: high fold variance
- **current_status:** contradicted
- **evidence:** EXP-005 → val_auc = 0.9421 ± 0.0114 (TCGA-Lung, 5-fold); degraded from
    baseline 0.948; logged 2025-04-08
- **decision:** DIAGNOSE — investigate whether LS token disrupts Mamba sequence length assumptions.
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
    If the AHGR (Adaptive Hierarchical Graph Reasoning) module is appended after the GMMamba
    encoder, then the 5-fold macro-F1 on TCGA-ESCA will increase by at least 2 percentage points
    compared to GMMamba without AHGR.
- **motivation:** >
    WSI patches share regional morphological context. Graph-based reasoning over patch neighborhoods
    has been shown to capture tissue architecture. AHGR adds local-global graph reasoning at
    adaptive scales, potentially capturing context missed by the linear Mamba scan.
- **expected_observation:** >
    macro_f1 on TCGA-ESCA will increase from ~0.79 (GMMamba) to ≥ 0.81 with AHGR.
- **experiment_assigned:** EXP-007
- **metric:** macro_f1 (5-fold mean)
- **success_criterion:** macro_f1 ≥ 0.81 on TCGA-ESCA
- **failure_criterion:** macro_f1 < 0.79 or fold std > 0.040
- **possible_outcomes:**
    - supports: macro_f1 ≥ 0.81
    - partially_supports: 0.79 ≤ macro_f1 < 0.81
    - contradicts: macro_f1 < 0.79
    - inconclusive: fold std > 0.040 masking effect
- **current_status:** inconclusive
- **evidence:** EXP-007 → macro_f1 = 0.8071 ± 0.0431 (TCGA-ESCA, 5-fold); std too high to
    conclude; logged 2025-04-15
- **decision:** REFINE — insufficient evidence. Increase seed count from 5 to 10; check for
    data imbalance in fold splits.
- **next_action:** Register HYP-008 with larger evaluation budget. Do not claim AHGR as a
    confirmed contribution until HYP-008 resolves.
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

---

## Field Quick Reference

| Field | Required | Set by | Used by |
|-------|----------|--------|---------|
| id | Yes | User/Claude | All protocols |
| registered | Yes | /research-start or /gap-scout | Decision log |
| status | Yes | Updated throughout | hypothesis_registry |
| type | Yes | User | Contribution map |
| claim | Yes | User | TRC, paper |
| hypothesis | Yes | User | Dialectical validation |
| rationale | Yes | User | Dialectical validation |
| prediction | Yes | User | Proxy kill check |
| success_criterion | Yes | User | Result Adequacy Gate |
| experiment | Yes | experiment-loop | results.tsv |
| evidence | Yes (after exp) | result-backfill | claim-evidence-table |
| conclusion | Yes (after exp) | User/Claude | paper |
| next_action | Optional | Claude | Session planning |
| **dialectical_score** | Yes (before exp) | /validate-hypothesis | Proxy gate |
| **validation_status** | Yes (before exp) | /validate-hypothesis | experiment-loop |
| **proxy_status** | Yes (after proxy) | /proxy-run | Full run decision |
| **proxy_metric** | Yes (after proxy) | /proxy-run | Tournament ranking |
| **tournament_round** | If tournament | /hypothesis-tournament | Tournament tracking |
| **max_gpu_hours** | Optional | User | Hard budget cap |
