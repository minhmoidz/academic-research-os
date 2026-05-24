# Skill: /literature-review

Systematic literature collection, paper-qa indexing, and literature matrix building.

---

## Trigger

User types `/literature-review` or invokes via Skill tool.

---

## Required Input (ask if missing)

1. Research question (from paper-brief.md)
2. PDF folder path (where local PDFs are stored)
3. List of search keywords (3–8 terms)

---

## Execution Steps

### Step 1: Read system files

```
Read .claude/research-os/04_LITERATURE_REVIEW_PLAYBOOK.md
Read .claude/research-os/13_ANTI_HALLUCINATION_RULES.md
```

### Step 2: Build paper-qa index

```bash
pqa -i [index-name] index [pdf-folder]
```

Confirm index was built (check output for number of papers indexed).
If paper-qa is not installed: report error, do not proceed.

### Step 3: Run discovery queries

For each keyword provided, query paper-qa:

```bash
pqa -i [index-name] ask "What methods address [keyword]?"
pqa -i [index-name] ask "What are limitations of existing approaches to [keyword]?"
pqa -i [index-name] ask "Does any paper address [gap]?"
```

Record all outputs verbatim. Do not summarize from memory.

### Step 4: Initialize literature-matrix.md

Fill Template 4 from `10_TEMPLATES.md`.
Fill each row from paper-qa output ONLY.
Mark any unknown cell as `?` — never fill from memory or training data.

### Step 5: Generate gap statement

Run the gap query:
```bash
pqa -i [index-name] ask "Does any paper simultaneously address [aspect 1] and [aspect 2]?"
```

Fill the "Gap column summary" in literature-matrix.md from this output.

### Step 6: Create literature-list.md

For each paper in the matrix, record:
- cite key (matches references.bib)
- title
- venue + year
- PDF filename (if available)
- paper-qa index confirmation

### Step 7: Update research-state.md

Set Evidence Gate: "Literature matrix complete: Yes/Partial"

---

## Safety Rules

- Matrix cells may ONLY be filled from paper-qa output — never from memory
- No citation written without a verified references.bib entry
- If paper-qa returns "I don't know" or low confidence, mark cell as `?`
- Do not write Related Work prose during this step

---

## Output

```
✓ paper-qa index built: [N] papers indexed
✓ literature-matrix.md created: [N] rows filled, [M] cells marked ?
✓ Gap statement: [paste from paper-qa output]
✓ literature-list.md created

Next: /plan-experiments or /draft-section (after evidence gate).
```
