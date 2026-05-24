# The 4 Hard Gates

## Overview

The Academic Research OS enforces four hard gates. A hard gate is a checkpoint that blocks all forward progress until specific, verifiable criteria are met. Gates cannot be bypassed by asking Claude to "just skip it" or "proceed anyway." They exist to prevent the most common integrity failures in AI-assisted research: premature novelty claims, cherry-picked metrics, and uncited performance numbers.

Each gate produces a named decision artifact. That artifact must exist and contain a pass verdict before the workflow advances.

---

## Gate 1 — Prior-Art / SOTA Check (Stage 6)

### What It Requires

Gate 1 requires a completed `prior_art_report.md` and a `sota_table.md`. The prior-art report must contain:

- A record of at least 3 distinct search queries run through the pqa index or an equivalent retrieval system
- A threat-level assessment (Low / Medium / High / Critical) for the proposed contribution
- A written analysis of the closest prior work, including paper title, venue, year, and the specific overlap with your proposed idea
- A "gap statement" — a precise description of what the closest prior work does not address, written in terms verifiable from the papers, not from memory

The SOTA table must list at least the top 3 published methods on your primary evaluation dataset and benchmark, with their reported metric values and citation keys. Values must come from the original papers or an authoritative leaderboard, not from memory or secondary sources.

### What Fails It

- The pqa index has fewer than 5 papers in the relevant area
- The closest prior work is not identified or is dismissed without analysis
- The gap statement uses forbidden phrases ("first to," "no prior work," "novel") without citing a completed search
- The SOTA table contains values typed from memory with no citation
- The threat level is "Low" but no search was performed (threat level requires evidence, not assumption)

### How to Pass It

Run `/prior-art-check` and answer all prompts with specific, citable answers. If the search reveals a paper that directly addresses your idea, update `research_direction.md` to narrow or reframe the contribution before proceeding. A narrowed contribution that passes Gate 1 is stronger than a broad contribution that bypasses it.

### What Happens If You Skip Gate 1?

If Gate 1 is not cleared, all novelty claims in `contributions.md`, `hypothesis.md`, and `paper.tex` are provisional and flagged with `TODO_NOVELTY_CHECK_NEEDED:`. The OS will refuse to write the Related Work section and will refuse to sign the Target Result Contract (Gate 2), because the contract requires a confirmed contribution to bind metrics to. Skipping Gate 1 defers — and amplifies — the risk of discovering prior art during peer review.

---

## Gate 2 — Target Result Contract (Stage 9)

### What It Binds

The Target Result Contract (`result_contract.md`) is a signed artifact that specifies:

- **Primary metric:** the single metric on which the paper's main claim rests (e.g., F1-score, BLEU, accuracy at k)
- **Primary dataset:** the evaluation dataset against which the primary metric is reported
- **Minimum threshold:** the numerical value the proposed method must exceed on the primary metric to support the main claim
- **Baseline set:** the specific baseline methods and their reported scores that define the competitive landscape
- **Venue tier:** the publication tier targeted, which determines how strong the result must be
- **Fold / split protocol:** the exact train/validation/test protocol (e.g., 5-fold cross-validation, held-out test set)

### What Cannot Be Changed After Signing

Once `result_contract.md` is signed (the file contains a `STATUS: SIGNED` line with a timestamp), the following cannot be changed without a `/pivot-decision` log entry:

- The primary metric
- The primary dataset
- The baseline set (adding baselines is allowed; removing them requires a pivot log)
- The fold/split protocol

Changing the minimum threshold downward after seeing results is a protocol violation. If results do not meet the threshold, the correct action is Gate 3 decision-making, not retroactively lowering the contract.

### Lifecycle

The contract is created during Stage 9, signed at the end of Stage 9, and remains active through Stage 16. At Gate 3, the contract is evaluated: results either meet it, partially meet it, or fail it. After Stage 17 (Evidence Freeze), the contract becomes a reference artifact — it is not modified but is cited in the adequacy decision.

### What Happens If You Skip Gate 2?

Without a signed contract, the experiment loop (Stages 10–15) has no objective criterion for what constitutes success. Results are then interpreted post-hoc to fit whatever the experiments happened to produce, which is the definition of outcome bias. Gate 3 cannot be run without Gate 2, because adequacy is always relative to a pre-specified contract.

---

## Gate 3 — Result Adequacy Gate (Stage 16)

### The 7 Decisions (A–G)

Gate 3 evaluates accumulated experimental results against the Target Result Contract and produces an `adequacy_decision.md` with one of seven decisions:

**Decision A — Proceed to Writing.**
Results meet or exceed all contract thresholds on all required metrics and datasets. The contribution is supported. Advance to Stage 17.

**Decision B — Proceed with Narrowed Claim.**
Results meet the threshold on a subset of conditions (e.g., one of two datasets, or a subgroup). Proceed to Stage 17 with a narrowed contribution statement. Update `contributions.md` before freezing.

**Decision C — Rerun for Variance Reduction.**
Results are close to the threshold but have high variance (e.g., wide confidence intervals across folds). Return to Stage 14 with additional seeds or folds, then re-evaluate at Gate 3.

**Decision D — Reframe Contribution.**
Results do not support the original claim but reveal a different, potentially publishable finding (e.g., a negative result with explanatory value, or a finding about failure modes). Update `research_direction.md`, narrow contributions, and re-enter Stage 7.

**Decision E — Downgrade Venue.**
Results are positive but below the threshold required for the target tier. The contribution is publishable at a lower tier. Update `venue_target.md` and re-sign a modified contract. Log the downgrade decision in `decision_log.md`.

**Decision F — Collect More Data.**
Results are inconclusive due to insufficient data (e.g., too few samples for statistical significance). Return to Stage 2 (Dataset Inventory) and identify additional data sources.

**Decision G — Abandon.**
Results consistently contradict the hypothesis across multiple reframings, the contribution cannot be defended at any venue, and the cost of continued experimentation exceeds expected value. Log the abandonment in `decision_log.md`, archive the project, and exit the workflow.

### What Triggers Each Decision

| Decision | Condition |
|----------|-----------|
| A | All contract thresholds met, p-value < 0.05 where required |
| B | Subset of thresholds met; narrowing does not vacate the paper |
| C | Mean near threshold but std > 30% of gap to threshold |
| D | Hypothesis falsified but an interpretable finding exists |
| E | Result is real but below tier-required margin |
| F | Confidence intervals span zero or include null hypothesis |
| G | Multiple D reframings have been exhausted |

### What Happens If You Skip Gate 3?

Skipping Gate 3 means proceeding to writing without knowing whether the evidence supports the claims. The resulting paper will contain implicit assumptions about result quality that have not been verified. This is the primary cause of papers with strong-sounding abstracts that fail desk review or receive "results do not support claims" rejections.

---

## Gate 4 — Evidence Freeze (Stage 17)

### What Gets Frozen

The Evidence Freeze locks two artifacts:

1. **`evidence_ledger.md`** — the complete record of all experimental results, literature citations, and data observations used in the paper. After freezing, no new rows may be added and no existing rows may be modified without re-running Gate 3.

2. **`claim-evidence-table.md`** — the mapping from each claim in the paper to one or more evidence IDs. Every quantitative claim, comparative claim, and novelty claim must have at least one entry in this table pointing to a valid evidence ID.

The freeze timestamp is written into both files and into `project_state.md`.

### The Two-Hop Chain

The Evidence Freeze enforces a two-hop traceability chain:

```
results.tsv  →  evidence_ledger.md  →  claim-evidence-table.md  →  paper.tex
```

- `results.tsv` contains raw experimental measurements (timestamp, config, metric, value)
- `evidence_ledger.md` assigns each result an evidence ID and a quality assessment
- `claim-evidence-table.md` maps each paper claim to one or more evidence IDs
- `paper.tex` cites evidence IDs inline as comments (e.g., `% EVID-EXP-7`)

If any link in this chain is broken — a claim in `paper.tex` that does not appear in `claim-evidence-table.md`, or an evidence ID that does not appear in `evidence_ledger.md` — the freeze is invalid and Gate 4 has not been passed.

### What Happens After the Freeze

Writing begins (Stage 18). The evidence ledger and claim-evidence table are read-only. If a reviewer requests an additional experiment, the paper enters a revision cycle: new experiments are run, Gate 3 is re-evaluated for the revision scope, a new partial freeze is declared, and the paper is updated. This cycle is logged in `decision_log.md`.

### What Happens If You Skip Gate 4?

Without a freeze, claims in the paper are not anchored to specific experimental results. Authors may unconsciously update their understanding of the results as they write, resulting in claims that do not match what was actually measured. The two-hop chain also serves as an audit trail during rebuttal — if a reviewer challenges a number, the chain points directly to the raw result file and the exact configuration that produced it.
