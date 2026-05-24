# Contradiction Note: CONTR-NNN

<!-- Filename convention: CONTR-NNN.md (sequential numbering).
     Purpose: analyze and track a specific tension between two or more papers.
     A contradiction note is created when evidence_matrix.csv has two rows with opposite `direction` values
     for the same or closely related claim. -->
<!-- Status: [open | resolved | acknowledged-in-draft] -->
<!-- Last updated: YYYY-MM-DD -->

---

## Identification

| Field | Value |
|---|---|
| Contradiction ID | CONTR-NNN |
| Status | [open \| resolved \| acknowledged-in-draft] |
| Resolution strategy | [accept A \| accept B \| conditional \| open question \| needs more evidence] |
| Impact on RQ | [must address \| can ignore \| supports nuanced conclusion] |
| Date opened | YYYY-MM-DD |
| Date resolved | YYYY-MM-DD (or "—") |

---

## Papers in tension

| Role | Citekey | Claim ID | Claim (short) |
|---|---|---|---|
| Paper A | @{citekey_a} | C??? | |
| Paper B | @{citekey_b} | C??? | |

<!-- If more than two papers are involved, add rows. -->

---

## What Paper A claims

**Claim (full):** "…" (exact quote or precise paraphrase)

**Source:** @{citekey_a}, {Section}, p.{N}

**Evidence basis:**
- Study type: [experiment | survey | meta-analysis | case-study | theory | opinion]
- Sample / dataset: …
- Metric: …
- Result: …
- Statistical significance: [yes / no / not reported]

**Claim ID in registry:** C???

**Evidence strength:** [strong | moderate | weak]

---

## What Paper B claims

**Claim (full):** "…" (exact quote or precise paraphrase)

**Source:** @{citekey_b}, {Section}, p.{N}

**Evidence basis:**
- Study type: [experiment | survey | meta-analysis | case-study | theory | opinion]
- Sample / dataset: …
- Metric: …
- Result: …
- Statistical significance: [yes / no / not reported]

**Claim ID in registry:** C???

**Evidence strength:** [strong | moderate | weak]

---

## Context comparison

<!-- Often contradictions disappear once you account for differences in context.
     Fill this table carefully — it is the most analytically important section. -->

| Dimension | Paper A | Paper B |
|---|---|---|
| Domain / task | | |
| Dataset | | |
| Scale (data / model / compute) | | |
| Evaluation metric | | |
| Time period of study | | |
| Methodology | | |
| Assumed baseline | | |
| Population / scope | | |

---

## Why they might both be right

<!-- Conditional validity: under what circumstances is each paper's claim valid?
     This is NOT speculation — ground each point in the context comparison above. -->

- Paper A's claim holds when: …
- Paper B's claim holds when: …
- If both are conditional, the unified view is: …

---

## Why they might be genuinely contradictory

<!-- If the context comparison does not explain away the tension,
     describe the genuine scientific disagreement.
     What would a decisive experiment need to measure? -->

- The irreducible tension is: …
- A decisive test would: …

---

## Impact on my research question

<!-- Choose one and explain: -->

- [ ] **Must address:** My thesis depends on resolving this. If I claim X, I must explain the contradiction.
- [ ] **Can ignore:** The contradiction is out of scope for my specific RQ because …
- [ ] **Supports nuanced conclusion:** I can acknowledge the tension and draw a conditional conclusion.

**Reasoning:** …

---

## Resolution strategy

<!-- Choose one: -->

- [ ] **Accept A** — Paper A's evidence is stronger for my context because …
- [ ] **Accept B** — Paper B's evidence is stronger for my context because …
- [ ] **Conditional** — Accept A when [conditions], accept B when [conditions].
- [ ] **Open question** — The contradiction is unresolved in the field; I will flag it as a limitation.
- [ ] **Needs more evidence** — A future experiment or review paper could settle this.

**Rationale:** …

---

## Draft language

<!-- If this contradiction is acknowledged-in-draft, paste the sentence(s) that handle it here.
     This ensures the draft does not contradict the contradiction registry. -->

> "While @{citekey_a} reports …, @{citekey_b} finds …. This discrepancy may be explained by …"

---

## Related

- Concept notes: `concept_{slug}.md`
- Claim IDs: C???, C???
- Evidence matrix rows: (filter `claim_id` = C???, C???)
