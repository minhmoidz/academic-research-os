# SKILL: /target-result-contract
## Purpose
Define the minimum result requirements BEFORE confirmatory experiments are run. This creates a binding contract: pass/fail thresholds are set in advance and cannot be lowered after results are seen. This prevents p-hacking, threshold sliding, and selective reporting.

---

## When to Run
- Stage 7 (Target Result Contract) of the research workflow.
- MUST be run before any CONFIRMATORY experiment begins.
- After venue_target.md and sota_baseline_table.md are complete.
- After hypothesis_registry.md contains at least one active hypothesis.

---

## Required Inputs
| Input | Source |
|-------|--------|
| venue_target.md | Must exist (run /venue-target first) |
| hypothesis_registry.md | Must exist (active hypotheses) |
| sota_baseline_table.md | Must exist (at least partially) |
| Proposed confirmatory experiments | User describes what they plan to run |

---

## Steps

### Step 1 — Load Reference Documents
1. Read `.claude/research-os/26_TARGET_RESULT_CONTRACT.md` for the contract schema and signing protocol.
2. Read `venue_target.md` — extract minimum acceptable improvement and required evidence.
3. Read `hypothesis_registry.md` — identify all hypotheses to be confirmed.
4. Read `sota_baseline_table.md` — identify best-known baseline values.

### Step 2 — List Confirmatory Experiments
Ask the user to specify each confirmatory experiment:
```
For each experiment:
  - What model/method variant is being tested?
  - What dataset(s) will be used?
  - What metric is primary?
  - What is the baseline being compared against?
  - How many runs / folds / seeds will be used?
  - What is the expected runtime?
```

### Step 3 — Set Pass/Fail Thresholds
For each (experiment, dataset, metric) triplet, define:

| Field | Description |
|-------|-------------|
| `min_value` | Minimum result to be considered a PASS |
| `required_delta` | Minimum improvement over named baseline |
| `required_datasets` | Which datasets must ALL pass (not just one) |
| `required_baselines` | Baselines that must be beaten |
| `acceptable_variance` | Max std across folds/seeds considered stable |

**Threshold derivation rules:**
- `min_value` ≥ venue minimum (from venue_target.md).
- `required_delta` must be positive and meaningful (not just noise-level improvement).
- For AUC on classification datasets: delta ≥ 0.5% recommended minimum for a claim; delta ≥ 1.0% for a strong claim.
- If user proposes a threshold that is below the strongest known baseline: flag and require explicit user override.

### Step 4 — Define What Happens If Contract is Not Met
The contract must specify the failure response:
```
If PASS on primary metric but not on secondary: → NARROW_CLAIM
If PASS on 1 dataset but not both: → PIVOT_DECISION required
If FAIL on primary metric: → PIVOT_DECISION required
If CRASH (>30% of runs fail): → DIAGNOSTIC experiment required first
```

### Step 5 — User Sign-Off
Present the full contract to the user and require explicit confirmation:
```
PLEASE CONFIRM this target result contract before any confirmatory experiment begins.
Once confirmed, the pass/fail thresholds CANNOT be lowered.
Any change after results are seen requires a DEC entry and creates TRC v2.

Type "CONFIRMED" to proceed.
```
Do not proceed to write the contract file until the user confirms.

### Step 6 — Write target_result_contract.md
```markdown
# Target Result Contract (TRC)

**Version:** 1.0
**Created:** [date]
**Status:** ACTIVE
**Signed by:** [user name or "user-confirmed"]

## Venue
[venue name] — Tier [X] — Deadline [date]

## Hypotheses Under Test
- HYP-001: [description]
- HYP-002: [description]

## Confirmatory Experiments

### EXP-CONF-001
- Method: [name]
- Dataset: [name]
- Primary metric: [metric]
- Pass threshold: [value]
- Required delta over [baseline]: [delta]
- Folds/seeds: [N]
- Max acceptable std: [value]

### EXP-CONF-002
[repeat as needed]

## Global Pass Criteria
All of the following must be true to pass this TRC:
1. [condition 1]
2. [condition 2]
3. [condition 3]

## Failure Response Table
| Scenario | Required Action |
|----------|----------------|
| FAIL on primary | Run /pivot-decision |
| FAIL on secondary only | Narrow claims; do not remove from paper |
| CRASH > 30% runs | Run DIAGNOSTIC first |
| PASS on 1 dataset only | Run /pivot-decision (NARROW_CLAIM likely) |

## Amendment Log
[Any changes must be logged here with date and DEC entry reference]
```

### Step 7 — Update project_state.md
```
trc_complete: true
trc_version: 1.0
trc_date: [date]
trc_status: ACTIVE
confirmatory_experiments_may_begin: true
```

---

## Output Files
- `target_result_contract.md` — created (BEFORE experiments)
- `project_state.md` — updated

---

## Safety Rules (Non-Negotiable)
1. **Claude must NOT modify the pass/fail threshold after confirmatory experiments begin.** Any threshold change after seeing results is a protocol violation.
2. **Any amendment to the TRC requires:** a `DEC-N` entry in decision_log.md, a version bump (TRC v2, v3...), and explicit user confirmation.
3. **Never create the TRC after experiments have been run.** If experiments were already run: use /result-backfill to document them, but the TRC is retrospective and must be clearly marked `RETROSPECTIVE` — this weakens the evidence claim.
4. **Never set a threshold below the strongest known published baseline.** Beating a weak baseline does not constitute a meaningful contribution.
5. **If the user proposes thresholds that guarantee success given known results:** flag this as a conflict of interest; require the user to justify or adjust.
6. **The TRC covers all confirmatory experiments.** Exploratory and diagnostic experiments are not covered, but their results cannot be used as confirmatory evidence without being retroactively included in a TRC amendment.
