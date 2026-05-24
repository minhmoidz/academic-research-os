# Reusable Templates

Copy these templates at the start of each project phase. Save filled versions in the project directory.

---

## Template 1: Paper Brief

Save as: `paper-brief.md`

```markdown
# Paper Brief
Date: 
Working title: 
Target venue: 
Page limit: 
Blind review: Yes / No

## Problem (2–3 sentences)


## Proposed approach (2–3 sentences)


## Primary falsifiable claim


## Datasets
| Dataset | N | Classes | Feature extractor | Available? |
|---------|---|---------|-------------------|-----------|
|         |   |         |                   |           |

## Baselines
| Method | Citation | Runnable? |
|--------|----------|-----------|

## Primary metric


## Key figure (planned — describe what it shows)


## Evidence gate status
- Literature matrix: [ ] Complete / [ ] In progress
- Experiments run: [ ] Yes / [ ] Planned
- Gap validated via paper-qa: [ ] Yes / [ ] Pending

## Current phase: [1-15]
```

---

## Template 2: Research Question

```markdown
# Research Questions

## Primary question
"Does [mechanism] reduce [limitation] compared to [baseline] on [task/dataset]?"

## Secondary questions
1. 
2. 

## Null hypothesis (H0)
[Method] does NOT improve [metric] over [baseline] by more than [threshold].

## Alternative hypothesis (H1)
[Method] improves [metric] over [baseline] by at least [minimum meaningful delta].

## Minimum meaningful delta (set before seeing results)


## Evidence required to accept H1

```

---

## Template 3: Problem Statement

```markdown
# Problem Statement

Domain: 

Existing approach: [method] addresses [problem] by [mechanism].

Limitation: However, [existing approach] fails when [condition] because [root cause].

Evidence of limitation: We observe [measurement] in [experiment/dataset].

Proposed fix: We propose [method], which [mechanism] to correct [limitation].

Expected outcome: This should improve [metric] on [dataset] because [causal argument].
```

---

## Template 4: Literature Matrix

Save as: `literature-matrix.md`

```markdown
# Literature Matrix
Built from paper-qa queries on [date]. NOT from memory.

| Paper (cite key) | Method type | Dataset | Key metric | Key limitation | Addresses our gap? |
|-----------------|-------------|---------|-----------|----------------|-------------------|
| [b1]            |             |         |           |                | No — because X    |
| [b2]            |             |         |           |                | Partially — but Y |

## Gap column summary
No prior work addresses: [gap statement]

Evidence from paper-qa:
Query: "Does any paper address [gap]?"
Answer: [paste paper-qa output]
```

---

## Template 5: Contribution Map

Save as: `contribution-map.md`

```markdown
# Contribution Map

| # | Claim | Type | Evidence pointer | Status |
|---|-------|------|-----------------|--------|
| 1 | We identify [X] | Empirical finding | Fig. 2 / results/analysis/norm.json | ✓ Available |
| 2 | We show [Y] causes [Z] | Analysis | Table II row +ComponentA vs +ComponentA+ComponentB | ✓ Available |
| 3 | [ProposedModule] achieves [W] | Performance | Table I / results/ours/summary.json | ✓ Available |

## Overclaiming risk check
- [ ] "First" claims verified via paper-qa
- [ ] Improvements confirmed on ALL stated benchmarks
- [ ] Gains survive ablation attribution
```

---

## Template 6: Claim-Evidence Table

Save as: `claim-evidence-table.md`

```markdown
# Claim-Evidence Table

| Section | Paragraph | Claim (quoted) | Evidence source | Verified? |
|---------|-----------|---------------|----------------|----------|
| Abstract | - | "[YourMethod] selects informative instances in [X]% of slides" | results/analysis/selection_stats.json | ✓ |
| Intro, para 2 | - | "hard groups carry only [ratio]× the norm" | results/analysis/norm_progression.json | ✓ |
| IV.B | para 1 | "+[X] pp AUC over [BaselineModel]" | results/ours/dataset-a/summary.json | ✓ |

## Unverified claims (resolve before submission)
- TODO_EVIDENCE_NEEDED: ...
- TODO_RESULT_NEEDED: ...
```

---

## Template 7: Experiment Matrix

Save as: `experiment-matrix.md`

```markdown
# Experiment Matrix

## Datasets
| Dataset | N | Classes | Feature | Split | Path | Verified? |
|---------|---|---------|---------|-------|------|----------|

## Methods
| Method | Config | Run status | Result path |
|--------|--------|-----------|-------------|
| BaselineModel | configs/baseline.yaml | ✓ Done | results/baseline/ |
| YourMethod (ProposedModule) | configs/your_method.yaml | ✓ Done | results/ours/ |

## Ablation table
| Config | ComponentA | ComponentB | ComponentC | ComponentD | Status |
|--------|-----------|-----------|-----------|-----------|--------|
| +CompA+cls | ✓ | ✗ | ✗ | ✓ | Done |

## Metric definition
Mean AUC ± population std over 5 folds (seed=42)
Std formula: σ = sqrt(Σ(xi-μ)²/N) where N=5
```

---

## Template 8: Figure Plan

```markdown
# Figure Plan

| # | Label | Type | What it shows | Data source | Status |
|---|-------|------|--------------|-------------|--------|
| 1 | fig:overview | Architecture | Pipeline from inputs to prediction | N/A (conceptual) | ✓ Done |
| 2 | fig:analysis | Bar chart (pgfplots) | Feature norms at pipeline stages | results/analysis/norm_progression.json | ✓ Done |

## Figure design notes
- Color convention: blue = backbone, orange = proposed additions
- Font: \footnotesize inside TikZ, \scriptsize for tensor labels
- Width: \columnwidth for all figures (two-column paper)
```

---

## Template 9: Section Review Report

```markdown
# Section Review Report

Section: 
Reviewer agent: 
Date: 

## Critical findings
1. [finding] — [location] — Fix: [action]

## Major findings
1. 

## Minor findings
1. 

## Resolved in this pass
- [finding from prior pass] → fixed at [location]

## Status after this pass
[ ] Ready for next pass
[ ] Needs re-review (Critical findings remain)
```

---

## Template 10: Revision Plan

```markdown
# Revision Plan

Source: [ ] Reviewer feedback / [ ] Self-review (pass N)
Date:

## Point-by-point response

| # | Reviewer point | Our response | Action | Location in paper | Status |
|---|---------------|-------------|--------|------------------|--------|
| 1 | "The analysis is indirect" | We agree; we add X to strengthen | Add sentence X to Limitations | Sec. IV.E | Done |

## New content added
- [description of addition] — motivated by reviewer point [N]

## Content removed or qualified
- [description] — previously overclaimed, now hedged/removed

## Result: changes to main tables
[ ] None (no new experiments)
[ ] Table updated: [description]
```

---

## Template 11: Final Audit Report

```markdown
# Final Audit Report

Paper: [title]
Audit date:
Auditor: Claude (+ human sign-off)

## Review passes completed
| Pass | Agent used | Date | Findings | Status |
|------|-----------|------|---------|--------|
| 1. Logic | logic-reviewer | | [N Critical, M Minor] | ✓ Resolved |

## Outstanding issues
None / [list any intentionally deferred items]

## Submission gate
[ ] All Critical findings resolved
[ ] Submission checklist (09_SUBMISSION_CHECKLIST.md) completed
[ ] Final PDF verified
[ ] Approved for submission
```

---

## Template 12: Example Paper Brief (Filled)

The following is a realistic filled example using the topic of retrieval-augmented agents for scientific literature analysis.

```markdown
# Paper Brief
Date: YYYY-MM-DD
Working title: "RALit: Retrieval-Augmented Agents for Evidence-Grounded Scientific Literature Analysis"
Target venue: ACL 2026
Page limit: 8 pages + references
Blind review: Yes

## Problem (2–3 sentences)
Scientific literature analysis tools struggle to ground claims in verified sources,
often hallucinating citations or summarizing papers they have not read. Existing
retrieval-augmented generation (RAG) approaches retrieve passages but do not reason
over multi-hop evidence chains. We address the gap between passage retrieval and
multi-step claim verification.

## Proposed approach (2–3 sentences)
We propose RALit, a retrieval-augmented agent that decomposes literature queries
into sub-claims, retrieves supporting passages for each sub-claim independently,
and aggregates evidence with explicit citation tracking. The agent uses a chain-of-thought
verifier that rejects unsupported sub-claims before synthesizing the final answer.

## Primary falsifiable claim
RALit achieves higher citation accuracy (fraction of cited claims traceable to a
retrieved passage) than a single-step RAG baseline on the [Dataset-A] benchmark,
under identical retrieval corpus and budget constraints.

## Datasets
| Dataset | N | Classes | Feature extractor | Available? |
|---------|---|---------|-------------------|-----------|
| Dataset-A | 500 queries | binary (supported/unsupported) | sentence-transformers/all-MiniLM-L6-v2 | ✓ |
| Dataset-B | 200 queries | 3-class (full/partial/none) | same | ✓ |

## Baselines
| Method | Citation | Runnable? |
|--------|----------|-----------|
| Single-step RAG | [b1] | ✓ |
| BaselineModel (multi-hop) | [b2] | TODO_CITATION_NEEDED |

## Primary metric
Citation accuracy (fraction of final claims with a retrieved passage as evidence)

## Key figure (planned — describe what it shows)
Fig. 1: System architecture — query decomposition → per-sub-claim retrieval → verifier → answer
Fig. 2: Bar chart comparing citation accuracy across baselines on Dataset-A and Dataset-B

## Evidence gate status
- Literature matrix: [ ] In progress
- Experiments run: [ ] Planned
- Gap validated via paper-qa: [ ] Pending

## Current phase: 2
```
