# Academic Research Protocol

**Version:** 1.0  
**Last Updated:** 2026-05-25  
**Applies To:** All research projects under this repository  
**Claude Research OS Integration:** See `.claude/` directory for stage definitions and command reference

---

## Core Rule

> **No claim enters the final draft unless it has a row in `evidence_matrix.csv` with a traceable source (citekey + page/section + quote or paraphrase).**

This rule is non-negotiable. If a claim cannot be traced to a row in the evidence matrix, it must be replaced with a `TODO_EVIDENCE_NEEDED:` marker and queued for verification before the Evidence Freeze (Stage 16).

---

## Overview

This protocol governs the full 10-step research workflow from question definition to citation-validated draft. It is designed to be used with the Claude Research OS (`.claude/research-os/`) and enforced by the anti-hallucination rules in `.claude/research-os/13_ANTI_HALLUCINATION_RULES.md`.

Each step produces one or more **artifacts** that must exist before proceeding to the next step. Skipping artifact production is not allowed.

---

## Step 1: Define the Research Question

**Artifact:** `research_questions/RQ-NNN.md`

1. Copy the template from `research_questions/RQ-001-template.md`.
2. Assign a sequential RQ number (RQ-001, RQ-002, ...).
3. Fill in every field. No field may be left blank or as placeholder text.
4. Set Status to `DRAFT` until the question is confirmed focused and answerable.
5. Promote to `ACTIVE` only after at least one pilot search confirms papers exist.

**Checklist before proceeding:**
- [ ] RQ is specific enough to be falsifiable or answerable with evidence
- [ ] Scope (included/excluded) is written out explicitly
- [ ] Success criteria include a minimum paper count and evidence matrix completion requirement
- [ ] Target output type is defined (paper / thesis / lit review / experiment plan)
- [ ] Risks section includes "papers may not exist" and "contradictory evidence"

---

## Step 2: Build the Search Strategy

**Artifacts:** `search/query_bank.md`, initial rows in `search/search_log.csv`

1. Start from the core terms in the RQ statement.
2. Expand to synonyms, related concepts, and method names (see `search/query_bank.md`).
3. Define exclusion terms to suppress off-topic results.
4. Write source-specific query syntax for each database you will search.
5. Log every search attempt in `search/search_log.csv` immediately after running it.

**Query saturation rule:** Stop expanding queries when three consecutive iterations add fewer than 5 new unique papers to the candidate pool.

**Query bank location:** `search/query_bank.md`  
**Search log location:** `search/search_log.csv`  
**Source catalog:** `search/sources.yaml`

---

## Step 3: Screening

**Artifacts:** `screening/screening_table.csv`, `screening/prisma_flow.md`

Screening is a two-pass process:

**Pass 1 — Title/Abstract Screen:**
- Apply inclusion/exclusion criteria from `screening/inclusion_exclusion.md`
- Record decision (include/exclude/borderline) and reason in `screening/screening_table.csv`
- Borderline papers proceed to Pass 2

**Pass 2 — Full-Text Screen:**
- Apply quality scoring rubric (5 criteria × 0-2 scale, max 10)
- Score ≥7: include; 4-6: borderline for manual review; <4: exclude
- Document reasoning for every borderline decision

**PRISMA flow:** Update `screening/prisma_flow.md` after each screening batch to track record counts at each stage.

---

## Step 4: Paper Intake

**Artifacts:** BibTeX entry in `library/references.bib`, row in `library/papers_manifest.csv`, note file in `notes/`

For each included paper:

1. Create a BibTeX entry using the naming convention: `authorYYYYkeyword`
   - `author` = first author's last name, lowercase
   - `YYYY` = 4-digit publication year
   - `keyword` = single most distinctive word from the title, lowercase
   - Example: `smith2024agents`, `brown2023retrieval`, `zhang2022survey`
2. Add the entry to `library/references.bib`.
3. Add a row to `library/papers_manifest.csv` with all metadata fields.
4. Create a note file at `notes/{citekey}.md` using the note template below.

**Note template fields:**
```
# {citekey} — {Title}

**Citation:** {full reference}  
**Year:** {YYYY}  
**Venue:** {journal/conference}  
**Type:** {empirical / survey / theoretical / position}

## Research Question Addressed
## Key Claims
## Evidence / Methods
## Key Results
## Limitations Acknowledged by Authors
## Relevance to This Project
## Quotes for Evidence Matrix
## Contradicts / Supports
## My Assessment
```

---

## Step 5: Evidence Extraction

**Artifact:** `evidence/evidence_matrix.csv`

For each included paper, extract every claim relevant to the research question into the evidence matrix.

**Column schema:**
```
claim_id, claim_text, citekey, source_type, page_or_section, quote_or_paraphrase, 
evidence_strength, my_confidence, contradicted_by, supports_rq, tags, date_added
```

**Evidence strength values:** strong_empirical / weak_empirical / theoretical / anecdotal / expert_opinion  
**My confidence values:** high / medium / low  
**Rules:**
- One row per claim, not per paper
- A paper may contribute multiple rows
- Claims must be specific and falsifiable; no vague summaries
- Direct quotes preferred over paraphrase; if paraphrasing, note it explicitly

---

## Step 6: Evidence Validation

**Artifact:** Updated `evidence/evidence_matrix.csv` with `validated` column

For every row in the evidence matrix:

1. Verify the citekey resolves to an entry in `library/references.bib`
2. Verify the page/section exists in the actual paper (not just the abstract)
3. Verify the quote/paraphrase accurately represents what the paper says
4. Check that the claim is not contradicted by findings from other rows (or flag the contradiction explicitly)
5. Set `validated = TRUE` only after completing all 4 checks

**Validation is required before Stage 16 (Evidence Freeze).** Any row with `validated = FALSE` at freeze time must be removed or downgraded to a `TODO_EVIDENCE_NEEDED:` marker in the draft.

---

## Step 7: Synthesis

**Artifacts:** `synthesis/literature_map.md`, `synthesis/argument_map.md`, `synthesis/gaps.md`

Synthesis is built entirely from the validated evidence matrix. No synthesis claim may be introduced from memory or general knowledge without a corresponding evidence matrix row.

**Literature map** (`synthesis/literature_map.md`):
- Cluster papers by theme/approach
- Show how clusters relate to each other
- Identify the dominant paradigms and outliers

**Argument map** (`synthesis/argument_map.md`):
- Map the logical structure: claim → evidence → rebuttal → counter-rebuttal
- Every node must cite at least one citekey
- Contradictions must be represented explicitly, not resolved by omission

**Gap analysis** (`synthesis/gaps.md`):
- List questions unanswered by the existing literature
- For each gap: what evidence exists, what is missing, what research would close it
- Gaps are the foundation for the research contribution claim

---

## Step 8: Adversarial Review

**Artifact:** Completed `prompts/adversarial_reviewer.md`

Before writing the draft, run the adversarial reviewer against the synthesis:

1. Open `prompts/adversarial_reviewer.md`
2. Fill in the synthesis claims you plan to make
3. Run the adversarial prompts (as Claude or with a second agent)
4. Document the strongest objections raised
5. For each objection: either find evidence to rebut it, narrow the claim, or add it to the limitations section

**No claim that cannot survive adversarial review should appear in the final draft.**

---

## Step 9: Draft Writing

**Artifact:** Draft document under `outputs/`

Draft writing rules:
- Write only from the evidence matrix and synthesis artifacts
- Every empirical claim must cite a validated evidence matrix row
- Use `TODO_EVIDENCE_NEEDED:` for any claim you want to make but cannot yet support
- Use `TODO_CITATION_NEEDED:` where a citation is needed but not yet retrieved
- Use `TODO_NOVELTY_CHECK_NEEDED:` before claiming any contribution is novel
- Do not write Related Work from memory — write only from `notes/` files and the evidence matrix
- Do not claim novelty before the Prior-Art/SOTA Check (Stage 6) passes

**Writing order:** Methods → Results → Discussion → Introduction → Abstract → Conclusion  
(Introduction and Abstract are written last because they depend on knowing what the paper actually shows.)

---

## Step 10: Citation Validation

**Artifact:** Citation validation report in `outputs/citation_validation_report.md`

Before submission:

1. Run `scripts/validate_citations.py` (or equivalent) to check:
   - Every `\cite{}` key exists in `library/references.bib`
   - Every citekey in `references.bib` appears at least once in the draft
   - No duplicate citekeys with different content
2. Manually spot-check 20% of citations: open the paper, verify the cited claim is actually in that paper at the cited location
3. Verify DOIs resolve (use `scripts/check_dois.py` if available)
4. Verify arXiv IDs match final published versions where applicable

**A draft may not be submitted if citation validation has not passed.**

---

## Anti-Hallucination Checklist

Claude must run this checklist **before writing any synthesis, claim, or related work paragraph**:

- [ ] **Source check:** Every claim I am about to write has a row in `evidence_matrix.csv`. I have read that row and confirmed the source paper says what I think it says.
- [ ] **Citekey check:** Every citekey I am about to use exists in `library/references.bib` and the paper is in `library/papers_manifest.csv`.
- [ ] **Novelty check:** I have not claimed this result/method is novel without completing the Prior-Art/SOTA Check. If unsure, I will insert `TODO_NOVELTY_CHECK_NEEDED:`.
- [ ] **Contradiction check:** I have searched the evidence matrix for claims that contradict what I am about to write. If contradictions exist, I will represent them explicitly rather than choosing the convenient version.
- [ ] **Memory check:** I am not writing from training-data memory. If a fact feels obvious or well-known but I cannot find it in the evidence matrix, I will insert `TODO_EVIDENCE_NEEDED:` instead of writing it as fact.

---

## File Naming Conventions

| Artifact | Convention | Example |
|---|---|---|
| BibTeX citekey | `authorYYYYkeyword` | `smith2024agents` |
| RQ file | `RQ-NNN-slug.md` | `RQ-001-llm-screening.md` |
| Note file | `{citekey}.md` | `smith2024agents.md` |
| Evidence matrix | `evidence_matrix.csv` | fixed name |
| Screening table | `screening_table.csv` | fixed name |
| Search log | `search_log.csv` | fixed name |
| Draft output | `draft_vN.md` or `draft_vN.tex` | `draft_v1.tex` |
| Figure | `fig_{descriptor}.pdf` | `fig_prisma_flow.pdf` |

**BibTeX citekey rules:**
- Author: first author last name only, all lowercase, no diacritics (é → e, ü → u)
- Year: 4-digit year of publication (use arXiv submission year for preprints)
- Keyword: single most distinctive content word from the title, lowercase
- If collision: append `a`, `b`, `c` (e.g., `smith2024agentsa`)

---

## Connection to Claude Research OS

This protocol maps to the 26-stage Claude Research OS workflow:

| Protocol Step | Research OS Stage(s) |
|---|---|
| 1. Define RQ | Stage 1: Research Question Definition |
| 2. Search strategy | Stage 3: Literature Search |
| 3. Screening | Stage 4: Screening & Selection |
| 4. Paper intake | Stage 5: Deep Reading |
| 5. Evidence extraction | Stage 7: Evidence Extraction |
| 6. Evidence validation | Stage 8: Evidence Validation |
| 7. Synthesis | Stage 10–12: Literature Map, Argument Map, Gap Analysis |
| 8. Adversarial review | Stage 13: Adversarial Review |
| 9. Draft writing | Stage 17–22: Draft, Section Writing |
| 10. Citation validation | Stage 24: Citation & Format Audit |

**Stage artifacts are located at:** `.claude/research-os/`  
**Stage command reference:** `.claude/research-os/11_COMMANDS.md`  
**Anti-hallucination rules:** `.claude/research-os/13_ANTI_HALLUCINATION_RULES.md`

---

## Session Start Protocol

At the start of every research session, follow these steps in order:

1. Open the project root and read `project_state.md` to identify current stage
2. Check `research_questions/RQ-NNN.md` for the active research question (Status: ACTIVE)
3. Read `evidence/evidence_matrix.csv` — know what is already validated before writing anything
4. Run `/research-status` (Claude Research OS command) to detect missing artifacts and blockers
5. Identify the current stage and the one artifact needed to advance
6. Report current stage and next safe action to the user
7. **Wait for user confirmation before writing any new content**

**Do not skip Step 7.** Writing before confirming the current stage has caused irreversible draft contamination in previous sessions.

---

## Maintenance

- This protocol document is versioned. Any change to the workflow must increment the version number and be logged in `CHANGELOG.md`.
- Protocol changes that affect the evidence matrix schema require re-validation of all existing rows.
- The protocol is reviewed at the end of each research project and updated based on lessons learned.
