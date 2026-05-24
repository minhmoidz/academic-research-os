# SOTA Baseline Table

Project: [project_name]
Date: [YYYY-MM-DD]
Task: [task description, e.g., "scientific document retrieval"]
Primary metric: [metric name, e.g., "Recall@10", "NDCG@10", "AUC"]

---

## Rules

- Every row must have a **Verified By** field. Only these values are valid:
    - `pqa:[query string]` — value extracted via paper-qa query
    - `PDF p.[N]` — extracted from a specific page of the paper PDF
    - `user-confirmed` — researcher confirmed the value from the original paper
    - `TODO_SOTA_NEEDED` — not yet verified; must be resolved before baseline claims are made
- Claude must NOT fill in SOTA values from memory.
- If a paper reports multiple results (different splits, settings, or configurations), record the most comparable setting to our experimental setup — not the best-case result.
- Evaluation protocol must match: if our experiments use 5-fold CV, baselines must also be evaluated under 5-fold CV, or the discrepancy must be explicitly noted.

---

## [Dataset-A Name]

| Method | Metric | Best Known Value | Confidence Interval / Std | Source Paper | Year | Verified By |
|--------|--------|-----------------|--------------------------|--------------|------|-------------|
| [Baseline-1] | [metric] | TODO_SOTA_NEEDED | — | [TODO_CITATION_NEEDED] | [YYYY] | TODO |
| [Baseline-2] | [metric] | TODO_SOTA_NEEDED | — | [TODO_CITATION_NEEDED] | [YYYY] | TODO |
| [Baseline-3] | [metric] | TODO_SOTA_NEEDED | — | [TODO_CITATION_NEEDED] | [YYYY] | TODO |

---

## [Dataset-B Name]

| Method | Metric | Best Known Value | Confidence Interval / Std | Source Paper | Year | Verified By |
|--------|--------|-----------------|--------------------------|--------------|------|-------------|
| [Baseline-1] | [metric] | TODO_SOTA_NEEDED | — | [TODO_CITATION_NEEDED] | [YYYY] | TODO |
| [Baseline-2] | [metric] | TODO_SOTA_NEEDED | — | [TODO_CITATION_NEEDED] | [YYYY] | TODO |
| [Baseline-3] | [metric] | TODO_SOTA_NEEDED | — | [TODO_CITATION_NEEDED] | [YYYY] | TODO |

---

## Notes on Protocol Differences

[Describe any differences between the evaluation protocols used in the papers above and the protocol used in your experiments. If protocols differ significantly, results cannot be directly compared — note this explicitly.]

---

## Verification Status

- [ ] All rows have a `Verified By` value that is not `TODO_SOTA_NEEDED`
- [ ] All protocols confirmed to match (or differences documented)
- [ ] All papers have entries in `references.bib` or `TODO_CITATION_NEEDED` markers
