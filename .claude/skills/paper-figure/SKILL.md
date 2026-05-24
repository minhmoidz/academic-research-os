# Skill: /design-figure

Create or adjust a figure for the paper using TikZ or pgfplots.

---

## Trigger

User types `/design-figure [figure-description]` or invokes via Skill tool.

---

## Required Input (ask if missing)

1. What the figure should show (describe in plain language)
2. Figure type: architecture diagram / bar chart / line plot / flow diagram / conceptual
3. Data source (for plots): which result file contains the values?
4. Column constraint: single-column (`\columnwidth`) or full-width (`\textwidth`)?
5. Color convention for this paper (e.g., blue = backbone, orange = proposed)

---

## Execution Steps

### Step 1: Read system file

```
Read .claude/research-os/07_FIGURE_AND_FORMAT_PLAYBOOK.md § Part 1
```

### Step 2: Choose tool

**Architecture / pipeline / conceptual diagrams:**
Use `thesis-figure-skill` (native skill).
Produce TikZ code embedded directly in `.tex`.

**Adjusting existing TikZ / pgfplots:**
Use `academic-writing-agents:latex-figure-specialist`.

**Bar charts and plots:**
Use pgfplots inside a `tikzpicture` environment.

### Step 3: Apply design rules

**Architecture figures:**
- Width: ≤ `\columnwidth` for single-column, ≤ `\textwidth` for full-width
- Font: `\footnotesize` or `\scriptsize` inside TikZ
- Every box must have a label; every arrow must have a direction
- No hardcoded hyperparameter formulas in boxes (mechanism only)
- Caption must explain what each color/box/arrow represents

**Bar charts (pgfplots):**
- Y-axis: start at value showing meaningful differences (not always 0)
- X-tick labels: set `text width=2.0cm` (minimum) to prevent line wrapping
- Bar width: 7pt for 2 bars, 5pt for 3+ bars
- Grid: `dotted, gray!30`
- Legend: inside plot area or at top — not below

### Step 4: Verify data values

For any plot:
1. Open the source result file
2. Copy each data value exactly
3. Verify annotation values (e.g., ratio labels) match analysis files

**Never interpolate, smooth, or estimate plot values.**

### Step 5: Wire label and reference

Ensure:
- Figure has `\label{fig:X}`
- Figure is `\ref{fig:X}`'d in the text **before** it appears
- Caption is self-contained (readable without the surrounding text)

---

## Safety Rules

- Data values in plots must exactly match result files
- Do not claim more than the figure shows in the caption
- No hardcoded hyperparameter formulas in figure boxes
- Do not change color meanings defined in the caption

---

## Output

TikZ code block ready to embed in `.tex`, followed by:
```
Figure: fig:[label]
Data source: [result file path]
Referenced in text at: [section/paragraph]
Caption: [proposed caption text]
```
