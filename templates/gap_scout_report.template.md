# Gap Scout Report

date: [YYYY-MM-DD]
literature_index: [path to pqa index]
queries_run: [N]
papers_consulted: [approximately N papers via pqa]
area_of_interest: [user-provided or "open exploration"]

---

## Identified Gaps

### Gap 1 — [TYPE: UNEXPLORED COMBINATION | CONTRADICTORY RESULTS | MISSING BASELINE | EFFICIENCY | GENERALIZATION]
Evidence: "[pqa quote supporting this gap]"
Description: [1-2 sentences]

### Gap 2 — [TYPE]
Evidence: "[pqa quote]"
Description: [...]

[...]

---

## Hypothesis Candidates

### HYP-C1
gap_type: [TYPE]
hypothesis: "If [X] is added to [Y], then [Z] on [D] will [increase/decrease] by at least [Δ]"
mechanism: "[Brief mechanistic reason]"
falsification: "[What result would disprove this]"
novelty_score: [1-5]
compute_cost_estimate: [low | medium | high]
expected_delta_estimate: [small | medium | large]
priority_score: [computed]

### HYP-C2
[...]

### HYP-C3
[...]

---

## Ranking

| Rank | ID | Gap Type | Priority | Compute | Expected Delta | Novelty |
|------|-----|---------|----------|---------|----------------|---------|
| 1 | HYP-C[N] | [TYPE] | [score] | [low/med/high] | [small/med/large] | [1-5] |
| 2 | HYP-C[N] | [TYPE] | [score] | [...] | [...] | [...] |
| 3 | HYP-C[N] | [TYPE] | [score] | [...] | [...] | [...] |

---

## Recommendation

**Top candidate:** HYP-C[N]
**Rationale:** [Why this is the best direction given novelty × compute × expected gain]
**Alternative:** HYP-C[M] if top candidate fails proxy or prior-art check

---

## Human Checkpoint 1

*[Waiting for user selection before registering any hypothesis]*

User selected: [HYP-C[N] | All for tournament | Custom direction]
Registered as: HYP-[NNN] in hypothesis_registry.md
