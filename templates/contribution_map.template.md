# Contribution Map

Project: [project_name]
Date: [YYYY-MM-DD]
Based on: hypothesis_registry.md + gap_statement.md + venue_target.md

---

## Rules

- Every claim listed here must be linked to a registered hypothesis (HYP-NNN).
- Status must be [HYPOTHESIS] until the hypothesis is confirmed (supported) by experiment evidence.
- Status becomes [CONFIRMED] only after the Evidence Freeze (Stage 17) and must include an evidence ID from evidence_ledger.md.
- Claims marked [CONFIRMED] before Stage 17 are protocol violations.
- If a claim is not supported by experiments, remove it or change it to [DROPPED].

---

## Contribution Claims

| # | Claim | Type | Hypothesis ID | Evidence Pointer | Status |
|---|-------|------|--------------|-----------------|--------|
| 1 | [State the specific contribution claim as it will appear in the paper] | [Empirical finding / Method design / Analysis / Dataset] | HYP-[NNN] | [Fig. N / Table N / EV-EXP-N — fill after Evidence Freeze] | [HYPOTHESIS / CONFIRMED / DROPPED] |
| 2 | [Contribution claim 2] | [Type] | HYP-[NNN] | [Evidence pointer or TODO_EVIDENCE_NEEDED] | [HYPOTHESIS] |
| 3 | [Contribution claim 3] | [Type] | HYP-[NNN] | [Evidence pointer or TODO_EVIDENCE_NEEDED] | [HYPOTHESIS] |

---

## Overclaiming Risk Check

Before finalizing claims, verify each of the following:

- [ ] "First" claims verified via paper-qa — no prior work found addressing the same specific point
- [ ] "State-of-the-art" claims backed by a comparison table showing the top result
- [ ] Improvements confirmed on ALL stated benchmarks (not just selected ones)
- [ ] Gains survive ablation attribution (each module individually contributes)
- [ ] No claim uses forbidden phrases without evidence (see `13_ANTI_HALLUCINATION_RULES.md`, Rule 14)

---

## Dropped Claims

List any claims that were planned but later dropped, with the reason:

| Claim (dropped) | Reason | Decision ID |
|----------------|--------|------------|
| [original claim text] | [e.g., "HYP-002 contradicted by EXP-005"] | DEC-[YYYY-MM-DD-NNN] |

---

## Claim Narrative (for Introduction)

[After Stage 17 Evidence Freeze only — draft the contribution bullet points that will appear in the Introduction. Each bullet must reference a CONFIRMED claim above.]

- TODO_EVIDENCE_NEEDED: complete after Evidence Freeze
