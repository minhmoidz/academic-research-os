# Skill: /format-paper

Compile, format, and fix LaTeX layout issues for a two-column IEEE conference paper.

---

## Trigger

User types `/format-paper` or invokes via Skill tool.

---

## Required Input (ask if missing)

1. Path to .tex file
2. Path to references.bib
3. Specific issue to fix (optional — if not provided, runs full compilation check)

---

## Execution Steps

### Step 1: Read system file

```
Read .claude/research-os/07_FIGURE_AND_FORMAT_PLAYBOOK.md
```

### Step 2: Compile with tectonic

```bash
tectonic [paper.tex]
```

Preferred compiler. Handles multi-pass automatically.

If tectonic not found at default path, try: `tectonic`

**Fallback (pdflatex):**
```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

### Step 3: Check compilation log

Look for:
- Undefined references (`?` in output)
- Overfull hboxes > 2pt
- Float placement warnings
- Missing citation keys

### Step 4: Fix layout issues

**Overfull hboxes:** Add `\-` hyphenation or `\allowbreak` at the overflow point.

**Column balance on last page:**
1. Add `\usepackage{balance}` to preamble if not present
2. Place `\balance` inside `\begin{thebibliography}` after the midpoint bibitem
3. Do NOT place `\balance` before `\begin{thebibliography}` — causes severe imbalance

**Float placement:**
- Use `[!t]` for figures and tables
- Use `[!ht]` only when figure must be near its citation
- Never use `[h]` alone in two-column papers

**Bibliography column break:**
- Use `\IEEEtriggeratref{N}` only when natural flow is broken
- Remove if it causes refs to jump to a new page alone

### Step 5: Verify output

- [ ] PDF compiles cleanly (no errors)
- [ ] No undefined references
- [ ] No overfull hboxes > 2pt
- [ ] Last page columns at 70–100% fill
- [ ] No isolated floats (figure alone on a page)
- [ ] Page count within venue limit

---

## Safety Rules

- **Never change numerical content while fixing formatting**
- **Never alter citation keys while fixing bibliography**
- **Never alter `\label{}`, `\ref{}`, `\eqref{}` while fixing layout**
- If fixing a float forces content rearrangement, check that no claim changed scope

---

## Output

```
Compilation: ✓ Clean / ✗ [N errors]
Overfull hboxes: [N found, M > 2pt]
Undefined references: [list]
Page count: [N] pages
Last page balance: [left%] / [right%]
Layout issues fixed: [list]
```
