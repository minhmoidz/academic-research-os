# Skill: /gap-scout

**Command:** `/gap-scout`  
**Purpose:** Autonomously discover research gaps from literature and propose ranked hypothesis candidates for user selection.  
**Stage:** 0.5 (before Stage 1 Idea Intake — runs when user has no committed hypothesis)  
**Protocol file:** `.claude/research-os/29_GAP_SCOUT_PROTOCOL.md`

---

## When This Skill Is Invoked

- User says "I don't have an idea yet" or "help me find a research direction"
- User has a dataset and baseline but does not know what to add or change
- A previous hypothesis was abandoned via `/pivot-decision` and a fresh direction is needed
- User explicitly types `/gap-scout`

---

## Required Inputs

| Input | Source | Required |
|-------|--------|----------|
| paper-qa index path | User provides or defaults to `./pqa_index/` | Yes |
| Task domain / research area | Asked interactively | Yes |
| Rough area of interest | Asked interactively (can be "open") | Optional |
| `project_profile.md` | Project root, if exists | Optional |

---

## Execution Steps

### Step 1 — Read project context
Read `project_profile.md` from the project root if it exists. Extract: `task_family`, `dataset_names`, `primary_metric`, `backbone`. If the file does not exist, ask the user for these fields briefly.

### Step 2 — Ask user for area of interest
Prompt:
```
What is your rough area of interest?
  - Type a keyword or phrase (e.g., "attention mechanisms for classification", "efficient inference")
  - Type "open" for full exploration across all gap types with no constraint
```
Wait for user response before proceeding.

### Step 3 — Run gap discovery queries (minimum 8 queries)
Use pqa to query across all 5 gap types defined in `29_GAP_SCOUT_PROTOCOL.md`:
- TYPE 1 (Unexplored Combination): ≥ 2 queries
- TYPE 2 (Contradictory Results): ≥ 2 queries
- TYPE 3 (Missing Baseline): ≥ 1 query
- TYPE 4 (Efficiency Gap): ≥ 1 query
- TYPE 5 (Generalization Gap): ≥ 1 query
- Additional targeted queries based on user's area of interest

Use the query templates from Section 3 of `29_GAP_SCOUT_PROTOCOL.md`. Substitute project-specific terms.

If pqa is not installed or index is empty: report "paper-qa index not found or empty — run `/tool-healthcheck` and add PDFs before gap scouting." Do not proceed with fabricated gaps.

### Step 4 — Formulate hypothesis candidates
For each identified gap:
- Assign a gap type (TYPE 1–5)
- Write a full `HYP-C[N]` block following the template in Section 4 of `29_GAP_SCOUT_PROTOCOL.md`
- Include: `hypothesis`, `mechanism`, `falsification`, `novelty_score`, `novelty_evidence`, `compute_cost_estimate`, `expected_delta_estimate`, `delta_evidence`, `priority_score`
- Maximum 5 candidates total

### Step 5 — Compute priority scores
```
priority_score = novelty_score × delta_multiplier / cost_multiplier
delta_multiplier: large=3, medium=2, small=1
cost_multiplier:  high=3, medium=2, low=1
```

### Step 6 — Rank candidates
Sort all candidates by `priority_score` descending.

### Step 7 — Write `gap_scout_report.md`
Write to project root using the template in Section 6 of `29_GAP_SCOUT_PROTOCOL.md`. Include all candidates, ranking table, and recommendation.

### Step 8 — Present top 3 to user
Display:
- Top 3 candidates with their priority scores, gap type, novelty score, expected delta, compute cost
- A 2–3 sentence justification for the top recommendation
- The alternative if the top candidate fails proxy

### Step 9 — Human Checkpoint 1 (REQUIRED — do not skip)
```
Which candidate would you like to pursue?
  [1] HYP-C1 — [short title] (priority: X.X)
  [2] HYP-C2 — [short title] (priority: X.X)
  [3] HYP-C3 — [short title] (priority: X.X)
  [A] Approve all top candidates for a Hypothesis Tournament (if ≥3 approved)
  [N] None — refine the search (add more papers or change area of interest)
```
**Do not proceed until user responds explicitly.**

### Step 10 — Register selected hypothesis
After user selects:
- If single candidate selected: register as `HYP-NNN` in `hypothesis_registry.md` with `validation_status: PENDING`
- If "Approve all": register all top candidates as `HYP-NNN`, `HYP-NNO`, etc. with `validation_status: PENDING`; note that tournament will be needed at Stage 11.5
- If "None": ask if user wants to add more PDFs and re-run, or manually specify an idea
- Update `project_state.md`: set stage to 1 (Idea Intake in progress)

---

## Output Artifacts

| Artifact | Location | Description |
|----------|----------|-------------|
| `gap_scout_report.md` | Project root | Full gap analysis, all HYP-C blocks, ranking table |
| `hypothesis_registry.md` | Project root | New HYP-NNN entry (post selection) |
| `project_state.md` | Project root | Stage updated to 1 |

---

## Forbidden Actions

- Proposing a gap without a pqa evidence quote — no gap can be invented from memory
- Proposing more than 5 candidates (caps the list; pick top 5 by evidence quality before scoring)
- Fabricating paper citations in gap_scout_report.md — all references must come from pqa output
- Skipping Human Checkpoint 1 — the skill must always pause and wait for user direction selection
- Auto-registering ALL candidates as HYP-NNN without user confirmation
- Setting novelty_score = 5 when pqa found a direct hit for the same combination
- Advancing to Stage 1 prose writing before the user selects a direction

---

## Error Conditions

| Condition | Response |
|-----------|----------|
| pqa not installed | "paper-qa not found. Run `/tool-healthcheck` first." |
| pqa index empty | "paper-qa index is empty. Add PDFs with `pqa add <path>` and re-run." |
| < 3 gaps found after 10+ queries | "Literature coverage insufficient — add more PDFs to the index." |
| All candidates have novelty_score ≤ 2 | Warn user: "All identified directions appear to have prior art. Consider adding more recent papers or narrowing the area of interest." |
