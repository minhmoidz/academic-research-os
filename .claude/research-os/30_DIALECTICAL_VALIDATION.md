# 30 — Dialectical Validation Gate

**Stage:** 1.5 — Between Hypothesis Registration (Stage 1) and Direction Lock (Stage 2)  
**Trigger:** Any hypothesis in `hypothesis_registry.md` with `validation_status: PENDING`  
**Command:** `/validate-hypothesis HYP-NNN`  
**Blocks:** No experiment may run against a hypothesis until this gate passes.

---

## 1. Why Dialectical Validation Exists

Experiments are expensive. A 5-fold cross-validation run on a large dataset can cost 10–100 GPU-hours. Running that experiment on a hypothesis with no mechanistic grounding wastes both compute and researcher time.

Empirical observation across ML research:

> **~85% of experiments that fail have no clear mechanistic argument before they run.**  
> "Sounds good" is not a mechanism. "Attention helps because it focuses" is not falsifiable.

Dialectical validation forces the researcher to:

1. State the mechanism precisely before seeing any results
2. Find prior evidence that the mechanism works in related domains
3. Subject the argument to adversarial critique from an independent perspective
4. Produce a score that gates whether the experiment is worth running

This process borrows from **formal argumentation theory** (Toulmin's argument model, structured controversy techniques) applied to empirical ML research. The goal is not to predict success — it is to ensure the experiment is *epistemically warranted*, meaning it tests something specific that can be refuted.

---

## 2. The 3-Step Dialectical Process

### Step 1 — Constructive Subagent

**Tool:** `academic-writing-agents:brainstormer` + paper-qa index  
**Access:** Has the full hypothesis text and task context.  
**Output:** A formal mechanistic argument with five required fields.

The constructive subagent must write:

```yaml
mechanism: >
  [The specific computational or statistical mechanism being exploited.
   Must name what changes in the model/data/training and why that change
   affects the learning signal. NOT: "attention helps." YES: "Cross-attention
   between patch tokens and class queries forces the encoder to route
   discriminative gradient signal through a bottleneck, reducing spurious
   correlations learned from co-occurring background features."]

pathway: >
  [The causal chain from mechanism to metric improvement.
   Trace: mechanism activates → intermediate effect → measured metric rises.
   Must be falsifiable at each step.]

prior_evidence:
  - "[Author et al., YEAR] found that [mechanism] improved [metric] by
     [delta] in [domain/task], using [experimental setup]."
  - "[Author et al., YEAR] demonstrates [pathway] through [experiment type],
     showing [intermediate effect] correlates with [metric]."
  # Minimum 2 entries. Both must be verified via paper-qa (not recalled from memory).
  # If paper-qa returns no supporting evidence, write: "NO_EVIDENCE_FOUND — pqa query: [query]"

prediction: >
  [Quantitative or directional prediction.
   Format: "Primary metric will [increase/decrease] by approximately [X%/X points]
   relative to baseline, under conditions [C1, C2].
   Effect will be smaller when [condition that weakens mechanism]."]

falsification: >
  [What result would conclusively refute this hypothesis.
   Must be specific: "If metric does not improve by at least [threshold] on
   [split/condition], the mechanism is not operative in this setting."
   NOT: "If it doesn't work." YES: "If ablation of [component] does not
   degrade performance by >2 points, the mechanism is not responsible."]
```

**Quality bar for constructive argument:**
- Mechanism must name a specific computational process (not a category like "better features")
- Prior evidence must be queried through paper-qa, not stated from memory
- Prediction must be quantitative or have a directional bound
- Falsification must be a specific experimental outcome, not a null result

---

### Step 2 — Adversarial Subagent

**Tool:** `academic-writing-agents:research-analyst` + paper-qa index  
**Access:** Hypothesis text ONLY — must NOT see the constructive argument before running.  
**Output:** Three-angle critique.

The adversarial subagent must investigate:

```yaml
prior_failure: >
  [Find at least one paper that attempted this mechanism (or a close variant)
   and found it ineffective or harmful. Report: "[Author, YEAR] tried [mechanism]
   on [task/domain] and found [negative result] because [reason]."
   If no failure found after thorough search, write: "NO_PRIOR_FAILURE_FOUND —
   this increases novelty confidence but reduces prior calibration."]

condition_violation: >
  [Examine whether the dataset/task conditions required for the mechanism to work
   are actually present in this project's setting.
   Check: data scale, label noise level, feature dimensionality, class imbalance,
   domain shift, annotation granularity.
   Report any condition the mechanism assumes that may not hold.]

alternative_explanation: >
  [If the experiment returns a positive result, what explanations other than the
   proposed mechanism could account for it?
   Examples: regularization effect, implicit data augmentation, lucky initialization,
   the baseline being under-tuned.
   List at least 2 plausible alternatives. These become ablation targets.]
```

**Isolation requirement:** The adversarial subagent must be invoked in a separate call with only the hypothesis text (not the constructive argument). This is not optional — seeing the constructive argument causes confirmation bias in the critique.

---

### Step 3 — Adjudication (Claude main context)

After receiving both outputs, Claude scores the hypothesis on four criteria:

| Criterion | Score (0–10) | Description |
|---|---|---|
| `mechanistic_specificity` | 0–10 | Is the mechanism a specific named process, or vague category language? |
| `literature_support` | 0–10 | Are prior_evidence entries verified via pqa? Do they actually support the mechanism in a related domain? |
| `falsifiability` | 0–10 | Is there a clear, specific prediction that can be refuted? Does falsification name an experimental outcome? |
| `adversarial_resistance` | 0–10 | Does the constructive argument survive the three-angle critique without collapse? |

**Scoring guide:**
- 9–10: Exceptionally rigorous; publishable-quality mechanistic argument
- 7–8: Strong; minor gaps that do not affect the core logic
- 5–6: Marginal; argument holds but has notable weaknesses
- 3–4: Weak; vague mechanism or insufficient evidence
- 0–2: Invalid; no mechanistic content or fatal logical flaw

**Gate rule:**

```
APPROVED if: aggregate_score >= 6.0 AND fatal_flaw = NO
REVISE   if: aggregate_score >= 4.0 AND fatal_flaw = NO (specific revision required)
REJECTED if: aggregate_score < 4.0 OR fatal_flaw = YES
```

**Fatal flaw detection:** A fatal flaw is any single finding from the adversarial subagent that makes the experiment uninterpretable even if it succeeds. Examples:
- The mechanism requires data properties the dataset does not have
- The proposed change is mathematically identical to an existing baseline
- The metric cannot distinguish the proposed mechanism from the alternative explanations

---

## 3. Output Format: `dialectical_validation.md`

Create one file per hypothesis at: `research_artifacts/dialectical_validation_HYP-NNN.md`

```markdown
# Dialectical Validation

hypothesis_id: HYP-NNN
date: YYYY-MM-DD
status: PENDING | APPROVED | REJECTED | REVISE

## Constructive Argument

mechanism: >
  [Specific mechanism text]

pathway: >
  [Causal chain text]

prior_evidence:
  - "[Full citation] found that [mechanism] improved [metric] by [delta] in [domain]."
  - "[Full citation] demonstrates [pathway] through [experiment type]."

prediction: >
  [Quantitative or directional prediction with conditions]

falsification: >
  [Specific experimental outcome that would refute]

## Adversarial Critique

prior_failure: >
  [Failure case found or NO_PRIOR_FAILURE_FOUND with search query]

condition_violation: >
  [Conditions the mechanism requires that may not hold]

alternative_explanation: >
  1. [Alternative 1]
  2. [Alternative 2]

## Adjudication

mechanistic_specificity: [0-10] — [one-sentence reason]
literature_support: [0-10] — [one-sentence reason]
falsifiability: [0-10] — [one-sentence reason]
adversarial_resistance: [0-10] — [one-sentence reason]
aggregate_score: [mean of four scores, one decimal]
fatal_flaw: YES — [description] | NO

## Decision

decision: APPROVED | REJECTED | REVISE
reason: >
  [Two to four sentences explaining the decision. If REVISE, specify exactly
   what must change. If REJECTED, state which criterion failed and why.]

next_action: >
  APPROVED → Proceed to proxy experiment planning (Stage 11.5)
  REVISE   → [Specific revision required] — resubmit for re-adjudication
  REJECTED → [Abandon | Reformulate as different hypothesis HYP-NNN+1]
```

---

## 4. Common Argument Failures

The following argument patterns sound compelling but fail the mechanistic specificity criterion:

**Vague mechanism (score 0–3 on mechanistic_specificity):**
- "Attention helps because it focuses on important parts" — does not name what computationally changes or why that affects the learning objective
- "More parameters = better capacity = better performance" — not a mechanism, it is a scaling assumption
- "Works in NLP, should work in vision" — domain transfer without stating what invariant property makes the mechanism transferable
- "Ensemble of diverse models reduces variance" — true but does not explain *why* this ensemble produces diversity

**Non-falsifiable predictions (score 0–3 on falsifiability):**
- "Performance will improve" — no direction, no magnitude, no condition
- "Results will be better with enough tuning" — unfalsifiable by construction
- "The model will generalize better" — no operationalization of generalization

**Circular prior evidence (score 0–3 on literature_support):**
- Citing papers that use the same method name without evidence the mechanism transfers
- Citing survey papers or review articles instead of papers with experimental evidence
- Stating evidence from memory without running a paper-qa query

**Acceptable argument patterns (score 7–10):**
- "[Mechanism X] reduces gradient variance during training [specific citation confirms this in similar architecture], which should improve convergence stability. Prediction: training loss at epoch N/4 will be 15% lower than baseline, and this advantage will persist to final evaluation."
- "[Module Y] projects features into a subspace where [property Z] is approximately satisfied [two pqa-verified papers]. Falsification: if removing Y does not degrade performance by more than 1 point on the primary metric, Y is not exploiting Z."

---

## 5. Integration with `hypothesis_registry.md`

After adjudication, update the hypothesis entry:

```yaml
# In hypothesis_registry.md — HYP-NNN entry
hypothesis_id: HYP-NNN
description: [...]
proposed_change: [...]
stage_registered: 1
dialectical_score: [aggregate score, e.g., 7.2]
validation_status: APPROVED | REJECTED | REVISE | PENDING
validation_date: YYYY-MM-DD
validation_file: research_artifacts/dialectical_validation_HYP-NNN.md
proxy_result: null       # filled after Stage 11.5
full_run_result: null    # filled after Stage 12
```

**Enforcement rule:** The experiment-loop and proxy-run skills must check `validation_status: APPROVED` before executing any experiment. A hypothesis with `PENDING`, `REVISE`, or `REJECTED` status blocks experiment execution.

---

## 6. Relation to Other Stages

| Stage | Gate | Requires |
|---|---|---|
| Stage 1 | Hypothesis Registration | Hypothesis text + task context |
| **Stage 1.5** | **Dialectical Validation** | **Constructive + adversarial argument, aggregate ≥ 6** |
| Stage 2 | Direction Lock | At least 1 APPROVED hypothesis |
| Stage 6 | Prior-Art Check | Validation already confirmed no duplicate |
| Stage 11.5 | Proxy Run | validation_status = APPROVED required |
| Stage 12 | Exploratory Experiments | PROXY_PASS required |

---

*Last updated: 2026-05-25 | Research OS v1.0*
