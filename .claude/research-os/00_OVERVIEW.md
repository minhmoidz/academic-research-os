# Claude Research Operating System — Overview

## What Is This?

The Claude Research Operating System (Research OS) is a persistent, reusable workflow framework that turns Claude Code into a rigorous research partner for ML/AI academic papers. It lives in `.claude/research-os/` and is activated at the start of every research session.

It does NOT replace your thinking. It enforces discipline on Claude's thinking.

---

## Core Principle

**Experiments are used to discover what is true, not to force the initial idea to be true.**

If evidence contradicts the initial hypothesis, Claude must update the research direction, narrow claims, pivot, change the venue target, or abandon the hypothesis. Claude must not bend the evidence to fit the original story.

**Positive results alone are not enough to write a paper.** Claude must also evaluate whether the result is strong enough for the target venue, whether prior work already did the same thing, and whether the contribution is defensible.

---

## What Problem Does It Solve?

Without this system, Claude will:
- Fabricate citations that sound plausible but don't exist
- Write Related Work from memory rather than from verified papers
- State results before experiments run
- Overclaim novelty without evidence
- Generate polished prose that hides logical gaps
- Force weak results into strong claims
- Forget workflow state between sessions
- Target ambitious venues without defining what results are needed

The Research OS prevents all of these by enforcing hard evidence gates, required artifacts at each stage, explicit TODO markers, and a fixed stage-gate order that no session can skip.

---

## Global Hard Gates

| Forbidden action | Required gate before allowed |
|-----------------|------------------------------|
| Write final paper prose | Stage 17 (Evidence Freeze) |
| Write Related Work from memory | Never |
| Claim novelty ("first", "novel") | Stage 6 (Prior-Art/SOTA Check) |
| Claim performance ("outperforms") | Stage 16 (Result Adequacy Gate) |
| Target a high-rank venue | Stage 9 (Target Result Contract) |
| Proceed to next stage | All required artifacts for current stage exist |

---

## How Sessions Should Start

At the start of every research session:
1. Read `12_SESSION_PROTOCOL.md` — 11-step session start protocol
2. Run `/research-status` — detect current project stage and blockers
3. Read `16_PROJECT_STATE.md` for format; read `project_state.md` in project root for current state
4. Confirm current stage, missing artifacts, and next safe action
5. Do not write content until this report is complete

---

## System Map

```
.claude/research-os/
├── 00_OVERVIEW.md              ← This file
├── 01_REPOSITORY_MAP.md        ← Tool catalog (available vs. missing)
├── 02_RESEARCH_WORKFLOW.md     ← Master 26-stage workflow
├── 03_IDEA_TO_PAPER_PLAYBOOK.md
├── 04_LITERATURE_REVIEW_PLAYBOOK.md
├── 05_EXPERIMENT_PLAYBOOK.md   ← Exploratory / diagnostic / confirmatory experiments
├── 06_WRITING_PLAYBOOK.md
├── 07_FIGURE_AND_FORMAT_PLAYBOOK.md
├── 08_REVIEW_AND_AUDIT_PLAYBOOK.md
├── 09_SUBMISSION_CHECKLIST.md
├── 10_TEMPLATES.md
├── 11_COMMANDS.md              ← All /commands reference
├── 12_SESSION_PROTOCOL.md      ← Session start/end protocol
├── 13_ANTI_HALLUCINATION_RULES.md
├── 14_CHANGELOG.md
├── 15_TOOL_HEALTHCHECK.md      ← Tool availability verification
├── 16_PROJECT_STATE.md         ← Persistent state file format
├── 17_DECISION_LOG.md          ← Append-only decision record
├── 18_EVIDENCE_LEDGER.md       ← EVID-* traceability system
├── 19_DRY_RUN_TEST.md          ← Compliance test protocol
├── 20_AUTONOMOUS_EXPERIMENT_LOOP.md
├── 21_EXPERIMENT_LOG_FORMAT.md
├── 22_HYPOTHESIS_REGISTRY.md   ← Pre-registered hypotheses
├── 23_RESEARCH_DIRECTION_UPDATE.md
├── 24_VENUE_TARGETING.md
├── 25_PRIOR_ART_COMPETITION.md
├── 26_TARGET_RESULT_CONTRACT.md
├── 27_RESULT_ADEQUACY_GATE.md
└── 28_PIVOT_POLICY.md

.claude/skills/
├── research-status/SKILL.md    ← /research-status
├── tool-healthcheck/SKILL.md   ← /tool-healthcheck
├── research-start/SKILL.md     ← /research-start
├── literature-review/SKILL.md  ← /literature-review
├── prior-art-check/SKILL.md    ← /prior-art-check
├── sota-check/SKILL.md         ← /sota-check
├── venue-target/SKILL.md       ← /venue-target
├── target-result-contract/SKILL.md
├── plan-experiments/SKILL.md   ← /plan-experiments
├── experiment-loop/SKILL.md    ← /experiment-loop
├── experiment-status/SKILL.md  ← /experiment-status
├── result-backfill/SKILL.md    ← /result-backfill
├── result-adequacy/SKILL.md    ← /result-adequacy
├── pivot-decision/SKILL.md     ← /pivot-decision
├── paper-draft/SKILL.md        ← /draft-section
├── paper-figure/SKILL.md       ← /design-figure
├── paper-format/SKILL.md       ← /format-paper
├── paper-review/SKILL.md       ← /review-paper
├── submission-audit/SKILL.md   ← /submission-check
└── archive-paper/SKILL.md      ← /archive-paper
```

---

## Workflow Summary (26 Stages)

| Stage | Name | Gate / Key output |
|-------|------|------------------|
| 0 | System Readiness | Tool healthcheck; project state loaded |
| 1 | Idea Intake | `paper_brief.md` |
| 2 | Problem Formulation | `hypothesis_registry.md` (HYP-001) |
| 3 | Venue Targeting | `venue_target.md`; minimum result defined |
| 4 | Initial Feasibility | Dataset + baseline + compute verified |
| 5 | Literature Grounding | `literature-matrix.md` via paper-qa |
| 6 | **Prior-Art/SOTA Check** | `novelty_risk_report.md`; threat ≤ Medium |
| 7 | Gap and Positioning | Gap validated via paper-qa |
| 8 | Contribution Contract | `contribution_contract.md`; all claims = hypotheses |
| 9 | **Target Result Contract** | `target_result_contract.md`; locked before experiments |
| 10 | Experiment Design | `experiment_matrix.md`; budget defined |
| 11 | Baseline/Implementation | Baselines confirmed runnable |
| 12 | Exploratory Loop | `results.tsv`; hypotheses tested |
| 13 | Research Direction Update | `research_direction.md`; evidence-based |
| 14 | Confirmatory Planning | Confirmatory matrix approved |
| 15 | Confirmatory Execution | All confirmatory runs logged |
| 16 | **Result Adequacy Gate** | `result_adequacy_report.md`; decision A–G |
| 17 | **Evidence Freeze** | `claim-evidence-table.md`; all claims traced |
| 18 | Paper Architecture | Outline + figure plan |
| 19 | Section Drafting | Draft `.tex` |
| 20 | Figure/Visual Design | TikZ + pgfplots |
| 21 | LaTeX Formatting | Compiled PDF |
| 22 | Multi-Agent Review | 12-pass review report |
| 23 | Revision and Re-Audit | P0 findings resolved |
| 24 | Submission Check | Checklist complete |
| 25 | Camera-Ready Archive | `archive/` directory |

Bold stages = hard gates that require explicit pass before advancing.

---

## Anti-Hallucination Summary

| Risk | Prevention mechanism |
|------|---------------------|
| Fake citations | paper-qa verifies claims; no `\cite{}` before bib key exists |
| Fake results | All numbers traced to result log files; `TODO_RESULT_NEEDED:` if missing |
| Fake baselines | Baseline table locked at Stage 10; no baseline added after |
| Overclaimed novelty | Stage 6 prior-art check required before any novelty claim |
| Result claims before experiments | Stage 16 gate required before performance claims |
| Forced narrative | Stage 13 direction update mandatory when hypotheses are contradicted |
| Session amnesia | `project_state.md` + `12_SESSION_PROTOCOL.md` restore full state |
| Venue overconfidence | `target_result_contract.md` defines venue-specific thresholds before experiments |

See `13_ANTI_HALLUCINATION_RULES.md` for all 13 rules.
