# 16_PROJECT_STATE.md — Project State Protocol

## Purpose

`project_state.md` is the single source of truth for the current status of a research
project. Claude must read this file at the start of every session and update it after
every session in which meaningful progress is made. If this file does not exist, Claude
must create it from scratch using the template below before doing anything else (Stage 0).

The file tracks stage position, artifacts, hypotheses, experiment state, writing status,
and active blockers. It enables any Claude session — even one with no prior context — to
pick up exactly where the last session left off.

---

## Rules

1. **Read at session start.** Do not write new content until this file is read and
   the current stage is confirmed with the user.
2. **Update after every session.** Update `current_stage`, `last_updated`,
   `session_count`, `completed_artifacts`, `missing_artifacts`, `active_blockers`,
   and `next_safe_action` after every session.
3. **If missing, create it.** If `project_state.md` does not exist, Claude must
   create it (using Stage 0) before doing anything else.
4. **Never delete prior state.** Move old hypothesis text to `hypothesis_status` notes
   rather than overwriting. Append to `decision_summary`.
5. **All timestamps in ISO 8601 format.** Example: `2026-05-24T14:30:00+07:00`
6. **Stage name must match the canonical name.** See the 26-stage list in
   `02_RESEARCH_WORKFLOW.md`.

---

## Template: project_state.md

Save this file as `project_state.md` in the project root directory.
Replace every `<placeholder>` with actual values.

```markdown
# project_state.md
# DO NOT EDIT MANUALLY — updated by Claude at end of each session.
# Read by Claude at the start of each session.

---

## Identity

project_name: <short-slug, e.g., my-research-project>
working_title: "<Full Working Paper Title>"
paper_type: <empirical | survey | system | theory | benchmark>
target_venue: <Venue Name>
target_venue_tier: <top-tier | strong | domain | workshop | arXiv>
target_deadline: <YYYY-MM-DD or "none">

---

## Stage

current_stage: <0-25>
stage_name: <canonical stage name from 02_RESEARCH_WORKFLOW.md>
last_updated: <ISO 8601 timestamp>
session_count: <integer>

---

## Hypothesis

original_hypothesis: >
  <One to three sentences stating the hypothesis as originally posed at Stage 2.
  Do not modify this field after Stage 2 is complete.>

current_hypothesis: >
  <Current working hypothesis. This may be narrowed, pivoted, or qualified
  compared to the original. Updated at Stages 6, 13, 17.>

hypothesis_status: <unchanged | narrowed | pivoted | abandoned>
hypothesis_notes: >
  <If pivoted or abandoned, explain why in 1-2 sentences and link to decision ID.>

---

## Research Direction

research_direction: >
  <Current research direction in one paragraph. What is being investigated,
  what approach is being taken, and what outcome is expected. Updated at
  Stages 1, 7, 13.>

---

## Stage Progress

completed_stages:
  - <stage number>: <stage name>  # completed YYYY-MM-DD
  # add one line per completed stage

---

## Artifacts

completed_artifacts:
  - paper_brief.md           # Stage 1
  - hypothesis_registry.md   # Stage 2
  - venue_profile.md         # Stage 3
  - feasibility_report.md    # Stage 4
  - literature_matrix.md     # Stage 5
  - gap_statement.md         # Stage 7
  - contribution_contract.md # Stage 8
  - result_contract.md       # Stage 9
  - experiment_plan.md       # Stage 10
  - results.tsv              # Stage 12+
  - evidence_ledger.md       # Stage 17
  - paper_outline.md         # Stage 18
  # Remove any not yet created. Add actual file path if different.

missing_artifacts:
  - <file_name>  # reason: <why it is needed>
  # list all files required for current_stage but not yet created

---

## Blockers

active_blockers:
  - id: BLK-001
    description: <what is blocked and why>
    affects_stage: <stage number>
    resolution: <how to unblock>
  # add one entry per active blocker; remove when resolved

---

## TODO Markers

active_todo_count: <integer — run grep to count>
active_todos:
  - file: <filename>
    line: <line number>
    type: <TODO_EVIDENCE_NEEDED | TODO_RESULT_NEEDED | TODO_CITATION_NEEDED>
    description: <brief description>
  # list up to 10 most critical; note total count above

---

## Hypotheses Registry

active_hypotheses:
  - id: HYP-001
    statement: "<hypothesis text>"
    status: <active | confirmed | refuted | abandoned>
    evidence: <experiment IDs or literature citations supporting/refuting>
  # one entry per hypothesis from hypothesis_registry.md

---

## Experiments

active_experiments:
  - id: <EXP-XXX from results.tsv>
    description: <what is being tested>
    status: <running | complete | failed | cancelled>
    config: <key config parameters>
  # list running or recently completed experiments

current_best_result:
  metric: <metric name, e.g., AUC, F1, Accuracy>
  value: <numeric value with std, e.g., 0.912 ± 0.008>
  experiment_id: <EXP-XXX>
  dataset: <dataset name>
  note: <any qualification, e.g., "single fold" or "5-fold mean">

---

## Evidence

evidence_status:
  total_claims: <integer>
  claims_with_evidence: <integer>
  fraction: <e.g., "7/12 (58%)">
  unverified_claims:
    - "<claim text>" — needs: <what evidence is required>

---

## Writing

writing_status:
  abstract:       <not started | drafted | reviewed | final>
  introduction:   <not started | drafted | reviewed | final>
  related_work:   <not started | drafted | reviewed | final>
  methodology:    <not started | drafted | reviewed | final>
  experiments:    <not started | drafted | reviewed | final>
  results:        <not started | drafted | reviewed | final>
  discussion:     <not started | drafted | reviewed | final>
  conclusion:     <not started | drafted | reviewed | final>
  references:     <not started | drafted | reviewed | final>
  appendix:       <not started | drafted | reviewed | final | n/a>

---

## Figures

figure_status:
  - id: FIG-01
    description: <what the figure shows>
    status: <planned | created | reviewed | final>
    file: <path to .tex or .pdf or null>
  # one entry per planned/created figure

---

## Review

review_status:
  logic_reviewer:           <not run | complete | issues-open>
  technical_reviewer:       <not run | complete | issues-open>
  consistency_checker:      <not run | complete | issues-open>
  bibliography_auditor:     <not run | complete | issues-open>
  writing_reviewer:         <not run | complete | issues-open>
  prose_polisher:           <not run | complete | issues-open>
  latex_figure_specialist:  <not run | complete | issues-open>
  latex_layout_auditor:     <not run | complete | issues-open>
  paper_crawler:            <not run | complete | issues-open>
  research_analyst:         <not run | complete | issues-open>
  brainstormer:             <not run | complete | issues-open>
  section_drafter:          <not run | complete | issues-open>

---

## Gate Status

current_gate: <gate name and stage, e.g., "Evidence Gate (Stage 17)">
gate_criteria_met:
  - criterion: "<gate criterion>"
    met: <yes | no | partial>
  # list all criteria for current gate

---

## Next Action

next_safe_action: >
  <One specific, concrete action Claude should take next. Must be compatible
  with current_stage and not skip any required gate. Example:
  "Run pqa index on the 8 PDFs in /literature/ to build the evidence index,
  then populate rows 1-4 of literature_matrix.md with pqa ask queries.">

---

## Decision Summary (Last 3)

- <DEC-ID>: <one-sentence summary of decision> (<date>)
- <DEC-ID>: <one-sentence summary of decision> (<date>)
- <DEC-ID>: <one-sentence summary of decision> (<date>)
# Full log in decision_log.md
```

---

## Example: Filled-In project_state.md

The following is a realistic example using the topic of retrieval-augmented agents for scientific literature analysis, at Stage 19 (Section Drafting).

```markdown
# project_state.md

## Identity

project_name: ralit-agents
working_title: "RALit: Retrieval-Augmented Agents for Evidence-Grounded Scientific Literature Analysis"
paper_type: empirical
target_venue: ACL 2026
target_venue_tier: top-tier
target_deadline: 2026-09-15

## Stage

current_stage: 19
stage_name: Section Drafting
last_updated: 2026-05-24T15:00:00+00:00
session_count: 11

## Hypothesis

original_hypothesis: >
  Adding a multi-hop sub-claim decomposition module to a single-step RAG baseline
  will improve citation accuracy and reduce hallucinated references on Dataset-A
  and Dataset-B compared to the BaselineModel.

current_hypothesis: >
  The sub-claim decomposition module improves citation accuracy by at least 5 percentage
  points on Dataset-A under identical retrieval budget, with the verifier component
  contributing the largest individual gain identified in ablation.

hypothesis_status: narrowed
hypothesis_notes: >
  Original hypothesis did not specify which sub-component contributed most.
  After ablation (EXP-031), the verifier was identified as the dominant contributor.
  See DEC-2026-05-10-003.

## Research Direction

research_direction: >
  We augment a single-step RAG system with a query decomposition agent and a
  chain-of-thought verifier. The decomposer breaks a literature query into
  sub-claims; the retriever fetches passages for each independently; the verifier
  rejects unsupported sub-claims before answer synthesis. The combined system
  (YourMethod) is evaluated on Dataset-A and Dataset-B with 5-fold CV against
  three baselines. The paper targets ACL 2026 and is in section drafting.

## Stage Progress

completed_stages:
  - 0: System Readiness  # completed 2026-04-01
  - 1: Idea Intake  # completed 2026-04-02
  - 2: Problem Formulation  # completed 2026-04-03
  - 3: Venue Targeting  # completed 2026-04-05
  - 4: Initial Feasibility Check  # completed 2026-04-06
  - 5: Literature Grounding  # completed 2026-04-12
  - 6: Prior-Art/SOTA Check  # completed 2026-04-15
  - 7: Gap/Positioning  # completed 2026-04-16
  - 8: Contribution Contract  # completed 2026-04-18
  - 9: Target Result Contract  # completed 2026-04-20
  - 10: Experiment Design  # completed 2026-04-22
  - 11: Baseline/Implementation Readiness  # completed 2026-04-25
  - 12: Exploratory Experiment Loop  # completed 2026-05-05
  - 13: Result Interpretation/Direction Update  # completed 2026-05-10
  - 14: Confirmatory Experiment Planning  # completed 2026-05-12
  - 15: Confirmatory Experiment Execution  # completed 2026-05-20
  - 16: Result Adequacy Gate  # completed 2026-05-21
  - 17: Evidence Freeze  # completed 2026-05-22
  - 18: Paper Architecture  # completed 2026-05-23

## Artifacts

completed_artifacts:
  - paper_brief.md
  - hypothesis_registry.md
  - venue_profile.md
  - feasibility_report.md
  - literature_matrix.md
  - gap_statement.md
  - contribution_contract.md
  - result_contract.md
  - experiment_plan.md
  - results.tsv
  - evidence_ledger.md
  - paper_outline.md

missing_artifacts:
  - main.tex  # reason: Section Drafting not yet complete
  - figures/fig1_architecture.tex  # reason: Figure Design (Stage 20) not started

## Blockers

active_blockers:
  - id: BLK-003
    description: Table I Dataset-B baselines not yet verified — ComparisonMethod rows are TODO_RESULT_NEEDED
    affects_stage: 19
    resolution: Run baselines on Dataset-B or obtain published numbers with citation

## Next Action

next_safe_action: >
  Draft the Methodology section (Section III) using paper_outline.md as the skeleton.
  Use only evidence IDs from evidence_ledger.md for any claims. Mark any claim
  lacking an evidence ID as TODO_EVIDENCE_NEEDED. Do not draft Abstract or
  Introduction until Methodology and Experiments sections are complete.

## Decision Summary (Last 3)

- DEC-2026-05-21-008: Adopted population std (÷N=5) for all result tables (2026-05-21)
- DEC-2026-05-10-003: Identified verifier as dominant contributor; narrowed hypothesis (2026-05-10)
- DEC-2026-04-05-001: Selected ACL over EMNLP due to broader NLP scope and results maturity (2026-04-05)
```
