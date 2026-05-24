# Result Adequacy Report

**Date:** [YYYY-MM-DD]  
**Stage:** 16 — Result Adequacy Gate  
**TRC reference:** TRC-[NNN]  
**Venue target:** [venue_target.md]

---

## Condition 1: TRC Compliance

| TRC criterion | Required | Achieved | Gap | Pass? |
|--------------|---------|---------|-----|-------|
| Primary metric on [Dataset-A] | > [X.XX] | [Y.YY] | [+/-Z] | [✓/✗] |
| Primary metric on [Dataset-B] | > [X.XX] | [Y.YY] | [+/-Z] | [✓/✗] |
| Cross-fold std | < [Y.YY] | [Z.ZZ] | — | [✓/✗] |
| Delta over SOTA | ≥ [Z]pp | [W]pp | — | [✓/✗] |

**TRC compliance:** [PASS / FAIL]

---

## Condition 2: SOTA Gap

| Method | [Dataset-A] metric | [Dataset-B] metric | Source |
|--------|-------------------|-------------------|--------|
| [BestKnownMethod] (SOTA) | [X.XX] | [X.XX] | sota_baseline_table.md |
| Our method | [Y.YY] | [Y.YY] | results.tsv |
| **Gap** | **[+/-Z]pp** | **[+/-Z]pp** | — |

**SOTA gap assessment:** [POSITIVE / NEGATIVE / NEUTRAL]

---

## Condition 3: Ablation Completeness

| Ablation | Completed? | Result | Contribution confirmed? |
|----------|-----------|--------|------------------------|
| [ModuleA] removed | [✓/✗] | [X.XX] | [Yes/No] |
| [ModuleB] removed | [✓/✗] | [X.XX] | [Yes/No] |
| Full model | [✓/✗] | [X.XX] | — |

**Ablation completeness:** [COMPLETE / INCOMPLETE]

---

## Condition 4: Cross-Dataset Stability

[Describe whether results hold across datasets. Note any dataset-specific patterns.]

**Stability:** [STABLE / MIXED / SINGLE-DATASET ONLY]

---

## Condition 5: Statistical Validity

- Number of folds / seeds: [K]
- Std formula: [population / sample]
- Consistent across all methods: [YES / NO]

**Statistical validity:** [VALID / INVALID]

---

## Condition 6: Claim-Result Alignment

[List any claims that are not supported by the current results. Use TODO_RESULT_NEEDED: for each.]

**Alignment:** [ALIGNED / MISALIGNED — N claims unsupported]

---

## Overall Decision

**Decision: [A / B / C / D / E / F / G]**

| Decision | Meaning |
|---------|---------|
| A | All conditions met — proceed to Evidence Freeze |
| B | TRC met but SOTA gap narrow — proceed with hedged claims |
| C | Ablations incomplete — complete them before proceeding |
| D | Negative SOTA gap — pivot or narrow claim required |
| E | High variance — add seeds or run more folds |
| F | Mixed cross-dataset — limit claim scope to Dataset-A |
| G | Fundamental failure — run /pivot-decision, consider ABANDON |

**Next action:** [Specific action based on decision]
