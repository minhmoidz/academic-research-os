# Slide Deck Outline

**Talk title:** [Replace with paper title]  
**Conference / venue:** [Replace]  
**Duration:** [e.g., 15 min talk + 5 min Q&A]  
**RQ reference:** RQ-001

---

## Slide 1 — Title

- Title
- Authors + affiliations
- Conference / date
- **Talking points:** Welcome; tell the audience what they will take away in one sentence.
- **Visual:** Simple title card, institution logo if required.

---

## Slide 2 — The Problem (Motivation)

- Hook: one striking statistic or pain point about the problem
- What is broken / inefficient / unknown today?
- **Evidence:** <!-- GAP-001 from gaps_and_opportunities.md -->
- **Talking points:** Make the audience feel the pain before presenting the solution.
- **Visual:** Problem diagram or before/after comparison.

---

## Slide 3 — Research Question

- State RQ-001 exactly
- Scope: what is included / excluded
- Why this question matters NOW
- **Talking points:** Keep this crisp. One question, one sentence.
- **Visual:** Single bold text card with the RQ.

---

## Slide 4 — Related Work (Cluster A)

- 3-5 bullet points summarizing Cluster A from `synthesis/literature_map.md`
- Key consensus finding
- Key open question from this cluster
- **Evidence:** <!-- C001, C002 -->
- **Talking points:** Don't list papers — synthesize the insight.
- **Visual:** Mini literature map or timeline.

---

## Slide 5 — Related Work (Clusters B & C)

- Summary of Clusters B and C
- Cross-cluster tension or contradiction (CONTR-001)
- The gap that motivates this work
- **Evidence:** <!-- C003, C004, C005 -->
- **Talking points:** End with "this gap is what we address."
- **Visual:** Comparison table or Venn diagram of approaches.

---

## Slide 6 — Method

- Search strategy (databases, date range, N papers retrieved)
- Inclusion / exclusion criteria (brief)
- PRISMA numbers: identified → screened → included
- Evidence extraction approach
- **Evidence:** <!-- screening/prisma_flow.md -->
- **Talking points:** Emphasize reproducibility — all materials in the repo.
- **Visual:** PRISMA flow diagram (export from prisma_flow.md Mermaid).

---

## Slide 7 — Key Findings (1 of 2)

- Finding 1 with supporting data / numbers
- Finding 2 with confidence level
- **Evidence:** <!-- C001, C004 | Confidence: high -->
- **Talking points:** Lead with the number / effect size. Explain what it means.
- **Visual:** Bar chart or comparison table from evidence_matrix.

---

## Slide 8 — Key Findings (2 of 2)

- Finding 3
- Contradiction / tension found in literature (CONTR-001)
- How the contradiction is resolved (or why it is still open)
- **Evidence:** <!-- C002, C005, C006 -->
- **Talking points:** Contradictions make the talk interesting — don't hide them.
- **Visual:** Side-by-side contrast of contradicting findings.

---

## Slide 9 — Contribution & Novelty

- What this work adds that didn't exist before
- How this advances the field beyond prior work
- Explicitly state: "To our knowledge, [novel claim]"
- **Evidence:** <!-- C001, C003 — ONLY after prior-art-check PASS -->
- **Talking points:** Be precise and humble. Say "suggests" not "proves."
- **Visual:** Contribution table (this work vs. prior work).

---

## Slide 10 — Limitations

- Search coverage (databases used, grey literature)
- Language bias (English only)
- Recency limitations
- Any quality or selection bias
- **Talking points:** Stating limitations builds credibility. Address the most likely objection.
- **Visual:** Honest limitations table.

---

## Slide 11 — Future Work

- Top 2-3 gaps from `synthesis/gaps_and_opportunities.md` (GAP-001, GAP-002)
- Specific next RQ that should be investigated
- Open challenge for the community
- **Talking points:** Leave the audience with a clear "what's next."
- **Visual:** Gap ranking table from gaps_and_opportunities.md.

---

## Slide 12 — Conclusion

- Restate RQ in one line
- Answer to RQ in one line
- Most important implication in one line
- Repo / paper URL
- **Talking points:** 3 sentences max. If it doesn't fit on 3 lines, the conclusion is not clear enough.
- **Visual:** Clean summary card + QR code linking to repo.

---

## Q&A Prep

Anticipated questions and prepared answers:

| Question | Answer | Evidence |
|---|---|---|
| "Why didn't you include [X database]?" | [Reason from sources.yaml] | search/sources.yaml |
| "How do you handle contradictory findings?" | [From contradiction_notes + argument_map] | evidence/claim_registry.md |
| "What's the quality threshold for inclusion?" | [From inclusion_exclusion.md] | screening/inclusion_exclusion.md |
| "Is your search replicable?" | "Yes — full queries in search/query_bank.md, log in search_log.csv" | search/ |
