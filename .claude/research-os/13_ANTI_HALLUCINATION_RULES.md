# Anti-Hallucination Rules

These rules are non-negotiable. They apply to every Claude session working on a research paper. No exception, no workaround.

---

## The Core Prohibition

**Claude must never generate content that presents invented information as factual.**

This includes: citations, BibTeX entries, dataset statistics, baseline results, metric values, ablation numbers, author names, venue names, paper titles, methodology claims, and novelty statements.

---

## Rule 1: No Fake Citations

**Never write a `\cite{key}` before confirming the paper exists.**

- Every citation key must appear in `references.bib`
- Every `references.bib` entry must correspond to a real paper Claude has verified via paper-qa, web search, or user-provided BibTeX
- If a citation is needed but unverified: write `\cite{TODO_CITATION_NEEDED:description_of_paper}`
- Never fabricate an author-year key and write prose around it

**Forbidden pattern:**
```latex
Recent work by Smith et al.~\cite{smith2024method} showed...
```
(if smith2024method does not exist in references.bib and was not verified)

**Correct pattern when missing:**
```latex
% TODO_CITATION_NEEDED: paper on [topic] from [year] by [authors if known]
Recent work on [topic]
```

---

## Rule 2: No Fake BibTeX

**Never generate a BibTeX entry from memory.**

If you need a BibTeX entry for a paper:
1. Ask the user to provide it
2. Fetch it from a verified source (DOI, DBLP, arXiv)
3. Use paper-qa to locate it in the indexed library

Never reconstruct a BibTeX entry by guessing page numbers, volume numbers, issue numbers, or proceedings names. These details are frequently wrong and constitute fabrication.

---

## Rule 3: No Fake Datasets

**Never describe a dataset you have not verified exists.**

- Dataset names, number of samples, splits, and class distributions must come from verified sources (paper-qa, user-provided data logs, official dataset websites)
- If dataset stats are unknown: write `TODO_RESULT_NEEDED: N samples in [split] for [dataset]`
- Never invent a dataset to fill a gap in the experimental setup description

---

## Rule 4: No Fake Baselines

**Never add a baseline method to a comparison table without the user confirming it was run.**

- Every row in a results table must correspond to an actual experiment run by the user
- Never estimate what a baseline "might" achieve
- Never copy numbers from a different paper's table without explicitly labeling the source
- If a baseline was not run: mark it `TODO_RESULT_NEEDED: run [method] on [dataset]`

---

## Rule 5: No Fake Metrics

**Never round, interpolate, or estimate experimental results.**

- All numbers in tables come from result log files provided by the user
- Never "clean up" a result (e.g., rounding 94.73% to 95% in the table)
- Never average across seeds without confirming the user ran multiple seeds
- Standard deviation must be computed from real per-fold or per-seed results

---

## Rule 6: No Fake Results

**Never upgrade a hypothesis to a claim before the experiment is run.**

- "We expect our method to outperform..." is a hypothesis → keep as hypothesis until verified
- "Our method achieves 97.05% AUC..." is a claim → requires a real log file showing this number
- Use `TODO_RESULT_NEEDED:` for any claim that depends on an experiment that hasn't been run

---

## Rule 7: No Unsupported Novelty Claims

**Never write "to our knowledge, the first" without evidence.**

- A novelty claim requires confirming that no prior work exists via paper-qa or literature search
- If you cannot verify uniqueness, write: "We are not aware of prior work that [X], though a full survey is beyond this paper's scope"
- Never state "state-of-the-art" without a comparison table showing it

---

## Rule 8: No Related Work from Memory

**Never write Related Work from what Claude "knows" about the field.**

The Related Work section must be built from:
1. Papers the user has provided as PDFs (indexed via paper-qa)
2. Papers with verified BibTeX entries in references.bib
3. Papers found through paper-crawler (DBLP/OpenAlex) with verified existence

If a paper is mentioned in Related Work but not in references.bib: it must not be cited until verified.

---

## Rule 9: Preserve Scientific Claims During Revision

**During prose revision, never alter numerical results, methodological descriptions, or citation keys.**

When rewriting a sentence for clarity or style:
- Keep all `\cite{}`, `\ref{}`, `\label{}`, `\eqref{}` unchanged
- Keep all numerical values unchanged (AUC %, std dev, parameter counts, etc.)
- Keep all method names and acronyms unchanged
- If a numerical claim looks wrong, flag it — do not silently "correct" it

---

## Rule 10: Use TODO Markers, Never Fill With Fiction

When evidence is missing, use exactly these markers:

| Situation | Marker |
|-----------|--------|
| Need a citation that doesn't exist yet | `TODO_CITATION_NEEDED: [description]` |
| Need an experiment result not yet run | `TODO_RESULT_NEEDED: [experiment]` |
| Need literature evidence not yet found | `TODO_EVIDENCE_NEEDED: [claim to support]` |
| Need a figure not yet created | `TODO_FIGURE_NEEDED: [description]` |
| Need author/venue/page info | `TODO_BIBINFO_NEEDED: [field] for [key]` |

**Never fill a TODO with fabricated content under any circumstances.**

---

## Rule 11: Experiment Claims Must Come from Logged Result Files

**Never write a performance claim from an experiment that is not in `results.tsv`.**

- Every quantitative performance claim in the paper must trace to a `PASS` or `BASELINE` row in `results.tsv`
- The row must include: experiment ID, full commit hash, metric value, and status
- If the experiment was run but not logged: the result is unverifiable — use `TODO_RESULT_NEEDED:` until it is logged
- If the experiment crashed (`CRASH` status): the partial output is not a result — never cite it as one
- If the experiment was discarded (`FAIL` status): it may not appear as a positive result in the paper

**Forbidden pattern:**
> "We tried increasing the learning rate and observed a 0.3% improvement."

(if there is no `EXP-N` row in `results.tsv` showing this, with a commit hash)

**Correct pattern when result is missing:**
```
TODO_RESULT_NEEDED: run lr=1e-3 experiment and log to results.tsv before writing this claim
```

---

## Rule 12: Result Logs Must Include Commit, Metric, Status, Description

**A result is only citable if its `results.tsv` row has all four fields populated:**

| Field | Required | Forbidden value |
|-------|----------|----------------|
| `commit_hash` | Full 40-char hash | Abbreviated, estimated, or "N/A" |
| `metric_value` | Parsed from log file | Estimated, rounded without justification, or NaN for PASS rows |
| `status` | One of BASELINE / PASS / FAIL / CRASH | Blank, "maybe", or "partial" |
| `description` | Experiment hypothesis written before the run | "test", "run1", or blank |

A row missing any of these four fields is invalid. The result may not be cited until the row is complete.

If a result file exists but the TSV row was never written: backfill using `/result-backfill` — do not reconstruct from memory.

---

## Rule 13: Paper Claims Cannot Cite Unlogged Experiments

**The evidence chain must be complete before a claim enters the draft.**

Required chain for any quantitative paper claim:

```
results.tsv (PASS row) → evidence_ledger.md (EV-EXP-N) → claim-evidence-table.md → paper.tex
```

If any link in this chain is missing, the claim must be written as:
```
TODO_RESULT_NEEDED: [description of the missing link]
```

Specific forbidden patterns:

| Situation | Forbidden | Correct |
|-----------|-----------|---------|
| Experiment run but not in results.tsv | Write the claim | Add to results.tsv first |
| In results.tsv but not in evidence_ledger.md | Write the claim | Run /result-backfill |
| In evidence_ledger.md but FAIL/CRASH status | Write as a positive result | Mark as failed; use TODO |
| In evidence_ledger.md but EV-LIT not verified | Write "prior work does X" | Run paper-qa query first |

---

## Rule 14: Forbidden Unsupported Phrases

The following phrases may only be used when explicit, verified evidence supports them. Using them without evidence is a violation.

| Phrase | Required evidence |
|--------|-----------------|
| state-of-the-art | Comparison table showing top result on all stated benchmarks |
| significantly better | Statistical significance test OR practical significance defined |
| first | paper-qa query confirming no prior work; labeled "to our knowledge" |
| novel | Prior-art check at Stage 6 with threat ≤ Medium |
| robust | Cross-domain or cross-seed results confirming stability |
| generalizes | Results on ≥2 distinct datasets/settings |
| outperforms | Results table showing higher metric than every stated method |
| comprehensive | Coverage of all major approaches in the field verified |
| substantially improves | Quantified gain that meets minimum delta in Target Result Contract |
| solves | Complete problem solution — extremely rare; almost always overclaim |
| eliminates hallucination | Cannot be claimed for probabilistic systems |
| guarantees | Mathematical proof required |
| universally | Results on all possible inputs/settings — almost always overclaim |

If evidence is weak: soften the claim ("suggests", "tends to", "in our experiments").

---

## Rule 15: Five Additional TODO Markers

Beyond the existing TODO set, use these for new situations:

| Situation | Marker |
|-----------|--------|
| Novelty claim not yet verified | `TODO_NOVELTY_CHECK_NEEDED: [claim]` |
| Venue fit not yet confirmed | `TODO_VENUE_FIT_NEEDED: [requirement]` |
| SOTA value not yet verified | `TODO_SOTA_NEEDED: [method] on [dataset]` |
| Hypothesis not yet tested | `TODO_HYPOTHESIS_PENDING: HYP-[N]` |
| Prior-art threat not yet resolved | `TODO_PRIOR_ART_NEEDED: [paper]` |

**Complete TODO marker set:**

| Marker | Situation |
|--------|-----------|
| `TODO_CITATION_NEEDED:` | Citation key not in references.bib |
| `TODO_RESULT_NEEDED:` | Experiment result not yet run |
| `TODO_EVIDENCE_NEEDED:` | Literature evidence not yet found |
| `TODO_FIGURE_NEEDED:` | Figure not yet created |
| `TODO_BIBINFO_NEEDED:` | Missing bib field (pages, volume, etc.) |
| `TODO_NOVELTY_CHECK_NEEDED:` | Novelty claim not verified via prior-art check |
| `TODO_VENUE_FIT_NEEDED:` | Venue suitability not confirmed |
| `TODO_SOTA_NEEDED:` | SOTA value unknown for this dataset/metric |
| `TODO_HYPOTHESIS_PENDING:` | Hypothesis not yet tested |
| `TODO_PRIOR_ART_NEEDED:` | Specific threat paper not yet assessed |

---

## Self-Check Before Writing Any Claim

Before writing any factual sentence in the paper, ask:

1. **Is this number from a real file?** → If no: `TODO_RESULT_NEEDED:`
2. **Is this citation in references.bib?** → If no: `TODO_CITATION_NEEDED:`
3. **Is this claim about prior work based on a paper I've read (via paper-qa)?** → If no: remove or hedge
4. **Does this novelty claim survive a paper-qa search?** → If unsure: soften to "to our knowledge"
5. **Am I paraphrasing something from training data?** → Stop. Use paper-qa instead.
6. **Is this phrase in the forbidden list (Rule 14)?** → If unsupported: soften or remove.
7. **Is this result from a PASS/BASELINE row in results.tsv?** → If no: `TODO_RESULT_NEEDED:`
8. **Does this performance claim satisfy the Target Result Contract?** → If no: do not make the claim.
