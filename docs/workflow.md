# Research Workflow Reference

## Overview

The Academic Research OS structures a research project into 26 discrete stages. Stages are grouped into five major phases. Each stage produces at least one named artifact, and four stages are designated **hard gates** that block forward progress until specific evidence criteria are met.

The workflow is linear by default. Iteration is allowed within a phase but backward movement across a gate requires an explicit `/pivot-decision` log entry.

---

## 26-Stage Summary Table

| Stage | Name | Key Outputs | Gate? | Primary Commands |
|-------|------|-------------|-------|-----------------|
| 0 | Research Question | `research_direction.md` | — | `/research-start` |
| 1 | Scope Definition | `scope.md` | — | `/define-scope` |
| 2 | Dataset Inventory | `dataset_inventory.md` | — | `/dataset-check` |
| 3 | Toolchain Setup | `.claude/` config, `tool_manifest.md` | — | `/tool-healthcheck` |
| 4 | Idea Formalization | `hypothesis.md` | — | `/formalize-hypothesis` |
| 5 | Literature Collection | `papers/` index, `pqa` index built | — | `/collect-literature` |
| 6 | Prior-Art / SOTA Check | `prior_art_report.md`, `sota_table.md` | **GATE 1** | `/prior-art-check` |
| 7 | Contribution Draft | `contributions.md` | — | `/draft-contributions` |
| 8 | Experiment Design | `experiment-plan.md` | — | `/design-experiments` |
| 9 | Target Result Contract | `venue_target.md`, `result_contract.md` | **GATE 2** | `/venue-target`, `/sign-contract` |
| 10 | Baseline Implementation | `baselines/` code, `baseline_results.tsv` | — | `/run-baselines` |
| 11 | Method Implementation | `method/` code | — | `/implement-method` |
| 12 | Pilot Experiment | `results/pilot/`, `pilot_summary.md` | — | `/run-pilot` |
| 13 | Ablation Design | `ablation_plan.md` | — | `/design-ablations` |
| 14 | Full Experiment Run | `results/full/`, `results.tsv` | — | `/experiment-loop` |
| 15 | Ablation Run | `results/ablations/`, `ablation_results.tsv` | — | `/run-ablations` |
| 16 | Result Adequacy Gate | `adequacy_decision.md` | **GATE 3** | `/result-adequacy` |
| 17 | Evidence Freeze | `evidence_ledger.md`, `claim-evidence-table.md` | **GATE 4** | `/freeze-evidence` |
| 18 | Outline and Structure | `outline.md` | — | `/build-outline` |
| 19 | Section Drafting | `paper.tex` (draft) | — | `/draft-section` |
| 20 | Figure and Table Generation | `figures/`, `tables/` | — | `/generate-figures` |
| 21 | Internal Review | `review_notes.md` | — | `/self-review` |
| 22 | Citation Validation | `references.bib` (validated) | — | `/validate-citations` |
| 23 | Formatting and Compliance | `paper.pdf` (compiled) | — | `/format-check` |
| 24 | External Review Response | `rebuttal.md` (if needed) | — | `/prepare-rebuttal` |
| 25 | Submission | Submission package | — | `/prepare-submission` |

---

## Phase Descriptions

### Stages 0–4: Setup and Idea

This phase establishes the research question, defines the project scope, inventories available data, configures the toolchain, and formalizes the initial hypothesis. No literature search has occurred yet, so no novelty claims may be made. The outputs are planning documents only.

The key artifact from this phase is `hypothesis.md`, which contains a falsifiable prediction, a proposed mechanism, and an estimated effect size. The hypothesis is a starting point for inquiry, not a commitment to a result. If experiments falsify the hypothesis, the workflow prescribes updating `research_direction.md` — not retrofitting the hypothesis to match results.

For an example project on retrieval-augmented agents for scientific literature analysis, Stage 0 would produce a research question such as: "Does integrating dense retrieval with a language model agent improve citation recall on domain-specific queries compared to keyword-only search?" This question is specific, testable, and does not assert a conclusion.

### Stages 5–9: Literature and Planning

This phase builds the literature foundation and planning artifacts that gate all subsequent work. Stage 5 collects PDFs and builds the pqa index. Stage 6 runs the Prior-Art/SOTA Check — the first hard gate — which establishes whether the proposed idea has been published and what the competitive performance landscape looks like. Failing to pass Gate 1 before claiming novelty is the most common integrity violation in research workflows.

Stages 7 and 8 translate the gate-cleared literature understanding into a contribution statement and a concrete experiment design. Stage 9 signs the Target Result Contract, which binds the project to specific metrics, datasets, and minimum thresholds. After Stage 9, changing the primary metric or primary dataset requires a `/pivot-decision` entry and re-running the contract.

### Stages 10–17: Experiments and Evidence

This is the longest phase and the empirical core of the workflow. Stages 10–11 implement baselines and the proposed method. Stages 12–15 run experiments in increasing scope: pilot, full, and ablation. The OS enforces the experiment-loop protocol (see [Bounded Experiment Loop](experiment-loop.md)) to ensure results are logged with full provenance.

Stage 16 is the Result Adequacy Gate, which determines whether accumulated results are sufficient for the claimed contribution and target venue. Decisions A through G describe outcomes ranging from "proceed to writing" to "abandon and pivot." Stage 17 freezes the evidence set: after the Evidence Freeze, no new experimental results may be incorporated into the paper without re-running Gate 3.

### Stages 18–21: Writing and Formatting

Paper writing begins only after evidence is frozen. Stage 18 builds a section outline from the evidence ledger and claim-evidence table. Stage 19 drafts each section with strict citation discipline — every quantitative claim cites a specific evidence ID. Stages 20–21 generate production-quality figures and tables, followed by an internal self-review against venue requirements.

The OS prohibits writing from memory or from recollected intuition. Every claim in a draft section must be traceable to a row in `claim-evidence-table.md`. Claims without evidence receive `TODO_RESULT_NEEDED:` markers, not fabricated numbers.

### Stages 22–25: Review and Submission

The final phase validates citations, checks formatting against venue style requirements, compiles the final PDF, and prepares the submission package. Stage 24 handles reviewer response if the paper goes through review cycles. Stage 25 produces the final submission-ready archive.

Throughout this phase, the evidence ledger remains frozen. Reviewer requests for additional experiments are handled by re-entering the workflow at Stage 14 (with a new `/pivot-decision` log entry), not by inserting unreferenced results into the paper.
