#!/bin/bash
# new-project.sh — Scaffold a new research project with the Academic Research OS
# Usage: ./new-project.sh /path/to/new-project-dir [project-name]
# Example: ./new-project.sh ~/papers/my-transformer-paper "My Transformer Paper"
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

if [ -z "$1" ]; then
  echo "Usage: $0 /path/to/new-project-dir [project-name]"
  echo "Example: $0 ~/papers/my-new-paper"
  exit 1
fi

TARGET="$1"
PROJECT_NAME="${2:-$(basename $TARGET)}"
TODAY=$(date +%Y-%m-%d)

# Create project directory
mkdir -p "$TARGET"
echo "✓ Created directory: $TARGET"

# Install Research OS
bash "$SCRIPT_DIR/install.sh" "$TARGET"

# Create paper_brief.md from template
if [ ! -f "$TARGET/paper_brief.md" ]; then
  cp "$REPO_DIR/templates/paper_brief.template.md" "$TARGET/paper_brief.md"
  echo "✓ Created paper_brief.md from template"
fi

# Create decision_log.md
if [ ! -f "$TARGET/decision_log.md" ]; then
  cat > "$TARGET/decision_log.md" << EOF
# Decision Log

Append-only log of all research decisions. Never delete or modify past entries.

---

## DEC-${TODAY}-001

**Date:** ${TODAY}
**Category:** PROJECT_START
**Summary:** Project initialized with Academic Research OS

**Context:** New project created via new-project.sh.
**Decision:** Begin at Stage 0 (System Readiness).
**Rationale:** Standard project initialization.
**Next action:** Run \`/tool-healthcheck\`, then \`/research-start\`.
EOF
  echo "✓ Created decision_log.md"
fi

# Initialize git if not already a repo
if [ ! -d "$TARGET/.git" ]; then
  cd "$TARGET"
  git init -q
  git checkout -q -b main 2>/dev/null || true
  echo "✓ Initialized git repository (branch: main)"
  cd - > /dev/null
fi

echo ""
echo "====================================================="
echo "New research project scaffolded: $PROJECT_NAME"
echo "Location: $TARGET"
echo "====================================================="
echo ""
echo "Files created:"
echo "  $TARGET/.claude/        (Research OS workflow + skills)"
echo "  $TARGET/CLAUDE.md       (Claude Code project instructions)"
echo "  $TARGET/project_state.md"
echo "  $TARGET/paper_brief.md"
echo "  $TARGET/hypothesis_registry.md"
echo "  $TARGET/decision_log.md"
echo ""
echo "Next steps:"
echo "  1. cd $TARGET"
echo "  2. claude"
echo "  3. /tool-healthcheck    — verify tools"
echo "  4. /research-start      — begin with your idea"
echo ""
