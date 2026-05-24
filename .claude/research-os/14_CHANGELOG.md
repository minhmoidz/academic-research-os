# Research OS Changelog

Track changes to the Research OS system itself. Every change to `.claude/research-os/` or `.claude/skills/` should be logged here.

---

## Format

```markdown
## [YYYY-MM-DD] — Short description (vX.Y)

### Added
- [new file or feature]

### Changed
- [modified behavior or file]

### Fixed
- [bug or inconsistency corrected]

### Removed
- [deleted file or deprecated rule]

### Context
- [why this change was made]
```

---

## [2026-05-24] — Initial public release (v1.0)

### Added
- All 29 research-os files (00_OVERVIEW.md through 28_PIVOT_POLICY.md)
- 21 skill files covering all 24 commands
- docs/ directory (11 documentation files)
- templates/ directory (17 reusable artifact templates)
- scripts/ directory (install.sh, new-project.sh, verify.sh)
- examples/toy-research-project/ with sample artifacts

### Context
- First public release of the Claude Research OS template
- Supports 26-stage evidence-first research workflow with 4 hard gates
- Compatible with Claude Code (claude.ai/code)
