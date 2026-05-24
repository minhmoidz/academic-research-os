# Claude Project Instructions
## Academic Research OS — Template Repository

---

## What This Repository Is

This is the Academic Research OS template repository. It contains:
- A 26-stage evidence-first research workflow
- 24 commands via 21 skill files
- 15 anti-hallucination rules for academic writing
- 17 artifact templates for every research stage
- 3 setup scripts for new and existing projects
- Documentation and quickstart guides
- A worked toy example project

This is a TEMPLATE. To use it in a real research project, run `scripts/new-project.sh` to copy the OS into your project directory.

---

## If You Are Developing This Template

When working on this template repository itself:
- Do not include private research data, private dataset names, or unpublished results in any file
- Use placeholder markers (`[your-value]`, `[YYYY-MM-DD]`, `TODO_RESULT_NEEDED:`) in all templates
- Test changes against `examples/toy-research-project/` before committing
- Run `scripts/verify.sh` to confirm all 29 workflow files and 21 skill files are present
- Update `11_COMMANDS.md` and `14_CHANGELOG.md` when adding or changing commands

---

## If You Are Inside a Research Project Using This OS

### Session Start (Required)

At the start of every research session, Claude must:

1. Read `.claude/CLAUDE.md` (inside the project directory, not this file)
2. Follow the 11-step session start protocol in `12_SESSION_PROTOCOL.md`
3. Read `project_state.md` in the project root for the current stage
4. Run `/research-status` to detect missing artifacts and blockers
5. Report current stage and next safe action
6. Wait for user confirmation before writing any content

### Core Operating Rules

- **Always follow** `.claude/research-os/02_RESEARCH_WORKFLOW.md` (26 stages)
- **Always follow** `.claude/research-os/13_ANTI_HALLUCINATION_RULES.md` (15 rules)
- **Do not write final paper prose** (Abstract, Introduction, Related Work, Method, Experiments, Conclusion, Limitations) before Stage 17 Evidence Freeze passes. Research notes, hypothesis notes, literature notes, experiment interpretation, TODO-based skeleton outlines, and all stage artifacts are allowed at any stage.
- **Do not write Related Work from memory** — always from paper-qa or a verified source
- **Do not claim novelty** before Stage 6 Prior-Art/SOTA Check passes
- **Do not claim performance** before Stage 16 Result Adequacy Gate passes
- **Do not target a venue** without defining venue-specific evidence requirements (Stage 9)
- **Experiments are for discovering what is true**, not proving the initial idea
- **If results contradict the initial hypothesis:** update `research_direction.md`, narrow claims, run `/pivot-decision`, or abandon — do not force the original story
- **Positive results alone are not sufficient** — evaluate venue fit, prior-art competition, and contribution defensibility before drafting
- **Use TODO markers instead of guessing:** `TODO_EVIDENCE_NEEDED:`, `TODO_RESULT_NEEDED:`, `TODO_CITATION_NEEDED:`, `TODO_NOVELTY_CHECK_NEEDED:`, `TODO_VENUE_FIT_NEEDED:`
- **Preserve** `\cite{}`, `\label{}`, `\ref{}`, `\eqref{}` during any prose revision — never alter citation keys while editing for style
- **Update** `project_state.md` after every meaningful session

### For Empirical Projects

Use the bounded autoresearch-style experiment loop (`/experiment-loop`, `20_AUTONOMOUS_EXPERIMENT_LOOP.md`) to produce traceable results before making any performance claims in the draft. Every experiment must be logged in `results.tsv` with a full commit hash before it can be cited in the paper.

### Paper-Specific Notes

See your project's `.claude/CLAUDE.md` for project-specific notes, including:
- LaTeX compiler path and version
- Citation format and bibliography style
- Column balance and figure width conventions
- Std formula (population vs. sample) for result tables

---

## The 26 Stages (Summary)

| Stage | Name | Key Output |
|-------|------|-----------|
| 0 | System Readiness | Tools verified, project structure created |
| 1 | Idea Intake | `paper_brief.md` |
| 2 | Problem Formulation | `hypothesis_registry.md` (initial entries) |
| 3 | Venue Targeting | `venue_target.md` |
| 4 | Initial Feasibility Check | `feasibility_report.md` |
| 5 | Literature Grounding | `literature_matrix.md`, paper-qa index |
| 6 | Prior-Art / SOTA Check | `prior_art_competition_table.md`, `sota_baseline_table.md`, `novelty_risk_report.md` |
| 7 | Gap and Positioning | `gap_statement.md` |
| 8 | Contribution Contract | `contribution_contract.md` |
| 9 | Target Result Contract | `target_result_contract.md` |
| 10 | Experiment Design | `experiment_matrix.md` |
| 11 | Baseline / Implementation Readiness | Baseline run confirmed |
| 12 | Exploratory Experiment Loop | `results.tsv` (exploratory rows) |
| 13 | Result Interpretation / Direction Update | `research_direction.md` updated |
| 14 | Confirmatory Experiment Planning | `experiment_plan.md` |
| 15 | Confirmatory Experiment Execution | `results.tsv` (confirmatory rows) |
| 16 | Result Adequacy Gate | `result_adequacy_report.md` |
| 17 | Evidence Freeze | `evidence_ledger.md`, `claim-evidence-table.md` |
| 18 | Paper Architecture | `paper_outline.md` |
| 19 | Section Drafting | Draft LaTeX sections |
| 20 | Figure and Table Design | TikZ / pgfplots figures |
| 21 | LaTeX Formatting | Compiled PDF |
| 22 | Multi-Agent Review | Review reports (P0/P1/P2) |
| 23 | Revision | Revised draft |
| 24 | Submission Preparation | Completed `09_SUBMISSION_CHECKLIST.md` |
| 25 | Archive | `archive/` directory |
