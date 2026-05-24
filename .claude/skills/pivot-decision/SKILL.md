# SKILL: /pivot-decision
## Purpose
Generate a structured, evidence-grounded decision when experimental results do not support the original hypothesis or when the result adequacy gate fails. Identifies one of 9 possible pivot decisions, states the evidence that triggered it, defines the next action, and lists what claims are now forbidden.

---

## When to Run
Trigger this skill when ANY of the following conditions occur:
- `/result-adequacy` returns decision B, C, D, E, F, or G.
- A hypothesis in `hypothesis_registry.md` is marked CONTRADICTED.
- `prior-art threat` in `sota_baseline_table.md` is HIGH or CRITICAL.
- Budget is exhausted with no PASS confirmatory result.
- User explicitly asks for a pivot assessment.
- Crash rate exceeds 30% of CONFIRMATORY runs.

---

## Required Inputs
| Input | Source | If Missing |
|-------|--------|------------|
| result_adequacy_report.md | /result-adequacy | Read results.tsv directly |
| hypothesis_registry.md | project root | REQUIRED |
| research_direction.md | project root | REQUIRED |
| results.tsv | project root | REQUIRED |

---

## The 9 Pivot Decisions

| Code | Decision | Trigger | Risk |
|------|----------|---------|------|
| PROCEED | No pivot needed — evidence is sufficient | Decision A from adequacy gate | None |
| RUN_MORE_EXPERIMENTS | Add more seeds/folds/datasets | Decision G (variance), D (below threshold by small margin) | Budget cost |
| NARROW_CLAIM | Reduce scope of contribution claim | Decision B (1 of 2 datasets), C (SOTA gap negative) | Weaker story |
| CHANGE_VENUE | Target a lower tier venue | Decision C or D with small gap | Timeline cost |
| PIVOT_ANALYSIS | Reframe paper as analysis/ablation study | All CONFIRMATORY fail but interesting patterns observed | Substantial rewrite |
| PIVOT_ROBUSTNESS | Reframe contribution as robustness/generalization | Results are stable but not best-in-class | Requires new experiments |
| PIVOT_BENCHMARK | Reframe as benchmark/dataset contribution | Results strong on evaluation methodology but not model | Requires dataset access |
| PIVOT_SYSTEM | Reframe as system/engineering paper | Implementation is novel but metrics are not exceptional | Different venue type |
| ABANDON | Stop pursuing this direction | No useful signal; concurrent work already published same result | Work loss — requires confirmation |

---

## Steps

### Step 1 — Load Pivot Policy
Read `.claude/research-os/28_PIVOT_POLICY.md` for decision rules, forbidden pivots, and documentation requirements.

### Step 2 — Gather Evidence State
Load current evidence:
1. Read `result_adequacy_report.md` — get decision code and failure reasons.
2. Read `results.tsv` — summarize: PASS count, FAIL count, best result, best delta.
3. Read `hypothesis_registry.md` — list: supported, contradicted, inconclusive hypotheses.
4. Read `research_direction.md` — get original claim and contribution statement.
5. Read `sota_baseline_table.md` — get prior-art threat level.

### Step 3 — Identify the Applicable Pivot Decision
Apply this decision tree:

```
IF adequacy gate = A → PROCEED (no pivot needed)
ELSE IF variance too high (decision G) → RUN_MORE_EXPERIMENTS
ELSE IF below threshold by margin < 0.5% AND budget allows → RUN_MORE_EXPERIMENTS
ELSE IF SOTA gap negative AND claim is "outperforms" AND results competitive:
  IF lower tier venue exists with appropriate deadline → CHANGE_VENUE
  ELSE → NARROW_CLAIM
ELSE IF all CONFIRMATORY fail BUT exploratory shows interesting patterns:
  IF patterns are publishable as analysis → PIVOT_ANALYSIS
  ELSE IF patterns show robustness insight → PIVOT_ROBUSTNESS
ELSE IF dataset / evaluation methodology is novel regardless of method performance → PIVOT_BENCHMARK
ELSE IF implementation is novel and engineering contribution is clear → PIVOT_SYSTEM
ELSE IF concurrent published paper covers exact contribution → ABANDON (after user confirmation)
ELSE → NARROW_CLAIM (default safe option)
```

### Step 4 — Generate the Pivot Recommendation
Produce a structured recommendation:

```markdown
## Pivot Decision: [CODE]

### Trigger Evidence
- [Specific result or condition that triggered this pivot]
- [Which TRC item failed, or which hypothesis was contradicted]
- [Best result achieved: metric=value vs. required=value]

### Recommended Decision: [CODE]
[2–3 sentence explanation of why this specific decision is appropriate given the evidence]

### Risk Assessment
- Upside: [what this pivot preserves or enables]
- Downside: [what is lost or what additional work is required]
- Timeline impact: [estimate]

### Next Actions
1. [Specific first action]
2. [Specific second action]
3. [Specific third action]

### Forbidden Claims After This Pivot
The following claims may NO longer be made after this pivot:
- FORBIDDEN: "[specific claim]" — reason: [evidence contradicts it / not supported]
- FORBIDDEN: "[specific claim]" — reason: [dataset scope no longer supports it]

### New Target Result Contract (if applicable)
[If the pivot changes the main claim: describe the new TRC that must be created before new CONFIRMATORY experiments begin]
```

### Step 5 — ABANDON Requires Special Handling
If the recommended decision is ABANDON:
1. Do NOT log immediately.
2. First present these alternative framings to the user:
   - Could the failed experiment be reframed as a negative result contribution?
   - Is there a workshop paper about "what we learned from this failure"?
   - Is there partial evidence for a narrower claim worth pursuing?
3. Only if the user confirms ABANDON: log the decision and explain clearly what was learned.
4. Write a brief negative_result_note.md documenting the hypothesis, the evidence against it, and the lessons.

### Step 6 — Update hypothesis_registry.md
For each contradicted hypothesis: update status to `CONTRADICTED` with the triggering experiment ID.
For hypotheses that survive the pivot: keep status; mark any that become out-of-scope as `RETIRED`.

### Step 7 — Log Decision in decision_log.md
```
DEC-[N] | [date] | PIVOT_DECISION | [CODE]: [summary] | Triggered by: [evidence] | Next: [action]
```

### Step 8 — Update research_direction.md
Version bump: v[N+1].
Add pivot section:
```markdown
## Pivot History
- v[N+1] ([date]): [CODE] — [reason] — [new direction]
```

### Step 9 — Create New TRC if Pivot Changes Main Claim
If the pivot changes the primary claim (e.g., NARROW_CLAIM, PIVOT_ANALYSIS):
- The old TRC is now SUPERSEDED.
- A new TRC must be created (run /target-result-contract) before new CONFIRMATORY experiments begin.
- Mark old TRC as `Status: SUPERSEDED by TRC v[N]`.

### Step 10 — Update project_state.md
```
pivot_decision_made: true
pivot_decision: [CODE]
pivot_date: [date]
trc_status: [SUPERSEDED/ACTIVE]
paper_writing_authorized: false  # reset; require new adequacy gate
```

---

## Output Files
- `decision_log.md` — appended
- `research_direction.md` — updated (version bump)
- `hypothesis_registry.md` — updated (status of contradicted hypotheses)
- `project_state.md` — updated
- `negative_result_note.md` — created only if ABANDON

---

## Safety Rules (Non-Negotiable)
1. **Never recommend PROCEED if the TRC is not met.** This safety rule has no exceptions.
2. **Never soften a pivot recommendation to protect the original narrative.** If evidence contradicts the hypothesis: state it plainly.
3. **ABANDON requires user confirmation.** Claude must present alternatives first.
4. **Forbidden pivot: redefining the metric after results are seen** to make a failed result appear successful.
5. **Forbidden pivot: hiding failed experiments** by selectively reporting only PASS results without disclosing FAIL runs.
6. **Forbidden pivot: dropping inconvenient baselines** from the comparison table because our method underperforms them.
7. **Every pivot must be logged** — an undocumented pivot is equivalent to p-hacking.
8. **If decision is not PROCEED:** paper_writing_authorized remains false until a new adequacy gate is passed.
