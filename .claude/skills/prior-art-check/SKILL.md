# /prior-art-check — Prior Art Systematic Search Skill

## Purpose

Systematically determine whether prior work already addresses the proposed contribution, and assess the novelty threat level before any performance claims are made in the paper. This skill produces a structured prior art competition table and a novelty risk report.

**This skill must be run before Stage 9 (Target Result Contract).** The TRC's `comparison_against_best_prior` field cannot be filled until this skill completes.

---

## Core Rule

**Never claim novelty without completing this check.**

Novelty is a factual question about what prior work exists — it is not a judgment call. If prior work exists that closely matches the proposed contribution, the novelty claim must be narrowed or abandoned regardless of how good our experimental results are.

---

## Required Inputs

Ask the user for the following before proceeding. Do not guess or infer from prior context.

1. **Research question / proposed contribution** — One sentence describing what the proposed method does that is claimed to be new. If `paper_brief.md` exists, read it and confirm with the user.

2. **Keywords for search** — 3 to 8 search terms covering the method, task, dataset, and technique. Example: `["transformer", "benchmark dataset", "state space model", "image classification", "attention aggregation", "self-supervised learning"]`

3. **PDF folder path** — The local folder containing downloaded PDFs for paper-qa indexing. Example: `./papers/`. If no local PDFs: note this and rely on pqa pre-built index (if available) or mark all cells as TODO_EVIDENCE_NEEDED.

4. **Existing pqa index name** — If a paper-qa index already exists, its name (e.g., `my_papers`). If not, the skill will guide the user to create one.

---

## Required Steps

### Step 1: Read Reference Documents

Read both reference files before proceeding:

- `.claude/research-os/25_PRIOR_ART_COMPETITION.md` (prior art methodology)
- `.claude/research-os/13_ANTI_HALLUCINATION_RULES.md` (hallucination prevention)

If `25_PRIOR_ART_COMPETITION.md` does not exist, proceed using the methodology defined in this SKILL.md and note the missing file in the report.

### Step 2: Read Project Brief

Read `paper_brief.md` from the project root (if it exists).

Extract:
- `main_claim` or `key_claim`
- `proposed_approach` (one sentence)
- `target_venue` and `paper_type`

If `paper_brief.md` does not exist: ask the user to provide the main contribution in one sentence before proceeding.

### Step 3: Prepare paper-qa Index

Check whether a pqa index exists:

```bash
ls .pqa/ 2>/dev/null || echo "No .pqa index found"
```

If an index exists, confirm its name with the user. If no index exists:

```bash
# If PDFs are available in ./papers/:
pqa -i [index_name] index ./papers/
```

Note: If no local PDFs and no index, mark all paper-qa evidence cells as `TODO_EVIDENCE_NEEDED: no index available` and note that web-based search is required.

### Step 4: Run paper-qa Queries

For each keyword provided, run the following queries. Record the full output (first 200 characters minimum per query). Do not paraphrase — paste actual pqa output.

**Query set A — Method-level search:**

```bash
pqa ask "What methods use [keyword] for [task]?"
pqa ask "Which papers propose [technique] for [task] classification?"
pqa ask "What is the best result on [dataset] for [task]?"
```

**Query set B — Contribution-specific search:**

```bash
pqa ask "Does any paper combine [module A] and [module B] for [task]?"
pqa ask "What papers address [specific limitation our method claims to solve]?"
pqa ask "Which papers use [architecture] as backbone for [task]?"
```

**Query set C — Dataset and benchmark search:**

```bash
pqa ask "What is the state-of-the-art result on [Dataset-A]?"
pqa ask "What methods have been evaluated on [Dataset-B]?"
pqa ask "What is the highest reported metric on [Dataset-B]?"
```

Record for each query:
- The exact query string
- The pqa output (paste raw)
- Papers mentioned in the output (title, authors, year if given)

### Step 5: Assign Threat Levels to Each Paper Found

For each paper identified in Step 4, assess the threat to novelty:

| Threat Level | Definition |
|-------------|-----------|
| None | Paper addresses a different task, dataset, or technique — no overlap |
| Low | Paper is related but uses a substantially different approach or evaluated on different data |
| Medium | Paper uses a similar technique but for a different task or without the specific contribution we claim |
| High | Paper uses the same or nearly the same technique for the same task; our contribution partially overlaps |
| Critical | Paper uses the same technique for the same task on the same dataset and reports competitive results — our novelty claim is directly threatened |

**Rule:** If ANY paper has threat level Critical, stop and require user decision before proceeding. Do not continue to Stage 9 (TRC creation) with an unresolved Critical threat.

### Step 6: Build Prior Art Competition Table

Create `prior_art_competition_table.md` in the project root.

```markdown
# Prior Art Competition Table

generated: YYYY-MM-DD
skill: /prior-art-check
index_used: [index name or "none — TODO_EVIDENCE_NEEDED"]
proposed_contribution: "[one sentence from paper_brief.md]"

## Search Keywords Used
[list of keywords]

## Queries Run
[for each query: the exact query text + first 100 chars of pqa output]

## Competition Table

| Paper | Method | Dataset | Metric | Value | Overlap with Our Claim | Threat | Evidence Source |
|-------|--------|---------|--------|-------|----------------------|--------|----------------|
| [title] | [method name] | [dataset] | [metric] | [value] | [specific overlap] | [None/Low/Medium/High/Critical] | [pqa query output / user-provided / TODO_EVIDENCE_NEEDED] |
| ... | | | | | | | |

Note: Every cell in the "Value" column must come from a verified source (pqa output pasted above, or user-provided table with citation). Never fill from memory.

## Cells with TODO_EVIDENCE_NEEDED
[list any cell that could not be filled with verified evidence]

## Summary: Best Known Prior Results

| Dataset | Task | Best Method | Best Metric | Best Acc | Source |
|---------|------|------------|------------|---------|--------|
| [Dataset-A] | [task description] | [method] | [value] | [value] | [source] |
| [Dataset-B] | [task description] | [method] | [value] | [value] | [source] |
```

**Evidence source rules:**
- `paper-qa query: "[query text]"` — for results found via pqa
- `user-provided: [citation]` — for results the user provides with a citation
- `TODO_EVIDENCE_NEEDED: [description]` — for cells that cannot be verified
- Never: `memory`, `assumed`, `likely`, `approximately`

### Step 7: Assess Overall Novelty Risk

Based on the competition table, assess:

1. **Maximum threat level** across all papers: None / Low / Medium / High / Critical

2. **Closest prior paper** (highest threat):
   - Title, method name, dataset, metric value
   - Specific overlap with our contribution
   - Specific technical difference (if any)

3. **Best known published result** on our primary dataset:
   - Method name, metric value, paper, source
   - This becomes `comparison_against_best_prior` in the TRC

4. **Novelty gap statement** (what is genuinely new):
   - One paragraph specifying what our method does that no prior paper does
   - Must be specific (technical or empirical difference) — not vague

### Step 8: Create Novelty Risk Report

Create `novelty_risk_report.md` in the project root.

```markdown
# Novelty Risk Report

generated: YYYY-MM-DD
skill: /prior-art-check
proposed_contribution: "[one sentence]"
prior_art_table: prior_art_competition_table.md

## Overall Threat Level
[None | Low | Medium | High | Critical]

## Threat Summary
[2-3 sentences: what prior work exists and how close it is]

## Closest Prior Paper
paper: [title]
method: [method name]
dataset: [dataset]
result: [metric value]
source: [evidence source]
overlap: >
  [Specific description of what overlaps with our contribution]
difference: >
  [Specific technical or empirical difference between our method and this paper]
  If no genuine difference found: write "TODO_EVIDENCE_NEEDED: no defensible difference identified"

## Best Known Published Result (Primary Dataset)
dataset: [Dataset-A]
best_method: [method]
best_metric: [value]
source: [evidence source]
note: This value must be used in the TRC's comparison_against_best_prior field.

## Best Known Published Result (Secondary Dataset)
dataset: [Dataset-B]
best_method: [method]
best_metric: [value]
source: [evidence source]

## Novelty Gap Statement
[One paragraph: what our method does that no prior paper does.
 Must reference specific technical components (e.g., "No prior paper applies
 [proposed technique] with [BaselineModel] as backbone for [Dataset-A]
 classification, though [paper X] uses a similar approach for a different task.")
 If novelty cannot be demonstrated: write TODO_EVIDENCE_NEEDED.]

## Recommendation

decision: [PROCEED | NARROW_CLAIM | DIFFERENTIATE | CRITICAL_STOP]

rationale: >
  [2-4 sentences with specific evidence from the table above]

if_critical_stop: >
  [Which paper poses the Critical threat and what must be resolved before proceeding.
   Leave blank if no Critical threat.]

next_action: >
  [Specific: "Update TRC comparison_against_best_prior with best known result.
   Proceed to Stage 9." or "Resolve Critical threat before TRC creation."]
```

### Step 9: Update Project State

Update `project_state.md`:

```markdown
prior_art_check:
  date: YYYY-MM-DD
  files_created: [prior_art_competition_table.md, novelty_risk_report.md]
  max_threat_level: [threat level]
  best_known_result: [method, metric value, dataset]
  novelty_recommendation: [PROCEED | NARROW_CLAIM | DIFFERENTIATE | CRITICAL_STOP]
```

---

## Output Summary

After completing all steps, print a brief summary:

```
Prior Art Check Complete
═══════════════════════════════════════════════════════════
Queries run: [N]
Papers evaluated: [N]
Highest threat: [level]
Best known prior: [method] — [metric value] on [dataset]
Novelty recommendation: [decision]

Files created:
  prior_art_competition_table.md
  novelty_risk_report.md

Next action: [specific instruction]
═══════════════════════════════════════════════════════════
```

---

## Safety Rules

1. **Never write Related Work prose during this check.** This skill produces tables and structured reports — not narrative prose. Prose comes at Stage 18 after the Evidence Freeze.

2. **Never claim novelty without completing this check.** The TRC cannot be written with `comparison_against_best_prior` empty or as a guess.

3. **Mark any unverified cell as `TODO_EVIDENCE_NEEDED`.** Do not estimate metric values from memory. Do not write "approximately" or "likely."

4. **If threat level = Critical:** Stop and require explicit user decision. Do not proceed to Stage 9. Options for the user:
   - Read the critical paper carefully and identify a genuine difference (→ update table and re-assess)
   - Narrow the contribution to avoid the overlapping claim (→ update paper_brief.md → re-run check)
   - Change venue to one where the overlapping paper is not well-known (→ requires strong justification)
   - Abandon (→ log DEC entry)

5. **Do not fill the competition table from memory.** Every paper title, metric value, and method name must be cited to a pqa query output or user-provided citation.

6. **Evidence source must be traceable.** Write `paper-qa query: "[exact query]"` next to any value found via pqa. Anyone reading the table must be able to reproduce the search.

7. **Do not omit papers that threaten novelty.** The temptation to ignore a closely related paper is real but forbidden. Every paper found in Step 4 must appear in the table.

---

## Special Case: No Local PDFs Available

If no local PDF folder exists and no pqa index exists:

1. Mark all paper-qa evidence cells as `TODO_EVIDENCE_NEEDED: no index available`
2. Ask the user to provide:
   - The best known result on the primary dataset (with citation)
   - Any closely related papers they are aware of
3. Fill these user-provided entries with source `user-provided: [citation]`
4. Set `max_threat_level` to UNKNOWN until pqa evidence is available
5. Recommend that the user download key related papers and re-run `/prior-art-check` before Stage 9

The TRC's `comparison_against_best_prior` must be filled before the TRC is signed off. If it remains TODO_EVIDENCE_NEEDED, Stage 9 is blocked.
