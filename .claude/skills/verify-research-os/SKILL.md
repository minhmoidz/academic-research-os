# Skill: /verify-research-os

**Purpose:** Verify that the entire Research OS is intact — all files present, all gates wired, CLAUDE.md pointing correctly, and project state up to date.  
**Stage:** Any (run when system integrity is in doubt, after a git pull, or at the start of a new machine setup)  
**Read-only:** Yes — never modifies files, only reports findings  
**Forbidden:** Never generates paper prose; never runs experiments; never modifies any file

---

## What This Skill Checks

This skill performs four categories of checks and produces a single integrity report. It does NOT overlap with `/tool-healthcheck` (which tests binary availability) or `/research-status` (which reports project progress). This skill tests the OS infrastructure itself.

---

## Check Category 1: Research OS Files (29 files)

Verify all 29 files exist in `.claude/research-os/`:

```bash
for f in \
  00_OVERVIEW.md \
  01_REPOSITORY_MAP.md \
  02_RESEARCH_WORKFLOW.md \
  03_IDEA_TO_PAPER_PLAYBOOK.md \
  04_LITERATURE_REVIEW_PLAYBOOK.md \
  05_EXPERIMENT_PLAYBOOK.md \
  06_WRITING_PLAYBOOK.md \
  07_FIGURE_AND_FORMAT_PLAYBOOK.md \
  08_REVIEW_AND_AUDIT_PLAYBOOK.md \
  09_SUBMISSION_CHECKLIST.md \
  10_TEMPLATES.md \
  11_COMMANDS.md \
  12_SESSION_PROTOCOL.md \
  13_ANTI_HALLUCINATION_RULES.md \
  14_CHANGELOG.md \
  15_TOOL_HEALTHCHECK.md \
  16_PROJECT_STATE.md \
  17_DECISION_LOG.md \
  18_EVIDENCE_LEDGER.md \
  19_DRY_RUN_TEST.md \
  20_AUTONOMOUS_EXPERIMENT_LOOP.md \
  21_EXPERIMENT_LOG_FORMAT.md \
  22_HYPOTHESIS_REGISTRY.md \
  23_RESEARCH_DIRECTION_UPDATE.md \
  24_VENUE_TARGETING.md \
  25_PRIOR_ART_COMPETITION.md \
  26_TARGET_RESULT_CONTRACT.md \
  27_RESULT_ADEQUACY_GATE.md \
  28_PIVOT_POLICY.md
do
  [ -f ".claude/research-os/$f" ] && echo "✓ $f" || echo "✗ MISSING: $f"
done
```

---

## Check Category 2: Skill Files (20 skills)

Verify all skill SKILL.md files exist:

```bash
for skill in \
  research-status \
  tool-healthcheck \
  verify-research-os \
  research-start \
  venue-target \
  prior-art-check \
  sota-check \
  literature-review \
  plan-experiments \
  target-result-contract \
  experiment-loop \
  experiment-status \
  result-backfill \
  result-adequacy \
  pivot-decision \
  paper-draft \
  paper-figure \
  paper-format \
  paper-review \
  submission-audit \
  archive-paper
do
  [ -f ".claude/skills/$skill/SKILL.md" ] && echo "✓ $skill" || echo "✗ MISSING: $skill"
done
```

---

## Check Category 3: CLAUDE.md Integrity

Read `.claude/CLAUDE.md` and verify:

```bash
grep -c "26-stage" .claude/CLAUDE.md          # expect ≥ 1
grep -c "Stage 17" .claude/CLAUDE.md           # expect ≥ 1
grep -c "13_ANTI_HALLUCINATION" .claude/CLAUDE.md  # expect ≥ 1
grep -c "02_RESEARCH_WORKFLOW" .claude/CLAUDE.md   # expect ≥ 1
grep -c "experiment-loop" .claude/CLAUDE.md    # expect ≥ 1
```

Check that the four hard gates are referenced:

| Gate | Marker to find in CLAUDE.md |
|------|-----------------------------|
| Stage 6 Prior-Art | `Stage 6` or `Prior-Art` |
| Stage 9 TRC | `Stage 9` or `Target Result Contract` |
| Stage 16 Adequacy | `Stage 16` or `Result Adequacy` |
| Stage 17 Freeze | `Stage 17` or `Evidence Freeze` |

---

## Check Category 4: Project State Currency

If `project_state.md` exists in the project root:

```bash
# Check last_updated field is present
grep "last_updated:" project_state.md

# Check current_stage is populated
grep "current_stage:" project_state.md

# Check next_safe_action is populated (not blank)
grep "next_safe_action:" project_state.md
```

If `project_state.md` is missing: report "Stage 0 not started — run /research-start before any research work."

If `last_updated` is more than 7 days old: flag "project_state.md may be stale — update before proceeding."

---

## Check Category 5: Tool Availability Summary

Quick availability check (not the deep test from `/tool-healthcheck`):

```bash
which pqa 2>/dev/null && echo "✓ pqa" || echo "✗ pqa not found"
which tectonic 2>/dev/null && echo "✓ tectonic" || echo "✗ tectonic not found"
which git 2>/dev/null && echo "✓ git" || echo "✗ git not found"
ls .claude/repos/academic-writing-agents/ 2>/dev/null && echo "✓ academic-writing-agents" || echo "✗ academic-writing-agents not found"
```

For missing binary tools: point to the install command in `01_REPOSITORY_MAP.md`.

---

## Output Format

```
═══════════════════════════════════════════════════════
Research OS Integrity Check — [timestamp]
═══════════════════════════════════════════════════════

RESEARCH-OS FILES (29 expected)
  ✓ [N]/29 present
  ✗ Missing: [list or "none"]

SKILL FILES (21 expected)
  ✓ [N]/21 present
  ✗ Missing: [list or "none"]

CLAUDE.MD INTEGRITY
  ✓ 26-stage workflow referenced
  ✓ All 4 hard gates referenced
  ✗ [specific missing reference if any]

PROJECT STATE
  Stage: [N] — [Stage Name]
  Last updated: [date]
  Status: [CURRENT / STALE (>7 days) / MISSING]

TOOL AVAILABILITY (quick check)
  ✓ pqa
  ✓ tectonic
  ✓ git
  ✓ academic-writing-agents
  ✗ [missing tool] — see 01_REPOSITORY_MAP.md

OVERALL: [PASS / WARN / FAIL]
  PASS  = all files present, all gates wired, tools available
  WARN  = optional files missing or state is stale
  FAIL  = required files missing or critical tools unavailable

Next recommended action: [specific action based on findings]
═══════════════════════════════════════════════════════
```

---

## Severity Classification

| Finding | Severity |
|---------|---------|
| Core research-os file missing (00-13) | FAIL — blocks all research work |
| Gate-related file missing (15-28) | FAIL — specific gate unusable |
| Skill file missing | WARN — that command unavailable |
| CLAUDE.md missing a gate reference | WARN — rule may not be enforced |
| project_state.md missing | WARN if Stage 0; FAIL if Stage ≥ 1 |
| project_state.md stale (>7 days) | WARN |
| Tool missing (pqa, tectonic) | FAIL for stages requiring that tool; WARN otherwise |
| academic-writing-agents missing | WARN — fallback procedures available |

---

## When to Run

- At the start of a new machine or new Claude session (alongside `/tool-healthcheck`)
- After any `git pull` or manual edit to `.claude/` files
- After a long gap between sessions (>1 week)
- If `/research-status` returns unexpected results
- Before running any gate command (`/prior-art-check`, `/target-result-contract`, `/result-adequacy`)
