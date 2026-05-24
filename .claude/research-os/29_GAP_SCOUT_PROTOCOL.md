# 29 — Gap Scout Protocol

**Stage:** 0.5 (before Stage 1 Idea Intake)  
**Trigger:** User has no idea yet, or has a dataset + baseline but no clear hypothesis direction.  
**Output:** `gap_scout_report.md` + registered hypothesis candidate(s) in `hypothesis_registry.md`

---

## 1. When to Use Gap Scout

Invoke the Gap Scout Protocol when any of the following conditions hold:

- User says "I don't have an idea yet" or "help me find a research direction"
- User has a dataset and a baseline model but does not know what to add or change
- User is in open exploration mode before committing to a specific hypothesis
- A previous hypothesis was abandoned (via `/pivot-decision`) and a fresh direction is needed
- Running as a precondition check before Stage 1 Idea Intake

Gap Scout is **Stage 0.5** — it feeds directly into Stage 1. The output is a ranked list of hypothesis candidates that the user selects from, not a final committed hypothesis.

---

## 2. Gap Taxonomy — Five Types of Research Gaps

```
TYPE 1: UNEXPLORED COMBINATION
  Technique A has worked well in domain/task X.
  Technique B has also worked well in domain/task X.
  No paper has combined A + B within X.
  Gap: "Combine A and B for X"
  Example: attention mechanisms combined with state-space models for document retrieval

TYPE 2: CONTRADICTORY RESULTS
  Paper P1: Technique C improves metric M on dataset D1.
  Paper P2: Technique C does not improve M on dataset D2 (or hurts).
  No paper explains the discrepancy or proposes a condition-aware variant.
  Gap: "Understand when/why C works — propose a condition-aware variant of C"
  Example: data augmentation improves accuracy on balanced sets but not on long-tail sets

TYPE 3: MISSING BASELINE
  Method D achieves SOTA on task X but has never been compared with method E on dataset F.
  Gap: "Fair comparison of D vs E; or a D+E combination"
  Example: a new RL exploration strategy never benchmarked against curiosity-driven baselines

TYPE 4: EFFICIENCY GAP
  Method G achieves strong performance but is computationally prohibitive for deployment.
  Gap: "Distillation / pruning / efficient variant of G"
  Example: a large transformer achieves best classification accuracy but runs 10× slower than real-time

TYPE 5: GENERALIZATION GAP
  Method H has been tested only on domain X; domain Y is structurally similar but untested.
  Gap: "Does H generalize to Y? If not, what adaptation is required?"
  Example: a retrieval model trained on web text never evaluated on scientific or legal corpora
```

---

## 3. Paper-qa Query Templates

Run at least 8 queries covering all 5 gap types. Substitute `[X]` with project-specific terms.

```bash
# --- TYPE 1: Unexplored Combinations ---
pqa ask "What techniques are commonly combined with [method] in [task]?"
pqa ask "Has [technique-A] been applied to [task] together with [technique-B]?"
pqa ask "What attention or aggregation strategies have been used with [backbone] for [task]?"

# --- TYPE 2: Contradictory Results ---
pqa ask "What methods achieve the best [metric] on [dataset]? Are there conflicting results across papers?"
pqa ask "Which papers report negative or mixed results for [technique] in [domain]?"
pqa ask "Are there papers where [method] underperforms its expected improvement on [dataset-type]?"

# --- TYPE 3: Missing Baselines ---
pqa ask "Has [method-A] been compared directly with [method-B] on [dataset]?"
pqa ask "What baselines are missing from evaluations of [technique] in [task]?"

# --- TYPE 4: Efficiency Gaps ---
pqa ask "What are the computational limitations or inference costs of [SOTA-method] in [domain]?"
pqa ask "Are there efficient variants or lightweight alternatives to [method] for [task]?"

# --- TYPE 5: Generalization Gaps ---
pqa ask "What datasets has [method] been evaluated on? What settings or domains are missing?"
pqa ask "Has [method] been tested on [target-domain]? What challenges does domain shift introduce?"
```

---

## 4. Hypothesis Formulation Protocol

Every identified gap must be formulated as a structured hypothesis candidate using this template. Do not propose a candidate without pqa evidence.

```markdown
## Candidate HYP-C[N]

gap_type: [TYPE 1 | TYPE 2 | TYPE 3 | TYPE 4 | TYPE 5]
gap_description: "[Concrete description of the gap, with pqa evidence quote]"
pqa_evidence: "[Short quote or paraphrase from the paper(s) supporting this gap]"

hypothesis: "If [X] is added to / replaces / is combined with [Y], then [metric Z] on [dataset D]
             will [increase / decrease] by at least [Δ]."
mechanism: "[Why would X affect Z through Y? Causal chain in 2-3 sentences.]"
falsification: "[What result would falsify this hypothesis? Be specific: e.g.,
               'If adding X yields <0.5pp improvement over baseline after 5-fold CV, reject.']"

novelty_score: [1-5]
  # 5 = clearly unexplored: no pqa hit, no arXiv result found
  # 4 = probably unexplored: weak pqa hit, no direct comparison found
  # 3 = uncertain: pqa shows related work but not this exact combination
  # 2 = likely explored: pqa shows close prior work
  # 1 = almost certainly published: pqa finds direct hit

novelty_evidence: "[Quote from pqa supporting the novelty score]"

compute_cost_estimate: [low | medium | high]
  # low    = proxy run <30 min,  full run <5 h
  # medium = proxy 30 min–2 h,  full run 5–20 h
  # high   = proxy >2 h,        full run >20 h

expected_delta_estimate: [small | medium | large]
  # Based on analogous experiments in related work cited in pqa
  # small  = <1 pp accuracy | <5 FID | <50 reward units
  # medium = 1–3 pp         | 5–20 FID | 50–200 reward
  # large  = >3 pp          | >20 FID | >200 reward
delta_evidence: "[Reference from pqa supporting the expected delta]"

priority_score: novelty_score × delta_multiplier / cost_multiplier
  # delta_multiplier: large=3, medium=2, small=1
  # cost_multiplier:  high=3, medium=2, low=1
  # Example: novelty=4, delta=large(3), cost=low(1) → priority = 4×3/1 = 12.0
```

---

## 5. Ranking and Selection

After formulating all candidates (3–5):

1. Sort by `priority_score` descending.
2. Present the top 3 candidates to the user with a brief justification for each.
3. **Human Checkpoint (required):** Wait for the user to select one or approve the top candidate for the next stage.
4. Do NOT automatically advance to Stage 1 — user must explicitly confirm the direction.

If the user wants to run multiple candidates: route to `/hypothesis-tournament` (Stage 11.5) after Stage 10 proxy validation.

---

## 6. Output: `gap_scout_report.md`

Write this file to the project root after completing all queries.

```markdown
# Gap Scout Report

date: YYYY-MM-DD
literature_index: [path/to/pqa/index or "not built"]
queries_run: [N]
papers_consulted: [N estimated from pqa]
area_of_interest: "[user-specified or 'open exploration']"

---

## Identified Gaps

### Gap 1 — [TYPE N]: [Short title]
Evidence: "[pqa quote]"
Gap description: "[...]"

### Gap 2 — ...

---

## Hypothesis Candidates

[Full HYP-C[N] blocks, one per candidate]

---

## Ranking

| Rank | ID     | Gap Type | Novelty | Delta  | Cost   | Priority |
|------|--------|----------|---------|--------|--------|----------|
| 1    | HYP-C1 | TYPE 1   | 4       | large  | low    | 12.0     |
| 2    | HYP-C3 | TYPE 5   | 5       | medium | medium | 5.0      |
| 3    | HYP-C2 | TYPE 2   | 3       | medium | low    | 3.0      |

---

## Recommendation

**Top candidate:** HYP-C[N]
**Rationale:** [2–3 sentences]
**Alternative if top fails proxy:** HYP-C[M] — [reason]

---

## Human Checkpoint 1

Waiting for user to select a direction before registering in hypothesis_registry.md.
```

---

## 7. Mandatory Rules

1. **Evidence required:** Never propose a gap without at least one pqa evidence quote. If pqa returns no relevant results, increase the paper set before proposing.
2. **Maximum 5 candidates:** Do not overwhelm the user. If more than 5 gaps are found, select the top 5 by evidence quality before computing priority scores.
3. **No invented citations:** All paper references in gap_scout_report.md must come from pqa output, not from memory.
4. **No auto-registration:** Only register the user-selected hypothesis in `hypothesis_registry.md` (as HYP-NNN) after Human Checkpoint 1 confirmation.
5. **Coverage check:** Run queries across all 5 gap types. Do not report only Type 1 gaps.
6. **Insufficient coverage:** If fewer than 3 distinct gaps are found after 10+ queries, output: `"Literature coverage insufficient — add more PDFs to the paper-qa index before re-running Gap Scout."` Do not fabricate gaps to meet the minimum.
7. **Novelty score honesty:** If pqa finds a direct hit for a proposed gap, set novelty_score ≤ 2 and flag the candidate as `"may already be solved."` Do not artificially inflate novelty.

---

## 8. Integration with Research OS Stages

```
Gap Scout (Stage 0.5)
    ↓ [user selects HYP-C]
Stage 1 — Idea Intake (register as HYP-NNN)
    ↓
Stage 2 — Literature Review
    ...
Stage 10 — Proxy Protocol
    ↓ [if multiple candidates survive]
Stage 11.5 — Hypothesis Tournament (/hypothesis-tournament)
    ↓
Stage 12 — Exploratory Experiments
```

If the user enters at Stage 1 with an existing idea, Gap Scout is optional (but recommended for novelty scoring).
