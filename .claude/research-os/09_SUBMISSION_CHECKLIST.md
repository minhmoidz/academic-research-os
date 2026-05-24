# Final Submission Checklist

Complete every item before submitting. No item may be skipped.

---

## A. Content Completeness

- [ ] All TODO markers resolved or intentionally left as future work (search: `grep -n "TODO_" paper.tex`)
- [ ] All `TODO_CITATION_NEEDED:` replaced with real `\cite{key}` entries
- [ ] All `TODO_RESULT_NEEDED:` replaced with verified numbers from result files
- [ ] All `TODO_EVIDENCE_NEEDED:` resolved via paper-qa or converted to hedged claims
- [ ] All `TODO_FIGURE_NEEDED:` replaced with actual figures
- [ ] Abstract matches final result tables (spot-check all numbers)
- [ ] Introduction contributions match what experiments actually show
- [ ] Conclusion does not claim anything not shown in experiments
- [ ] Limitations honestly states scope restrictions
- [ ] Author names and affiliations are real (no placeholder names)

---

## B. Citations and Bibliography

- [ ] All `\cite{key}` keys exist in references.bib (`grep "\cite{" paper.tex | sort -u` vs `grep "@" references.bib`)
- [ ] All references.bib entries are used (no ghost entries)
- [ ] All proceedings entries have: pages, in-proceedings name
- [ ] All journal entries have: volume, issue number (`no.~X`), pages, year
- [ ] No arXiv-only citations for papers published in peer-reviewed venues
- [ ] Author names use `~` for non-breaking spaces: `A.~Lastname`
- [ ] Title field capitalization: proper nouns and acronyms in `{}`
- [ ] Venue names consistent across all entries
- [ ] `bibliography-auditor` agent run with no Critical findings

---

## C. Results and Claims

- [ ] `result-map.md` completed: every table cell traced to a source file
- [ ] Std values computed consistently (all population std OR all sample std — confirmed)
- [ ] All 5 folds completed for all methods (no partial averaging)
- [ ] Baseline results confirmed to use same preprocessing and evaluation protocol as proposed method
- [ ] Ablation results confirmed to isolate single variables
- [ ] Sensitivity table results confirmed from fold-0 runs
- [ ] Multi-seed results (if any) from real multiple seeds, not one seed

---

## D. Figures and Tables

- [ ] All figures cited in text with `\ref{fig:X}` before they appear
- [ ] All tables cited in text with `\ref{tab:X}` before they appear
- [ ] All `\label{fig:X}` and `\label{tab:X}` are referenced somewhere
- [ ] Figure captions are self-contained (readable without the text)
- [ ] Table captions are above the table body
- [ ] Bold = highest per column, underline = second highest (consistent throughout)
- [ ] No data values in figures that differ from the main tables
- [ ] All figures have appropriate size for single/double column
- [ ] `latex-layout-auditor` run: no float on isolated page, last page balanced

---

## E. Equations and Math

- [ ] All `\label{eq:X}` are referenced with `\eqref{eq:X}` somewhere in the text
- [ ] All mathematical symbols defined on first use
- [ ] Notation consistent throughout (same variable name for same quantity)
- [ ] Dimensions of all tensors/vectors stated explicitly or inferable from context
- [ ] All temperature/hyperparameter values in equations match config files

---

## F. LaTeX Compilation

- [ ] PDF compiles cleanly with tectonic or pdflatex (no critical errors)
- [ ] No undefined references (`grep "?" paper.log` for `?` in output — means undefined ref)
- [ ] No overfull hboxes > 2pt
- [ ] Page count within venue limit (check venue requirements)
- [ ] Margins match venue template (IEEEtran: auto; custom venues: verify)
- [ ] Blind review compliance: author names hidden if required by venue
- [ ] All required sections present (check venue call for papers)
- [ ] File size acceptable (typical: < 10MB for conference; check venue)

---

## G. Scope and Honesty

- [ ] Every "to our knowledge, the first" qualified and defensible
- [ ] Every "state-of-the-art" claim backed by a comparison table showing it
- [ ] Every "consistently improves" backed by improvement on ALL benchmarks stated
- [ ] Statistical significance caveat present if n < 30 folds
- [ ] Limitations honest about: data scope, statistical power, generalization limits
- [ ] Inference-time overhead disclosed if significantly worse than baselines

---

## H. Pre-submission Final Checks

- [ ] 10 review passes from `08_REVIEW_AND_AUDIT_PLAYBOOK.md` completed
- [ ] No unresolved Critical findings from any review pass
- [ ] Supplementary materials (if any) compiled and page-counted
- [ ] PDF rendered correctly (no blank pages, no missing figures)
- [ ] All co-authors have read and approved the final draft
- [ ] Submission system requirements checked (file format, anonymization, page limit)

---

## Sign-off

When all items above are checked, fill in:

```
Submission checklist completed: [date]
Target venue: [venue name, year]
Submission deadline: [date]
Submitted by: [name]
Final PDF: [filename]
Git commit / version: [hash or tag]
```
