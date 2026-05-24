# Figure and Format Playbook

---

## Part 1: Figure Design

### When to Use thesis-figure-skill

Use `thesis-figure-skill` for:
- Architecture diagrams (model pipeline, module connectivity)
- Method diagrams (algorithm flow, data transformation pipeline)
- Conceptual figures (bias illustration, motivation diagrams)
- Any figure that will be embedded directly in the `.tex` file as TikZ code

**Invocation:** `/thesis-figure-skill` → describe the figure, specify TikZ output

### When to Use latex-figure-specialist (academic-writing-agents)

Use `academic-writing-agents:latex-figure-specialist` for:
- Editing and adjusting existing TikZ/pgfplots figures
- Fixing label/ref wiring issues
- Adjusting layout within an existing figure
- Adding or modifying pgfplots charts

### TikZ vs draw.io XML

| Criterion | TikZ | draw.io XML |
|-----------|------|-------------|
| Output format | Embeds in .tex | External image (PNG/SVG) |
| Reproducibility | Perfect (code is the figure) | Needs draw.io to edit |
| Style consistency | Matches paper fonts/colors | May look different |
| Use for | Architecture diagrams, bar charts, flowcharts in paper | Slides, talks, external presentations |
| Quality | Publication-ready | Good for drafts |

**Default: use TikZ for all figures in the paper.**

---

### Architecture Figure Design Rules

1. **Two-column papers:** Figure width ≤ `\columnwidth` for single-column figures, ≤ `\textwidth` for full-width
2. **Color convention:** Use consistent colors for proposed vs. existing components (e.g., blue = backbone, orange = proposed)
3. **Font size:** Use `\footnotesize` or `\scriptsize` inside TikZ for readability
4. **Labels:** Every module box must have a label. Every arrow must have a direction.
5. **No hardcoded formulas:** Figures show mechanisms, not specific hyperparameter values (e.g., "entropy-guided reweighting" not "w_g = 0.7 + 0.8H̃_g")
6. **Caption:** Caption must explain what each color/box/arrow represents
7. **Cross-reference:** Figure must be `\ref{}`'d in the text before it appears

### Bar Chart / Plot Design Rules (pgfplots)

1. **Y-axis:** Always starts at a value that shows meaningful differences (not always 0)
2. **X-tick labels:** Sufficient `text width` to prevent line wrapping (e.g., `text width=2.0cm`)
3. **Legend:** Inside the plot area or at top, not below where it wastes space
4. **Grid lines:** `dotted, gray!30` — subtle, not distracting
5. **Colors:** Use named colors defined in preamble, not inline RGB
6. **Bar width:** Scale to bar count — typically 7pt for 2 bars, 5pt for 3+

### Figure Content Rules

- Every data point in a figure must come from a real result file
- Annotation values (e.g., "0.897×") must match the analysis result files exactly
- Do not smooth or interpolate curves without stating it explicitly

---

## Part 2: Table Design

### Table Formatting Rules (IEEEtran two-column)

1. Use `\footnotesize` for table content in two-column papers
2. Use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`) — not `\hline`
3. Caption ABOVE the table (`\caption{}` before `\begin{tabular}`)
4. Column widths: use `p{Xcm}` for text, `>{\centering}p{Xcm}` for centered numbers
5. Bold the best result, underline the second-best in results tables
6. Add dataset size `\tiny(N=152)` in column headers for context
7. `\setlength{\tabcolsep}{3.5pt}` to tighten spacing if needed
8. `\renewcommand{\arraystretch}{1.15}` for readability

### Table Content Rules

- Every number in the table must have a source in `result-map.md`
- Std values must use the same formula (population or sample) across ALL rows
- Missing baselines: either exclude entirely OR mark with `—` with footnote explaining why

---

## Part 3: LaTeX Compilation

### Compiling with Tectonic (Preferred)

```bash
tectonic conference_paper.tex
```

Tectonic auto-downloads packages, handles multi-pass for cross-references, and produces clean output. The 0.8–1.0pt vbox warning from `balance` package is normal.

### Compiling with pdflatex

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

Three passes required: first for aux file, bibtex for references, two more to resolve all cross-references.

### Debugging LaTeX Errors

**Common errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `Undefined control sequence` | Package not loaded or typo | Check `\usepackage` list |
| `Overfull \hbox (Xpt)` | Long word/formula overflows column | Add `\-` hyphenation hint or `\allowbreak` |
| `Overfull \vbox (Xpt)` | Column content slightly too tall | If <1pt: ignore. If >3pt: check float placement |
| `Undefined references` | `\ref{key}` or `\cite{key}` not found | Check label/key spelling; recompile twice |
| `Float too large` | Figure exceeds page height | Reduce figure size or use `[p]` placement |

### Bibliography Tips

- Use `\IEEEtriggeratref{N}` to control column break in bibliography (IEEEtran)
- Use `\usepackage{balance}` + `\balance` inside bibliography for last-page equalization
- Run `bibliography-auditor` agent to find: arXiv-only citations, missing page numbers, inconsistent venue names

---

## Part 4: Column Balance for Two-Column Papers

### Last Page Optimization

1. Preferred: natural flow with `\balance` placed inside the bibliography at ~50% point of last-page content
2. Alternative: `\IEEEtriggeratref{N}` with N chosen to fill the last full column on the penultimate page
3. Last-page column at 70–85% fill is acceptable and normal

### Float Placement

- Use `[!t]` for figures and tables (forces top-of-column)
- For a figure that must be near its reference: use `[!ht]`
- Never use `[h]` alone in a two-column paper — floats will drift
- Check float proximity: every float should appear within 1 column of its first citation

---

## Part 5: Preserving Scientific Meaning

When improving figure aesthetics, **never change:**
- Data values displayed in plots
- Axis ranges that encode meaningful comparison
- Color meanings defined in captions
- Arrow directions in architecture diagrams
- Module names or acronyms

When improving table formatting, **never change:**
- Numerical values in cells
- Bold/underline designations (these encode rankings)
- Column header text (these define the measurement)
