# 25 — Prior Art and Competition Check

**Purpose:** Systematic verification of novelty before any novelty claim is made in the paper.
This check must be completed before Stage 7 (Gap and Positioning). Claude must not claim novelty
until this check passes.

---

## Core Principle

> Prior work may already address the same problem, use the same method, or achieve better results
> than the proposed approach. Claude must not claim novelty until this check passes. Ignoring
> closer prior work to protect the story is a form of scientific misconduct.

This check is required at:
- **Stage 6:** Before contribution claims are finalized
- **Stage 8:** After pilot experiments, if new methods were discovered during experimentation
- **Stage 15+:** If a new paper appears that may overlap during the writing phase
- **Revision cycle:** If reviewers cite prior work not in the current analysis

---

## Required Outputs

This check produces three artifact files, all in the project root:

1. **`prior_art_competition_table.md`** — Systematic comparison of related work
2. **`sota_baseline_table.md`** — Verified SOTA results on target datasets
3. **`novelty_risk_report.md`** — Per-claim threat assessment and recommended actions

None of these files may be filled from memory. Every row must have a verifiable evidence source.

---

## Template 1: `prior_art_competition_table.md`

```markdown
# Prior Art Competition Table

Project: [Project name]
Date: YYYY-MM-DD
Total papers: [N]
High/Critical threat papers: [N]
Check performed by: [paper-qa query / manual PDF review / DBLP search]

---

## Scope

Research question being checked: [One sentence describing the specific contribution we are
checking novelty for, e.g., "Attention-gating in Mamba-based multiple instance learning for
WSI classification."]

---

## Table

| # | Paper | Year | Venue | Method | Dataset | Metric | Best Result | Key Limitation | Similarity (%) | Threat | Differentiation | Evidence Source |
|---|-------|------|-------|--------|---------|--------|-------------|----------------|---------------|--------|-----------------|-----------------|
| 1 | [Title] | YYYY | [Venue] | [Method summary] | [Datasets] | [Metric] | [Value] | [What the paper cannot do] | [0-100%] | [Low/Med/High/Crit] | [How our work differs] | [pqa query / PDF read / user-provided / DBLP] |

---

## Notes

- Similarity (%) is a rough estimate of conceptual overlap with our specific contribution claim.
  It is not a precise measure. High similarity (>50%) triggers manual review of that paper.
- Evidence Source must never be "from memory" or "general knowledge."
  If the source is unknown: mark as TODO_EVIDENCE_NEEDED.
- Papers from the last 12 months require special attention — conference proceedings are delayed
  on arXiv and DBLP; check both.
```

### Minimum Requirements

- **At least 5 papers** must be included.
- **Must include all papers from the last 24 months** that appear in a paper-qa query on the
  research topic. Use `pqa ask "methods for [topic] in [application domain] 2023 2024 2025"`.
- **At least one paper from each of:** NeurIPS/ICML/ICLR, CVPR/ECCV/MICCAI, and a relevant
  journal must be checked if applicable to the domain.
- **Any paper with similarity > 50%** must be elevated to Threat Level High or Critical and
  include a specific, detailed differentiation rationale.

### Evidence Source Options (in order of reliability)

1. `paper-qa query` — pqa was indexed with the paper's PDF; most reliable
2. `PDF read` — Claude or the researcher read the PDF directly
3. `DBLP/Semantic Scholar search` — abstract-level knowledge; verify with PDF for High/Critical papers
4. `user-provided` — researcher confirmed the paper's content manually
5. `TODO_EVIDENCE_NEEDED` — cannot verify; must be resolved before Stage 7

---

## Template 2: `sota_baseline_table.md`

```markdown
# SOTA Baseline Table

Project: [Project name]
Date: YYYY-MM-DD
Task: [e.g., WSI classification for cancer subtyping]
Primary metric: [e.g., AUC]

---

## [Dataset Name]

| Method | Metric | Best Known Value | Confidence Interval / Std | Source Paper | Year | Verified By |
|--------|--------|-----------------|--------------------------|--------------|------|-------------|
| BaselineModel | AUC | TODO_SOTA_NEEDED | — | [citation] | YYYY | TODO |
| ComparisonMethod | AUC | TODO_SOTA_NEEDED | — | [citation] | YYYY | TODO |
| TransMIL | AUC | TODO_SOTA_NEEDED | — | [citation] | YYYY | TODO |
| ABMIL | AUC | TODO_SOTA_NEEDED | — | [citation] | YYYY | TODO |
| DSMIL | AUC | TODO_SOTA_NEEDED | — | [citation] | YYYY | TODO |

---

## Rules

- Every row must have a **Verified By** field:
    - `pqa:[query string]` — value extracted via paper-qa
    - `PDF p.[N]` — extracted from a specific page of the PDF
    - `user-confirmed` — researcher confirmed the value from the original paper
    - `TODO_SOTA_NEEDED` — not yet verified; must be resolved before baseline claims are made
- Claude must NOT fill in SOTA values from memory.
- If a paper reports multiple results (different splits, feature extractors, or settings),
  record the most comparable setting to our experimental setup, not the best-case result.
- Evaluation protocol must match: if our experiments use 5-fold CV, baselines must also be
  evaluated under 5-fold CV or the discrepancy must be noted.
```

---

## Template 3: `novelty_risk_report.md`

```markdown
# Novelty Risk Report

Project: [Project name]
Date: YYYY-MM-DD
Based on: prior_art_competition_table.md (version YYYY-MM-DD)

---

## Contribution Claims Assessed

For each claim in contribution_contract.md, assess novelty risk.

---

### Claim 1: [Exact claim text, e.g., "AttentionModule module is a novel attention-gating mechanism for
Mamba-based MIL"]

- **novelty_claim:** [One sentence stating specifically what we claim is novel]
- **threat_level:** [Low / Medium / High / Critical]
- **closest_prior_work:** [Paper name, year, venue — and why it is the closest]
- **differentiation:** [How our work differs from the closest prior work; be specific]
- **differentiation_strength:** [strong / moderate / weak / speculative]
- **claim_status:** [defensible / needs-qualification / needs-pivot / indefensible]
- **recommended_action:** [proceed / qualify claim / run more experiments / pivot / abandon claim]

---

### Claim 2: [...]

[Repeat for each claim in contribution_contract.md]

---

## Overall Novelty Assessment

- **highest_threat_level:** [across all claims]
- **number_of_defensible_claims:** [N of total N]
- **recommended_next_step:** [proceed to Stage 7 / differentiate / narrow / pivot / abandon]
- **blocking_issues:** [list any issues that must be resolved before proceeding]
```

---

## Threat Level Definitions

| Level | Definition | Required Action |
|-------|-----------|-----------------|
| **Low** | Related domain or problem but meaningfully different method, task, or goal. No direct conflict with our contribution claim. | Proceed; cite the paper and acknowledge the broader area. |
| **Medium** | Same broad area and similar approach, but meaningfully different scope, dataset, or design choice. | Define explicit differentiation in the paper; update contribution_contract.md with qualification. |
| **High** | Strong conceptual overlap with our specific claim; reviewers will likely cite this paper as prior work. The contribution must be explicitly differentiated. | Differentiate specifically in related work; consider narrowing the claim; run /pivot-decision if needed. |
| **Critical** | Prior work already does the same thing, or achieves substantially better results with less complexity. Proceeding without a major pivot will result in rejection. | Stop and reassess; pivot, fundamentally redesign the contribution, downgrade venue, or abandon the claim. |

---

## Decision Tree After Prior-Art Check

```
                    [Prior-art check complete]
                            |
              +-------------+-------------+
              |             |             |
         threat=Low    threat=Medium  threat=High or Critical
              |             |             |
              |        Define explicit    |
              |        differentiation    |
              |        Update             |
              |        contribution_      |
              |        contract.md        |
              |             |             |
              |             |       +-----------+----------+
              |             |       |                      |
              |             |  threat=High           threat=Critical
              |             |       |                      |
              |             |  Narrow scope /         Consider:
              |             |  new angle /            - Fundamental redesign
              |             |  run /pivot-decision    - Pivot to different claim
              |             |       |                 - Downgrade venue
              |             |       |                 - Abandon contribution
              v             v       v                      v
         [Stage 7:    [Stage 7 with    [Direction update per 23_RESEARCH_DIRECTION_UPDATE.md]
          Gap and      qualifications]
          Positioning]
```

---

## Running the Check with paper-qa

If paper-qa is configured (`pqa`) and PDFs are indexed, run the following queries **before**
filling the prior art table. Record the query string and result in the Evidence Source column.

```bash
# General prior-art search
pqa ask "attention gating in multiple instance learning for whole slide images"

# Method-specific search
pqa ask "Mamba state space model for computational pathology 2024"

# Dataset-specific search
pqa ask "[your domain] benchmark classification AUC benchmark 2023 2024"

# Very recent work (last 12 months)
pqa ask "MIL WSI classification 2024 2025 new method"
```

If paper-qa is not available, mark every Evidence Source cell that would require it as
`TODO_EVIDENCE_NEEDED`. These must be resolved before Stage 7.

---

## Special Rules for Recent Work (Last 12 Months)

Conference proceedings for venues like MICCAI, CVPR, and NeurIPS appear on arXiv several months
before the official proceedings are indexed. This creates a systematic gap in standard literature
searches.

**Required actions for work within the last 12 months:**

1. Search arXiv directly: `arxiv.org/search/?query=[topic]&searchtype=all&start=0`
2. Check the proceedings page of recent relevant conferences directly (MICCAI 2024, NeurIPS 2024)
3. If a paper appears to overlap but is not yet available in the pqa index, note it as
   `Threat Level: [estimated]` with source `arXiv abstract only — PDF not yet indexed`
4. Before Stage 7, resolve all `arXiv abstract only` entries by reading the PDF

---

## What Claude Must Never Do

- Claim novelty before this check is complete and documented.
- Skip a paper from prior_art_competition_table because it is close and potentially threatening.
- Fill SOTA values in sota_baseline_table from memory.
- Mark a paper as Threat Level Low when its method description clearly overlaps with the
  contribution claim, in order to avoid the differentiation work.
- Proceed past Stage 6 with any `claim_status: indefensible` claims in novelty_risk_report.md.
- Use "concurrent work" framing to dismiss a paper published more than 6 months before the
  intended submission date.

---

## Relationship to Other System Files

| File | Relationship |
|------|-------------|
| `hypothesis_registry.md` | Prior-art findings may trigger new hypotheses or invalidate existing ones |
| `contribution_contract.md` | Claims with threat=High/Critical must be revised or removed |
| `research_direction.md` | Prior-art findings may trigger a direction update (see 23_RESEARCH_DIRECTION_UPDATE.md) |
| `24_VENUE_TARGETING.md` | Prior-art findings may affect required novelty level for target venue |
| `decision_log.md` | All pivots triggered by prior-art findings are logged here |
| `13_ANTI_HALLUCINATION_RULES.md` | Rules 3-5 directly govern this check |
| `04_LITERATURE_REVIEW_PLAYBOOK.md` | The literature review feeds into this table |
