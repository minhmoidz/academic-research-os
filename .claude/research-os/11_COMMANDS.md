# Research OS Command Reference

All commands are invocable via the Skill tool or by typing the command in Claude Code.
For full details on each command, see the corresponding SKILL.md file.

---

## Navigation Commands

### /research-status

**Purpose:** Report current project stage, artifacts, blockers, and next safe action.  
**Stage:** Any (run at session start)  
**Skill:** `.claude/skills/research-status/SKILL.md`  
**Required inputs:** Project directory (reads `project_state.md`)  
**Expected output:** Status report (stage, artifacts, TODOs, gate, next action)  
**Forbidden:** Never generates paper prose; never modifies files

---

### /tool-healthcheck

**Purpose:** Verify that all Research OS tools are actually available and usable.  
**Stage:** Stage 0  
**Skill:** `.claude/skills/tool-healthcheck/SKILL.md`  
**Required inputs:** Project directory  
**Expected output:** Working/Missing tool report + install commands for missing tools  
**Forbidden:** Never uses a tool marked Missing for a required stage

---

### /verify-research-os

**Purpose:** Verify that the entire Research OS infrastructure is intact — all 29 research-os files, all 21 skill files, CLAUDE.md gate references, project state currency, and quick tool availability.  
**Stage:** Any (run after git pull, new machine setup, long session gap, or when `/research-status` returns unexpected results)  
**Skill:** `.claude/skills/verify-research-os/SKILL.md`  
**Required inputs:** Project directory (`.claude/` folder)  
**Expected output:** Integrity report (PASS / WARN / FAIL) per category, list of missing files, next recommended action  
**Forbidden:** Never modifies files; never generates paper prose; never runs experiments  
**Difference from `/tool-healthcheck`:** `/tool-healthcheck` tests binary tool availability (pqa runs, tectonic compiles). `/verify-research-os` tests OS infrastructure integrity (all workflow files present, all skill files present, CLAUDE.md correctly wired, project state not stale).

---

### /gap-scout

**Purpose:** Autonomously discover research gaps from literature and propose 3-5 hypothesis candidates when the user has no idea.  
**Stage:** 0.5 (before Stage 1 — run when user has no idea)  
**Skill:** `.claude/skills/gap-scout/SKILL.md`  
**Required inputs:** paper-qa index path, rough area of interest (or "open")  
**Expected output:** `gap_scout_report.md` with ranked candidates, top 3 presented to user  
**Forbidden:** Never invent gaps without pqa evidence; never register hypotheses without user confirmation

---

### /validate-hypothesis

**Purpose:** Run dialectical validation on a hypothesis — constructive argument, adversarial critique, adjudication score. Gate before any experiment.  
**Stage:** 1.5 (after Stage 1 Hypothesis Registration, before Stage 2 Direction Lock)  
**Skill:** `.claude/skills/validate-hypothesis/SKILL.md`  
**Required inputs:** HYP-NNN from hypothesis_registry.md, project_profile.md (for paradigm context), paper-qa index  
**Expected output:** `dialectical_validation.md` with score 0-10 and decision APPROVED/REJECTED/REVISE  
**Forbidden:** Never approve hypothesis with fatal_flaw = YES; never skip adversarial phase; never run constructive and adversarial in same subagent call

---

### /proxy-run

**Purpose:** Run a cheap proxy experiment (proxy_fraction × full run) before committing full compute budget.  
**Stage:** 11.5 (before Stage 12 Exploratory Experiments)  
**Skill:** `.claude/skills/proxy-run/SKILL.md`  
**Required inputs:** HYP-NNN (validation_status = APPROVED), project_profile.md, config file path, git clean  
**Expected output:** results.tsv row (PROXY_PASS / PROXY_KILL / PROXY_NAN / PROXY_FAIL) + recommendation  
**Forbidden:** Never skip proxy and go straight to full run; never modify protected files; never retry PROXY_KILL with same config

---

### /hypothesis-tournament

**Purpose:** Compare multiple APPROVED hypothesis candidates via Successive Halving: proxy → 1-fold → 3-fold → full K-fold. Eliminates weak candidates cheaply.  
**Stage:** 11.5 (when ≥ 3 APPROVED candidates exist)  
**Skill:** `.claude/skills/hypothesis-tournament/SKILL.md`  
**Required inputs:** List of HYP-NNN IDs (all APPROVED), project_profile.md, git clean  
**Expected output:** Tournament results (all rounds logged to results.tsv), winner declared, confirmatory run scheduled  
**Forbidden:** Change config between rounds; different folds for different candidates in same round; skip Human Checkpoint before starting

---

### /auto-research

**Purpose:** Run the full semi-autonomous research pipeline: gap-scout → validate → proxy-tournament → confirmatory → evidence → draft.  
**Stage:** 0 → 19 (full pipeline, 3 human checkpoints)  
**Required inputs:** project_profile.md (filled), paper-qa index, compute budget confirmation  
**Expected output:** Complete research artifacts from gap_scout_report.md through paper draft  
**Human Checkpoints:**  
  1. After /gap-scout: user selects direction  
  2. After proxy tournament: user reviews results, approves confirmatory  
  3. After Result Adequacy Gate: user approves paper writing  
**Forbidden:** Skip any human checkpoint; write paper prose before Evidence Freeze; run confirmatory without PROXY_PASS

---

### /resume-research-session

**Purpose:** Resume a research session by restoring full project context.  
**Stage:** Any (run at start of every session on existing project)  
**Invocation prompt:**
```
Read .claude/research-os/12_SESSION_PROTOCOL.md.
Run the 11-step session start protocol.
Read project_state.md and report: current stage, completed artifacts,
missing artifacts, active blockers, current gate, next safe action.
Do not write any content until I confirm the next step.
```

---

## Research Setup Commands

### /research-start

**Purpose:** Initialize a new research project with paper brief, hypothesis registry, and project state.  
**Stage:** Stage 1  
**Skill:** `.claude/skills/research-start/SKILL.md`  
**Required inputs:** Working title, raw idea description  
**Expected output:** `paper_brief.md`, `project_state.md` (Stage 1), `hypothesis_registry.md` (empty)  
**Forbidden:** No paper prose; no citations; no results

---

### /venue-target

**Purpose:** Select target venue, define venue-tier evidence requirements, create `venue_target.md`.  
**Stage:** Stage 3  
**Skill:** `.claude/skills/venue-target/SKILL.md`  
**Required inputs:** Paper type, current results (if any), candidate venues  
**Expected output:** `venue_target.md` + `decision_log.md` entry  
**Forbidden:** Never assumes Tier-1 without evidence; never skips minimum result definition

---

### /build-contribution-map

**Purpose:** Create `contribution_contract.md` mapping each contribution claim to a hypothesis ID and evidence pointer.  
**Stage:** Stage 8  
**Tools:** `03_IDEA_TO_PAPER_PLAYBOOK.md`, `10_TEMPLATES.md` (Template 5)  
**Required inputs:** `venue_target.md`, `hypothesis_registry.md`, gap statement  
**Expected output:** `contribution_contract.md` with all claims = hypotheses, not confirmed facts  
**Forbidden:** No claim marked [CONFIRMED] without evidence ID

---

### /target-result-contract

**Purpose:** Define binding minimum result requirements BEFORE confirmatory experiments.  
**Stage:** Stage 9  
**Skill:** `.claude/skills/target-result-contract/SKILL.md`  
**Required inputs:** `venue_target.md`, `contribution_contract.md`, `sota_baseline_table.md`  
**Expected output:** `target_result_contract.md` (signed off by user)  
**Forbidden:** Cannot be created after confirmatory experiments; cannot lower bar after seeing results

---

## Literature Commands

### /literature-review

**Purpose:** Build paper-qa index and literature matrix from local PDFs.  
**Stage:** Stage 5  
**Skill:** `.claude/skills/literature-review/SKILL.md`  
**Required inputs:** Keywords, PDF folder path  
**Expected output:** `literature-matrix.md` (cells from paper-qa only), `literature_list.md`  
**Forbidden:** No Related Work prose; no citation from memory

---

### /prior-art-check

**Purpose:** Assess whether prior work already addresses the proposed contribution.  
**Stage:** Stage 6  
**Skill:** `.claude/skills/prior-art-check/SKILL.md`  
**Required inputs:** Research question, keywords, paper-qa index (if available)  
**Expected output:** `prior_art_competition_table.md` + `novelty_risk_report.md`  
**Forbidden:** No novelty claim before this passes; unknown cells marked TODO

---

### /sota-check

**Purpose:** Identify best known results on target datasets to set the performance bar.  
**Stage:** Stage 6  
**Skill:** `.claude/skills/sota-check/SKILL.md`  
**Required inputs:** Target task, dataset(s), primary metric  
**Expected output:** `sota_baseline_table.md` (values from paper-qa or user-provided, never from memory)  
**Forbidden:** Never fill SOTA values from memory; never claim "achieves SOTA" without this table

---

## Experiment Commands

### /plan-experiments

**Purpose:** Design the full experiment matrix before running anything.  
**Stage:** Stage 10  
**Skill:** `.claude/skills/plan-experiments/SKILL.md`  
**Required inputs:** `contribution_contract.md`, `target_result_contract.md`, `hypothesis_registry.md`  
**Expected output:** `experiment_matrix.md` with exploratory, diagnostic, and confirmatory experiments  
**Forbidden:** No confirmatory experiments before this plan is approved

---

### /experiment-loop

**Purpose:** Run a bounded, autoresearch-style experiment loop. Evidence producer only — never writes prose.  
**Stage:** Stages 12, 15  
**Skill:** `.claude/skills/experiment-loop/SKILL.md`  
**Required inputs:** `experiment-plan.md` (objective, editable files, protected files, metric, budget)  
**Expected output:** `results.tsv`, `experiment_notes.md`, `failed_runs.md`, `best_result.md`, `evidence_ledger.md`  
**Forbidden:** Modify protected files; invent results; write prose; skip baseline; run on main branch  
**Invocation prompt:**
```
Read .claude/research-os/20_AUTONOMOUS_EXPERIMENT_LOOP.md and 13_ANTI_HALLUCINATION_RULES.md.
Read experiment-plan.md, experiment_matrix.md, evidence_ledger.md, results.tsv.
Run a bounded experiment loop with budget [N].
Baseline first. Log every run. Never modify protected files.
```

---

### /experiment-status

**Purpose:** Report current state of all experiments without running anything.  
**Stage:** Any (during or after experiment phases)  
**Skill:** `.claude/skills/experiment-status/SKILL.md`  
**Required inputs:** Project directory  
**Expected output:** Status report (total runs, best result, budget used, hypothesis status)  
**Forbidden:** Never generates results from memory; never runs experiments

---

### /result-backfill

**Purpose:** Backfill `evidence_ledger.md` and `claim-evidence-table.md` from existing result files.  
**Stage:** Stage 17  
**Skill:** `.claude/skills/result-backfill/SKILL.md`  
**Required inputs:** Result files directory, list of paper claims  
**Expected output:** Updated `evidence_ledger.md` + `claim-evidence-table.md`  
**Forbidden:** No ledger entries from memory; no EVID entries for FAIL/CRASH runs

---

### /result-adequacy

**Purpose:** Stage 16 gate — evaluate whether results are strong enough for the target venue.  
**Stage:** Stage 16  
**Skill:** `.claude/skills/result-adequacy/SKILL.md`  
**Required inputs:** `results.tsv`, `target_result_contract.md`, `sota_baseline_table.md`, `venue_target.md`  
**Expected output:** `result_adequacy_report.md` with decision A/B/C/D/E/F/G  
**Forbidden:** Cannot pass gate with negative gap_over_prior when claiming "outperforms"; cannot weaken TRC retroactively

---

### /pivot-decision

**Purpose:** Generate a structured pivot decision when results don't support the original hypothesis.  
**Stage:** After Stage 13, 16, or any time a hypothesis is CONTRADICTED  
**Skill:** `.claude/skills/pivot-decision/SKILL.md`  
**Required inputs:** `result_adequacy_report.md` or `hypothesis_registry.md` contradiction  
**Expected output:** Pivot recommendation (1 of 9 decisions) + `decision_log.md` entry + updated `research_direction.md`  
**Forbidden:** Never recommends PROCEED when TRC not met; never conceals negative results

---

## Paper Writing Commands

### /create-paper-outline

**Purpose:** Create the paper section skeleton before any prose is written.  
**Stage:** Stage 18  
**Tools:** `academic-writing-agents:section-drafter`, `06_WRITING_PLAYBOOK.md`  
**Required inputs:** `contribution_contract.md`, `claim-evidence-table.md`, `venue_target.md`  
**Expected output:** Section list, figure plan, table plan, page/word budget  
**Forbidden:** No prose during architecture; no LaTeX content before outline approved

---

### /draft-section [section-name]

**Purpose:** Draft a specific paper section using verified evidence only.  
**Stage:** Stage 19  
**Skill:** `.claude/skills/paper-draft/SKILL.md`  
**Required inputs:** Section name, `claim-evidence-table.md` rows for that section, literature matrix rows  
**Expected output:** Draft LaTeX for the section with proper citations and equation references  
**Forbidden:** No Related Work from memory; no `\cite{key}` without bib key; no results without EVID  
**Section order:** Method → Experiments → Analysis → Related Work → Introduction → Conclusion → Limitations → Abstract  
**Invocation prompt:**
```
Read .claude/research-os/06_WRITING_PLAYBOOK.md (section for [section name])
and .claude/research-os/13_ANTI_HALLUCINATION_RULES.md.
Draft [section name] using:
- Evidence: [relevant claim-evidence-table rows]
- Literature: [relevant literature-matrix rows]
Mark any missing evidence as TODO_*.
```

---

### /design-figure [description]

**Purpose:** Create a figure or diagram for the paper.  
**Stage:** Stage 20  
**Skill:** `.claude/skills/paper-figure/SKILL.md`  
**Required inputs:** Figure description, data source (result file), column constraint  
**Expected output:** TikZ code or pgfplots chart  
**Forbidden:** Data values must match result files exactly; no hardcoded hyperparameter formulas

---

### /format-paper

**Purpose:** Compile, format, and fix LaTeX layout issues.  
**Stage:** Stage 21  
**Skill:** `.claude/skills/paper-format/SKILL.md`  
**Required inputs:** `.tex` file, `references.bib`  
**Expected output:** Compiled PDF with clean log, balanced columns  
**Forbidden:** Never change numerical content while fixing formatting; never alter citation keys

---

## Review Commands

### /review-paper

**Purpose:** Run all 12 review passes.  
**Stage:** Stage 22  
**Skill:** `.claude/skills/paper-review/SKILL.md`  
**Required inputs:** Compiled PDF + `.tex` source  
**Expected output:** Review report (severity P0/P1/P2) for each of 12 passes  
**Forbidden:** Do not rewrite immediately after review; produce report first; passes run in order  
**Passes:** logic → technical → claim-evidence → citation → prior-art/novelty → venue-fit → writing → de-AI → figure/table → layout → paper-code-alignment → final skeptical

---

### /apply-revision-plan

**Purpose:** Apply fixes from review report systematically.  
**Stage:** Stage 23  
**Tools:** All review agents (re-run relevant passes after fixes)  
**Required inputs:** Review report, prioritized revision plan  
**Expected output:** Revised `.tex`, revision log  
**Forbidden:** No new claims during revision without new evidence; do not alter `\cite{}`, `\label{}`, `\ref{}`

---

## Submission and Archive Commands

### /submission-check

**Purpose:** Complete final submission checklist before submitting.  
**Stage:** Stage 24  
**Skill:** `.claude/skills/submission-audit/SKILL.md`  
**Required inputs:** Final PDF, `references.bib`, `result_to_claim_map.md`  
**Expected output:** Completed `09_SUBMISSION_CHECKLIST.md`  
**Forbidden:** No items skipped without documented justification; no P0 findings outstanding

---

### /archive-paper

**Purpose:** Create camera-ready archive after submission.  
**Stage:** Stage 25  
**Skill:** `.claude/skills/archive-paper/SKILL.md`  
**Required inputs:** Final submitted PDF + all source files  
**Expected output:** `archive/` directory with source, figures, results, configs, git hashes  
**Forbidden:** Never delete original files when archiving; never archive without result files

---

## Command Flow Summary

```
System check:    /research-status → /tool-healthcheck → /verify-research-os
New project:     /research-start (or /gap-scout nếu chưa có idea)
Validation:      /validate-hypothesis (BẮT BUỘC trước mọi experiment)
Venue:           /venue-target
Literature:      /literature-review → /prior-art-check → /sota-check
Planning:        /build-contribution-map → /target-result-contract → /plan-experiments
Experiments:     /proxy-run (single) hoặc /hypothesis-tournament (multiple) → /experiment-loop
Evaluation:      /result-adequacy → (if fail) /pivot-decision
Evidence:        /result-backfill
Writing:         /create-paper-outline → /draft-section [each] → /design-figure → /format-paper
Review:          /review-paper → /apply-revision-plan
Submission:      /submission-check → /archive-paper

Full autonomous: /auto-research (covers gap-scout through draft, 3 human checkpoints)
```
