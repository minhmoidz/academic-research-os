#!/bin/bash
# install.sh — Install Academic Research OS into an existing project directory
# Usage: ./install.sh /path/to/your/project
# Example: ./install.sh ~/papers/my-new-paper
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

if [ -z "$1" ]; then
  echo "Usage: $0 /path/to/your/project"
  echo "Example: $0 ~/papers/my-new-paper"
  exit 1
fi

TARGET="$1"

if [ ! -d "$TARGET" ]; then
  echo "Error: Target directory '$TARGET' does not exist."
  echo "Create it first with: mkdir -p $TARGET"
  exit 1
fi

echo "Installing Academic Research OS into: $TARGET"
echo ""

# Copy .claude directory
if [ -d "$TARGET/.claude" ]; then
  echo "Warning: $TARGET/.claude already exists."
  read -p "Overwrite? (y/N) " -n 1 -r
  echo ""
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
  fi
fi

cp -r "$REPO_DIR/.claude" "$TARGET/"
echo "✓ Copied .claude/ (research-os + skills)"

# Copy root CLAUDE.md (project-level instructions)
if [ ! -f "$TARGET/CLAUDE.md" ]; then
  cp "$REPO_DIR/CLAUDE.md" "$TARGET/CLAUDE.md"
  echo "✓ Copied CLAUDE.md"
else
  echo "  Skipped CLAUDE.md (already exists)"
fi

# Create project_state.md from template if it doesn't exist
if [ ! -f "$TARGET/project_state.md" ]; then
  cp "$REPO_DIR/templates/project_state.template.md" "$TARGET/project_state.md"
  echo "✓ Created project_state.md from template"
else
  echo "  Skipped project_state.md (already exists)"
fi

# Create hypothesis_registry.md if it doesn't exist
if [ ! -f "$TARGET/hypothesis_registry.md" ]; then
  echo "# Hypothesis Registry" > "$TARGET/hypothesis_registry.md"
  echo "" >> "$TARGET/hypothesis_registry.md"
  echo "No hypotheses registered yet. Run \`/research-start\` to begin." >> "$TARGET/hypothesis_registry.md"
  echo "✓ Created hypothesis_registry.md (empty)"
fi

echo ""
echo "====================================================="
echo "Academic Research OS installed successfully."
echo "====================================================="
echo ""
echo "Next steps:"
echo "  1. cd $TARGET"
echo "  2. claude"
echo "  3. In Claude Code, type: /research-status"
echo "  4. Run: /tool-healthcheck"
echo "  5. Start a new project: /research-start"
echo ""
echo "Full documentation: $(dirname $SCRIPT_DIR)/docs/"
