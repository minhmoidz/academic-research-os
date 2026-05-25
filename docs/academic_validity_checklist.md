# Academic Validity Checklist

Use this checklist before declaring a literature review complete or before submission.
Every item maps to a specific failure mode — work through them in order.

---

## 1. Bibliography Integrity

| # | Check | How to verify | Status |
|---|---|---|---|
| 1.1 | Every BibTeX entry has a `doi` or `url` field | `python scripts/validate_bib_metadata.py` | ☐ |
| 1.2 | Every entry has `author`, `title`, and `year` | `python scripts/validate_bib_metadata.py` (soft warning) | ☐ |
| 1.3 | All DOIs match the canonical `10.NNNN/...` format | `python scripts/validate_bib_metadata.py` (soft warning) | ☐ |
| 1.4 | All DOIs resolve — open each DOI URL in a browser and confirm the page loads | Manual: click each `doi` field value in `references.bib` | ☐ |
| 1.5 | No duplicate citekeys in `references.bib` | `grep -n "^@" library/references.bib \| sort` | ☐ |
| 1.6 | Citekey convention followed (`authorYYYYkeyword`) | Visual check of references.bib | ☐ |

---

## 2. Evidence Matrix Integrity

| # | Check | How to verify | Status |
|---|---|---|---|
| 2.1 | Every claim in `evidence_matrix.csv` has a `paper_citekey` in `references.bib` | `python scripts/validate_evidence_matrix.py` | ☐ |
| 2.2 | Every claim has a corresponding `## CXXX` section in `claim_registry.md` | `python scripts/validate_evidence_matrix.py` | ☐ |
| 2.3 | All `confidence` values are `high`, `medium`, or `low` | `python scripts/validate_evidence_matrix.py` | ☐ |
| 2.4 | All `direction` values are `supports`, `contradicts`, `partially-supports`, or `unclear` | `python scripts/validate_evidence_matrix.py` | ☐ |
| 2.5 | No duplicate `claim_id` values | `python scripts/validate_evidence_matrix.py` | ☐ |
| 2.6 | `citation_location` is specific (e.g., "Table 2 p.8", not "p.1" or blank) | Visual check of evidence_matrix.csv | ☐ |

---

## 3. Citation Consistency

| # | Check | How to verify | Status |
|---|---|---|---|
| 3.1 | Every `@citekey` in notes and draft exists in `references.bib` | `python scripts/validate_citations.py` | ☐ |
| 3.2 | Every citekey in `papers_manifest.csv` exists in `references.bib` | `python scripts/validate_csv_rows.py` | ☐ |
| 3.3 | No citekeys in `references.bib` that are never cited anywhere | `python scripts/validate_citations.py` (orphan check) | ☐ |

---

## 4. Claim Accuracy — Per-Paper Spot-Check

For every claim marked `confidence: high` in `evidence_matrix.csv`, verify:

| # | Check | Notes |
|---|---|---|
| 4.1 | Open the source paper at the `citation_location` cited | E.g., "Table 2 p.8" — open the PDF and look at Table 2 |
| 4.2 | Confirm the **exact number** matches what is in the paper | Numerical claims are the #1 hallucination failure mode |
| 4.3 | Confirm the **sample size** (n=X) matches | LLMs commonly pick up n from a different part of the paper |
| 4.4 | Confirm the **statistical qualifier** is present if claimed | p-values, confidence intervals, kappa values |
| 4.5 | Confirm the **scope** is not overgeneralised | Check for domain/language/corpus limitations in the paper |

---

## 5. Synthesis Validity

| # | Check | How to verify | Status |
|---|---|---|---|
| 5.1 | Contradictions are documented in `notes/contradiction_notes/` | `ls notes/contradiction_notes/` | ☐ |
| 5.2 | Each synthesis statement in `synthesis/` traces to ≥1 claim ID | Check `synthesis/argument_map.md` and `literature_map.md` | ☐ |
| 5.3 | Identified gaps in `synthesis/gaps_and_opportunities.md` are supported by the literature map, not assumed | Visual check of GAP-NNN entries | ☐ |
| 5.4 | No "studies show" / "it is well known" phrases without claim IDs | `python scripts/check_claims_without_sources.py --strict` | ☐ |

---

## 6. Draft Quality

| # | Check | How to verify | Status |
|---|---|---|---|
| 6.1 | Every factual sentence in `draft.md` has an `<!-- Evidence: CXXX -->` comment | `python scripts/validate_evidence_matrix.py` | ☐ |
| 6.2 | TODO markers are resolved or explicitly deferred | `grep -n "TODO_" outputs/draft.md` | ☐ |
| 6.3 | All `@citekey` references in draft match `references.bib` | `python scripts/validate_citations.py` | ☐ |
| 6.4 | Abstract compresses the full argument (motivation → gap → method → result → takeaway) | Read abstract alone — does it stand alone? | ☐ |
| 6.5 | Limitations section addresses at least: scope, dataset, confidence levels | Read § Limitations | ☐ |

---

## 7. Data Completeness

| # | Check | How to verify | Status |
|---|---|---|---|
| 7.1 | `evidence_matrix.csv` has ≥1 data row | `python scripts/validate_csv_rows.py` | ☐ |
| 7.2 | `search_log.csv` documents all search runs | `python scripts/validate_csv_rows.py` | ☐ |
| 7.3 | `screening_table.csv` has a decision for every paper retrieved | `python scripts/validate_csv_rows.py` | ☐ |
| 7.4 | `screening/prisma_flow.md` numbers match `search_log.csv` totals | Cross-check manually | ☐ |

---

## 8. Full CI Pass

Run all validation scripts locally before the final push:

```bash
python scripts/validate_bib_metadata.py
python scripts/validate_csv_rows.py
python scripts/validate_citations.py
python scripts/validate_evidence_matrix.py
python scripts/check_claims_without_sources.py
python scripts/check_claims_without_sources.py --strict
```

All commands must exit with code 0. If GitHub Actions is configured, verify all jobs show green on the final commit.

---

## 9. Sign-Off

| Role | Name | Date | Signature |
|---|---|---|---|
| Lead reviewer | | | |
| Second reviewer (if applicable) | | | |
| PI / supervisor sign-off | | | |

---

*This checklist is part of the Academic Research OS. Last format revision: 2026-05-25.*
