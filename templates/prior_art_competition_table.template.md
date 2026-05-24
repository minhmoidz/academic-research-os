# Prior Art Competition Table

Project: [project_name]
Date: [YYYY-MM-DD]
Total papers: [N]
High/Critical threat papers: [N]
Check performed by: [paper-qa query / manual PDF review / DBLP search / combination]

---

## Scope

Research question being checked: [One sentence describing the specific contribution we are
checking novelty for. Be precise — novelty is always relative to a specific claim, not the whole paper.]

---

## Table

| # | Paper | Year | Venue | Method | Dataset | Metric | Best Result | Key Limitation | Similarity (%) | Threat | Differentiation | Evidence Source |
|---|-------|------|-------|--------|---------|--------|-------------|----------------|---------------|--------|-----------------|-----------------|
| 1 | [Title] | [YYYY] | [Venue] | [Method summary in 5-10 words] | [Dataset names] | [Primary metric] | [Best value reported] | [What the paper cannot do that we do] | [0–100%] | [Low / Med / High / Crit] | [How our work differs — be specific] | [pqa query / PDF read / user-provided / DBLP] |
| 2 | [Title] | [YYYY] | [Venue] | [Method summary] | [Dataset names] | [Metric] | [Value] | [Limitation] | [%] | [Level] | [Differentiation] | [Source] |

---

## Threat Level Definitions

| Level | Definition | Required Action |
|-------|-----------|-----------------|
| Low | Related domain or problem but meaningfully different method, task, or goal | Cite and acknowledge; no major differentiation needed |
| Medium | Same broad area and similar approach, but different scope, dataset, or design | Explicit differentiation in related work; update contribution_contract.md |
| High | Strong conceptual overlap; reviewers will likely cite this as prior work | Differentiate specifically; consider narrowing the claim |
| Critical | Prior work already does the same thing or achieves better results with less complexity | Stop; pivot, redesign, downgrade venue, or abandon the claim |

---

## Notes

- Similarity (%) is a rough estimate of conceptual overlap with our specific contribution claim. It is not a precise measure. Papers with similarity > 50% require manual PDF review.
- Evidence Source must never be "from memory" or "general knowledge." If unknown: `TODO_EVIDENCE_NEEDED:`.
- Papers from the last 12 months require special attention — check arXiv directly for papers not yet indexed.
- At least 5 papers must be included; at least one from each of: a top-tier conference, a domain conference, and a journal (if applicable to the research area).

---

## Minimum Requirements Checklist

- [ ] At least 5 papers included
- [ ] All papers from the last 24 months verified via paper-qa query
- [ ] At least one paper from each relevant venue tier included
- [ ] All papers with similarity > 50% reviewed via PDF read (not just abstract)
- [ ] No evidence source is "from memory" or "general knowledge"
- [ ] All TODO_EVIDENCE_NEEDED entries resolved before proceeding to Stage 7
