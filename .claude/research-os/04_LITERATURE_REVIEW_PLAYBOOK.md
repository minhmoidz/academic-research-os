# Literature Review Playbook

---

## Principle: Never Write Related Work from Memory

Claude's training data contains knowledge of many papers, but that knowledge is:
- Potentially outdated (training cutoff)
- Potentially confabulated (plausible-sounding but incorrect details)
- Not verified against the actual paper content

Every claim in Related Work must trace to a paper you can read. If the PDF is not available and paper-qa cannot find it, the paper cannot be cited.

---

## Step 1: Collect Papers

### Method A: Paper Crawler (DBLP/OpenAlex)
```
Use: academic-writing-agents:paper-crawler
Input: Keywords, research area
Output: Verified paper list with titles, authors, years, venues
```

Query DBLP and OpenAlex with your primary keywords:
- Method name keywords (e.g., "multiple instance learning", "Mamba", "WSI classification")
- Problem keywords (e.g., "selection bias", "group reweighting")
- Application domain keywords (e.g., "computational pathology", "whole slide image")

### Method B: Citation Snowballing
- Start from 2–3 anchor papers you know are relevant
- Follow their reference lists
- Use paper-qa to answer "what does [paper X] cite for [concept Y]?"

### Method C: User-Provided Papers
- User drops PDFs into a designated folder (e.g., `literature/`)
- Index immediately with paper-qa before reading

**Output:** A verified paper list in `literature-list.md`:
```
| Title | Authors | Year | Venue | Relevance | PDF available? |
|-------|---------|------|-------|-----------|----------------|
```

---

## Step 2: Index Papers with paper-qa

Once PDFs are collected:

```bash
# Index a folder of PDFs
pqa -i my_project index literature/

# Ask questions against the indexed library
pqa ask "What methods address CSS selection bias in grouped MIL?"
pqa ask "What datasets are used for WSI classification benchmarks?"
pqa ask "What is the limitation of [method X]?"
```

**Rule:** Only paper-qa outputs can fill the literature matrix. No filling from memory.

---

## Step 3: Build the Literature Matrix

Rows = papers. Columns = dimensions relevant to your gap.

**Standard column set:**
| Paper | Method type | Dataset | Key metric | Key limitation | Addresses gap? |
|-------|-------------|---------|-----------|----------------|----------------|

**Custom columns** (add based on your specific gap):
- For reweighting papers: "reweighting signal used", "operates at instance/group/bag level"
- For MIL papers: "backbone", "aggregation method", "feature extractor"

**Rule:** Each cell is filled by a paper-qa query with the paper as context, or left as `?` if the information isn't in the available PDF.

**Use:** `04_LITERATURE_REVIEW_PLAYBOOK.md`, `academic-writing-agents:research-analyst`

---

## Step 4: Group Papers by Concept (Not by Chronology)

Related Work should be organized around the **concepts** your paper intersects, not around "first X was proposed, then Y, then Z."

**Good structure:**
```
III-A. Attention-Based MIL          → What's shared + what's missing
III-B. State-Space and Group MIL   → BaselineModel gap identified here
III-C. Hard-Instance Weighting         → Why ProposedModule differs
```

**Bad structure:**
```
In 2021, AuthorA et al. proposed... In 2022, PriorMethod... In 2023, BaselineModel...
```

For each concept group:
1. State what the group shares in approach
2. State what the group achieves
3. State what the group does NOT address (the gap)
4. Cite 3–5 representative papers from your verified list

**Rule:** The gap sentence must be verifiable from paper-qa, not asserted.

---

## Step 5: Verify Each Citation

Before finalizing Related Work:

```bash
# Check that every cited paper is indexed
pqa ask "Summarize the main contribution of [paper title]"
```

For each `\cite{key}` in the Related Work section:
- [ ] Key exists in `references.bib`
- [ ] `references.bib` entry has correct title, authors, year, venue
- [ ] The claim attributed to this paper matches what paper-qa returns
- [ ] No claims are attributed to a paper that doesn't support them

**Use:** `academic-writing-agents:bibliography-auditor` for final citation audit.

---

## Step 6: Avoid Common Related Work Mistakes

| Mistake | Prevention |
|---------|-----------|
| Listing papers without synthesis | Group by concept, state what each group misses |
| Citing papers you haven't read | Paper-qa required before citation |
| "X et al. proposed Y" × 6 sentences | Vary sentence openers; merge short entries |
| Overstating prior work's limitations | Quote paper-qa output, don't exaggerate |
| Missing the closest competing paper | Search paper-qa for the most similar approach |
| Not explaining why ProposedModule differs | Write explicit differentiation (3 axes or less) |
| Alphabetical/chronological order | Organize by concept |

---

## Step 7: Mark Missing Citations

If you need a citation but don't have a verified paper:

```latex
% TODO_CITATION_NEEDED: paper showing entropy-based difficulty in MIL context
```

Use `TODO_CITATION_NEEDED:` in the `.tex` source. Never write a `\cite{key}` without a verified entry.

Run `academic-writing-agents:bibliography-auditor` to find all unresolved TODOs before submission.

---

## Literature Review Checklist (Pre-Drafting)

- [ ] Paper list has ≥ 10 verified papers
- [ ] All PDFs indexed in paper-qa
- [ ] Literature matrix built from paper-qa queries (not memory)
- [ ] At least one gap column with explicit "no prior work on X" evidence
- [ ] Closest competing paper identified and analyzed
- [ ] All cited papers exist in references.bib
- [ ] Related Work organized by concept, not chronologically
- [ ] Differentiation from prior work stated explicitly for each major axis
