# Claim Registry

<!-- Purpose: the authoritative record of every claim tracked in this project.
     Every row in evidence_matrix.csv MUST have a corresponding entry here.
     Every factual sentence in draft.md MUST cite at least one Claim ID from this registry.
     
     Workflow:
       1. Read a paper → extract claims → add rows to evidence_matrix.csv
       2. Add full entries here
       3. When drafting, insert <!-- Evidence: CXXX --> comments next to each claim sentence
       4. Before submission, run the audit: every CXXX in the draft must appear in this registry
     
     Numbering: sequential, never reuse a retired ID. If a claim is withdrawn, mark it
     [withdrawn] and explain — do not delete the entry. -->

<!-- Last updated: 2026-05-25 -->

---

## C001 — LLM-assisted review cuts synthesis time by ~60%

**Full claim:** "LLM-assisted literature review reduces the time required to synthesize 100 papers by approximately 60% compared to unassisted manual review."

**Source:** @wang2024llmreview, Table 2, p.8

**Evidence type:** experiment

**Confidence:** high

**Study context:** Randomized controlled study with 24 graduate students across two conditions (manual vs. GPT-4-assisted). Time measured from task assignment to submission of synthesis document. Statistically significant (p < 0.01, independent samples t-test).

**Supporting claims:** C002 (automated extraction enables the speed gain), C004 (RAG reduces the hallucination cost of that speed gain), C008 (structured prompting improves accuracy of LLM outputs used in the pipeline)

**Contradicted by:** C007 (LLM assistance does not improve recall of relevant papers), C003 (hallucination rate introduces a quality cost not captured by time metric alone)

**Used in:** `draft.md` § Related Work ¶2

**Status:** active

**Notes:** Time efficiency is the primary benefit. Quality trade-offs are addressed by citing C003 and C004 together. C007 bounds the claim: the time saving applies to synthesis, not to discovery.

---

## C002 — Automated citation extraction achieves >90% F1

**Full claim:** "Automated citation extraction from PDFs using large language models achieves greater than 90% F1 on structured scientific documents."

**Source:** @lee2023citextract, Table 4, p.12

**Evidence type:** experiment

**Confidence:** high

**Study context:** Evaluated on PubMed and arXiv corpora. Inter-annotator agreement between human annotators reported (Cohen's kappa = 0.87), establishing a reliable ground truth. Error analysis shows most failures occur on non-standard reference formats (conference proceedings without DOI).

**Supporting claims:** C001 (reliable extraction is a prerequisite for the speed gains in C001), C006 (paper classification is the downstream task enabled by accurate extraction)

**Contradicted by:** (none currently registered)

**Used in:** `draft.md` § Related Work ¶1

**Status:** active

**Notes:** The >90% F1 figure is for structured PDFs; performance on scanned or poorly formatted documents is reported as 74% F1 in the same paper (Table 5) — important scope limitation.

---

## C003 — LLM summaries contain factual errors at 12–18% rate

**Full claim:** "LLM-generated summaries of scientific abstracts contain factual errors at a rate of 12–18% when evaluated by domain experts, rising to 28% for methods sections."

**Source:** @chen2024hallucination, Sec 4.2, p.6

**Evidence type:** experiment

**Confidence:** high

**Study context:** Expert panel of 15 domain reviewers (5 per domain: medicine, computer science, economics). Each expert reviewed 60 LLM-generated summaries and flagged factual errors. Inter-rater reliability: Fleiss' kappa = 0.81. Error categories: number/statistic distortion (42%), method misattribution (31%), causal inversion (27%).

**Supporting claims:** (none — this is a negative finding that bounds C001)

**Contradicted by:** C004 (RAG-based approaches reduce this rate by ~40%), C005 (human evaluators in a different study find LLM syntheses equally credible — methodological difference: C005 evaluates full syntheses, C003 evaluates individual summaries)

**Used in:** `draft.md` § Discussion ¶1 (limitation of LLM-assisted review)

**Status:** active

**Notes:** Core tension with C001. To use C001 responsibly in the draft, C003 must appear in the same paragraph or in limitations. Resolution: cite C004 as a mitigation. See also CONTR-001 for the C001 vs. C003 contradiction note.

---

## C004 — RAG reduces hallucination in scientific summarization by ~40%

**Full claim:** "Retrieval-augmented generation reduces hallucination rate in scientific summarization by approximately 40% relative to standard prompting, though improvement varies by domain (22–55%)."

**Source:** @zhao2024rag, Table 3, p.10

**Evidence type:** experiment

**Confidence:** medium

**Study context:** Tested on three benchmarks (SciFact, QASPER, and a proprietary medical QA set). No statistical significance tests reported — relative improvement only. Domain variation (22–55%) is wide, suggesting the aggregate 40% figure masks important heterogeneity.

**Supporting claims:** C001 (RAG is a practical mitigation for the quality cost identified in C003, enabling C001's pipeline to be deployed responsibly)

**Contradicted by:** (none directly; C003 provides the baseline that C004 improves on)

**Used in:** `draft.md` § Related Work ¶3

**Status:** active

**Notes:** Confidence is medium rather than high because no significance tests are reported. When citing in draft, hedge: "approximately 40%" and note the domain variability in a parenthetical or footnote.

---

## C005 — Human judges rate LLM syntheses as equally credible to human-written ones

**Full claim:** "In double-blind evaluation, human researchers rate LLM-assisted literature syntheses as equally credible to human-written syntheses (no statistically significant difference in credibility scores)."

**Source:** @patel2023credibility, Sec 5, p.14

**Evidence type:** experiment

**Confidence:** medium

**Study context:** n = 40 evaluators (graduate students and postdocs); rated abstracts on a 7-point credibility scale. Limitation noted by authors: only abstract-length syntheses were evaluated, not full sections. Potential demand characteristics: evaluators may have suspected LLM involvement despite blinding procedure.

**Supporting claims:** C001 (credibility parity strengthens the case for LLM-assisted review)

**Contradicted by:** C003 (expert domain reviewers do find errors — the contradiction may be explained by evaluator expertise: patel2023credibility uses general credibility rating, chen2024hallucination uses domain expert error-spotting)

**Used in:** `draft.md` § Discussion ¶2 (pending — flagged for verification before inclusion)

**Status:** active

**Notes:** Use with care. The methodological gap between C005 and C003 should be addressed in the draft. See contradiction note CONTR-002.

---

## C006 — GPT-4 classifies paper methodology with 94% accuracy

**Full claim:** "GPT-4 correctly identifies the methodology of a scientific paper (qualitative vs. quantitative) with 94% accuracy on a held-out test set."

**Source:** @kim2024classify, Table 1, p.5

**Evidence type:** experiment

**Confidence:** high

**Study context:** Binary classification task on 500 papers sampled from Web of Science. Human baseline accuracy on the same task: 97%. Error analysis: most GPT-4 errors occur on mixed-methods papers (misclassified as quantitative 71% of the time).

**Supporting claims:** C002 (accurate classification downstream of accurate extraction makes the full pipeline viable), C010 (automated classification is a key step in structured evidence matrix protocols)

**Contradicted by:** C009 (domain-adapted LLMs are not better than general LLMs on domain-specific tasks — C006's strong result with a general LLM is consistent with C009's finding)

**Used in:** `draft.md` § none (background claim, not yet placed)

**Status:** active

**Notes:** 94% accuracy is high but the binary task is simpler than fine-grained methodology classification. If the draft needs finer-grained claims (e.g., RCT vs. observational study), this figure does not apply. Do not over-generalize.

---

## C007

**Full claim:** "LLM assistance in literature review does not significantly reduce missed relevant papers compared to manual keyword search."

**Source:** @huang2024recall, Sec 3.3, p.9

**Evidence type:** experiment

**Confidence:** medium

**Study context:** 6 systematic reviews compared; LLM-assisted recall 0.87 vs. Boolean-only 0.85 (p=0.31, not significant). Different metric from C001 (time efficiency) — both claims can coexist.

**Supporting claims:** none

**Contradicted by:** C001 (C001 shows efficiency gains; C007 shows no recall gains — these address different metrics and are not genuinely contradictory)

**Used in:** `draft.md` § discussion

**Status:** active

**Notes:** Critical boundary condition: LLM assistance improves speed but not coverage. Protocol design must retain systematic Boolean search. Do not cite C007 as evidence that LLM assistance is ineffective overall.

---

## C008

**Full claim:** "Chain-of-thought prompting improves LLM accuracy on evidence quality assessment tasks from 61% to 79%."

**Source:** @sun2024cot, Table 2, p.7

**Evidence type:** experiment

**Confidence:** medium

**Study context:** Measured on a custom evidence quality rubric (GRADE-inspired). Rubric was not independently validated. Inter-annotator agreement among human raters: kappa=0.71. Improvement is real but rubric validity is uncertain.

**Supporting claims:** C004 (both show that structured prompting strategies reduce LLM error rates)

**Contradicted by:** none directly; validity of the rubric is the main caveat

**Used in:** `draft.md` § method (pending)

**Status:** active

**Notes:** Medium confidence because the rubric itself is unvalidated. Do not claim 79% as an absolute accuracy figure — always qualify with "on the GRADE-inspired rubric used in the study."

---

## C009

**Full claim:** "LLMs trained on scientific corpora perform no better than general LLMs on domain-specific claim verification tasks."

**Source:** @nguyen2024domainadapt, Sec 4, p.11

**Evidence type:** experiment

**Confidence:** low

**Study context:** Only 2 domain-adapted models tested (BioMedLM, SciDeBERTa) vs. GPT-4. Small evaluation set (n=200 claims per domain). Results: biomedical 0.79 vs 0.81, CS 0.83 vs 0.82 — differences are small and may not be significant.

**Supporting claims:** C006 (general GPT-4 strong performance on methodology classification is consistent with C009's finding)

**Contradicted by:** common assumption that domain pretraining helps; C009 challenges this but with very low statistical power

**Used in:** `draft.md` § none (background, low confidence — use cautiously)

**Status:** active

**Notes:** LOW CONFIDENCE. n=200 is insufficient to draw strong conclusions. Treat as a preliminary finding. Do not present this as established fact. Phrase as: "Preliminary evidence suggests that domain adaptation may not provide consistent benefits (nguyen2024domainadapt), though larger-scale evaluations are needed."

---

## C010

**Full claim:** "A structured evidence matrix protocol combined with LLM-assisted screening reduces duplicate claim registration by 73% versus unstructured note-taking."

**Source:** @ross2024protocol, Sec 6, p.16

**Evidence type:** case-study

**Confidence:** medium

**Study context:** Single-group pilot study at one institution (n=8 research teams). No control condition — comparison is self-reported retrospective vs. structured condition. Methodology directly relevant to the design of this Research OS.

**Supporting claims:** C001 (both support the value of structured LLM-assisted workflows)

**Contradicted by:** none directly; main weakness is lack of control condition

**Used in:** `draft.md` § method

**Status:** active

**Notes:** The 73% figure is compelling but comes from a single-group study with no randomization. Cite with appropriate hedging: "In a pilot evaluation, ross2024protocol found..." Do not present as a robust empirical result without the caveat about study design.
