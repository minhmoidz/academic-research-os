# Anti-Hallucination Rules Reference

## 1. Why Anti-Hallucination Rules Exist in Academic Research Workflows

AI language models are trained on large corpora that include published research. This creates a specific failure mode in research assistance: the model can generate plausible-sounding academic prose — including specific numbers, citation-like references, and novelty claims — that are drawn from training-data patterns rather than from actual evidence in the current project.

This failure mode is not "making things up" in the obvious sense. The model may produce a claim like "recall@10 improves by approximately 8% when re-ranking is added" that is plausible based on training-data patterns about retrieval systems — but that is not the result of any experiment run in this project. Without explicit rules preventing this, AI-assisted writing workflows systematically produce papers with unverifiable claims.

The 15 anti-hallucination rules enforce a single discipline: **every claim in the paper must be traceable to a specific, documented artifact in this project.** No claim may be made from pattern-matching, intuition, training-data knowledge, or approximation.

---

## 2. Summary Table of All 15 Rules

| Rule # | Short Name | What It Forbids | Correct Alternative |
|--------|-----------|-----------------|---------------------|
| R-1 | No Memory Numbers | Reporting metric values from memory or training data | Copy values from `results.tsv` or from the original paper's table |
| R-2 | No Uncited Baselines | Including a baseline result without a citation key | Add the citation to `references.bib` and verify the value from the source |
| R-3 | No Fabricated Confidence | Writing "approximately," "roughly," or "about X%" for unrun experiments | Use `TODO_RESULT_NEEDED:` and `XX.X` placeholder |
| R-4 | No Pre-Gate Novelty | Writing "first," "novel," "no prior work" before Gate 1 passes | Use `TODO_NOVELTY_CHECK_NEEDED:` |
| R-5 | No Pre-Contract Claims | Stating performance claims before Gate 2 (Target Result Contract) is signed | Write the claim only after the contract is signed and Gate 3 is passed |
| R-6 | No Cherry-Picked Metrics | Reporting only the metric where results are strongest | Report all metrics specified in `experiment-plan.md` |
| R-7 | No Post-Hoc Metric Switch | Switching the primary metric after seeing results | Log a `/pivot-decision` entry; the switch must be documented |
| R-8 | No Partial Fold Averaging | Averaging fewer than the contracted number of folds | Run all folds; if a fold fails, log as FAILED and re-run |
| R-9 | No Unreviewed Evidence | Using a DRAFT evidence entry in the paper | Only APPROVED entries may appear in `claim-evidence-table.md` |
| R-10 | No Paraphrased Numbers | Paraphrasing a prior paper's result instead of citing the exact table value | Quote the exact value with citation; note if the value is from a figure |
| R-11 | No Invented Citations | Generating a citation that was not verified by reading the paper | All citations must appear in `references.bib` with verified metadata |
| R-12 | No Implicit Superiority | Claiming the method "outperforms" without a direct, same-protocol comparison | Specify dataset, protocol, and metric; cite evidence IDs |
| R-13 | No Scope Creep Claims | Claiming generalization to datasets or tasks not evaluated | Run the generalization experiment or remove the claim |
| R-14 | No Theory-Free Guarantees | Writing "guarantees," "provably," or "always" without a formal proof | Remove the guarantee or replace with "empirically, on the evaluated tasks" |
| R-15 | No Silent Assumption | Making a claim that depends on an unstated assumption | State the assumption explicitly in the text |

---

## 3. The 10 TODO Marker Types with Usage Examples

TODO markers are the correct substitute for any claim that cannot yet be supported by evidence. They are scannable by the OS's artifact checker and serve as a structured to-do list for evidence collection.

### `TODO_RESULT_NEEDED:`
Use when a quantitative claim requires an experiment that has not been run.
```latex
% TODO_RESULT_NEEDED: run generalization experiment on BioASQ
Our method achieves \textbf{XX.X\%} recall@10 on BioASQ.
```

### `TODO_EVIDENCE_NEEDED:`
Use when a claim exists in the outline but neither an experiment nor a citation has been identified to support it.
```latex
% TODO_EVIDENCE_NEEDED: is there a published analysis of re-ranking latency?
The re-ranking step adds minimal latency to the retrieval pipeline.
```

### `TODO_CITATION_NEEDED:`
Use when a literature claim needs a citation that has not yet been verified and added to `references.bib`.
```latex
% TODO_CITATION_NEEDED: find and verify citation for this claim
Retrieval-augmented generation was introduced by Lewis et al. \cite{TODO}.
```

### `TODO_NOVELTY_CHECK_NEEDED:`
Use for any novelty claim before Gate 1 (Prior-Art Check) is complete.
```latex
% TODO_NOVELTY_CHECK_NEEDED: Gate 1 not yet passed
To our knowledge, this is the first system to combine iterative re-ranking
with agent-based traversal for scientific literature QA.
```

### `TODO_VENUE_FIT_NEEDED:`
Use for claims about publication suitability or contribution framing that depend on Gate 2 (venue selection).
```latex
% TODO_VENUE_FIT_NEEDED: venue not yet selected
This contribution is appropriate for a full paper at a top-tier venue.
```

### `TODO_STAT_TEST_NEEDED:`
Use when a claim of statistical significance has not yet been verified with a test.
```latex
% TODO_STAT_TEST_NEEDED: run paired t-test across folds
The improvement is statistically significant (p < 0.05).
```

### `TODO_ABLATION_NEEDED:`
Use when an ablation claim references a component that has not yet been ablated.
```latex
% TODO_ABLATION_NEEDED: ablation removing re-ranker not yet run
Re-ranking is the primary driver of the observed improvement.
```

### `TODO_DATASET_CHECK_NEEDED:`
Use when a claim about dataset properties has not been verified by inspecting the data.
```latex
% TODO_DATASET_CHECK_NEEDED: verify split sizes by running dataset_stats.py
The test split contains 1,200 queries.
```

### `TODO_REPRO_NEEDED:`
Use when a claim about reproducibility (code release, hyperparameter sensitivity) has not been verified.
```latex
% TODO_REPRO_NEEDED: run with 3 different random seeds
Results are consistent across random seeds.
```

### `TODO_REVIEW_NEEDED:`
Use to flag a passage that needs human review before the Evidence Freeze.
```latex
% TODO_REVIEW_NEEDED: this paragraph makes claims from three evidence IDs; verify chain
The combination of dense retrieval, re-ranking, and agent-based traversal...
```

---

## 4. The Forbidden Phrases List

The following phrases are blocked before their corresponding evidence requirements are met. When Claude detects these phrases in a draft, it inserts the appropriate TODO marker and states which evidence is needed.

| Phrase | Required Evidence to Use It |
|--------|----------------------------|
| "state-of-the-art" / "SOTA" | An approved SOTA table entry showing your result exceeds all published baselines |
| "first" / "first to" | Gate 1 passed; prior-art report showing no prior work on this specific combination |
| "novel" | Gate 1 passed; gap statement in `prior_art_report.md` |
| "outperforms" / "surpasses" | Direct same-protocol comparison with citation; EVID-EXP entry with delta and p-value |
| "guarantees" / "provably" / "always" | Formal proof in the paper or in a cited theorem |
| "significantly better" | Statistical test result with p-value; EVID-EXP entry with test type and result |
| "generalizes to" | Evaluation on the claimed domain; EVID-EXP entry |
| "robust to" | Sensitivity analysis or ablation on the varied condition; EVID-EXP entry |
| "minimal overhead" / "negligible cost" | Timing measurement; EVID-EXP entry with latency or FLOPs |
| "to our knowledge" | Gate 1 passed; explicit search log in `prior_art_report.md` |
| "as shown in" (without a figure/table reference) | The figure or table must exist in the paper; `\ref{}` must resolve |
| "approximately X%" (for unrun experiment) | `TODO_RESULT_NEEDED:` with `XX.X` placeholder instead |

---

## 5. The 8-Question Self-Check Before Writing Any Claim

Before writing any sentence that makes a factual, quantitative, comparative, or novelty claim, ask these eight questions:

**Q1: Is there an approved evidence entry in `evidence_ledger.md` that supports this claim?**
If no: insert `TODO_RESULT_NEEDED:` or `TODO_EVIDENCE_NEEDED:` and do not write the claim.

**Q2: Is the exact number I am writing the same as the number in `results.tsv` or the source paper's table?**
If no: look up the exact number. Do not round, estimate, or paraphrase.

**Q3: Does this claim use any forbidden phrase (state-of-the-art, first, outperforms, etc.)?**
If yes: check whether the required evidence exists. If not, insert the appropriate TODO marker.

**Q4: Does this claim depend on a comparison? If so, is the comparison same-protocol (same dataset, same evaluation code, same metric)?**
If no: add a caveat ("under our evaluation protocol") or remove the comparison.

**Q5: Is the fold count and averaging consistent with the Target Result Contract?**
If no: do not report the number until the full fold count is complete.

**Q6: Does this claim require a citation to a prior paper? Is that citation in `references.bib` with verified metadata?**
If no: insert `TODO_CITATION_NEEDED:` and do not write the citation key.

**Q7: Does this claim make a scope statement (e.g., "generalizes to," "works for all")? Has that scope been evaluated?**
If no: narrow the scope to what was actually evaluated.

**Q8: If this claim appeared in a reviewer's list of objections, could I point to a specific file, row, and timestamp in this project's artifacts to defend it?**
If no: the claim is not ready to be written.

All eight questions must be answerable affirmatively before the claim is written in `paper.tex`.
