# Contributing to Academic Research OS

Thank you for your interest in improving the Academic Research OS template. This project is designed to enforce evidence-first research practices, and contributions must reflect those same values: no fabricated examples, no invented results, and all proposed changes tested against a real or toy research project.

---

## Code of Conduct

- **Evidence-first.** All examples in documentation or templates must use placeholder markers (`[your-value]`, `TODO_RESULT_NEEDED:`, etc.) rather than invented data. Never include fake citations, fake metrics, or fabricated experiment results — even for illustration.
- **No hallucinated content.** Do not add workflow descriptions that reference features or behaviors that do not exist in the current codebase.
- **Constructive and specific.** Issues and PRs should describe a specific problem and a specific proposed fix, not general preferences.

---

## Reporting Issues

Use GitHub Issues to report:

- A workflow file that contains an error, inconsistency, or stale reference
- A template that is missing a required field
- A skill file that does not match its corresponding command in `11_COMMANDS.md`
- A README or documentation inconsistency

When filing an issue, include:
1. Which file(s) are affected (full path)
2. What the current behavior is
3. What the expected behavior should be
4. Whether you have a proposed fix (optional)

---

## Proposing New Skills or Workflow Improvements

New skills and workflow stages should be proposed as GitHub Issues before implementation. Include:

1. **Problem statement:** What research failure mode does this skill prevent?
2. **Stage mapping:** Which stage(s) in `02_RESEARCH_WORKFLOW.md` does it affect?
3. **Input/output spec:** What does the skill read? What does it produce?
4. **Anti-hallucination impact:** Does the skill introduce any risk of generated content being presented as factual? How is this prevented?
5. **Command name:** The `/command-name` that would invoke it (must not conflict with existing commands in `11_COMMANDS.md`)

If approved, the implementation must follow the existing skill file structure (see any existing skill in `.claude/skills/` for the pattern).

---

## Submitting a Pull Request

### Branch Naming

Use the format: `type/short-description`

Examples:
- `fix/template-missing-status-field`
- `feat/new-pivot-decision-skill`
- `docs/clarify-gate-2-rules`
- `refactor/consolidate-evidence-ledger-format`

### Before Opening a PR

1. Run `/verify-research-os` (or `scripts/verify.sh`) in the toy example project and confirm all checks pass.
2. Run `scripts/verify.sh examples/toy-research-project/` and confirm PASS or document any WARN with justification.
3. If you added or renamed a file in `.claude/research-os/` or `.claude/skills/`, update:
   - `01_REPOSITORY_MAP.md` (file count and listing)
   - `11_COMMANDS.md` if a command was added or changed
   - `14_CHANGELOG.md` with a new entry under the relevant version

### PR Description Template

```markdown
## What this changes
[One paragraph describing what was changed and why]

## Files changed
- [file path]: [what changed]

## Test
- [ ] `scripts/verify.sh` passes on toy example project
- [ ] `11_COMMANDS.md` updated (if commands changed)
- [ ] `14_CHANGELOG.md` updated
- [ ] No private research data included
- [ ] No fabricated examples (all examples use placeholder markers)

## Related issue
Closes #[issue number]
```

### Updating 14_CHANGELOG.md

Add an entry under `## [Unreleased]` in the format:

```markdown
### Added / Changed / Fixed / Removed
- [Description of change] — [file or area affected]
```

---

## What This Project Does Not Accept

- Contributions that add project-specific content (real dataset names, real model weights, real result tables)
- Contributions that weaken or remove anti-hallucination rules (13_ANTI_HALLUCINATION_RULES.md)
- Contributions that allow paper prose to be drafted before Stage 17 Evidence Freeze
- PRs that lower any gate threshold without a documented research rationale
- Fabricated example results, even for documentation purposes
