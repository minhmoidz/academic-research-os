# Inclusion and Exclusion Criteria

**Project:** LLM-Assisted Literature Screening  
**RQ:** RQ-001-llm-screening.md  
**Last Updated:** 2026-05-25  
**Applies to:** Title/abstract screening (Pass 1) and full-text screening (Pass 2)

---

## Inclusion Criteria

A paper must satisfy **all** of the following to be considered for inclusion.

| ID | Criterion | Rationale |
|---|---|---|
| I1 | **Topic relevance:** Paper evaluates the use of a language model (any size or architecture) to assist or automate literature screening, study selection, or title/abstract review for systematic or scoping reviews | Directly addresses the research question |
| I2 | **Empirical evaluation:** Paper reports at least one quantitative metric comparing LLM performance to a human baseline or to another automated method (e.g., recall, precision, F1, sensitivity, specificity, Cohen's kappa, time, cost) | Enables evidence extraction; opinion papers alone cannot populate the evidence matrix |
| I3 | **Publication year 2020 or later:** Published or posted on a preprint server from 2020-01-01 onward | Pre-2020 papers predate the modern large LLM era; comparison to earlier NLP methods is a different research question |
| I4 | **Language: English full text available:** The paper is written in English and the full text is accessible (open access, institutional access, author preprint, or Semantic Scholar PDF link) | Full text is required for evidence extraction and validation |
| I5 | **Venue quality:** Published in a peer-reviewed journal, conference proceedings, or is a preprint on arXiv/bioRxiv/medRxiv that (a) was posted 2022 or later and (b) has a clearly described methodology with reported statistics | Ensures minimum methodological rigor; older unreviewed preprints are excluded |
| I6 | **Evidence type:** Paper reports primary data (original screening experiment) OR meta-analytic data (pooled analysis of multiple screening studies) | Secondary analysis or pure literature review without empirical data cannot contribute to the evidence matrix |

---

## Exclusion Criteria

A paper is excluded if it meets **any** of the following.

| ID | Criterion | Rationale |
|---|---|---|
| E1 | **Off-topic LLM application:** Paper uses LLMs for a task other than literature screening or study selection (e.g., data extraction, evidence synthesis, full-text analysis, clinical decision support, patient screening) | Different task from the RQ; confounds results |
| E2 | **Non-LLM automation only:** Paper describes or evaluates a screening automation system that uses only rule-based methods, keyword matching, or classical ML (SVM, logistic regression, random forest) without a language model component | Outside scope of RQ-001 |
| E3 | **No empirical evaluation:** Paper is an opinion piece, editorial, commentary, perspective, or methodological framework without experimental data | Cannot contribute validated claims to the evidence matrix |
| E4 | **No human comparison or gold standard:** Paper evaluates an LLM screener but does not compare to human screening or an established gold standard (e.g., Cochrane review inclusion list) | Cannot assess whether LLM performance is adequate |
| E5 | **Pre-2020 publication:** Published or posted before 2020-01-01 | See I3 rationale |
| E6 | **Non-English or no English full text available:** Paper is not available in English or full text cannot be obtained through any available channel | Cannot complete evidence extraction |
| E7 | **Duplicate or superseded:** Paper is a duplicate of another included paper (same study), or is an arXiv preprint that has been superseded by an included published version | Avoid double-counting; keep the most complete version |
| E8 | **Retracted or withdrawn:** Paper has been retracted, withdrawn, or flagged with an expression of concern | Cannot rely on retracted evidence |

---

## Quality Scoring Rubric

Applied during **Pass 2 (full-text screening)** to papers that pass the inclusion/exclusion filter. Score each paper on 5 criteria, 0–2 points each.

**Maximum possible score: 10**

### Criterion 1: Relevance (0–2)

| Score | Description |
|---|---|
| 0 | Paper is tangentially related to LLM screening; main contribution is a different topic |
| 1 | Paper addresses LLM screening but only as a secondary or supporting component |
| 2 | LLM-assisted literature screening is the central research contribution of the paper |

### Criterion 2: Evidence Strength (0–2)

| Score | Description |
|---|---|
| 0 | No quantitative evaluation, or evaluation on a toy dataset (<50 papers screened) |
| 1 | Quantitative evaluation on a realistic dataset (≥50 papers) but without human comparison, OR human comparison on a small dataset (50–200 papers) |
| 2 | Rigorous quantitative evaluation with human comparison on ≥200 papers, with appropriate statistical reporting (confidence intervals, significance tests, or kappa) |

### Criterion 3: Method Clarity (0–2)

| Score | Description |
|---|---|
| 0 | LLM prompting strategy and evaluation protocol are not described; results cannot be reproduced |
| 1 | Methodology is partially described; key details (prompt text, model version, inclusion criteria used) are missing or unclear |
| 2 | Full methodology is described: model name and version, prompt text or link to prompt repository, inclusion/exclusion criteria used, screening protocol, and evaluation metrics all reported |

### Criterion 4: Citation Value (0–2)

| Score | Description |
|---|---|
| 0 | Paper makes no claims that advance understanding of LLM screening performance; primarily confirmatory with no new insight |
| 1 | Paper provides useful data points but conclusions are narrow or domain-specific with limited generalizability |
| 2 | Paper contributes generalizable findings, introduces a new benchmark or dataset, or contradicts prevailing assumptions in a well-supported way |

### Criterion 5: Recency (0–2)

| Score | Description |
|---|---|
| 0 | Published before 2022 (pre-ChatGPT era; technology comparisons may be obsolete) |
| 1 | Published 2022–2023 (GPT-3.5 era; findings may be partially outdated for GPT-4+ models) |
| 2 | Published 2024 or later (current LLM generation; directly applicable) |

---

## Score Thresholds

| Score Range | Decision | Action |
|---|---|---|
| 7–10 | **Include** | Add to evidence matrix; create note file |
| 4–6 | **Borderline** | Manual review by second screener; document disagreement resolution |
| 0–3 | **Exclude** | Record in screening_table.csv with reason; do not add to evidence matrix |

---

## Decision Protocol

### Who Screens

- **Primary screener:** The researcher conducting the literature review (typically the project lead)
- **Secondary screener:** A second researcher, or Claude acting as an adversarial screener, for borderline cases
- **Tie-breaker:** If two screeners disagree on a borderline paper, the more conservative decision (exclude) is taken unless the paper scores ≥7 on Criterion 2 (Evidence Strength)

### When to Apply Each Pass

- **Pass 1 (title/abstract):** Apply inclusion/exclusion criteria (I1–I6 and E1–E8). Record decision in `screening/screening_table.csv`. Do not score — just include/exclude/borderline.
- **Pass 2 (full-text):** Apply quality scoring rubric. Record score and breakdown in `screening/screening_table.csv`. Finalize include/exclude decision.

### Resolving Disagreements

1. Document both screeners' scores in `screening/screening_table.csv` (columns `score_s1`, `score_s2`)
2. Discuss the specific criterion causing disagreement
3. Apply the conservative rule if no consensus is reached within 10 minutes
4. Record the final decision reason in the `reason` column

### Edge Cases

- **Preprints later published:** If a preprint is screened and then a published version appears, update the entry — do not create a new row. Set the citekey to the published version.
- **Papers behind paywall with no accessible version:** If the abstract passes Pass 1 but full text cannot be obtained, record as `exclude` with reason `inaccessible_full_text`. Note the paper in a separate list for potential institutional access request.
- **Highly influential papers that barely miss the date cutoff:** Papers from 2018–2019 that are frequently cited in included papers may be added as background references but are NOT included in the evidence matrix synthesis.
