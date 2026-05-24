# Idea-to-Paper Playbook

Use this playbook at the start of a new research project to convert a rough idea into a structured plan.

---

## Step 1: Idea Clarification Questions

Ask these before writing anything:

1. **What is broken?** What specific limitation, failure mode, or gap exists in current methods?
2. **How do you know it's broken?** Do you have empirical evidence (a measurement, a plot, a failed baseline)?
3. **What is your fix?** Describe it in one sentence without jargon.
4. **Why would your fix work?** What is the causal mechanism?
5. **How will you test it?** What dataset, metric, and baseline comparison?
6. **What would falsify your hypothesis?** What result would convince you the approach doesn't work?
7. **Who cares?** What real downstream impact does solving this have?
8. **What is the closest existing work?** Name 2–3 papers. (If you can't name any, literature review is needed first.)

Do not proceed until all 8 questions have concrete answers.

---

## Step 2: Problem Statement Template

Fill in this template:

```
DOMAIN: [field, e.g., "multiple instance learning for WSI classification"]

EXISTING APPROACH: [method name] addresses [problem] by [mechanism].

LIMITATION: However, [existing approach] fails when [condition] because [root cause].

EVIDENCE OF LIMITATION: We observe [measurement / phenomenon] in [experiment / dataset].

PROPOSED FIX: We propose [method name], which [mechanism] to correct [limitation].

EXPECTED OUTCOME: This should improve [metric] on [dataset] because [causal argument].
```

---

## Step 3: Research Question Template

```
Primary research question:
"Does [proposed mechanism] reduce [limitation] compared to [existing approach] on [task/dataset]?"

Secondary questions (optional):
1. "Which component of [proposed method] contributes most to the improvement?"
2. "Does the improvement generalize to [other setting / dataset]?"
3. "What conditions are necessary for [proposed mechanism] to work?"
```

The primary question must be:
- Specific (names method, metric, dataset)
- Falsifiable (a negative result is possible and meaningful)
- Answerable within the paper's experimental scope

---

## Step 4: Hypothesis Template

```
NULL HYPOTHESIS (H0):
[Proposed method] does not improve [metric] over [baseline] on [dataset] (p > 0.05 / difference < [threshold]).

ALTERNATIVE HYPOTHESIS (H1):
[Proposed method] improves [metric] over [baseline] on [dataset] by at least [minimum meaningful difference].

MINIMUM MEANINGFUL DIFFERENCE:
[Define: e.g., "at least 0.5 pp AUC improvement" — must be set before seeing results]

EVIDENCE REQUIRED TO ACCEPT H1:
[e.g., "5-fold mean AUC gain ≥ 0.5 pp on at least 2 of 3 benchmarks"]
```

---

## Step 5: Contribution Candidate Template

For each candidate contribution, fill in:

```
CONTRIBUTION CANDIDATE [N]:

Claim: [One sentence stating what you show/demonstrate/discover]

Type: [ ] Empirical finding  [ ] New method  [ ] New analysis  [ ] New dataset

Evidence needed: [What experiment / measurement / figure will support this]

Evidence status: [ ] Available  [ ] Planned  [ ] TODO_RESULT_NEEDED

Risk of overclaiming: [What would make this claim false or already known?]

Literature check needed: [ ] Yes (use paper-qa)  [ ] No (trivially verifiable)
```

**Rule:** A contribution is not a contribution until the "Evidence needed" cell is filled with a real file or a confirmed planned experiment — not with "TBD" or "we believe."

---

## Step 6: Risk of Overclaiming Checklist

Before finalizing the contribution list, check each item:

- [ ] Have I verified no prior paper makes the same claim? (paper-qa search required)
- [ ] Is my "first" qualifier bounded? ("to our knowledge" + scoped to a specific subfield)
- [ ] Are my metric improvements on the right test set (not the validation set)?
- [ ] Do my gains survive across multiple datasets / settings (not just one cherry-picked result)?
- [ ] Am I reporting mean AND variance? (Single-number results without std are incomplete)
- [ ] Have I run ablations to attribute gains to the right component?
- [ ] Are my "state-of-the-art" comparisons using the same feature extractor / protocol?
- [ ] Do my Limitations acknowledge the conditions under which the method might fail?

---

## Step 7: Minimum Evidence Required Before Writing

**Do not write paper prose until:**

| Requirement | Status check |
|-------------|-------------|
| At least 10 verified related papers in references.bib | ✓/✗ |
| Literature matrix built from paper-qa (not memory) | ✓/✗ |
| Gap validated: paper-qa confirms no paper does exactly what we claim | ✓/✗ |
| At least one complete run of the proposed method on at least one dataset | ✓/✗ |
| At least one baseline result confirmed to compare against | ✓/✗ |
| Contribution map has evidence pointers (not all TODO) | ✓/✗ |
| Paper brief reviewed and accepted by user | ✓/✗ |

If any item is ✗, resolve it before drafting. Mark remaining unknowns as `TODO_RESULT_NEEDED:` or `TODO_EVIDENCE_NEEDED:` in the skeleton.

---

## Paper Brief Template (Fill and Save as `paper-brief.md`)

```markdown
# Paper Brief

**Working title:** 
**Target venue:** 
**Page limit:** 
**Blind review:** Yes / No

## Problem
[2–3 sentences: what is broken and why it matters]

## Proposed approach
[2–3 sentences: what we do and why it should work]

## Primary claim
[One sentence: the falsifiable main claim]

## Datasets
- Dataset 1: [name, N samples, task]
- Dataset 2: ...

## Baselines
- Baseline 1: [method name, citation]
- Baseline 2: ...

## Primary metric
[e.g., mean AUC over 5-fold cross-validation]

## Key figure (planned)
[Describe the one figure that best communicates the core finding]

## Evidence gate status
- Literature matrix: [ ] Complete / [ ] In progress
- Experiments run: [ ] Yes / [ ] Planned
- Gap validated: [ ] Yes / [ ] Pending paper-qa search

## Status
Phase: [1-15]
Last updated: [date]
```
