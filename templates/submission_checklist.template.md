# Submission Checklist

**Paper:** [title]  
**Target venue:** [venue]  
**Submission deadline:** [YYYY-MM-DD HH:MM timezone]  
**Checklist completed by:** [YYYY-MM-DD]

---

## Section 1: Content Gates

- [ ] Stage 17 Evidence Freeze passed (`evidence_status: FROZEN` in `project_state.md`)
- [ ] All P0 review findings resolved
- [ ] No `TODO_` markers remaining in `.tex` file
- [ ] All `\cite{key}` keys resolved in `references.bib`
- [ ] All `\ref{}` and `\eqref{}` labels resolve without warnings
- [ ] All claims in paper traced to EVID entries in `claim-evidence-table.md`

---

## Section 2: Results Verification

- [ ] All numbers in tables verified against source files in `results.tsv`
- [ ] Std formula consistent (population or sample) across all rows
- [ ] All [K]-fold runs completed (no partial fold averaging)
- [ ] Baseline results use same seeds and splits as proposed method

---

## Section 3: LaTeX and PDF

- [ ] Compiles without errors: `tectonic [paper].tex`
- [ ] No overfull/underfull hbox warnings in final sections
- [ ] Column balance correct (two-column layouts)
- [ ] All figures render correctly at print resolution
- [ ] Figure captions complete and accurate
- [ ] Table alignment and formatting correct
- [ ] Page limit not exceeded

---

## Section 4: References

- [ ] No unresolved `\cite{}` (no `?` in compiled PDF)
- [ ] All authors spelled correctly
- [ ] All venues spelled correctly (no "Workshop" vs "Conference" mix-up)
- [ ] No arXiv-only citations for key claims (if venue requires published refs)
- [ ] BibTeX entry types correct (@inproceedings vs @article vs @misc)

---

## Section 5: Venue Requirements

- [ ] Abstract within word limit
- [ ] Paper within page limit (excluding references)
- [ ] Anonymized (if blind review): no author names, no self-identifying references
- [ ] Supplementary material within limit (if applicable)
- [ ] Ethics/reproducibility statement included (if required)
- [ ] Code/data availability statement included (if required)

---

## Section 6: Final Review

- [ ] `/review-paper` 12-pass review completed
- [ ] All P0 findings resolved
- [ ] PDF proofread end-to-end
- [ ] Abstract matches paper content exactly
- [ ] Conclusion matches experimental results exactly

---

## Sign-Off

Checklist completed: [YYYY-MM-DD]  
Submitted to: [venue name]  
Submission ID: [ID or "pending"]  
Confirmation received: [YES / NO]
