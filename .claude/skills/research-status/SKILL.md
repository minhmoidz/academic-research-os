# /research-status — Research OS Status Report Skill

## Purpose

Report the current state of the research project within the Research OS workflow. This skill reads project artifacts from disk, counts open TODO markers, checks which required files exist, and outputs a structured status report. It never generates paper prose or makes assumptions about missing data.

---

## When to Use This Skill

- At the start of every session to restore context
- After completing a major stage to confirm progress
- When uncertain about which stage the project is in
- When another skill needs to know the current state before proceeding

---

## Required Steps

Execute all steps in order. Do not skip steps. Do not assume file contents — read them.

### Step 1: Read Session Protocol

Read `.claude/research-os/12_SESSION_PROTOCOL.md` to confirm the current workflow stage definitions and stage sequence.

### Step 2: Read Project State

Read `project_state.md` from the project root.

- If the file exists: extract `current_stage`, `last_updated`, `last_action`, `completed_stages`, `blockers`
- If the file does not exist: set stage = 0 and report that `/research-start` must be run before any other command

### Step 3: Read Hypothesis Registry

Read `hypothesis_registry.md` from the project root (if it exists).

- Count total hypotheses
- Count hypotheses by status: ACTIVE, CONFIRMED, REJECTED, NARROWED, REDIRECTED
- Note the primary hypothesis text

### Step 4: Read Results Log

Read `results.tsv` from the project root (if it exists).

- Count total experiment rows
- Find the row with the highest value for the primary metric (AUC or Accuracy)
- Note the experiment ID and value
- If the file does not exist: note "no experiments logged"

### Step 5: Read Evidence Ledger

Read `evidence_ledger.md` from the project root (if it exists).

- Count total evidence entries (EV-NNN)
- Count entries with status VERIFIED vs. TODO_EVIDENCE_NEEDED
- Note any entries with status CRITICAL_MISSING

### Step 6: Count Open TODO Markers

Run the following command:

```bash
grep -rn "TODO_EVIDENCE_NEEDED\|TODO_RESULT_NEEDED\|TODO_CITATION_NEEDED\|TODO_FIGURE_NEEDED\|TODO_ANALYSIS_NEEDED" \
  --include="*.tex" --include="*.md" . 2>/dev/null | wc -l
```

Also run:

```bash
grep -rn "TODO_EVIDENCE_NEEDED\|TODO_RESULT_NEEDED\|TODO_CITATION_NEEDED\|TODO_FIGURE_NEEDED\|TODO_ANALYSIS_NEEDED" \
  --include="*.tex" --include="*.md" . 2>/dev/null | head -20
```

Report both the count and the first 20 occurrences (file:line:content).

### Step 7: Check Artifact File Existence

Check whether each of the following files exists in the project root. Use `ls -la [filename] 2>/dev/null` for each:

| File | Required By Stage |
|------|------------------|
| `paper_brief.md` | Stage 1 |
| `venue_target.md` | Stage 3 |
| `literature-matrix.md` | Stage 5 |
| `hypothesis_registry.md` | Stage 6 |
| `results.tsv` | Stage 15 |
| `evidence_ledger.md` | Stage 12 |
| `claim-evidence-table.md` | Stage 12 |
| `research_direction.md` | Stage 7 |
| `target_result_contract.md` | Stage 9 |
| `result_adequacy_report.md` | Stage 16 |
| `decision_log.md` | Stage 16 (if pivot) |
| `prior_art_competition_table.md` | Stage 8 |
| `novelty_risk_report.md` | Stage 8 |
| `experiment_plan.md` | Stage 14 |
| `main.tex` | Stage 18 |
| `references.bib` | Stage 18 |

### Step 8: Check Active Gate

Based on `current_stage` from `project_state.md`, determine which gate currently applies:

| Stage | Gate |
|-------|------|
| 0–2 | Idea Gate: paper_brief.md must be complete |
| 3–4 | Venue Gate: venue_target.md must define tier and deadline |
| 5–6 | Literature Gate: literature-matrix.md must exist, pqa indexed |
| 7–8 | Novelty Gate: prior_art_competition_table.md must pass |
| 9 | TRC Gate: target_result_contract.md must be signed off |
| 10–14 | Experiment Design Gate: experiment_plan.md approved |
| 15 | Experiment Execution: results.tsv must be populated |
| 16 | Result Adequacy Gate: result_adequacy_report.md Decision A required |
| 17 | Evidence Freeze Gate: evidence_ledger.md must be complete |
| 18–21 | Writing Gate: no TODO_RESULT_NEEDED in prose |
| 22–24 | Review Gate: all 10 review passes complete |
| 25–26 | Submission Gate: submission checklist complete |

### Step 9: Output Status Report

Print the full report in the format below.

---

## Output Format

```
═══════════════════════════════════════════════════════════
Research OS Status Report
═══════════════════════════════════════════════════════════
Project: [name from paper_brief.md or directory name]
Current Stage: [N] — [Stage Name]
Last Updated: [timestamp from project_state.md]
Last Action: [last_action from project_state.md]

───────────────────────────────────────────────────────────
Workflow Progress
───────────────────────────────────────────────────────────
Completed Stages: [comma-separated list, or "none"]
Current Stage:    Stage [N] — [name]
Next Stage:       Stage [N+1] — [name]
Blockers:         [list of blockers, or "none"]

───────────────────────────────────────────────────────────
Artifact Status
───────────────────────────────────────────────────────────
  ✓ paper_brief.md
  ✗ venue_target.md          [MISSING — required for Stage 3]
  ✓ literature-matrix.md
  ✓ hypothesis_registry.md   [3 hypotheses: 1 ACTIVE, 2 CONFIRMED]
  ✗ results.tsv              [MISSING — required for Stage 15]
  ✓ evidence_ledger.md       [12 entries: 10 VERIFIED, 2 TODO]
  ✗ claim-evidence-table.md  [MISSING — required for Stage 12]
  ✗ research_direction.md    [MISSING — required for Stage 7]
  ✓ target_result_contract.md [TRC-001, status: ACTIVE]
  ✗ result_adequacy_report.md [MISSING — required for Stage 16]
  ...

───────────────────────────────────────────────────────────
Evidence Status
───────────────────────────────────────────────────────────
  Open TODO markers:          [N total]
    TODO_EVIDENCE_NEEDED:     [N occurrences]
    TODO_RESULT_NEEDED:       [N occurrences]
    TODO_CITATION_NEEDED:     [N occurrences]
    TODO_FIGURE_NEEDED:       [N occurrences]
    TODO_ANALYSIS_NEEDED:     [N occurrences]

  Top open TODOs (first 5):
    [file:line]: [TODO text snippet]
    ...

  Experiments logged:         [N runs in results.tsv, or "none"]
  Best result:                AUC = [value] (EXP-NNN, dataset=[name])
  Evidence entries:           [N total: M verified, K pending]

───────────────────────────────────────────────────────────
Hypothesis Status
───────────────────────────────────────────────────────────
  Total hypotheses: [N]
  Primary hypothesis: "[H1 text]"
  Status: [ACTIVE | CONFIRMED | REJECTED | NARROWED]

───────────────────────────────────────────────────────────
Current Gate
───────────────────────────────────────────────────────────
  Active gate: [gate name]
  Gate status: [OPEN / BLOCKED / PASSED]
  Reason if blocked: [specific missing artifact or condition]

───────────────────────────────────────────────────────────
Next Safe Action
───────────────────────────────────────────────────────────
  [One specific, concrete recommended action with the tool/command to use]
  Example: "Run /literature-review to build literature-matrix.md (Stage 5)"

═══════════════════════════════════════════════════════════
```

---

## Safety Rules

1. **Never generate paper prose.** This skill reads and reports — it never writes sections, abstracts, or contributions.

2. **Never assume file contents.** If a file is missing, report it as MISSING. Do not guess what it contains.

3. **Never invent experiment results.** Report only what is in `results.tsv`. If the file is missing or empty, report "no experiments logged."

4. **Report TODOs from actual file scan.** The grep output in Step 6 is required — do not estimate TODO counts from memory.

5. **If `project_state.md` is missing:** Report Stage 0 and instruct the user to run `/research-start` before any other action. Do not infer the current stage from other files.

6. **Do not advance the stage.** This skill reads state but does not modify `project_state.md`. Only stage-specific skills may update the current stage.

7. **If blockers exist:** List them explicitly. Do not proceed past a blocker without resolving it.

---

## Special Cases

### If project_state.md is missing

```
═══════════════════════════════════════════════════════════
Research OS Status Report
═══════════════════════════════════════════════════════════
Project: [directory name]
Current Stage: 0 — NOT STARTED

project_state.md was not found in the project root.
The Research OS has not been initialized for this project.

Next Safe Action:
  Run /research-start to initialize the project.
  This will create paper_brief.md, project_state.md, and
  all required Stage 1 artifacts.
═══════════════════════════════════════════════════════════
```

### If project is at Evidence Freeze (Stage 17) but TODOs remain

Report:
```
  WARNING: Stage 17 (Evidence Freeze) requires 0 open TODO_RESULT_NEEDED markers.
  Found [N] open TODO_RESULT_NEEDED markers. Stage 17 cannot pass until these are resolved.
  Locations: [list files with TODO_RESULT_NEEDED]
```

### If TRC exists but result_adequacy_report.md is missing and current stage >= 15

Report:
```
  WARNING: Experiments appear to be complete (results.tsv exists) but
  result_adequacy_report.md has not been generated.
  Stage 16 (Result Adequacy Gate) must be run before any paper prose is drafted.
  Next action: Run /result-adequacy to evaluate experiments against TRC-[NNN].
```
