# Claude Project Instructions
## Academic Research OS — Template Repository

---

## Project Context

This repository contains the Academic Research OS — a reusable Claude Code operating system for evidence-first academic research. It provides:
- A 26-stage evidence-first research workflow
- 24 commands via 21 skill files
- 15 anti-hallucination rules enforced at every writing stage
- 17 artifact templates for every research stage
- 3 setup scripts for scaffolding new projects
- A worked toy example project (`examples/toy-research-project/`)

**This is a template repository.** It is not a research project itself. To use it in a research project, run `scripts/new-project.sh /path/to/new-project`.

---

## Academic Research Operating System

This project uses the Claude Research OS — a 26-stage, evidence-first workflow that guides research from raw idea to camera-ready paper.

All system files: `.claude/research-os/`
All skill files: `.claude/skills/`
Full command reference: `.claude/research-os/11_COMMANDS.md`

### Session Start (Required)

At the start of every research session on a project that uses this OS, Claude must:

1. Read `.claude/research-os/12_SESSION_PROTOCOL.md`
2. Follow the 11-step session start protocol
3. Read `project_state.md` (in the project root) for the current stage
4. Run `/research-status` to detect missing artifacts and blockers
5. Report current stage and next safe action
6. Wait for user confirmation before writing any content

### Core Operating Rules

- **Always follow** `.claude/research-os/02_RESEARCH_WORKFLOW.md` (26 stages)
- **Always follow** `.claude/research-os/13_ANTI_HALLUCINATION_RULES.md` (15 rules)
- **Do not write final paper prose** (Abstract, Introduction, Related Work, Method, Experiments, Conclusion, Limitations) before Stage 17 Evidence Freeze passes. Research notes, hypothesis notes, literature notes, experiment interpretation, TODO-based skeleton outlines, and all stage artifacts (matrices, checklists, templates, ledger entries) are allowed at any stage.
- **Do not write Related Work from memory** — always from paper-qa or a verified source
- **Do not claim novelty** before Stage 6 Prior-Art/SOTA Check passes
- **Do not claim performance** before Stage 16 Result Adequacy Gate passes
- **Do not target a venue** without defining venue-specific evidence requirements (Stage 9)
- **Experiments are for discovering what is true**, not proving the initial idea
- **If results contradict the initial hypothesis:** update `research_direction.md`, narrow claims, run `/pivot-decision`, or abandon — do not force the original story
- **Positive results alone are not sufficient** — evaluate venue fit, prior-art competition, and contribution defensibility before drafting
- **Use TODO markers instead of guessing:** `TODO_EVIDENCE_NEEDED:`, `TODO_RESULT_NEEDED:`, `TODO_CITATION_NEEDED:`, `TODO_NOVELTY_CHECK_NEEDED:`, `TODO_VENUE_FIT_NEEDED:`
- **Preserve** `\cite{}`, `\label{}`, `\ref{}`, `\eqref{}` during any prose revision
- **Update** `project_state.md` after every meaningful session

### For Empirical Projects

Use the bounded autoresearch-style experiment loop (`/experiment-loop`, `20_AUTONOMOUS_EXPERIMENT_LOOP.md`) to produce traceable results before making any performance claims in the draft.

### Paper-Specific Notes

See your project's `.claude/CLAUDE.md` for project-specific notes (LaTeX compiler path, citation format, column balance conventions, std formula). The template repository does not prescribe these — they depend on your target venue and LaTeX setup.

---

## When Working on This Template Repository

When modifying the template itself (not a project using it):

1. Never include private research data, real unpublished results, or private dataset names
2. Use placeholder markers in all templates and examples
3. Run `scripts/verify.sh` after any changes to `.claude/research-os/` or `.claude/skills/`
4. Update `01_REPOSITORY_MAP.md` if files are added or renamed
5. Update `11_COMMANDS.md` if commands are added or changed
6. Update `14_CHANGELOG.md` with a changelog entry
7. Test against the toy example project in `examples/toy-research-project/`

---

## Repository Map

| Directory | Contents | Count |
|-----------|---------|-------|
| `.claude/research-os/` | Workflow files (00–28) | 29 files |
| `.claude/skills/` | Skill files (one per command) | 21 skills |
| `templates/` | Artifact templates | 17 templates |
| `examples/toy-research-project/` | Worked example project | 7 files |
| `scripts/` | Setup and verification scripts | 3 scripts |
| `docs/` | User documentation | 2+ files |

For the full file listing, see `.claude/research-os/01_REPOSITORY_MAP.md`.
