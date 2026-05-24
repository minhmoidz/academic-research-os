# 23 — Research Direction Update Protocol

**Purpose:** Define the structured process for updating the research direction when experimental
evidence contradicts, partially supports, or reshapes the original hypothesis. This protocol
prevents the most common form of research misconduct in ML papers: maintaining a narrative
that the data no longer supports.

---

## Core Principle

> The paper story must be built from evidence, not from the original idea alone.
> If experiments contradict the initial hypothesis, Claude must update the research direction,
> narrow the claim, pivot, downgrade the venue target, or abandon the hypothesis.
> Maintaining the original narrative despite contradicting evidence is a form of research
> misconduct. Claude must not bend the evidence to fit the story.

This protocol is triggered automatically when any of the following occur. It is never optional.

---

## Trigger Conditions

A direction update is **mandatory** when:

| Trigger | Source | Example |
|---------|--------|---------|
| Any hypothesis is marked `contradicted` | Hypothesis Registry (HYP-NNN) | AttentionModule module degrades AUC |
| An unexpected positive finding appears | Experiment log (EXP-N) | Ablation reveals unexpected synergy |
| A prior-art check finds closer work | Prior Art Table (25_PRIOR_ART) | A 2024 paper already uses the method |
| Results do not meet the target result contract | Stage 9 target contract | AUC 0.87 vs required 0.90 |
| Reviewer feedback contradicts the framing | Revision cycle | Reviewers dispute novelty claim |
| Venue requirements cannot be met with current results | 24_VENUE_TARGETING | Results insufficient for MICCAI |
| A contribution claim is found to be unsupported | Contribution contract audit | No ablation supports the claimed gain |

**A direction update is NOT triggered by:** minor wording changes, figure revisions, or
experiment reruns that produce consistent results.

---

## Direction Update Process (7 Steps)

Perform these steps in order. Do not skip steps.

```
Step 1: Log the triggering experiment or evidence
        → Record in experiment_log.md which result triggered the update.
        → Note the specific metric, value, and the registered hypothesis it contradicts.

Step 2: Update the hypothesis registry
        → Change the hypothesis status (pending → contradicted / inconclusive).
        → Add evidence field with EXP-N reference and result value.
        → Add decision field: DIAGNOSE / REFINE / PIVOT / ABANDON.
        → Add next_action.

Step 3: Create a DEC entry in decision_log.md
        → Format: DEC-NNN | YYYY-MM-DD | reason | consequence | alternatives considered
        → This entry is permanent and must not be deleted.

Step 4: Update research_direction.md
        → Increment direction_version (e.g., 1.0 → 1.1 for refinement, 1.x → 2.0 for pivot).
        → Update current_direction, evidence_so_far, what_changed, unsupported_claims.
        → Update recommended_framing and claims_to_avoid.

Step 5: Update project_state.md
        → Record current stage, last direction update, and outstanding decisions.

Step 6: Update contribution_contract.md if claims change
        → Remove or qualify any contribution claim that is no longer supported.
        → Add new potential claims from unexpected findings (with TODO_RESULT_NEEDED if
          confirmatory experiment not yet run).

Step 7: Consider running /pivot-decision skill
        → Use when the update is substantial (pivot_recommendation: pivot or abandon).
        → The skill will assess all evidence and recommend framing options.
```

---

## Template: `research_direction.md`

Create this file in the project root and update it at every direction update.

```markdown
# Research Direction

Project: [Project name]
Direction version: 1.0
Last updated: YYYY-MM-DD
Updated by: [experiment trigger / prior-art check / reviewer feedback]

---

## Original Idea

[1-3 sentences describing what the researcher started with, before any experiments.]

## Original Hypothesis IDs

- HYP-001: [one-line summary]
- HYP-002: [one-line summary]
- HYP-003: [one-line summary]

---

## Current Direction

[What the research is actually about now, based on evidence. This may differ substantially
from the original idea. If it differs, explain the divergence.]

## Direction Version History

| Version | Date | Trigger | What Changed |
|---------|------|---------|--------------|
| 1.0 | YYYY-MM-DD | Initial registration | — |
| 1.1 | YYYY-MM-DD | EXP-005 contradicted HYP-002 | LS module removed from contribution list |
| 2.0 | YYYY-MM-DD | Prior-art check found concurrent work | Framing shifted from method novelty to analysis |

---

## Evidence So Far

[Summary of what experiments have shown. Use bullet points. Every bullet must reference
an EXP-N or HYP-N ID. Do not write evidence from memory.]

- EXP-003 (HYP-001 supported): AttentionModule module improves AUC by +2.7pp on Dataset-A.
- EXP-005 (HYP-002 contradicted): LS token degrades AUC by -0.6pp on Dataset-B.
- EXP-007 (HYP-003 inconclusive): ProposedModule shows positive trend but high fold variance.

---

## Supported Claims

[Only claims backed by supported hypotheses. Format: Claim | Evidence ID | Strength]

| Claim | Evidence | Strength |
|-------|----------|----------|
| AttentionModule module improves Dataset-A metric | EXP-003, HYP-001 | Strong (5-fold, low std) |

---

## Unsupported Claims

[Claims that were initially planned but are no longer supported. These must NOT appear
in the paper. Claude must enforce this list during writing.]

| Claim | Reason No Longer Supported | Logged In |
|-------|---------------------------|-----------|
| LS token improves Lung classification | HYP-002 contradicted by EXP-005 | DEC-003 |

---

## New Hypotheses Discovered Through Experiments

[Unexpected findings that have become new hypotheses. These are not yet claims.]

- HYP-008: [Registered YYYY-MM-DD after EXP-007; confirmatory experiment pending]

---

## Recommended Framing

[How to frame the paper given actual evidence. This may be different from the originally
planned framing. Be specific about what can and cannot be claimed.]

Example: "The paper should be framed as a component analysis of attention-gating mechanisms
in Mamba-based MIL, with AttentionModule as the primary supported contribution. Do not frame the paper
as a complete system paper given ProposedModule is still inconclusive."

---

## Claims to Avoid

[Explicit list of things the paper must NOT claim, with justification.]

- Do NOT claim LS token improves performance (contradicted by EXP-005).
- Do NOT claim ProposedModule is a confirmed contribution (HYP-003 inconclusive; needs HYP-008).
- Do NOT claim results generalize beyond Dataset-A and Dataset-B (not tested).

---

## Next Experiments

[What experiments would strengthen the current direction. Each entry must reference a
planned EXP-N or a new hypothesis.]

- EXP-008: Larger evaluation of ProposedModule (10 seeds) → tests HYP-008
- EXP-009: Cross-dataset evaluation on Dataset-C → tests generalization

---

## Pivot Recommendation

[none / narrow / pivot / downgrade-venue / abandon]

Current recommendation: **narrow**
Rationale: [Explain why this pivot level is appropriate given current evidence.]

---

## Venue Impact

[If direction changed, assess impact on venue targeting. Reference 24_VENUE_TARGETING.md.]

Current venue target: [venue]
Is current evidence sufficient for this venue? [yes / marginal / no]
Recommended venue action: [proceed / downgrade to Tier N / add experiments first]
```

---

## Common Direction Update Patterns

These patterns describe frequent research situations and how to handle each.

### Pattern 1: Initial idea too broad

**Situation:** The original idea was stated at a general level (e.g., "attention improves MIL").
Experiments show improvement on one dataset but not another, or only for one metric.

**Correct response:** Narrow the contribution claim to the specific setting where it works.
Update `current_direction` to reflect the narrower scope. Update `claims_to_avoid` to forbid
the broad generalization. This is acceptable scientifically — narrower claims are honest claims.

**Incorrect response:** Claiming the broad result while "supplementing" with the positive case.

---

### Pattern 2: Performance gain smaller than expected

**Situation:** The method works, but the gain is +0.8pp instead of the expected +2.0pp. The gain
is real but does not meet the success criterion for the target venue.

**Correct response:** Frame around stability, robustness, or computational efficiency if those
hold. Downgrade venue if the gain is insufficient for the original target. Do not inflate the
result or cherry-pick the best fold.

**Incorrect response:** Reporting only the best fold, or redefining the metric to show a larger gap.

---

### Pattern 3: Prior work already does it

**Situation:** A prior-art check (Stage 6, `25_PRIOR_ART_COMPETITION.md`) finds a concurrent or
prior paper using the same method.

**Correct response:** Differentiate explicitly (different task, dataset, analysis angle, or scale).
If differentiation is impossible, pivot to a comparison or analysis paper. Update
`contribution_contract.md` to replace novelty claims with differentiation claims.

**Incorrect response:** Ignoring the prior work or citing it without discussing the overlap.

---

### Pattern 4: Only works on one dataset

**Situation:** The method improves AUC on Dataset-A but shows no improvement on Dataset-B.

**Correct response:** Limit the scope of the claim to Dataset-A. Add a clear limitation section.
Investigate whether there is a dataset-specific reason (class balance, slide quality, etc.) and
frame it as an analysis finding.

**Incorrect response:** Presenting the Dataset-A result as the headline and downplaying the Dataset-B result.

---

### Pattern 5: Method doesn't work at all

**Situation:** All tested hypotheses are contradicted. The method underperforms the baseline.

**Correct response:** Consider pivoting to a failure-mode analysis, a negative result paper, or
abandoning the direction. A well-documented negative result has scientific value. Log all
decisions in `decision_log.md`. Notify the researcher and recommend a frank reassessment.

**Incorrect response:** Continuing to pursue the direction with hope that a new hyperparameter
will fix it, without updating the hypothesis registry.

---

## What Claude Must Never Do

- Revert a `contradicted` hypothesis to `pending` to justify running more experiments.
- Write contribution claims for hypotheses that are `inconclusive` or `contradicted`.
- Use results from an experiment that tested a different variant than specified in the hypothesis.
- Copy SOTA results from memory to fill `evidence` fields without experiment log backing.
- Change the `recommended_framing` to match the original idea rather than the actual evidence.
- Omit the `claims_to_avoid` section from `research_direction.md`.

---

## Relationship to Other Files

| File | Role in Direction Update |
|------|--------------------------|
| `hypothesis_registry.md` | Source of truth for what was predicted and what happened |
| `decision_log.md` | Permanent record of all direction decisions |
| `contribution_contract.md` | Updated whenever a claim is added, qualified, or removed |
| `experiment_log.md` | Evidence source; no evidence exists without an entry here |
| `24_VENUE_TARGETING.md` | Venue may need to be downgraded after direction update |
| `25_PRIOR_ART_COMPETITION.md` | May trigger direction update if closer work is found |
| `project_state.md` | Reflects current stage and outstanding direction decisions |
