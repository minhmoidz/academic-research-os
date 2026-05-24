# Review and Audit Playbook

Run all 10 passes before declaring paper ready for submission. No shortcutting.

---

## Overview: 10 Review Passes

| Pass | Tool | Finds |
|------|------|-------|
| 1. Logic | `logic-reviewer` | Argument gaps, unsupported conclusions |
| 2. Technical | `technical-reviewer` | Math errors, methodology problems |
| 3. Claim-evidence | `consistency-checker` + manual | Claims without evidence pointers |
| 4. Citation | `bibliography-auditor` | Missing/wrong citations |
| 5. Writing/style | `writing-reviewer` | Grammar, clarity, academic tone |
| 6. De-AI | `prose-polisher` + manual | AI-pattern prose signatures |
| 7. Figure/table | `latex-figure-specialist` + `consistency-checker` | Caption mismatch, data errors |
| 8. LaTeX/layout | `latex-layout-auditor` | Float placement, column balance |
| 9. Paper-code alignment | `technical-reviewer` + manual log check | Results match real experiments |
| 10. Final skeptical | `logic-reviewer` full re-read | Holistic quality gate |

---

## Pass 1: Logic Review

**Tool:** `academic-writing-agents:logic-reviewer`

**Prompt pattern:**
```
Review [file.tex] for logical flow, argument structure, and narrative coherence.
Check: abstract chain (problem→gap→fix→evidence), contribution-to-experiment alignment,
ablation conclusion validity, claim-evidence matching across all sections.
Rate findings: Critical / Minor.
```

**Severity:**
- Critical: Conclusion not supported by shown evidence; contribution claimed but no experiment for it
- Minor: Transition awkward; paragraph order suboptimal

**How to turn findings into revisions:**
1. Critical: Fix before any other pass
2. Minor: Fix in Pass 5 (writing/style) if prose-level; fix in Pass 3 if evidence-level

---

## Pass 2: Technical Review

**Tool:** `academic-writing-agents:technical-reviewer`

**Check list:**
- All equations: notation consistent, dimensions correct
- Method description: matches code (check against actual implementation)
- Hyperparameter values in paper match config files
- Std formula consistent across all result rows (population vs. sample)
- Ablation logic: each row isolates one variable
- Complexity claims (O(G²D) vs O(N²D)) verified
- Auxiliary head architecture matches code

**Severity:**
- Critical: Wrong formula; result not reproducible from stated method; dimension mismatch
- Minor: Inconsistent notation (e.g., H̃ vs Ĥ for the same variable)

---

## Pass 3: Claim-Evidence Review

**Tool:** `academic-writing-agents:consistency-checker` + manual

**Process:**
1. For every quantitative claim in the paper, find its source in `result-map.md`
2. For every "prior work does X" claim, run paper-qa to confirm
3. Flag any claim that cannot be traced to a result file or a verified paper

**Markers to resolve:**
- `TODO_EVIDENCE_NEEDED:` → run paper-qa search, or remove claim
- `TODO_RESULT_NEEDED:` → run experiment or mark explicitly as future work
- `TODO_CITATION_NEEDED:` → find verified paper or remove attribution

**Severity:**
- Critical: Claim in paper has no traceable evidence (fabrication risk)
- Minor: Hedging language inconsistency

---

## Pass 4: Citation Review

**Tool:** `academic-writing-agents:bibliography-auditor`

**Check list:**
- All `\cite{key}` keys exist in references.bib
- All references.bib entries have: authors, title, venue, year, pages (for proceedings)
- No arXiv-only citations for results that have been published in peer-reviewed venues
- Title capitalization: proper nouns and acronyms capitalized in `{}`
- Venue names consistent (e.g., always "Proc. NeurIPS" not mix of "NeurIPS" and "Advances in NeurIPS")
- Issue numbers present for journal articles (`no.~X`)
- No ghost entries (bibitems with no \cite in the paper)

---

## Pass 5: Writing/Style Review

**Tool:** `academic-writing-agents:writing-reviewer`

**Focus areas:**
- Grammar errors
- Passive voice overuse
- Sentence length variation (no paragraph of all-similar-length sentences)
- Forbidden phrases: "It is worth noting", "Furthermore", "Moreover", "In this paper we", "leverage", "facilitate", "encompasses"
- Hedging calibration: "suggest" vs "show" vs "demonstrate" (match to evidence strength)
- Pronoun clarity: "this" and "these" at sentence start must have clear antecedents

After this pass: run `latex-rhythm-refiner` on the full `.tex` file for rhythm.

---

## Pass 6: De-AI Review

**Tool:** Manual + `academic-writing-agents:prose-polisher`

**Patterns to find and fix:**

| AI Pattern | Detection | Fix |
|-----------|-----------|-----|
| Perfectly parallel N-item list | All items: same syntactic form | Break 1–2 items to different structure |
| "The following subsections detail..." | Meta-commentary | Delete or replace with technical content |
| "Together, these choices yield a fully end-to-end..." | Template closure | Replace with concrete statement |
| "proves sufficient: X shifts Y toward Z" | Colon-rephrased aphorism | Split into 2 plain sentences |
| "By combining A, B, C, and D, METHOD improves..." | Template completion | Front-load the numbers, not the list |
| "we attribute this to..." × 3 | Repeated framing | Vary: "A likely cause is...", "Our reading is..." |
| 5+ consecutive "The [noun]..." sentences | Parallel opener | Insert first-person opener or connective |

**Invocation:**
```
Use prose-polisher on [section] to improve clarity and vary sentence structure.
Specifically: break parallel list at [lines], remove meta-commentary at [line].
Preserve all \cite, \ref, \label, \eqref, and all numerical values.
```

---

## Pass 7: Figure and Table Review

**Tools:** `academic-writing-agents:latex-figure-specialist`, `consistency-checker`

**Check list:**
- Every figure cited in text before it appears on the page
- Every table cited in text before it appears on the page
- Figure captions are self-contained (don't require reading the text to understand)
- No data values in figures that differ from the main result tables
- No hardcoded hyperparameter formulas in figure boxes (show mechanism, not specific values)
- Column headers in tables match what's actually measured
- Bold/underline designations in tables are correct (highest = bold, second = underline)
- X-tick labels in plots don't wrap to 2 lines while neighbors stay on 1

---

## Pass 8: LaTeX/Layout Review

**Tool:** `academic-writing-agents:latex-layout-auditor`

**Check list:**
- No overfull hboxes > 2pt (visible margin overflow)
- No isolated floats (figure on a page with no text)
- Last page column balance (aim for 70–100% fill both columns)
- Bibliography column distribution natural (no forced breaks causing 20% fill)
- Figure placement within 1 column of first citation
- Tables fit within column width
- No orphaned section headings at bottom of column

**Fix strategy:** See `07_FIGURE_AND_FORMAT_PLAYBOOK.md` Part 3 and 4.

---

## Pass 9: Paper-Code-Result Alignment

**Tool:** Manual + `academic-writing-agents:technical-reviewer`

This is the most important pass for empirical papers. Run it on the compiled PDF against the actual code and result files.

**For every result in every table:**
1. Open the source result file
2. Confirm the number matches the paper
3. Confirm the metric definition matches the code's evaluation script
4. Confirm the dataset split matches the stated protocol

**For every method description in Section III:**
1. Find the corresponding class or function in the code
2. Confirm the architecture matches the text
3. Confirm the training objective matches the loss computation

**Red flags:**
- A result in the paper that differs from any result file by more than rounding
- A module described in the method that doesn't exist in the code
- A hyperparameter in the paper that doesn't match any config file

---

## Pass 10: Final Skeptical Review

**Tool:** `academic-writing-agents:logic-reviewer` (full re-read after all passes)

**The adversarial reviewer test:** Read the paper as a skeptical NeurIPS/CVPR reviewer who:
- Wants to reject papers with unsupported claims
- Checks contribution 1 against Section IV analysis
- Checks "to our knowledge, the first" against their own knowledge
- Asks "what would the result look like if the proposed component didn't help?"
- Asks "is the improvement large enough to matter clinically / practically?"
- Asks "are the baselines fair?"

**Pass criteria:** After this pass, no Critical findings remain. Minor findings may be tolerated if documented.

---

## Severity Levels

| Level | Definition | Action |
|-------|-----------|--------|
| **Critical** | Factual error, unsupported claim, reproducibility blocker, fabrication risk | Must fix before submission |
| **Major** | Logic gap, significant overstatement, layout defect visible at arm's length | Should fix; justify if not |
| **Minor** | Style issue, prose improvement, cosmetic layout, optional strengthening | Fix in final polish pass |
| **Info** | Observation for author's awareness | No action required |
