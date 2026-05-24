# Prior-Art Check and SOTA Baseline Guide

## Overview

The Prior-Art Check (Stage 6, Gate 1) is the single most important integrity step in the workflow. It answers two questions before any novelty claim is written: Has this been done before? And if not, what is the performance level a new method must exceed to be considered a contribution?

Failing to check prior art is the leading cause of papers receiving "this was already published" rejections, of researchers discovering overlapping work at the camera-ready stage, and of AI-assisted workflows generating false novelty claims from training data rather than from an actual literature search.

---

## 1. Why Prior-Art Checking Is Required Before Any Novelty Claim

AI language models — including Claude — have extensive knowledge of published research up to their training cutoff. This creates a specific risk: the model can generate plausible-sounding novelty claims ("to our knowledge, this is the first work to...") that are drawn from training-data intuitions rather than from an actual search of the current literature.

The prior-art check enforces a discipline that no claim of novelty, priority, or superiority may be written until:
1. A retrieval-based search has been executed against a current literature collection
2. The search results have been reviewed and documented
3. A threat-level assessment has been recorded

This requirement applies even when the researcher believes the idea is original. Confidence in originality is not a substitute for evidence of originality.

---

## 2. How to Build a paper-qa Index from Local PDFs

paper-qa (pqa) builds a dense retrieval index from a local collection of PDFs. This index is then used to answer specific research questions by retrieving and synthesizing passages from the papers.

**Step 1: Collect relevant PDFs.**
Create a `papers/` directory in your project root. Populate it with PDFs of relevant papers. For a project on retrieval-augmented agents for scientific literature analysis, collect papers on:
- Retrieval-augmented generation (RAG)
- Scientific question answering
- Citation recommendation systems
- Literature-aware language models
- Related benchmarks and datasets

Aim for at least 20–30 papers before the prior-art check. More is better. Include papers you expect to be related and papers you are uncertain about.

**Step 2: Build the index.**
```bash
pqa build papers/
```

This creates a `.pqa/` directory with the vector index. Building 50 papers typically takes 2–5 minutes.

**Step 3: Verify the index.**
```bash
pqa ask "What methods use dense retrieval for scientific literature question answering?"
```

If the answer cites papers from your collection, the index is working.

**Step 4: Run targeted queries (see Section 3).**

---

## 3. The 9-Step Prior-Art Search Protocol

Run these nine queries through pqa (or equivalent retrieval system) and document the results in `prior_art_report.md`:

**Query 1 — Core method.**
Ask about the specific technical approach you are proposing.
Example: "What methods combine retrieval-augmented generation with agent-based search for scientific paper analysis?"

**Query 2 — Task framing.**
Ask about the task or problem you are solving.
Example: "What systems have been built for automated scientific literature review or survey generation?"

**Query 3 — Dataset overlap.**
Ask whether your evaluation dataset has been used in prior work.
Example: "Which papers have used the ScientificQA or S2ORC datasets for question answering evaluation?"

**Query 4 — Closest baseline.**
Ask about the method you expect to be the closest baseline.
Example: "How does DPR (Dense Passage Retrieval) perform on scientific literature QA tasks?"

**Query 5 — Year-range sweep.**
Ask about recent work in the last 2 years to catch late-breaking papers.
Example: "What is the most recent work on retrieval-augmented agents for scientific question answering, published in 2023 or 2024?"

**Query 6 — Negative framing.**
Ask what has been tried and found to not work.
Example: "What limitations or failure modes have been reported for retrieval-augmented scientific QA systems?"

**Query 7 — Adjacent fields.**
Ask whether your idea has been applied in adjacent domains.
Example: "Have retrieval-augmented agents been used in medical literature analysis or legal document review?"

**Query 8 — Benchmark search.**
Ask whether a benchmark exists that directly evaluates what you are proposing.
Example: "What benchmarks exist for evaluating scientific citation accuracy or literature retrieval quality?"

**Query 9 — Novelty stress test.**
Ask the retrieval system whether your proposed contribution already exists.
Example: "Does any published system combine iterative re-ranking with agent-based literature traversal for scientific QA?"

Document each query, the top 3 retrieved passages, and a one-sentence assessment of relevance.

---

## 4. Threat Levels and What to Do at Each Level

After completing the 9-step search, assign a threat level to the proposed contribution:

### Low Threat

**Condition:** No paper in the retrieved results directly addresses the proposed approach. The closest prior work addresses a related but distinct problem, uses a substantially different method, or evaluates on different data.

**Action:** Proceed to Stage 7. Document the gap in `prior_art_report.md` with specific citations to the closest work.

### Medium Threat

**Condition:** One or more papers address a similar approach, but there are meaningful differences in scope, method, evaluation, or publication date (e.g., your work extends a prior workshop paper into a full evaluation).

**Action:** Proceed to Stage 7, but narrow the contribution statement to explicitly address the distinguishing factors. The contribution section must explain what you do that prior work did not.

### High Threat

**Condition:** A published paper addresses substantially the same approach and evaluation. There is significant overlap, but differences exist (e.g., you use a different backbone model, a different dataset, or a different application domain).

**Action:** Do not proceed to Stage 7 until you run an expanded search (add more papers to the index, search Google Scholar, and check arXiv in the past 12 months). If the threat remains High after expanded search, update `research_direction.md` to pivot the contribution. Document the pivot in `decision_log.md`.

### Critical Threat

**Condition:** A published paper directly addresses the same approach, evaluation, and application. The proposed work would be a duplication.

**Action:** Do not proceed. Run `/pivot-decision` and select "abandon or pivot." Update `research_direction.md` with a substantially different direction. Do not discard the prior literature — it becomes the foundation for Related Work when a new direction is established.

---

## 5. SOTA Baseline Table: What It Contains, How to Fill It, Forbidden Values

The SOTA table (`sota_table.md`) defines the competitive landscape for your primary evaluation task. It is used to set the minimum threshold in the Target Result Contract (Gate 2).

**Required columns:**

| Method | Venue | Year | Dataset | Primary Metric | Value | Source |
|--------|-------|------|---------|----------------|-------|--------|
| [Name] | [Conf/Journal] | [YYYY] | [Dataset name] | [Metric] | [Numerical value] | [Citation key] |

**Example:**

| Method | Venue | Year | Dataset | Primary Metric | Value | Source |
|--------|-------|------|---------|----------------|-------|--------|
| BM25 + GPT-4 | — | 2023 | ScientificQA | recall@10 | 0.61 | \cite{smith2023} |
| DPR-Sci | ACL | 2023 | ScientificQA | recall@10 | 0.67 | \cite{johnson2023} |
| SciAgent | EMNLP | 2024 | ScientificQA | recall@10 | 0.71 | \cite{chen2024} |

**How to fill the table:**

1. Each row must correspond to a published paper with a citation key in `references.bib`.
2. The metric value must come from the original paper's results table, not from a secondary source.
3. If a paper reports multiple metrics, record only the metric that matches your primary evaluation metric.
4. If a paper does not evaluate on your exact dataset, note "different dataset" in a comment column — do not convert or extrapolate their number.

**Forbidden values:**

- Values recalled from memory without a citation
- Values from a paper you have not read (only from abstract)
- Values from a leaderboard that does not cite a peer-reviewed paper
- Estimated or rounded values from figures (if a number cannot be read from a table, mark it as "figure-only, not reported numerically")
- Values for a different dataset presented as if they are for your dataset

---

## 6. Common Mistakes

**Mistake 1: Claiming "first" without a prior-art check.**
Writing "to our knowledge, this is the first work to combine X and Y" without completing the 9-step search protocol is a protocol violation. The phrase is blocked until Gate 1 passes. Use `TODO_NOVELTY_CHECK_NEEDED:` as a placeholder.

**Mistake 2: Filling the SOTA table from memory.**
Claude's training data contains many reported results. Those results may be from a different version of a dataset, a different evaluation protocol, or a different year's leaderboard. Always read the source paper and copy the number from its results table.

**Mistake 3: Using a small index for the prior-art check.**
Running the 9-step protocol against a 5-paper index produces false confidence. The index must cover the relevant literature area adequately. If you are uncertain whether the index is comprehensive enough, search arXiv and Google Scholar for additional papers and add them before running the check.

**Mistake 4: Treating "not retrieved" as "does not exist."**
If pqa does not retrieve a relevant paper, it may be because the paper is not in the index, not because it does not exist. Supplement pqa with a manual Google Scholar search for the closest prior work before assigning a Low threat level.

**Mistake 5: Not updating the SOTA table when new papers appear.**
If you discover a new SOTA paper after Gate 1 (e.g., a paper published while you were running experiments), add it to `sota_table.md` and re-evaluate whether it changes the minimum threshold. If the new paper exceeds your method's result, you must log this in `decision_log.md` and re-run Gate 3.
