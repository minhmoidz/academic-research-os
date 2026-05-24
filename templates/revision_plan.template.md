# Revision Plan

**Paper:** [working title]  
**Review date:** [YYYY-MM-DD]  
**Reviewer:** [Claude review pass / human reviewer / both]  
**Based on:** [review report filename]

---

## P0 Findings (Must Fix Before Submission)

| ID | Section | Finding | Fix | Status |
|----|---------|---------|-----|--------|
| P0-1 | [section] | [description of critical issue] | [specific fix] | [TODO / IN PROGRESS / DONE] |
| P0-2 | [section] | [description] | [fix] | [TODO] |

---

## P1 Findings (Strong Recommendations)

| ID | Section | Finding | Fix | Status |
|----|---------|---------|-----|--------|
| P1-1 | [section] | [description] | [fix] | [TODO] |
| P1-2 | [section] | [description] | [fix] | [TODO] |

---

## P2 Findings (Minor / Optional)

| ID | Section | Finding | Fix | Status |
|----|---------|---------|-----|--------|
| P2-1 | [section] | [description] | [fix] | [TODO] |

---

## Revision Protocol

1. Fix all P0 findings first — do not start P1 until P0 is complete
2. After fixing P0, re-run the relevant review passes from `/review-paper`
3. Fix P1 findings in order of severity
4. For any fix involving numerical claims: verify the number did not change
5. For any fix involving citations: verify `\cite{key}` keys are preserved
6. After all fixes: re-run full `/review-paper` (12 passes)
7. If any new P0 findings appear: add them to this plan

---

## Rules During Revision

- Never alter `\cite{}`, `\label{}`, `\ref{}`, `\eqref{}` keys
- Never change numerical values while fixing prose
- Never add new claims without a corresponding EVID entry
- If a claim looks wrong: flag it with `TODO_RESULT_NEEDED:`, do not silently "correct" it

---

## Re-Run Checklist

After all fixes are applied:

- [ ] 12-pass review re-run: `/review-paper`
- [ ] LaTeX compiles cleanly: `tectonic [paper].tex`
- [ ] All TODO markers resolved or documented as acceptable
- [ ] PDF inspected visually (figures, tables, page balance)
- [ ] Submission checklist re-checked: `/submission-check`
