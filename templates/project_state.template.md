# project_state.md
# DO NOT EDIT MANUALLY — updated by Claude at end of each session.
# Read by Claude at the start of each session.

---

## Identity

project_name: [short-slug, e.g., rag-scilit]
working_title: "[Full Working Paper Title]"
paper_type: [empirical | survey | system | theory | benchmark]
target_venue: [Venue Name]
target_venue_tier: [top-tier | strong | domain | workshop | arXiv]
target_deadline: [YYYY-MM-DD or "none"]

---

## Stage

current_stage: [0-25]
stage_name: [canonical stage name from 02_RESEARCH_WORKFLOW.md]
last_updated: [ISO 8601 timestamp, e.g., 2026-05-24T14:30:00+00:00]
session_count: [integer]

---

## Hypothesis

original_hypothesis: >
  [One to three sentences stating the hypothesis as originally posed at Stage 2.
  Do not modify this field after Stage 2 is complete.]

current_hypothesis: >
  [Current working hypothesis. This may be narrowed, pivoted, or qualified
  compared to the original. Updated at Stages 6, 13, 17.]

hypothesis_status: [unchanged | narrowed | pivoted | abandoned]
hypothesis_notes: >
  [If pivoted or abandoned, explain why in 1-2 sentences and link to decision ID.]

---

## Research Direction

research_direction: >
  [Current research direction in one paragraph. What is being investigated,
  what approach is being taken, and what outcome is expected. Updated at
  Stages 1, 7, 13.]

---

## Stage Progress

completed_stages:
  - [stage number]: [stage name]  # completed YYYY-MM-DD
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
  - [file_name]  # reason: [why it is needed]
  # list all files required for current_stage but not yet created

---

## Blockers

active_blockers:
  - id: BLK-001
    description: [what is blocked and why]
    affects_stage: [stage number]
    resolution: [how to unblock]
  # add one entry per active blocker; remove when resolved

---

## TODO Markers

active_todo_count: [integer — run grep to count]
active_todos:
  - file: [filename]
    line: [line number]
    type: [TODO_EVIDENCE_NEEDED | TODO_RESULT_NEEDED | TODO_CITATION_NEEDED]
    description: [brief description]
  # list up to 10 most critical; note total count above

---

## Hypotheses Registry

active_hypotheses:
  - id: HYP-001
    statement: "[hypothesis text]"
    status: [active | confirmed | refuted | abandoned]
    evidence: [experiment IDs or literature citations supporting/refuting]
  # one entry per hypothesis from hypothesis_registry.md

---

## Experiments

active_experiments:
  - id: [EXP-XXX from results.tsv]
    description: [what is being tested]
    status: [running | complete | failed | cancelled]
    config: [key config parameters]
  # list running or recently completed experiments

current_best_result:
  metric: [metric name, e.g., AUC, F1, Accuracy, Recall@10]
  value: [numeric value with std, e.g., 0.912 ± 0.008]
  experiment_id: [EXP-XXX]
  dataset: [dataset name]
  note: [any qualification, e.g., "single fold" or "5-fold mean"]

---

## Evidence

evidence_status:
  total_claims: [integer]
  claims_with_evidence: [integer]
  fraction: [e.g., "7/12 (58%)"]
  unverified_claims:
    - "[claim text]" — needs: [what evidence is required]

---

## Writing

writing_status:
  abstract:       [not started | drafted | reviewed | final]
  introduction:   [not started | drafted | reviewed | final]
  related_work:   [not started | drafted | reviewed | final]
  methodology:    [not started | drafted | reviewed | final]
  experiments:    [not started | drafted | reviewed | final]
  results:        [not started | drafted | reviewed | final]
  discussion:     [not started | drafted | reviewed | final]
  conclusion:     [not started | drafted | reviewed | final]
  references:     [not started | drafted | reviewed | final]
  appendix:       [not started | drafted | reviewed | final | n/a]

---

## Figures

figure_status:
  - id: FIG-01
    description: [what the figure shows]
    status: [planned | created | reviewed | final]
    file: [path to .tex or .pdf or null]
  # one entry per planned/created figure

---

## Review

review_status:
  logic_reviewer:           [not run | complete | issues-open]
  technical_reviewer:       [not run | complete | issues-open]
  consistency_checker:      [not run | complete | issues-open]
  bibliography_auditor:     [not run | complete | issues-open]
  writing_reviewer:         [not run | complete | issues-open]
  prose_polisher:           [not run | complete | issues-open]
  latex_figure_specialist:  [not run | complete | issues-open]
  latex_layout_auditor:     [not run | complete | issues-open]
  paper_crawler:            [not run | complete | issues-open]
  research_analyst:         [not run | complete | issues-open]
  brainstormer:             [not run | complete | issues-open]
  section_drafter:          [not run | complete | issues-open]

---

## Gate Status

current_gate: [gate name and stage, e.g., "Evidence Gate (Stage 17)"]
gate_criteria_met:
  - criterion: "[gate criterion]"
    met: [yes | no | partial]
  # list all criteria for current gate

---

## Next Action

next_safe_action: >
  [One specific, concrete action Claude should take next. Must be compatible
  with current_stage and not skip any required gate. Example:
  "Run pqa index on the PDFs in /literature/ to build the evidence index,
  then populate rows 1-4 of literature_matrix.md with pqa ask queries."]

---

## Decision Summary (Last 3)

- [DEC-ID]: [one-sentence summary of decision] ([date])
- [DEC-ID]: [one-sentence summary of decision] ([date])
- [DEC-ID]: [one-sentence summary of decision] ([date])
# Full log in decision_log.md
