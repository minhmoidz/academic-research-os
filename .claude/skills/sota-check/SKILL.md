# SKILL: /sota-check
## Purpose
Identify the current state-of-the-art results on the target task and datasets to establish what performance level is required to make a credible contribution claim.

---

## When to Run
- Stage 5 (Prior-Art Competition Assessment) of the research workflow.
- Any time a claim of "outperforms SOTA" or "achieves competitive results" is being drafted.
- Before committing to a target venue tier.
- Before finalizing target_result_contract.md.

---

## Required Inputs
| Input | Source |
|-------|--------|
| Target task name | User / research_direction.md |
| Target dataset(s) | User / hypothesis_registry.md |
| Primary metric (e.g., AUC, Accuracy, F1) | User / hypothesis_registry.md |

---

## Steps

### Step 1 — Load Prior-Art Baseline
1. Read `.claude/research-os/25_PRIOR_ART_COMPETITION.md` for the SOTA assessment template and verification rules.
2. Read `sota_baseline_table.md` if it already exists (do not overwrite verified values).

### Step 2 — Query Paper-QA for Best Known Results
For each (dataset, metric) pair, run:
```
pqa ask "What is the best known [metric] result on [dataset] for [task]? Include method name, authors, year, and venue."
```
- Record each result returned, including the PDF source pqa cites.
- If pqa returns no result: mark the cell as `TODO_SOTA_NEEDED` (never fabricate).

### Step 3 — Supplement with Additional Queries
Run secondary queries to catch recent unpublished-but-public results:
```
pqa ask "What methods have reported results on [dataset] for [task] in the last two years?"
pqa ask "Is there a leaderboard or benchmark comparison for [task] on [dataset]?"
```

### Step 4 — Build the SOTA Baseline Table
Create or update `sota_baseline_table.md` with the following columns:

| Method | Dataset | Metric | Best Known Value | Source (bib key) | Year | Venue | Verified By |
|--------|---------|--------|-----------------|------------------|------|-------|-------------|

Verification policy:
- **Verified By** must be one of: `pqa`, `manual-read`, `author-confirmed`.
- Values from paper-qa response are marked `pqa`.
- Values you personally looked up in a PDF are marked `manual-read`.
- Never mark a value `verified` without a source entry.
- Leave cells `TODO_SOTA_NEEDED` when no reliable source is found.

### Step 5 — Load Our Current Best Result
Read `results.tsv` and extract the best PASS result for each (dataset, metric) pair.

Format from results.tsv:
```
run_id | timestamp | commit_hash | experiment_type | hypothesis_id | dataset | metric | value | direction | baseline_comparison | status | evidence_id | notes
```
Filter: `experiment_type=CONFIRMATORY`, `status=PASS`.

### Step 6 — Compute Gap Analysis
For each (dataset, metric) pair where both SOTA and our result exist:

```
gap = our_value - sota_best_value   (for higher-is-better metrics)
gap = sota_best_value - our_value   (for lower-is-better metrics)
```

Classify:
- **Exceeds SOTA:** gap > 0 and gap > noise floor (> 0.5% AUC / > 1.0 pp Accuracy recommended minimum)
- **Competitive:** gap is within ±1% of best known result
- **Below SOTA:** gap < 0

### Step 7 — Report
Output a summary block:

```
SOTA CHECK REPORT — [date]
Task: [task]
Primary metric: [metric]

Dataset: [name]
  SOTA best:  [value] ([Method], [Year])
  Our best:   [value] (EXP-N, commit [hash])
  Gap:        [+/-X.XX] → [Exceeds SOTA / Competitive / Below SOTA]

Overall assessment: [statement]
Minimum to claim SOTA on all datasets: [values per dataset]
```

### Step 8 — Update project_state.md
Add entry:
```
sota_check_complete: true
sota_check_date: [date]
sota_check_verdict: [Exceeds/Competitive/Below]
```

---

## Output Files
- `sota_baseline_table.md` — created or updated
- `project_state.md` — updated

---

## Safety Rules
1. **Never fill SOTA values from memory or training data.** Every value must be cited to a specific PDF source or `TODO_SOTA_NEEDED`.
2. **Never claim "achieves SOTA" in the paper** without this table being fully verified (no TODO cells for the claimed datasets).
3. **Never omit inconvenient SOTA results.** If a method outperforms ours on any dataset, it must appear in the table.
4. **If pqa returns a result with low confidence:** mark the value as `pqa-low-confidence` and require manual verification before using in claims.
5. **Do not modify existing verified values** — if you find a contradiction, add a new row marked `CONFLICT` and flag for human resolution.

---

## Common Failure Modes to Avoid
- Reporting our best result on a held-out test split as "SOTA" when the prior best was on the same split.
- Using validation-set numbers to compare against test-set SOTA.
- Missing concurrent arXiv papers that are already indexed in pqa but not yet published.
- Ignoring domain-specific baselines (e.g., pretrained encoders for the target domain).
