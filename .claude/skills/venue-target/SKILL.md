# SKILL: /venue-target
## Purpose
Select and commit to a target venue. Define venue-specific evidence requirements, deadline constraints, and the minimum result level required for acceptance at that tier.

---

## When to Run
- Stage 6 (Venue Targeting) of the research workflow.
- Before writing target_result_contract.md (venue tier determines the pass threshold).
- After sota_baseline_table.md is at least partially complete.
- If experimental results suggest the current venue tier is too ambitious or too conservative.

---

## Required Inputs
| Input | Source |
|-------|--------|
| Paper type (full paper / short paper / workshop) | User |
| Current best result (if any) | results.tsv or "not yet run" |
| Novelty level (algorithmic / benchmark / application) | User / research_direction.md |
| Candidate venues (if user has preferences) | User |

---

## Steps

### Step 1 — Load Venue Targeting Guidelines
Read `.claude/research-os/24_VENUE_TARGETING.md` for tier definitions, evidence requirements, and decision rules.

### Step 2 — Elicit Candidate Venues
If `venue_target.md` does not already exist, ask the user:
```
Which venues are you considering? (list 1–4 candidates)
What is your submission deadline?
Is this a full paper or short/workshop paper?
Is double-blind review required?
```

### Step 3 — Evaluate Each Candidate Venue
For each candidate venue, collect and record:

| Field | Value |
|-------|-------|
| Venue name | |
| Tier (1 / 2 / 3 / Workshop) | |
| Full-paper page limit | |
| Submission deadline | |
| Double-blind? | |
| Review criteria emphasis | |
| Typical acceptance rate | |
| Evidence strength required | |

**Tier definitions (use these consistently):**
- **Tier 1:** Top venues (e.g., NeurIPS, ICML, ICLR, CVPR, MICCAI, TPAMI). Require strong ablations, multiple datasets, significant improvement over strong baselines, and high novelty.
- **Tier 2:** Strong venues (e.g., ECCV, ICCV, AAAI, TMI, MedIA). Require solid results, at least 2 datasets, clear ablation, reasonable novelty.
- **Tier 3:** Solid venues (e.g., MIDL, ISBI, BMVC, domain-specific journals). Require valid results on at least 1 dataset, any ablation, incremental novelty acceptable.
- **Workshop:** Preliminary results acceptable; hypothesis + early evidence sufficient.

### Step 4 — Map Current Evidence to Venue Requirements
Load current evidence state:
1. Read `results.tsv` — get best PASS result and count of valid experiments.
2. Read `sota_baseline_table.md` — get gap over SOTA.
3. Read `hypothesis_registry.md` — assess how many hypotheses are supported.

Then evaluate:
```
For each candidate venue:
  Does current evidence meet Tier evidence requirements? YES / PARTIAL / NO
  Is the performance gap above the venue's implied minimum? YES / BORDERLINE / NO
  Is the ablation complete enough? YES / PARTIAL / NO
```

### Step 5 — Generate Venue Recommendation
Apply the following decision logic:
- If evidence is STRONG (exceeds SOTA, full ablation, 2+ datasets): recommend Tier 1.
- If evidence is SOLID (competitive with SOTA, ablation exists, 2 datasets): recommend Tier 2.
- If evidence is EMERGING (below SOTA but novel mechanism, 1 dataset, partial ablation): recommend Tier 3.
- If no confirmatory experiments run yet: recommend **tentative** venue; lock in after Stage 16.

### Step 6 — Create venue_target.md
Write `venue_target.md` using this template:

```markdown
# Venue Target

**Primary venue:** [name]
**Tier:** [1/2/3/Workshop]
**Submission deadline:** [date]
**Page limit:** [N pages]
**Double-blind:** [yes/no]

## Evidence Requirements for This Venue
- Minimum datasets: [N]
- Required baselines: [list]
- Required ablation components: [list]
- Minimum acceptable improvement over strongest baseline: [value]
- Required: statistical significance / variance / std? [yes/no]

## Backup Venue (if primary is rejected)
**Backup venue:** [name]
**Tier:** [tier]
**Backup deadline:** [date]

## Decision Rationale
[2–4 sentences explaining why this venue was chosen given current evidence]

## Status
tentative / confirmed (confirm after Stage 16 result adequacy gate)
```

### Step 7 — Log Decision
Append to `decision_log.md`:
```
DEC-[N] | [date] | VENUE_SELECTION | Selected [venue] (Tier [X]) | Rationale: [brief] | Status: tentative
```

### Step 8 — Update project_state.md
```
venue_target_complete: true
target_venue: [name]
venue_tier: [X]
venue_decision_status: tentative
```

---

## Output Files
- `venue_target.md` — created or updated
- `decision_log.md` — appended
- `project_state.md` — updated

---

## Safety Rules
1. **Never assume Tier 1 is appropriate** without verifying that evidence meets Tier 1 requirements (exceptional results, not just "good").
2. **Never recommend a venue without defining the minimum acceptable result** for that venue (this flows into target_result_contract.md).
3. **If no confirmatory experiments have been run:** mark venue selection as `tentative`; require reconfirmation after Stage 16.
4. **Never recommend a venue that the user explicitly ruled out** without stating a specific reason and asking for user confirmation.
5. **If deadline has already passed:** flag immediately; do not proceed without identifying an alternative.
6. **Do not inflate novelty claims to justify a higher tier.** Tier assignment must reflect evidence, not aspiration.
