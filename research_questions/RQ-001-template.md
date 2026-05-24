# RQ-001 — LLM-Assisted Literature Screening

**Status:** ACTIVE  
**Target Output:** Empirical research paper (conference or journal)  
**Last Updated:** 2026-05-25  
**Related RQs:** RQ-002-llm-evidence-extraction.md (planned)

---

## Research Question Statement

> Does LLM-assisted literature screening improve recall and precision compared to manual expert screening in systematic literature reviews, and what are the operational trade-offs (cost, time, reproducibility)?

**Refined sub-questions:**
1. What recall rate do LLM-based screening tools achieve relative to human expert panels on the same inclusion/exclusion criteria?
2. Do LLM screeners introduce systematic bias (e.g., favoring papers that match training-data priors over actual criteria)?
3. What is the cost-per-paper comparison between LLM-assisted and fully manual screening at scales of 500, 5,000, and 50,000 candidate papers?
4. Is LLM screening reproducible across multiple runs with the same prompt and candidate set?

---

## Scope

### Included
- Studies that empirically compare LLM-assisted screening to human screening on the same paper set
- Studies using any LLM (GPT-4, Claude, Gemini, open-weight models) for title/abstract screening
- Studies in any domain (biomedical, CS, social science) as long as the screening methodology is documented
- Systematic reviews and meta-analyses that report screening statistics (recall, precision, F1, Cohen's kappa)
- Preprints (arXiv, bioRxiv, medRxiv) if dated 2022 or later and methodology is clear
- Tool papers that describe and evaluate LLM screening systems

### Excluded
- Studies that only use keyword-based automation (no LLM component)
- Studies that use LLMs only for data extraction, not screening
- Opinion pieces, editorials, and commentary without empirical evaluation
- Studies that do not report recall or precision metrics (or equivalent)
- Papers published before 2020 (pre-LLM era, not directly comparable)
- Duplicate reports of the same study (keep the most complete version)

---

## Target Output Type

**Primary:** Empirical paper — survey/benchmark of LLM screening tools with original evaluation  
**Secondary:** Systematic review of published evidence on LLM screening performance  
**Venue target:** To be determined after Stage 9 (Venue Targeting). Candidate venues: JMLR, ACL Findings, NAACL, ECIR, SIGIR.

---

## Success Criteria

| Criterion | Minimum Threshold | Desired |
|---|---|---|
| High-quality papers in synthesis | ≥ 15 papers (score ≥ 7) | ≥ 25 papers |
| Evidence matrix rows | ≥ 40 validated rows | ≥ 80 rows |
| Domains represented | ≥ 2 domains | ≥ 4 domains |
| Contradiction analysis complete | Yes — all major contradictions documented | — |
| Gap analysis complete | ≥ 3 actionable research gaps identified | ≥ 5 gaps |
| Adversarial review passed | Yes — all major objections addressed or acknowledged | — |
| Citation validation | 100% of citations validated | — |

**Definition of "high-quality paper":** Quality score ≥ 7 on the `screening/inclusion_exclusion.md` rubric (5 criteria × 0-2 scale).

---

## Assumptions

1. Peer-reviewed publications on LLM screening exist in sufficient numbers (pilot search suggests ≥ 30 papers published 2022–2025).
2. Human expert screening data is reported in these studies with enough detail to compare (recall, precision, or kappa).
3. The research question is not already comprehensively answered by a recent meta-analysis (to be verified in Stage 6 Prior-Art Check).
4. LLM API costs are stable enough that cost comparisons reported in 2023–2024 papers remain directionally informative.

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Insufficient papers exist | Low (pilot search found >20) | High — cannot complete synthesis | Broaden scope to include grey literature and tool documentation |
| Papers report incompatible metrics | Medium | Medium — limits quantitative comparison | Standardize to recall@95precision or equivalent; report qualitative comparison where needed |
| LLM tools evolve faster than literature | High | Medium — findings may date quickly | Focus on methodology evaluation principles, not specific tool versions |
| Contradictory evidence dominates | Medium | Low — contradiction IS a finding | Document contradictions explicitly in the gap analysis |
| Prior-art check reveals existing survey | Medium | High — novelty threatened | Narrow to a specific domain or tool type; or reframe as replication/update study |
| No access to full-text papers | Low | Medium | Use Semantic Scholar, Unpaywall, institutional access; flag inaccessible papers |

---

## Related RQs

- **RQ-002 (planned):** Does LLM-assisted evidence extraction improve accuracy compared to manual extraction?
- **RQ-003 (planned):** What prompt engineering strategies most improve LLM screening recall?

These RQs are downstream of RQ-001. Do not begin RQ-002 or RQ-003 until RQ-001 reaches Stage 16 (Evidence Freeze).

---

## Change Log

| Date | Change | Reason |
|---|---|---|
| 2026-05-25 | Created from template | Initial project setup |
| — | — | — |

---

## How to Use This Template

1. Copy this file and rename it `RQ-NNN-your-slug.md` (increment N).
2. Replace every field with content specific to your research question.
3. Do not leave any section blank — write "N/A" and a one-line explanation if a section truly does not apply.
4. Set Status to `DRAFT` until the question passes the pilot search check.
5. Reference this file at session start before reading the evidence matrix.
6. Update `Last Updated` every time you modify this file.

**Status values:**
- `DRAFT` — Question defined but pilot search not yet complete
- `ACTIVE` — Pilot search confirms papers exist; screening in progress or complete
- `COMPLETED` — Evidence matrix validated, synthesis complete, draft written
- `ARCHIVED` — Question abandoned; reason documented in the Change Log
