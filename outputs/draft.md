# Draft: [TITLE PLACEHOLDER]

<!-- ============================================================
     CORE RULE — READ BEFORE EDITING
     ============================================================
     Every sentence that makes a factual claim MUST have a claim ID
     comment immediately after it, in the format:

       <!-- Evidence: C001, C003 | Confidence: high -- >

     NO EXCEPTIONS. A sentence without a claim ID is an unsupported
     claim and MUST NOT appear in the final draft.

     If you cannot supply a claim ID, write:
       [TODO_EVIDENCE_NEEDED: describe the claim you want to make]

     Do not delete TODO markers — they are tracked for the audit.
     ============================================================ -->

<!-- Stage gate: Do not write final prose (Abstract, Introduction, Related Work,
     Method, Results, Discussion, Conclusion, Limitations) until Stage 17
     Evidence Freeze passes. Until then, this file should contain:
       - TODO markers
       - skeleton section stubs with evidence comments
       - placeholder sentences showing WHERE claims will go
     -->

<!-- Draft status: skeleton -->
<!-- Last updated: YYYY-MM-DD -->

---

## Title

[TITLE PLACEHOLDER — finalize after Stage 16 Result Adequacy Gate]

*Working title:* Structured LLM-Assisted Literature Review: Efficiency, Quality, and Protocol Design

---

## Abstract

<!-- The abstract must compress the entire argument into ~250 words.
     Write it last. Fill in the TODO markers as each section is completed.
     Claim IDs in comments show which evidence anchors each sentence. -->

[TODO_EVIDENCE_NEEDED: 1–2 sentence motivation — what problem does this paper address?]
<!-- Evidence: C001, C003 | Confidence: high — the efficiency vs. quality tension is the core motivation -->

[TODO_EVIDENCE_NEEDED: 1 sentence describing the approach / method]
<!-- Evidence: C004, C008, C010 | Confidence: medium — the combined protocol is the approach -->

[TODO_RESULT_NEEDED: 1–2 sentences on key quantitative findings]
<!-- Evidence: C001 (60% time reduction), C004 (~40% hallucination reduction) | Confidence: medium -->

[TODO_EVIDENCE_NEEDED: 1 sentence on main contribution / takeaway]
<!-- Evidence: GAP-001 from gaps_and_opportunities.md — this paper fills the untested combination gap -->

---

## 1. Introduction

<!-- Paragraph structure:
     P1 — Opening hook + motivation (what problem? why does it matter?)
     P2 — What exists (prior work, briefly)
     P3 — What is missing (the gap that this paper fills)
     P4 — What this paper does (approach overview)
     P5 — Contributions (bulleted)
     P6 — Paper structure ("The rest of this paper is organized as follows…")
-->

### P1 — Motivation

[TODO_EVIDENCE_NEEDED: Opening sentence establishing the scale of the problem — how many papers are published per year, why synthesis is a bottleneck]
<!-- Evidence: [TODO_CITATION_NEEDED: a citation for publication volume growth] -->

Manually synthesizing a large body of literature is time-intensive, with researchers spending an estimated [TODO_RESULT_NEEDED: X hours] per 100-paper review.
<!-- Evidence: C001 | Confidence: high — wang2024llmreview, Table 2 -->

Recent advances in large language models have raised the prospect of automating or augmenting this process, yet concerns about factual reliability have limited adoption.
<!-- Evidence: C003 | Confidence: high — chen2024hallucination, Sec 4.2 -->

### P2 — Prior work (brief)

Large language models achieve high accuracy on structured scientific text processing tasks including citation extraction and methodology classification.
<!-- Evidence: C002, C006 | Confidence: high — lee2023citextract, kim2024classify -->

Initial workflow studies suggest that LLM-assisted review can reduce synthesis time by approximately 60%.
<!-- Evidence: C001 | Confidence: high — wang2024llmreview -->

Retrieval-augmented generation and chain-of-thought prompting have each been shown to reduce error rates in LLM-generated scientific text.
<!-- Evidence: C004, C008 | Confidence: medium — zhao2024rag, sun2024cot -->

### P3 — The gap

[TODO_NOVELTY_CHECK_NEEDED: Confirm no prior paper tests RAG + CoT + structured protocol together — see GAP-001]

However, these mitigations have been studied in isolation; no study has evaluated their combined effect within a unified, structured review protocol.
<!-- Evidence: GAP-001 in gaps_and_opportunities.md — confirmed gap as of 2026-05-25 -->

Furthermore, LLM assistance does not appear to improve the recall of relevant papers, suggesting that it should supplement rather than replace systematic search.
<!-- Evidence: C007 | Confidence: medium — huang2024recall -->

### P4 — This paper

This paper presents [APPROACH NAME PLACEHOLDER], a structured protocol combining RAG, chain-of-thought prompting, and an evidence matrix framework for LLM-assisted literature review.
<!-- Evidence: C010 (protocol design inspiration) | Confidence: medium — ross2024protocol -->

[TODO_EVIDENCE_NEEDED: sentence summarizing the evaluation setup]

### P5 — Contributions

1. [TODO_EVIDENCE_NEEDED: Contribution 1 — the protocol design]
   <!-- Evidence: C010 | Confidence: medium -->
2. [TODO_EVIDENCE_NEEDED: Contribution 2 — the empirical evaluation of the combined pipeline]
   <!-- Evidence: GAP-001 — this is the gap being filled -->
3. [TODO_EVIDENCE_NEEDED: Contribution 3 — practical guidance on threshold / scope]
   <!-- Evidence: GAP-002 | Confidence: high (gap confirmed) -->

### P6 — Paper structure

[TODO_EVIDENCE_NEEDED: standard "rest of paper" sentence — fill when section order is final]

---

## 2. Related Work

<!-- Organized by the three clusters in synthesis/literature_map.md.
     Each subsection = one cluster.
     Do not introduce claims here that are not in the evidence matrix. -->

### 2.1 LLM Capabilities for Scientific Text Processing
<!-- Cluster 1 from literature_map.md -->

Large language models demonstrate strong and near-human-level performance on structured scientific text processing tasks.
<!-- Evidence: C002, C006 | Confidence: high -->

[TODO_EVIDENCE_NEEDED: 2–3 sentences characterizing extraction and classification capability, citing C002 and C006, with explicit scope limitation on non-English text and scanned documents]
<!-- Evidence: C002 (>90% F1 extraction), C006 (94% classification accuracy) | Confidence: high within English STEM scope -->

Domain-adapted models do not consistently outperform general-purpose LLMs on these tasks, suggesting that scale and instruction-following ability are more important than domain pretraining for surface-level extraction.
<!-- Evidence: C009 | Confidence: low — nguyen2024domainadapt (small evaluation set n=200; treat as preliminary finding only) -->

### 2.2 LLM-Assisted Literature Review Workflows
<!-- Cluster 2 from literature_map.md -->

Controlled studies have demonstrated meaningful time savings for LLM-assisted synthesis tasks.
<!-- Evidence: C001 | Confidence: high -->

[TODO_EVIDENCE_NEEDED: 2 sentences on wang2024llmreview findings with specific figures — 60% time reduction, p<0.01, n=24]
<!-- Evidence: C001 | Confidence: high -->

Human evaluators rate LLM-assisted syntheses as equally credible to human-written ones in abstract-length evaluations, though this finding does not extend to full-section synthesis and is contested by expert-level error analysis.
<!-- Evidence: C005 | Confidence: medium — patel2023credibility (abstract-length scope only; see CONTR-002) -->

Crucially, LLM assistance does not improve recall of relevant papers compared to systematic Boolean search, implying that the two approaches should be used in combination rather than substitution.
<!-- Evidence: C007 | Confidence: medium — huang2024recall; directly bounds the scope of C001 -->

Structured evidence matrix protocols reduce duplicate claim registration and improve synthesis consistency in single-institution deployments.
<!-- Evidence: C010 | Confidence: medium — ross2024protocol (single institution, no control condition) -->

### 2.3 Reliability, Hallucination, and Quality Control
<!-- Cluster 3 from literature_map.md -->

LLM-generated scientific summaries contain factual errors at rates that domain experts consider problematic: 12–18% at abstract level and 28% for methods sections, with numerical distortion accounting for 42% of all errors.
<!-- Evidence: C003 | Confidence: high — chen2024hallucination, expert panel n=15, Fleiss kappa=0.81 -->

Retrieval-augmented generation reduces hallucination by approximately 40% relative to standard prompting, though improvement varies substantially by domain (22–55%) and no statistical significance tests are reported.
<!-- Evidence: C004 | Confidence: medium — zhao2024rag -->

Chain-of-thought prompting improves LLM accuracy on structured evidence quality assessment tasks from 61% to 79%, though the evaluation rubric was not independently validated.
<!-- Evidence: C008 | Confidence: medium — sun2024cot -->

[TODO_EVIDENCE_NEEDED: synthesis sentence noting that RAG and CoT have not been tested in combination — sets up the gap and transitions to § 3]
<!-- Evidence: GAP-001 | Confidence: high (gap confirmed from literature map as of 2026-05-25) -->

### 2.4 Gap and Motivation for This Work

No prior study evaluates the combined effect of RAG, chain-of-thought prompting, and a structured evidence matrix protocol within a single unified literature review pipeline.
<!-- Evidence: GAP-001 in synthesis/gaps_and_opportunities.md | Confidence: high -->

The synthesis above reveals that the efficiency gains documented in prior work (C001) rest on quality mitigations (C004, C008) that have only been demonstrated independently — the combined effect on the key failure mode (C003) remains an open empirical question.
<!-- Evidence: C001, C003, C004, C008 | Confidence: medium — inference from independent studies, not measured jointly -->

---

## 3. Method / Approach

<!-- Describe the protocol. Every design decision must be justified by a claim ID
     or explicitly flagged as [DESIGN CHOICE: rationale without a claim ID]. -->

### 3.1 Pipeline overview

[TODO_EVIDENCE_NEEDED: System diagram — Figure 1 — to be inserted here]

The protocol consists of four stages: (1) systematic Boolean search for paper discovery, (2) LLM-assisted screening and structured metadata extraction, (3) RAG + CoT synthesis generation, and (4) structured evidence matrix construction with human spot-checking.
<!-- Evidence: C007 (Boolean search for recall), C002 (LLM extraction), C004 + C008 (RAG + CoT), C010 (evidence matrix) | Confidence: medium — design integrates findings from multiple independent studies -->

### 3.2 Stage 1: Paper discovery via systematic Boolean search

[TODO_EVIDENCE_NEEDED: Description of the Boolean search strategy — databases, date ranges, query terms; see search/query_bank.md]

LLM assistance is explicitly excluded from this stage to preserve the recall that systematic search provides and to avoid the recall deficit documented in prior work.
<!-- Evidence: C007 | Confidence: medium — huang2024recall -->

### 3.3 Stage 2: LLM-assisted screening and extraction

[TODO_EVIDENCE_NEEDED: Screening rubric description — reference screening/screening_rubric.md]

Metadata extraction (title, authors, year, venue, methodology type) is performed by a prompted LLM, exploiting the high accuracy that has been demonstrated on structured scientific PDFs.
<!-- Evidence: C002 (>90% F1), C006 (94% accuracy) | Confidence: high within scope of English-language structured PDFs -->

[DESIGN CHOICE: Scanned and non-standard format PDFs are flagged for manual extraction because LLM extraction accuracy drops to ~74% F1 on those documents — lee2023citextract, Table 5.]

### 3.4 Stage 3: RAG + CoT synthesis generation

[TODO_EVIDENCE_NEEDED: Technical description of RAG setup — retrieval index type, chunk size, top-k, embedding model]

[TODO_EVIDENCE_NEEDED: Chain-of-thought prompt template — reference prompts/synthesis_cot.md]

The rationale for combining RAG and CoT is that each addresses a distinct failure mode documented in the literature: RAG reduces parametric hallucination by grounding generation in retrieved source text, while CoT reduces reasoning shortcuts in quality assessment tasks.
<!-- Evidence: C004 (RAG rationale, ~40% hallucination reduction), C008 (CoT rationale, 18 pp accuracy gain) | Confidence: medium — combining inferred from independent results; joint effect is the empirical contribution of this paper -->

### 3.5 Stage 4: Evidence matrix and human verification

[TODO_EVIDENCE_NEEDED: Description of evidence matrix format — reference evidence/evidence_matrix.csv schema]

The structured evidence tracking approach is adapted from the protocol described in @ross2024protocol, with modifications to integrate the RAG-augmented synthesis stage.
<!-- Evidence: C010 | Confidence: medium — ross2024protocol -->

[DESIGN CHOICE: Human spot-checking is required for all claims rated high-confidence before they enter the draft. This is not validated empirically within this paper but is a conservative safeguard given the residual hallucination rate after RAG (estimated 7–11%).]

---

## 4. Results / Findings

<!-- STAGE GATE: Do not populate this section with real findings until Stage 16
     Result Adequacy Gate passes. All result sentences require TODO_RESULT_NEEDED
     markers until experiments are verified and logged in evidence_matrix.csv. -->

### 4.1 Hallucination rate: combined pipeline vs. baselines

[TODO_RESULT_NEEDED: Primary result — hallucination rate (%) of full pipeline vs. RAG-only, CoT-only, and unaugmented baseline]
<!-- Evidence: [experiment to be run — see plan_experiments/ for design] | Confidence: TBD -->

### 4.2 Time-to-synthesis

[TODO_RESULT_NEEDED: Time-to-synthesis (hours per 100 papers) for combined pipeline vs. manual control condition]
<!-- Evidence: [experiment to be run] | Confidence: TBD -->

### 4.3 Ablation: contribution of each component

[TODO_RESULT_NEEDED: Ablation table — RAG alone, CoT alone, protocol alone, full combination]
<!-- Evidence: [experiment to be run — 2x2 factorial design matching GAP-001 potential approach] | Confidence: TBD -->

### 4.4 Recall preservation

[TODO_RESULT_NEEDED: Recall rate (%) of combined pipeline (Boolean + LLM) vs. Boolean-only condition, measured against gold-standard reference list]
<!-- Evidence: [experiment to be run] | Confidence: TBD -->

---

## 5. Discussion

### 5.1 The quality–efficiency trade-off

[TODO_EVIDENCE_NEEDED: Synthesis of C001 + C003 + C004 — state the core trade-off and whether this paper's results resolve it]
<!-- Evidence: C001 (efficiency), C003 (quality cost), C004 (mitigation) | Confidence: medium -->

The residual hallucination rate after applying the combined protocol [TODO_RESULT_NEEDED: insert figure from § 4.1] must be evaluated against an acceptable threshold for the target use case — a threshold the field has not yet formally defined.
<!-- Evidence: GAP-002 in synthesis/gaps_and_opportunities.md | Confidence: high (gap confirmed) -->

### 5.2 Scope of the efficiency gains

The ~60% time reduction documented by @wang2024llmreview applies to synthesis tasks only, and should not be interpreted as an overall review time reduction because systematic Boolean search for discovery is retained in this protocol.
<!-- Evidence: C001, C007 | Confidence: high -->

[TODO_EVIDENCE_NEEDED: Estimate what fraction of total review time is synthesis vs. discovery, so readers can calibrate the practical impact]

### 5.3 Implications for practice

[TODO_EVIDENCE_NEEDED: 2–3 practical recommendations for researchers considering LLM-assisted review, each traced to a claim ID]
<!-- Evidence: C001 (efficiency), C007 (keep Boolean search), C004 + C008 (apply RAG + CoT), C010 (use structured protocol) | Confidence: medium -->

### 5.4 Limitations

1. **No established acceptable hallucination threshold.** The field lacks a formal definition of acceptable error rates for AI-assisted systematic reviews, making it difficult to declare whether the pipeline's residual error rate is "good enough."
   <!-- Evidence: GAP-002 | Confidence: high -->

2. **Recall is not improved by LLM assistance.** The current protocol mitigates this by maintaining systematic Boolean search, but does not eliminate the risk of missed papers in users who substitute LLM-assisted search for Boolean search.
   <!-- Evidence: C007 | Confidence: medium -->

3. **Evaluated on English-language STEM documents only.** Generalization to non-English corpora and to social science or humanities domains is not established.
   <!-- Evidence: GAP-004 in synthesis/gaps_and_opportunities.md | Confidence: high -->

4. **Combined mitigation effect inferred, not pre-measured.** [TODO_RESULT_NEEDED: replace this placeholder with the empirical result from § 4.3 once available.]
   <!-- Evidence: GAP-001 | Confidence: high (gap confirmed; this paper fills it) -->

5. **Credibility equivalence does not imply factual equivalence.** Human credibility ratings (@patel2023credibility) are insensitive to the error categories documented by domain experts (@chen2024hallucination). These two findings address different constructs and must not be conflated.
   <!-- Evidence: C005, C003 | Confidence: high (CONTR-002 in contradiction_notes/) -->

6. **Single rubric for quality assessment.** The chain-of-thought quality rubric (@sun2024cot) has not been independently validated; accuracy figures may not replicate on different rubrics or disciplines.
   <!-- Evidence: C008 | Confidence: medium -->

---

## 6. Conclusion

[TODO_EVIDENCE_NEEDED: 1–2 sentences restating the thesis and whether results support it — write after § 4 is populated]
<!-- Evidence: C001, C004, C008, C010 | Confidence: medium — pending Stage 16 gate -->

[TODO_EVIDENCE_NEEDED: 1 sentence on the main empirical contribution — what this paper established that prior work had not]
<!-- Evidence: GAP-001 (now filled by this paper's experiment) -->

The most critical open question for future work is the definition of an acceptable hallucination threshold for AI-assisted systematic reviews, without which progress in the field cannot be benchmarked against a meaningful standard.
<!-- Evidence: GAP-002 | Confidence: high -->

[TODO_EVIDENCE_NEEDED: 1 sentence on open-source model evaluation as future direction]
<!-- Evidence: GAP-005 | Confidence: high -->

---

## References

<!-- All references must match entries in library/references.bib.
     Do not add a reference that does not have a verified BibTeX entry.
     Cross-check every @citekey in this document against references.bib before submission.
     Run: python scripts/validate_citations.py to check for orphans. -->

[TODO_CITATION_NEEDED: verify all citekeys below have matching references.bib entries before submission]

- @wang2024llmreview
- @lee2023citextract
- @chen2024hallucination
- @zhao2024rag
- @patel2023credibility
- @huang2024recall
- @kim2024classify
- @sun2024cot
- @nguyen2024domainadapt
- @ross2024protocol
