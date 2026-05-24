# Example: Toy Research Project

This directory shows what a research project looks like at **Stage 12 (Exploratory Experiments)** using the Academic Research OS.

**Topic:** Retrieval-augmented agents for scientific literature analysis

## What This Example Shows

| Artifact | Stage it represents | File |
|----------|-------------------|------|
| Project state | Stage 12 (mid-experiments) | `sample_project_state.md` |
| Hypothesis registry | 2 hypotheses registered, 1 under test | `sample_hypothesis_registry.md` |
| Literature matrix | 5-row matrix built from paper-qa | `sample_literature_matrix.md` |
| Evidence ledger | 2 EVID entries from exploratory runs | `sample_evidence_ledger.md` |
| Experiment matrix | 3 experiments planned | `sample_experiment_matrix.md` |
| Result adequacy report | Decision A (all conditions met) | `sample_result_adequacy_report.md` |

## How to Read These Examples

These files are **filled-in versions of the templates** in `../../templates/`. They show what the artifacts look like with real content for a specific project topic.

The content is fictional but structurally correct — the numbers, hypotheses, and claims do not come from a real paper. They are calibrated to illustrate the workflow rules.

## Research Topic Summary

**Working title:** Re-ranking for Scientific Literature Retrieval  
**Core claim:** Adding a cross-encoder re-ranking step after BM25 retrieval improves Recall@10 on scientific QA datasets.  
**Datasets:** SciDocs-Retrieval (500 papers), BEIR-SciQ (1000 questions)  
**Baseline:** BM25 (standard retrieval)  
**Proposed addition:** Cross-encoder re-ranker  
**Current stage:** Stage 12 — first exploratory run completed, one hypothesis supported, planning confirmatory experiments
