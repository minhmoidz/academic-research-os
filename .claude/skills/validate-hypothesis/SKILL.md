# Skill: /validate-hypothesis

**Command:** `/validate-hypothesis HYP-NNN`  
**Stage:** 1.5 — Between Hypothesis Registration (Stage 1) and Direction Lock (Stage 2)  
**Protocol reference:** `.claude/research-os/30_DIALECTICAL_VALIDATION.md`

---

## Purpose

Run a full dialectical validation on one hypothesis entry. Produces a scored record of the mechanistic argument, adversarial critique, and adjudication decision. Updates `hypothesis_registry.md` with `dialectical_score` and `validation_status`. Only hypotheses with `validation_status: APPROVED` may proceed to proxy experiments.

---

## Required Inputs

Before running, verify these are available:

1. `hypothesis_registry.md` — must contain HYP-NNN with `validation_status: PENDING`
2. `project_profile.md` — provides `task_family`, `proposed_change`, `baseline_system` for context
3. Paper-qa index — must be accessible (check `project_profile.md` for `pqa_index_path`)
4. `research_artifacts/` directory — must exist for output file

If any input is missing, report the blocker and stop.

---

## Forbidden Actions

- Running any experiment (training, evaluation, inference) during this skill
- Marking a hypothesis `APPROVED` without computing all four adjudication scores
- Approving a hypothesis when `fatal_flaw = YES`
- Running constructive and adversarial subagents in the same call or with shared context
- Accepting prior_evidence entries that were not verified through paper-qa (memory recall is not evidence)
- Skipping the adversarial phase because the constructive argument looks strong

---

## Execution Steps

### Step 1 — Read hypothesis entry

Read `hypothesis_registry.md`. Find the entry for HYP-NNN. Extract:
- `description`: full hypothesis text
- `proposed_change`: what modification is being proposed
- `task_family`: from `project_profile.md` (classification, detection, generation, retrieval, RL, etc.)
- `baseline_system`: from `project_profile.md`

Verify `validation_status: PENDING`. If status is already `APPROVED`, `REJECTED`, or `REVISE`, report current status and stop (do not re-adjudicate without explicit user instruction).

### Step 2 — Read project context

Read `project_profile.md`. Extract relevant context fields:
- `task_family`
- `domain`
- `dataset_description` (do not include specific dataset names in the validation argument — keep it domain-level)
- `baseline_system`
- `pqa_index_path`

This context is passed to the constructive subagent to calibrate mechanism specificity.

### Step 3 — CONSTRUCTIVE PHASE

Invoke `academic-writing-agents:brainstormer` with the following prompt structure:

```
Context: [task_family] task, [domain] domain, baseline: [baseline_system]
Hypothesis: [description + proposed_change]
Paper-qa index: [pqa_index_path]

Write a formal mechanistic argument with these five fields:
  mechanism, pathway, prior_evidence (minimum 2, pqa-verified), prediction, falsification

For prior_evidence: you MUST query paper-qa using relevant search terms.
Do not state evidence from memory. If pqa returns nothing, write NO_EVIDENCE_FOUND.
```

Receive and store the constructive argument. Do not show it to the adversarial subagent.

### Step 4 — ADVERSARIAL PHASE

Invoke `academic-writing-agents:research-analyst` with ONLY the hypothesis text. Do not include the constructive argument in this call.

```
Hypothesis (no other context): [description + proposed_change]
Task: [task_family], Domain: [domain]
Paper-qa index: [pqa_index_path]

Critique this hypothesis from three angles:
  1. prior_failure: Find a paper that tried this mechanism and failed. Search pqa.
  2. condition_violation: What conditions does this mechanism require that may not hold?
  3. alternative_explanation: If experiment returns positive result, what else could explain it?
```

Receive adversarial output. Now combine with constructive argument for adjudication.

### Step 5 — ADJUDICATION

Score the combined record on four criteria (0–10 each):

**mechanistic_specificity (0–10)**
- Does the mechanism name a specific computational process?
- 0–2: Vague category language ("better features", "more context")
- 5–6: Names a process but without clear computational detail
- 8–10: Names specific operation, layer interaction, or mathematical property

**literature_support (0–10)**
- Are prior_evidence entries verified by paper-qa?
- 0–2: No pqa queries, all from memory, or NO_EVIDENCE_FOUND for both
- 5–6: One pqa-verified entry, domain adjacent
- 8–10: Two or more pqa-verified entries, same or close domain

**falsifiability (0–10)**
- Is there a specific prediction that can be refuted by a concrete experimental outcome?
- 0–2: "It will improve" — no bound, no condition
- 5–6: Directional prediction with approximate magnitude
- 8–10: Specific threshold, named split/condition, ablation target named

**adversarial_resistance (0–10)**
- Does the constructive argument survive the three-angle critique?
- 0–2: prior_failure directly contradicts the mechanism, or condition_violation is fatal
- 5–6: Critique raises concerns but constructive argument has partial answers
- 8–10: Argument addresses all three angles; alternative explanations are testable ablations

**Compute aggregate:**
```
aggregate_score = (mechanistic_specificity + literature_support + falsifiability + adversarial_resistance) / 4
```

**Detect fatal flaw:** A fatal flaw exists if any of the following is true:
- The adversarial `condition_violation` identifies a dataset property that makes the mechanism inoperative and cannot be addressed
- The adversarial `prior_failure` shows the mechanism was tried on an identical or near-identical setting and failed
- The mechanism is mathematically equivalent to the baseline (proposed change is a no-op)
- The metric cannot distinguish the mechanism from the alternative explanations even with ablations

### Step 6 — Write validation file

Create `research_artifacts/dialectical_validation_HYP-NNN.md` using the template from `30_DIALECTICAL_VALIDATION.md` Section 3. Fill all fields with actual content from steps 3–5.

### Step 7 — Update hypothesis_registry.md

Find the HYP-NNN entry and add these fields:

```yaml
dialectical_score: [aggregate_score]
validation_status: APPROVED | REJECTED | REVISE
validation_date: YYYY-MM-DD
validation_file: research_artifacts/dialectical_validation_HYP-NNN.md
```

Apply gate rule:
- `APPROVED` if `aggregate_score >= 6.0` AND `fatal_flaw = NO`
- `REVISE` if `4.0 <= aggregate_score < 6.0` AND `fatal_flaw = NO`
- `REJECTED` if `aggregate_score < 4.0` OR `fatal_flaw = YES`

### Step 8 — Report decision

Output a concise report:

```
Dialectical Validation — HYP-NNN
Decision: [APPROVED | REJECTED | REVISE]
Score: [aggregate] / 10 ([s1] / [s2] / [s3] / [s4])
Fatal flaw: [YES / NO]

[If APPROVED]
All four criteria passed. Proceed to proxy experiment planning.
Next: /proxy-run HYP-NNN --config [config path]

[If REVISE]
Specific revision required: [what must change]
Resubmit with revised argument before proceeding.

[If REJECTED]
Failed criterion: [criterion name — reason]
Recommendation: [Abandon | Reformulate as HYP-NNN+1 with different mechanism]
```

### Step 9 — Update project_state.md

Add a one-line entry:
```
[YYYY-MM-DD] Dialectical Validation: HYP-NNN → [APPROVED|REJECTED|REVISE] (score: X.X)
```

---

## Output Summary

| Artifact | Location | Content |
|---|---|---|
| `dialectical_validation_HYP-NNN.md` | `research_artifacts/` | Full validation record |
| `hypothesis_registry.md` | project root | Updated with score and status |
| `project_state.md` | project root | One-line entry added |
| Skill report | Console | Decision + score breakdown + next action |

---

## Forbidden Patterns (Enforcement)

| Pattern | Why Forbidden |
|---|---|
| Constructive and adversarial in same subagent call | Causes confirmation bias — adversarial loses independence |
| Approving with `fatal_flaw = YES` | Makes experiment uninterpretable; wastes full budget |
| Skipping pqa in constructive phase | Memory recall is not verified evidence; literature_support score must be 0 if pqa not queried |
| Re-adjudicating an already-APPROVED hypothesis | Creates conflicting records; only rerun if user explicitly requests revision |

---

*Research OS v1.0 | Stage 1.5 | See 30_DIALECTICAL_VALIDATION.md for full protocol*
