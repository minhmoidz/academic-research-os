# Session Protocol and Project State

## Overview

Research projects span many sessions over weeks or months. Without a structured handoff protocol, each new session risks repeating completed work, losing context about decisions made in prior sessions, or inadvertently advancing past a gate that was not properly cleared. The session protocol ensures continuity, traceability, and correct resumption regardless of the gap between sessions.

---

## 1. The 11-Step Session Start Protocol

At the start of every session, Claude executes the following protocol. Steps 1–5 are read-only; Steps 6–11 involve reporting and confirmation.

1. **Read `.claude/research-os/12_SESSION_PROTOCOL.md`** — Load the full protocol. This file is the authoritative source; if it conflicts with any other instruction, it takes precedence.

2. **Read `project_state.md`** — Determine the current stage number, the last completed action, the last updated timestamp, and any open blockers noted in the previous session.

3. **Read `decision_log.md`** — Scan the last 5 entries to understand recent decisions, pivots, and rationale that may affect the current session's actions.

4. **Read `research_direction.md`** — Confirm the current research question and hypothesis. Check whether a pivot has changed the direction since the last session.

5. **Run `/research-status`** — Execute the artifact scanner to detect which stages are complete, which are partially complete, and which required files are missing.

6. **Report current stage** — State the current stage number, stage name, and a one-sentence summary of what was last accomplished.

7. **Report any missing artifacts** — List files that are required for the current stage but do not exist.

8. **Report the next safe action** — State the single next action that is safe to take given the current stage and gate status. Do not propose multiple actions; propose one.

9. **Report any blockers** — If any gate is not cleared and forward progress is blocked, state which gate and what is needed to clear it.

10. **Confirm before writing** — Do not write any artifact, paper prose, or code without explicit confirmation from the researcher. The report in Steps 6–9 is informational only.

11. **Wait for researcher instruction** — The session begins active work only after the researcher confirms the next action or provides a different instruction.

---

## 2. What project_state.md Contains and Why It Must Be Updated Every Session

`project_state.md` is the single source of truth for the project's current position in the 26-stage workflow. It must be updated at the end of every session — not at the start of the next session, because a gap (machine restart, collaborator change, session timeout) may mean the next session starts without access to Claude's in-context memory.

**Required fields in project_state.md:**

```markdown
# Project State

## Current Stage
[Stage number and name, e.g., "Stage 14: Full Experiment Run"]

## Last Action Completed
[One sentence describing the last completed action, e.g.,
"Run-012 completed: recall@10 = 0.714 on ScientificQA (5-fold)"]

## Last Updated
[ISO 8601 timestamp, e.g., "2024-11-20T16:42:00Z"]

## Open Blockers
[List any conditions that must be met before the next action.
If none, write "None."]

## Next Planned Action
[The action confirmed for the next session, e.g.,
"Run ablation removing re-ranker component (run-013)"]

## Gate Status
- Gate 1 (Prior-Art): [PASSED | NOT STARTED | IN PROGRESS]
- Gate 2 (Contract): [SIGNED | NOT STARTED | PROVISIONAL]
- Gate 3 (Adequacy): [PASSED: Decision A | NOT RUN | Decision D — reframing]
- Gate 4 (Freeze): [FROZEN: 2024-11-20T09:00:00Z | NOT FROZEN]

## Active Artifacts
[List of artifacts currently being edited or that are in DRAFT status]
```

**Why every session:** Claude Code does not retain memory between sessions by default. If `project_state.md` is not updated, the next session's Step 2 reads stale information. The session start protocol then reports an incorrect current stage, potentially causing duplicate work or skipped gates.

---

## 3. The decision_log.md: Format, When to Write an Entry, How to Find Past Decisions

`decision_log.md` records every significant decision made during the research project — not routine actions (running an experiment), but choices that affect the research direction, evidence scope, or submission strategy.

**When to write an entry:**
- After any `/pivot-decision` command
- After any gate decision (Pass / Fail / Decision A-G)
- When changing the venue target
- When abandoning a hypothesis and adopting a new one
- When discovering a prior-art conflict and reframing the contribution
- When responding to a reviewer and deciding which experiments to run

**Entry format:**

```markdown
## Decision Entry — 2024-11-18T14:30:00Z

**Decision type:** Hypothesis reframe
**Trigger:** Gate 3 returned Decision D (results do not support original claim,
but a different finding exists)
**Original claim:** "Re-ranking improves recall for all query types"
**Finding:** Re-ranking improves recall only for multi-hop queries
(single-hop queries show no statistically significant difference)
**New direction:** Narrow contribution to multi-hop query improvement;
add query-type breakdown to results table
**Actions taken:**
- Updated `research_direction.md` with narrowed claim
- Updated `contributions.md` — removed claim C-7 (single-hop recall)
- Scheduled run-013 (ablation on query type)
**Rationale:** The multi-hop finding is publishable at Tier 3;
abandoning would waste the existing evidence
**Signed by:** [researcher name or "auto-logged by OS"]
```

**Finding past decisions:**
`decision_log.md` is in reverse-chronological order (newest entries at the top). To find why a specific choice was made, search the file for the relevant date range or keyword (e.g., "venue," "pivot," "Gate 3"). Each entry's "Trigger" field names the event that prompted the decision.

---

## 4. How to Resume a Session After a Long Gap

A "long gap" is any gap longer than one week, or any gap after which the researcher is uncertain about the exact current state. The session start protocol (Section 1) is sufficient for normal resumption. For long-gap resumption, add the following steps after Step 5:

**Step 5a: Read `evidence_ledger.md`** — Review which evidence entries are APPROVED, which are DRAFT, and which evidence IDs are referenced in `claim-evidence-table.md`. This confirms whether the Evidence Freeze has occurred.

**Step 5b: Read the last 10 rows of `results.tsv`** — Identify the most recent experiments and their status. Confirm that no FAILED runs are waiting for resolution.

**Step 5c: Check git log** — Run `git log --oneline -20` to see the last 20 commits. This provides a concrete timeline of what was done.

**Step 5d: Check for new SOTA papers** — If more than 4 weeks have passed since Gate 1, run a brief pqa query to check for newly published papers in the relevant area. If a new paper exceeds your method's results, log this in `decision_log.md`.

After these additional steps, proceed to Step 6 (Report current stage) as normal.

---

## 5. The /verify-research-os Command: When to Run It, What It Checks

`/verify-research-os` checks the integrity of the Research OS system files themselves, not the external tools (that is `/tool-healthcheck`'s job) and not the project artifacts (that is `/research-status`'s job).

**When to run it:**
- After cloning the template repository for the first time
- After manually editing any file in `.claude/research-os/`
- After a Claude Code update that may have changed plugin behavior
- If a slash command (e.g., `/research-status`) produces unexpected output or errors
- If you suspect a system file was accidentally modified

**What it checks:**

| Check | Description |
|-------|-------------|
| File count | All 26 stage definition files (01_STAGE_XX.md through 26_STAGE_XX.md) are present |
| File integrity | No stage file is empty or truncated |
| Hook configuration | All required hooks in `.claude/settings.json` are present and point to valid targets |
| Command registry | All slash commands documented in `11_COMMANDS.md` are registered |
| Anti-hallucination rules | `13_ANTI_HALLUCINATION_RULES.md` contains exactly 15 rules |
| Session protocol | `12_SESSION_PROTOCOL.md` contains all 11 steps |
| Plugin linkage | The academic-writing-agents plugin is loaded and responds to a ping |

**What it does not check:**
- Whether `project_state.md` is up to date (use `/research-status`)
- Whether external tools are installed (use `/tool-healthcheck`)
- Whether experiment results are valid (use Gate 3)

**Expected output when all checks pass:**
```
[OK] Stage files: 26/26 present
[OK] Hook configuration: valid
[OK] Command registry: all commands registered
[OK] Anti-hallucination rules: 15/15 present
[OK] Session protocol: 11/11 steps present
[OK] Plugin: academic-writing-agents loaded
Research OS integrity: VERIFIED
```

If any check fails, the output will name the specific file or configuration that failed and suggest a remediation step.
