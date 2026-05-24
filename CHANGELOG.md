# Changelog

All notable changes to Academic Research OS are documented here.

This format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

(Changes not yet in a release will appear here.)

---

## [1.0.0] — 2026-05-24

### Added

- Initial public release of Academic Research OS for Claude Code
- 26-stage evidence-first research workflow (`02_RESEARCH_WORKFLOW.md`)
- 4 hard gates enforcing evidence discipline at key research checkpoints:
  - Gate 1: Prior-Art / SOTA Check (Stage 6)
  - Gate 2: Target Result Contract (Stage 9)
  - Gate 3: Result Adequacy Gate (Stage 16)
  - Gate 4: Evidence Freeze (Stage 17)
- 24 commands via 21 skill files covering the full research lifecycle
- 29 Research OS workflow files (00_OVERVIEW through 28_PIVOT_POLICY)
- 11 documentation files in `docs/`
- 17 artifact templates in `templates/`
- 3 setup scripts in `scripts/` (new-project.sh, install.sh, verify.sh)
- Bounded experiment loop adapted from autoresearch patterns (`20_AUTONOMOUS_EXPERIMENT_LOOP.md`)
- 15 anti-hallucination rules enforced at every stage (`13_ANTI_HALLUCINATION_RULES.md`)
- Multi-agent review system via academic-writing-agents plugin (`08_REVIEW_AND_AUDIT_PLAYBOOK.md`)
- Decision log protocol for append-only research decision tracking (`17_DECISION_LOG.md`)
- Hypothesis registry with pre-registration and status transitions (`22_HYPOTHESIS_REGISTRY.md`)
- Evidence ledger linking experiment runs to paper claims (`18_EVIDENCE_LEDGER.md`)
- Target Result Contract with binding pass/fail criteria (`26_TARGET_RESULT_CONTRACT.md`)
- Result Adequacy Report with 7-decision framework (`27_RESULT_ADEQUACY_GATE.md`)
- Research direction update protocol for handling contradicted hypotheses (`23_RESEARCH_DIRECTION_UPDATE.md`)
- Prior-art competition table and novelty risk report templates (`25_PRIOR_ART_COMPETITION.md`)
- Toy example project demonstrating the workflow end-to-end (`examples/toy-research-project/`)
- Root-level CLAUDE.md and .claude/CLAUDE.md for Claude Code integration
- MIT License

### Design Principles

- No paper prose may be written before Stage 17 Evidence Freeze
- No novelty claim may be made before Stage 6 Prior-Art Check passes
- No performance claim may be made before Stage 16 Result Adequacy Gate passes
- All TODO markers (`TODO_EVIDENCE_NEEDED:`, `TODO_RESULT_NEEDED:`, etc.) must be resolved before submission
- Every quantitative claim must trace to a logged experiment row in `results.tsv`
- All citations must correspond to verified entries in `references.bib`
