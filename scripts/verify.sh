#!/bin/bash
# verify.sh — Verify Research OS integrity in a project directory
# Usage: ./verify.sh [project-dir]  (default: current directory)
# Also works as a standalone check for the template repo itself.

PROJECT_DIR="${1:-.}"
CLAUDE_DIR="$PROJECT_DIR/.claude"

PASS=0
WARN=0
FAIL=0

echo "====================================================="
echo "Research OS Integrity Check"
echo "Directory: $(realpath $PROJECT_DIR)"
echo "Date: $(date +%Y-%m-%d)"
echo "====================================================="
echo ""

# ---- Check 1: Research OS files (29 expected) ----
echo "RESEARCH-OS FILES (29 expected)"
ROSDIR="$CLAUDE_DIR/research-os"
MISSING_ROS=()
for f in \
  00_OVERVIEW.md 01_REPOSITORY_MAP.md 02_RESEARCH_WORKFLOW.md \
  03_IDEA_TO_PAPER_PLAYBOOK.md 04_LITERATURE_REVIEW_PLAYBOOK.md \
  05_EXPERIMENT_PLAYBOOK.md 06_WRITING_PLAYBOOK.md \
  07_FIGURE_AND_FORMAT_PLAYBOOK.md 08_REVIEW_AND_AUDIT_PLAYBOOK.md \
  09_SUBMISSION_CHECKLIST.md 10_TEMPLATES.md 11_COMMANDS.md \
  12_SESSION_PROTOCOL.md 13_ANTI_HALLUCINATION_RULES.md 14_CHANGELOG.md \
  15_TOOL_HEALTHCHECK.md 16_PROJECT_STATE.md 17_DECISION_LOG.md \
  18_EVIDENCE_LEDGER.md 19_DRY_RUN_TEST.md 20_AUTONOMOUS_EXPERIMENT_LOOP.md \
  21_EXPERIMENT_LOG_FORMAT.md 22_HYPOTHESIS_REGISTRY.md \
  23_RESEARCH_DIRECTION_UPDATE.md 24_VENUE_TARGETING.md \
  25_PRIOR_ART_COMPETITION.md 26_TARGET_RESULT_CONTRACT.md \
  27_RESULT_ADEQUACY_GATE.md 28_PIVOT_POLICY.md
do
  [ -f "$ROSDIR/$f" ] || MISSING_ROS+=("$f")
done

ROS_COUNT=$((29 - ${#MISSING_ROS[@]}))
if [ ${#MISSING_ROS[@]} -eq 0 ]; then
  echo "  ✓ $ROS_COUNT/29 present"
  PASS=$((PASS+1))
else
  echo "  ✗ $ROS_COUNT/29 present"
  for m in "${MISSING_ROS[@]}"; do echo "    MISSING: $m"; done
  FAIL=$((FAIL+1))
fi

# ---- Check 2: Skill files (21 expected) ----
echo ""
echo "SKILL FILES (21 expected)"
MISSING_SK=()
for skill in \
  research-status tool-healthcheck verify-research-os research-start \
  literature-review prior-art-check sota-check venue-target \
  target-result-contract plan-experiments experiment-loop experiment-status \
  result-backfill result-adequacy pivot-decision paper-draft paper-figure \
  paper-format paper-review submission-audit archive-paper
do
  [ -f "$CLAUDE_DIR/skills/$skill/SKILL.md" ] || MISSING_SK+=("$skill")
done

SK_COUNT=$((21 - ${#MISSING_SK[@]}))
if [ ${#MISSING_SK[@]} -eq 0 ]; then
  echo "  ✓ $SK_COUNT/21 present"
  PASS=$((PASS+1))
else
  echo "  ✗ $SK_COUNT/21 present"
  for m in "${MISSING_SK[@]}"; do echo "    MISSING: $m/SKILL.md"; done
  WARN=$((WARN+1))
fi

# ---- Check 3: CLAUDE.md wiring ----
echo ""
echo "CLAUDE.MD INTEGRITY"
CLAUDEMD="$CLAUDE_DIR/CLAUDE.md"
if [ ! -f "$CLAUDEMD" ]; then
  echo "  ✗ .claude/CLAUDE.md not found"
  FAIL=$((FAIL+1))
else
  GATES_FOUND=0
  grep -q "Stage 6\|Prior-Art" "$CLAUDEMD" && GATES_FOUND=$((GATES_FOUND+1))
  grep -q "Stage 9\|Target Result" "$CLAUDEMD" && GATES_FOUND=$((GATES_FOUND+1))
  grep -q "Stage 16\|Result Adequacy" "$CLAUDEMD" && GATES_FOUND=$((GATES_FOUND+1))
  grep -q "Stage 17\|Evidence Freeze" "$CLAUDEMD" && GATES_FOUND=$((GATES_FOUND+1))
  if [ $GATES_FOUND -eq 4 ]; then
    echo "  ✓ All 4 hard gates referenced"
    PASS=$((PASS+1))
  else
    echo "  ⚠ Only $GATES_FOUND/4 hard gates found in CLAUDE.md"
    WARN=$((WARN+1))
  fi
fi

# ---- Check 4: Project state ----
echo ""
echo "PROJECT STATE"
STATE="$PROJECT_DIR/project_state.md"
if [ ! -f "$STATE" ]; then
  echo "  ⚠ project_state.md not found — run /research-start to initialize"
  WARN=$((WARN+1))
else
  STAGE=$(grep "current_stage:" "$STATE" 2>/dev/null | head -1)
  UPDATED=$(grep "last_updated:" "$STATE" 2>/dev/null | head -1)
  echo "  ✓ project_state.md exists"
  echo "    $STAGE"
  echo "    $UPDATED"
  PASS=$((PASS+1))
fi

# ---- Check 5: Key tools ----
echo ""
echo "TOOL AVAILABILITY (quick check)"
command -v pqa &>/dev/null && echo "  ✓ pqa" || echo "  ✗ pqa not found — pip install paper-qa"
command -v tectonic &>/dev/null && echo "  ✓ tectonic" || echo "  ⚠ tectonic not found — see docs/installation.md"
command -v git &>/dev/null && echo "  ✓ git" || echo "  ✗ git not found"
[ -d "$CLAUDE_DIR/repos/academic-writing-agents" ] && echo "  ✓ academic-writing-agents" || echo "  ⚠ academic-writing-agents not found — see 01_REPOSITORY_MAP.md"

# ---- Summary ----
echo ""
echo "====================================================="
TOTAL=$((PASS+WARN+FAIL))
if [ $FAIL -eq 0 ] && [ $WARN -eq 0 ]; then
  echo "OVERALL: PASS ($PASS/$TOTAL checks passed)"
elif [ $FAIL -eq 0 ]; then
  echo "OVERALL: WARN ($PASS passed, $WARN warnings, 0 failures)"
else
  echo "OVERALL: FAIL ($PASS passed, $WARN warnings, $FAIL failures)"
fi
echo "====================================================="

[ $FAIL -eq 0 ]
