# Research OS Changelog

Track changes to the Research OS system itself (not the paper). Every change to any file in `.claude/research-os/` or `.claude/skills/` should be logged here.

---

## Format

```
## [Date] — [Short description]

### Changed
- `filename.md` § Section — [what changed and why]

### Added
- `filename.md` — [new file, purpose]

### Removed
- `filename.md` — [why removed]

### Fixed
- `filename.md` — [bug or error fixed]
```

---

## [2026-05-24] — Initial creation

### Added
- `00_OVERVIEW.md` — System overview, core principle, phase table, hallucination prevention
- `01_REPOSITORY_MAP.md` — Catalog of all available tools: academic-writing-agents (12 agents), paper-qa, 11 native skills; records which external tools are NOT available
- `02_RESEARCH_WORKFLOW.md` — Full 15-phase evidence-first research workflow with gates
- `03_IDEA_TO_PAPER_PLAYBOOK.md` — Idea-to-plan process: 8 clarification questions, hypothesis template, contribution map, overclaiming risk checklist
- `04_LITERATURE_REVIEW_PLAYBOOK.md` — Literature collection using paper-qa, matrix building, gap statement validation
- `05_EXPERIMENT_PLAYBOOK.md` — Experiment matrix, baseline verification, result file linking, reproducibility checklist
- `06_WRITING_PLAYBOOK.md` — Section-by-section writing guidance with allowed claims, forbidden patterns, revision checklists
- `07_FIGURE_AND_FORMAT_PLAYBOOK.md` — TikZ figures, pgfplots charts, LaTeX compilation, column balance
- `08_REVIEW_AND_AUDIT_PLAYBOOK.md` — 10 review passes with tools, severity levels, and fix strategies
- `09_SUBMISSION_CHECKLIST.md` — 8-section pre-submission checklist with 50+ verification items
- `10_TEMPLATES.md` — 11 reusable templates (Paper Brief through Final Audit Report)
- `11_COMMANDS.md` — 12 invocable commands (/research-start through /submission-check)
- `12_SESSION_PROTOCOL.md` — Session start/end protocol, research-state.md format
- `13_ANTI_HALLUCINATION_RULES.md` — 10 strict rules preventing fabricated citations, results, datasets, and baselines
- `14_CHANGELOG.md` — This file

### Added (Skills)
- `.claude/skills/research-start/SKILL.md` — /research-start skill
- `.claude/skills/literature-review/SKILL.md` — /literature-review skill
- `.claude/skills/paper-draft/SKILL.md` — /draft-section skill
- `.claude/skills/paper-review/SKILL.md` — /review-paper skill
- `.claude/skills/paper-format/SKILL.md` — /format-paper skill
- `.claude/skills/paper-figure/SKILL.md` — /design-figure skill
- `.claude/skills/submission-audit/SKILL.md` — /submission-check skill

### Context
- Created for Gmmamba_ours project (AHGR paper for IEEE conference)
- Tools available: academic-writing-agents plugin (12 agents), paper-qa, 11 native skills
- Tools NOT available: latex-paper-skills, claude-paper-review, AI-research-feedback, paper-audit
- Tectonic compiler at `/opt/anaconda3/bin/tectonic` (not system pdflatex)

---

## [2026-05-24] — autoresearch integration (karpathy/autoresearch)

### Added
- `18_EVIDENCE_LEDGER.md` — Evidence ID system (`EV-EXP-N`, `EV-LIT-N`, `EV-DATA-N`, `EV-REPO-N`); two-hop chain from results.tsv → ledger → claim-evidence table → paper.tex
- `20_AUTONOMOUS_EXPERIMENT_LOOP.md` — Bounded experiment loop adapted from karpathy/autoresearch. Preserves: fixed harness, one editable file, git branch isolation, TSV logging, keep/discard on metric, simplicity criterion, crash handling. Adds: hard budget, user-defined metric, pre-registered hypotheses, evidence artifact updates, paper-claim gate
- `21_EXPERIMENT_LOG_FORMAT.md` — Exact format spec for results.tsv, experiment_notes.md, failed_runs.md, best_result.md, result_to_claim_map.md; file-relationship diagram; validation shell commands
- `.claude/skills/experiment-loop/SKILL.md` — `/experiment-loop` skill; bounded loop with 5-step pre-flight, 8-step main loop (hypothesis → modify → commit → run → parse → log → keep/discard → artifact update), completion report

### Changed
- `02_RESEARCH_WORKFLOW.md` § Phase 7A — Inserted new phase between Phase 7 (Experiment Planning) and Phase 8 (Evidence Tracking); skippable for non-empirical projects
- `05_EXPERIMENT_PLAYBOOK.md` § Step 10 — Added bounded loop reference table, results.tsv format snippet, evidence output requirements, invocation pointer
- `11_COMMANDS.md` — Added `/experiment-loop`, `/experiment-status`, `/result-backfill` with full purpose/inputs/outputs/safety rules
- `13_ANTI_HALLUCINATION_RULES.md` — Added Rule 11 (claims must come from logged result files), Rule 12 (result logs must have all four fields), Rule 13 (paper claims cannot cite unlogged experiments); includes forbidden-pattern / correct-pattern examples and a claim-chain diagram
- `CLAUDE.md` — Added one sentence directing empirical projects to use `/experiment-loop` before making performance claims

### Context
- Source repo: https://github.com/karpathy/autoresearch (master branch, inspected 2026-05-24)
- Key files inspected: README.md, program.md, prepare.py, train.py, pyproject.toml
- autoresearch runs unbounded until interrupted — our adaptation adds hard budget and evidence traceability
- autoresearch uses val_bpb on language modeling — our adaptation uses user-defined metric and direction

---

## [2026-05-24] — Major overhaul: 26-stage workflow, 4 hard gates, 24 commands, 15 anti-hallucination rules

### Changed

- `00_OVERVIEW.md` — Complete rewrite: 26-stage workflow overview, system map with all 28 research-os files and 20 skills, 4 hard gates table, anti-hallucination summary, core principle prominently stated ("Experiments are for discovering what is true, not proving the initial idea")
- `01_REPOSITORY_MAP.md` — Complete rewrite: 13 tools catalogued (academic-writing-agents ✓, paper-qa ✓, 5 native skills ~, 5 MISSING repos with install commands, autoresearch patterns integrated); Quick-reference table added
- `02_RESEARCH_WORKFLOW.md` — Complete rewrite from 15-phase to 26-stage workflow. Each stage now has: goal, required inputs/outputs, skills/tools, pass criteria, fail conditions, forbidden actions, next allowed stage. Global hard gates table. Stage-to-artifact map. Pivot/return paths table.
- `05_EXPERIMENT_PLAYBOOK.md` — Added "Three Experiment Types" section: Exploratory (discover), Diagnostic (explain), Confirmatory (support claims); 6-type outcome classification; KEEP/REFINE/DIAGNOSE/PIVOT/ABANDON/HOLD decision schema
- `11_COMMANDS.md` — Complete rewrite: 24 commands in 6 groups (Navigation, Research Setup, Literature, Experiments, Paper Writing, Review/Submission). Each command has purpose/stage/skill/inputs/outputs/forbidden behavior.
- `12_SESSION_PROTOCOL.md` — Expanded to 11-step session start protocol; clear status report template; "during session" protocols for prose writing, editing, hypothesis contradiction, and results; session end steps
- `13_ANTI_HALLUCINATION_RULES.md` — Added Rule 14 (forbidden unsupported phrases: state-of-the-art, first, novel, outperforms, guarantees, etc.) and Rule 15 (5 new TODO markers); updated Self-Check to 8 questions
- `.claude/CLAUDE.md` — Complete rewrite of Academic Research OS section: 26-stage workflow, 15 non-negotiable rules, venue-targeting gates, experiment philosophy, paper-specific notes

### Added (Research OS files)

- `15_TOOL_HEALTHCHECK.md` — Stage 0 system readiness; tests pqa, tectonic (live compile), git, python3, pytorch/CUDA, 7 ML dependencies, academic-writing-agents; marks native Claude skills as "assumed available"; tool_healthcheck_report.md template; stage-gating rules
- `16_PROJECT_STATE.md` — project_state.md template with 16 field groups (project identity, current stage, hypothesis, research direction, completed stages, artifacts, blockers, TODO count, hypothesis registry, active experiments, current best result, evidence status, writing/figure/review status, gate status, next safe action, decision summary); realistic filled-in example for MIL project
- `17_DECISION_LOG.md` — DEC-YYYY-MM-DD-NNN format; 12 decision categories; append-only rules; 10 required fields per entry; 3 worked examples (pivot after weak results, venue downgrade, claim narrowing)
- `19_DRY_RUN_TEST.md` — Compliance test using vague transformer efficiency idea; expected correct behaviors for Stages 0-9; 8 named FAIL behaviors; 8 automatic-fail conditions; 10-item compliance checklist
- `22_HYPOTHESIS_REGISTRY.md` — HYP-NNN format; status state machine (pending→testing→{supported/partially_supported/contradicted/inconclusive}); 3 worked examples from MIL project
- `23_RESEARCH_DIRECTION_UPDATE.md` — 7-step update protocol; research_direction.md template with version history; 5 common direction update patterns; forbidden actions
- `24_VENUE_TARGETING.md` — 6-tier classification (NeurIPS/ICML → thesis); evidence requirements per tier; venue_target.md template; MICCAI vs ISBI comparison example; hard rules
- `25_PRIOR_ART_COMPETITION.md` — prior_art_competition_table.md (threat levels Low/Medium/High/Critical), sota_baseline_table.md, novelty_risk_report.md templates; decision tree; 12-month lag handling for recent papers
- `26_TARGET_RESULT_CONTRACT.md` — Binding pre-experiment agreement template; contract_id, all required fields, MIL/TCGA example with specific thresholds (>0.920 AUC, <1.0pp std); TRC lifecycle; modification protocol (requires DEC entry)
- `27_RESULT_ADEQUACY_GATE.md` — Stage 16 gate; 6 evaluation conditions; decisions A-G with precise trigger conditions; result_adequacy_report.md template; hard prohibition on prose before Decision A
- `28_PIVOT_POLICY.md` — 9 decisions (PROCEED through ABANDON); 5 forbidden pivot types; 6 concrete case studies; 10-step pivot execution protocol; DEC log format for each pivot type

### Added (Skills)

- `.claude/skills/research-status/SKILL.md` — /research-status: reads project_state.md, hypothesis_registry.md, results.tsv, evidence_ledger.md; greps TODOs; checks 16 artifact files; structured console report
- `.claude/skills/tool-healthcheck/SKILL.md` — /tool-healthcheck: tests pqa, tectonic (live compile), git, python3, pytorch/CUDA, ML deps, academic-writing-agents; install commands for 5 missing repos
- `.claude/skills/prior-art-check/SKILL.md` — /prior-art-check: 9-step paper-qa search; prior_art_competition_table.md with threat levels; hard-stop on Critical threats
- `.claude/skills/sota-check/SKILL.md` — /sota-check: paper-qa best-result queries; sota_baseline_table.md; gap computation
- `.claude/skills/venue-target/SKILL.md` — /venue-target: tier evaluation; venue_target.md; decision log entry
- `.claude/skills/target-result-contract/SKILL.md` — /target-result-contract: binding thresholds before confirmatory experiments; user sign-off required
- `.claude/skills/plan-experiments/SKILL.md` — /plan-experiments: full experiment matrix (exploratory/diagnostic/confirmatory); protected files; budget
- `.claude/skills/experiment-status/SKILL.md` — /experiment-status: read-only diagnostic; run counts by status; best result; hypothesis and budget status
- `.claude/skills/result-backfill/SKILL.md` — /result-backfill: scans result directories; EVID-EXP-NNN entries; claim-evidence table
- `.claude/skills/result-adequacy/SKILL.md` — /result-adequacy: Stage 16 gate; TRC compliance + SOTA gap + ablation + stability; Decision A-G
- `.claude/skills/pivot-decision/SKILL.md` — /pivot-decision: 9-decision pivot; all logged to decision_log.md; forbidden pivots named
- `.claude/skills/archive-paper/SKILL.md` — /archive-paper: post-submission archive; source, figures, results, configs, git hashes; README_ARCHIVE.md

### Context

- This overhaul makes the Research OS a general-purpose, reusable system — not project-specific
- Core principle enforced throughout: experiments discover truth, not confirm the initial idea
- All 15 anti-hallucination rules now cover citations, baselines, datasets, results, metrics, novelty, related work, revision, TODO markers, logged experiments, result log completeness, claim chain, forbidden phrases, and new TODO types
- 4 hard gates: Stage 6 (Prior-Art/SOTA), Stage 9 (Target Result Contract), Stage 16 (Result Adequacy), Stage 17 (Evidence Freeze)
- No paper prose was generated during this session

---

## [2026-05-24] — Three targeted fixes: /verify-research-os, prose/notes distinction, autoresearch clone note

### Added

- `15_TOOL_HEALTHCHECK.md` was already present. New: `.claude/skills/verify-research-os/SKILL.md` — `/verify-research-os` command; checks 29 research-os files, 21 skill files, CLAUDE.md gate references, project_state.md currency, and quick tool availability; PASS/WARN/FAIL report; never modifies files

### Changed

- `11_COMMANDS.md` § Navigation Commands — Added `/verify-research-os` entry with distinction from `/tool-healthcheck` (OS file integrity vs. binary tool availability)
- `02_RESEARCH_WORKFLOW.md` § Global Hard Gates — Clarified row 1: "Write final paper prose" now lists exactly which sections are prohibited; added explicit "Before Stage 17, Claude MAY write" block (research notes, hypothesis notes, literature notes, experiment interpretation, TODO-based outlines, stage artifacts); added worked example of final prose vs. research note
- `12_SESSION_PROTOCOL.md` § Rules for Session Continuity — Rule 3 expanded: defines "final paper prose" precisely and explicitly permits research notes, hypothesis notes, literature notes, rough outlines, and stage artifacts before Stage 17
- `01_REPOSITORY_MAP.md` § Tool 13 autoresearch — Added optional clone command with note that patterns are already integrated; clone only needed for reading the original source during real auto-loop sessions
- `.claude/CLAUDE.md` § Core Operating Rules — Rule "Do not write paper prose" expanded to define what is prohibited vs. what is allowed before Evidence Freeze

### Why

Without the prose/notes distinction, Claude could become overly cautious and refuse to write useful pre-freeze artifacts (outlines, notes, interpretation). The gate governs final submission prose only — not working documents.

---

## [2026-05-25] — Autonomous Research Pipeline: Gap Scout, Dialectical Validation, Proxy Protocol, Hypothesis Tournament, Project Profile

### Added (Research OS files)

- `29_GAP_SCOUT_PROTOCOL.md` — Stage 0.5 (optional): 5-step literature-driven gap discovery when user has no idea; 5 gap types (Unexplored Combination, Contradictory Results, Missing Baseline, Efficiency Gap, Generalization Gap); pqa query templates; gap_scout_report.md output format; human checkpoint before hypothesis registration
- `30_DIALECTICAL_VALIDATION.md` — Stage 1.5 (required before any experiment): 3-step Structured Controversy Protocol; Step 1 constructive subagent (mechanism/pathway/prior_evidence/prediction/falsification); Step 2 adversarial subagent (independent/blind — prior_failure/condition_violation/alternative_explanation); Step 3 adjudication scoring 0-10; gate ≥6 AND no fatal_flaw; dialectical_validation.md output; updates hypothesis_registry.md fields
- `31_PROXY_EXPERIMENT_PROTOCOL.md` — Stage 11.5 (required before full experiments): proxy_fraction × full_run_time budget; kill signals (NaN, below-threshold, early unhealthy); PROXY_PASS/KILL/NAN/FAIL statuses; compute savings table; updates results.tsv with proxy prefix
- `32_HYPOTHESIS_TOURNAMENT.md` — Successive Halving algorithm for multiple hypothesis candidates; Round 0 proxy (all candidates) → Round 1 1-fold (survivors) → Round 2 3-fold → Full K-fold winner; 57%+ compute saved vs. naive testing; tournament_bracket.md format; human checkpoint after Round 0
- `33_PROJECT_PROFILE_SPEC.md` — Universal adapter between Research OS and project code; Fundamental Research Equation (X/Y/Z/D/Δ); Universal Experiment Interface (3 shell commands: train_command, eval_command, metric_extract); 7 field groups; 5 complete paradigm examples (Supervised/Retrieval/RL/Generative/Self-supervised); OS usage table; common errors table

### Added (Skills)

- `.claude/skills/gap-scout/SKILL.md` — `/gap-scout`: pqa literature queries per gap type; gap_scout_report.md with 3-5 ranked candidates; human checkpoint before hypothesis registration; anti-hallucination rules (no invented gaps)
- `.claude/skills/validate-hypothesis/SKILL.md` — `/validate-hypothesis`: launches brainstormer (constructive) + research-analyst (adversarial, blind); adjudication 0-10; APPROVED/REJECTED/REVISE; updates hypothesis_registry.md dialectical fields; gate enforcement
- `.claude/skills/proxy-run/SKILL.md` — `/proxy-run`: reads project_profile.md experiment interface; substitutes {config}/{out_dir}; runs with --proxy flag; parses metric_extract float; applies kill signals; writes PROXY_PASS/KILL/NAN/FAIL to results.tsv and hypothesis_registry.md
- `.claude/skills/hypothesis-tournament/SKILL.md` — `/hypothesis-tournament`: Successive Halving; runs proxy for all candidates; scores and ranks; eliminates bottom half; advances survivors to Round 1/2/Full; tournament_bracket.md; human checkpoint after Round 0

### Added (Templates)

- `templates/project_profile.template.md` — Fill-in template for project_profile.md; all 7 field groups with inline comments and paradigm guidance; warning: fill before Stage 0 experiments
- `templates/dialectical_validation.template.md` — Template for dialectical_validation.md output; constructive + adversarial + adjudication sections; score + decision
- `templates/gap_scout_report.template.md` — Template for gap_scout_report.md; per-gap-type sections; ranked candidates table; human checkpoint decision

### Changed

- `02_RESEARCH_WORKFLOW.md` — Added Stage 0.5 (Gap Scout), Stage 1.5 (Dialectical Validation), Stage 11.5 (Proxy Protocol) with full goal/inputs/outputs/pass criteria/forbidden actions; added hard gate rows for both new gates; updated stage-to-artifact map
- `11_COMMANDS.md` — Added 5 commands: /gap-scout, /validate-hypothesis, /proxy-run, /hypothesis-tournament, /auto-research; updated quick reference; updated new project flow
- `22_HYPOTHESIS_REGISTRY.md` — Added 6 new fields: dialectical_score (0-10), validation_status (PENDING/APPROVED/REJECTED/REVISE), proxy_status (NOT_RUN/PROXY_PASS/PROXY_KILL/PROXY_NAN/PROXY_FAIL), proxy_metric (float), tournament_round (null/0/1/2/WINNER/ELIMINATED), max_gpu_hours (float)
- `scripts/new-project.sh` — Added automatic creation of project_profile.md from template during project initialization

### Why

The previous OS required user to have a research idea before starting. The upgrade adds:
1. Autonomous gap discovery (literature-driven, not hallucinated) — 5 gap types with pqa evidence
2. Argument-first gate (dialectical validation before ANY experiment) — prevents expensive dead-end runs
3. Proxy runs (25% budget) before committing full compute — saves 75% if hypothesis fails early
4. Tournament-style hypothesis selection (Successive Halving) — logarithmic vs. linear cost for N candidates
5. Universal project adapter (project_profile.md) — makes OS work for any AI paradigm without code changes

---

## [Template for future entries]

```
## [YYYY-MM-DD] — [Short description]

### Changed
- `file.md` § [Section name] — [what changed, why]

### Fixed
- `file.md` — [what was wrong, what the fix is]
```
