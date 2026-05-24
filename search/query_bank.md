# Query Bank

**Project:** LLM-Assisted Literature Screening  
**RQ:** RQ-001-llm-screening.md  
**Last Updated:** 2026-05-25  
**Status:** Iteration 3 — approaching saturation (see log below)

---

## Core Terms

These terms define the semantic center of the search. All queries must include at least one term from each group unless otherwise noted.

### Group A — Technology (pick ≥1)
```
"large language model"
LLM
"language model"
GPT-4
ChatGPT
Claude
Gemini
"foundation model"
```

### Group B — Task (pick ≥1)
```
"literature screening"
"title-abstract screening"
"systematic review"
"abstract screening"
"literature review"
"study selection"
```

### Group C — Evaluation (pick ≥1)
```
recall
precision
"sensitivity"
"human agreement"
"Cohen's kappa"
automation
"semi-automation"
```

### Core Compound Query (Boolean)
```
(("large language model" OR "LLM" OR "language model") 
AND 
("literature screening" OR "systematic review" OR "study selection" OR "abstract screening") 
AND 
(recall OR precision OR sensitivity OR kappa OR "human agreement"))
```

---

## Expanded Terms

Use these to catch papers that do not use the core terminology directly.

### LLM Synonyms / Variants
```
"transformer model"
"pretrained language model"
"generative AI"
"AI-assisted"
"machine learning"   [only when combined with screening context — see exclusion terms]
"natural language processing"
NLP
```

### Screening / Review Synonyms
```
"evidence synthesis"
"scoping review"
"rapid review"
"machine-assisted review"
"citation screening"
"eligibility assessment"
"PICO"          [biomedical framing]
```

### Tool/System Names (search specifically for these)
```
Rayyan
Covidence
ASReview
Abstrackr
SWIFT-Review
RobotReviewer
"DistillerSR"
"EPPI-Reviewer"
```

### Expanded Compound Query (broader)
```
(("LLM" OR "GPT" OR "language model" OR "NLP" OR "transformer") 
AND 
("systematic review" OR "literature review" OR "evidence synthesis" OR "scoping review") 
AND 
(automation OR "semi-automated" OR "human-in-the-loop" OR efficiency OR recall))
```

---

## Exclusion Terms

Add these as NOT filters to suppress common off-topic results.

```
NOT ("movie review" OR "book review" OR "product review")
NOT ("peer review" OR "code review")        [unless combined with screening context]
NOT ("sentiment analysis")
NOT ("clinical trial" OR "randomized controlled trial")  [unless studying the review process itself]
NOT ("gene expression" OR "genomics" OR "proteomics")   [domain-specific, not method-focused]
NOT ("image screening" OR "radiograph" OR "mammography") [medical imaging, different task]
NOT ("spam detection" OR "email filtering")
```

**Note:** Apply exclusion terms only on Google Scholar, Semantic Scholar, and PubMed. arXiv and ACM DL searches rely on category filtering instead.

---

## Source-Specific Query Syntax

### Google Scholar
```
"large language model" "systematic review" screening recall
```
- Use quoted phrases for exact matches
- No Boolean operators (Scholar ignores OR/AND/NOT)
- Sort by relevance first; switch to "Recent" for post-2023 coverage
- Max ~1000 results per query; paginate manually with custom date ranges

### Semantic Scholar
**API query:**
```json
{
  "query": "LLM systematic review literature screening recall precision",
  "fields": "title,authors,year,venue,externalIds,abstract,citationCount",
  "publicationTypes": ["JournalArticle", "Conference"],
  "year": "2020-2026"
}
```
**Web UI:**
```
LLM systematic review literature screening recall precision
Filters: Year 2020–2026, Fields of Study: Computer Science
```

### arXiv
```
ti:(language model) AND abs:(systematic review OR literature screening) AND abs:(recall)
cat:cs.CL OR cat:cs.IR OR cat:cs.AI
```
- Use the arXiv advanced search at arxiv.org/search/advanced
- Filter by categories: cs.CL (Computation and Language), cs.IR (Information Retrieval)
- Date range: 2022-01-01 to present (LLM era)

### PubMed / MEDLINE
```
(("language model"[tiab] OR "LLM"[tiab] OR "ChatGPT"[tiab] OR "GPT-4"[tiab])
AND
("systematic review"[tiab] OR "literature screening"[tiab] OR "study selection"[tiab])
AND
(recall[tiab] OR precision[tiab] OR sensitivity[tiab] OR "kappa"[tiab]))
```
- Apply MeSH terms: "Systematic Review as Topic" [Mesh], "Natural Language Processing" [Mesh]
- Limit: English language, 2020–present
- Export to .nbib for Zotero import

### ACM Digital Library
```
Title: ("language model" OR "LLM") AND Abstract: ("systematic review" OR "literature screening") AND Abstract: (recall OR precision)
```
- Use ACM Advanced Search
- Filter: ACM Conferences + ACM Journals
- Date: 2020–2026
- Conference filters: SIGIR, ECIR, NAACL, ACL, EMNLP

### IEEE Xplore
```
("Abstract":"language model" AND "Abstract":"systematic review" AND "Abstract":"screening") AND "Publication Year":[2020 TO 2026]
```
- Use IEEE Advanced Search
- Content type: Journals + Conference Papers
- Publisher: IEEE
- Add: ("Title":"LLM-assisted" OR "Title":"automated screening")

---

## Search Iteration Log

Track every change to the query strategy and why it was made.

| Iteration | Date | Source | Change | Reason | New Papers Found |
|---|---|---|---|---|---|
| 1 | 2026-05-10 | Google Scholar, Semantic Scholar | Initial core query | First search | 47 candidate papers |
| 2 | 2026-05-15 | arXiv, PubMed | Added domain-specific syntax; added tool names (Rayyan, ASReview) | Core query missed tool-evaluation papers | 23 new candidates |
| 3 | 2026-05-22 | ACM DL, IEEE Xplore | Added ACM and IEEE sources; broadened Group C to include "kappa" | Missed CS conference papers | 12 new candidates |
| 4 | — | — | Planned: add bioRxiv for biomedical preprints | May catch more recent empirical studies | TBD |

---

## Query Saturation Assessment

**Current status:** Not yet saturated (Iteration 3 still found 12 new papers)

**Saturation rule:** Stop expanding when three consecutive iterations add fewer than 5 new unique papers to the candidate pool.

**Deduplication note:** After each iteration, load all new candidate IDs (DOI, arXiv ID, or title+year hash) into `search/search_log.csv` and check against existing rows. Count only papers not previously found as "new."

**Estimated saturation:** After 1–2 more iterations or when bioRxiv search is complete.

**When saturation is reached:**
1. Mark the query bank as "SATURATED" in the header
2. Record the final total candidate count in `screening/prisma_flow.md`
3. Proceed to full-text screening (Step 3)

---

## Notes

- **Grey literature:** Conference workshop papers and technical reports are included if they contain empirical evaluation. Blog posts and vendor white papers are excluded.
- **Non-English papers:** Excluded at this stage. If a high-citation paper is found in another language, note it in `screening/screening_table.csv` with decision = exclude and reason = language.
- **Preprints:** Include if (a) posted 2022 or later, (b) methodology is clearly described, and (c) the paper has not been retracted. Prefer the peer-reviewed version if available.
- **Version deduplication:** If an arXiv preprint and a published version of the same paper are both found, keep only the published version. Link both in `library/papers_manifest.csv`.
