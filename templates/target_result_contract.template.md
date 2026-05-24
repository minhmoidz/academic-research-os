# Target Result Contract

**Contract ID:** TRC-[NNN]  
**Created:** [YYYY-MM-DD]  
**Status:** [DRAFT / SIGNED / ACTIVE / COMPLETED / SUPERSEDED]  
**Linked venue:** [venue_target.md]  
**Linked hypotheses:** [HYP-NNN, HYP-NNN]

---

## ⚠️ Binding Agreement

This contract defines the minimum results required for this research to support a submission to the target venue. It is binding from the moment it is signed. It may NOT be modified after confirmatory experiments begin without a DEC log entry.

---

## Primary Metric

- **Metric name:** [e.g., mean AUC, Recall@10, accuracy, F1]
- **Averaging:** [e.g., mean over 5-fold cross-validation, mean over 3 seeds]
- **Std formula:** [population std ÷N or sample std ÷(N-1) — choose ONE and apply consistently]

---

## Minimum Thresholds (Pass Criteria)

| Criterion | Threshold | Rationale |
|-----------|-----------|-----------|
| Primary metric on [Dataset-A] | > [X.XX] | Exceeds [BestKnownBaseline] by ≥ [delta] |
| Primary metric on [Dataset-B] | > [X.XX] | Non-negative vs. [BestKnownBaseline] |
| Cross-fold std | < [Y.YY] | Stable enough for reproducibility claim |
| Delta over SOTA | ≥ [Z]pp | Minimum meaningful improvement for [Venue Tier] |
| Ablation completeness | All [N] ablations must run | Required for contribution defensibility |

---

## Required Experiments

- [ ] Confirmatory run: [ProposedMethod] on [Dataset-A], all [K] folds
- [ ] Confirmatory run: [ProposedMethod] on [Dataset-B], all [K] folds
- [ ] Baseline run: [BaselineModel] on [Dataset-A] (same splits, same seeds)
- [ ] Baseline run: [BaselineModel] on [Dataset-B]
- [ ] Ablation: [Component A] removed
- [ ] Ablation: [Component B] removed
- [ ] Ablation: [Component A+B] removed (full model vs. baseline)

---

## Failure Conditions

If any of the following occurs, this TRC is NOT met and `/pivot-decision` must be run:

- Primary metric on [Dataset-A] ≤ [BestKnownBaseline] value
- Cross-fold std > [Y.YY]pp (result too noisy to claim)
- Any ablation not completed (partial ablation = no ablation claim)
- Fewer than [K] folds completed for any confirmatory run

---

## Sign-Off

Signed by user on [YYYY-MM-DD]: [YES / NO]

*After sign-off: do not lower thresholds. Do not redefine the primary metric. Any modification requires a new DEC log entry.*

---

## Modification Log

| Date | Change | Reason | DEC entry |
|------|--------|--------|-----------|
| [YYYY-MM-DD] | [what changed] | [why] | DEC-[YYYY-MM-DD]-[NNN] |
