# Literature Map

<!-- Purpose: cluster the papers in this project's library into thematic groups,
     document consensus and disagreement within each cluster, and trace how the
     field has evolved over time. Update this file whenever a new paper is added
     to the library or a concept note is revised.
     
     This document feeds directly into:
       - draft.md § Related Work (each cluster = one subsection)
       - argument_map.md (cluster consensus → supporting argument or counterargument)
       - gaps_and_opportunities.md (cluster disagreements → gap candidates) -->

<!-- Last updated: 2026-05-25 -->

---

## Overview

| Field | Value |
|---|---|
| Total papers in library | 10 (as of 2026-05-25) |
| Date range | 2023–2024 |
| Earliest paper | lee2023citextract (2023) |
| Most recent paper | ross2024protocol (2024) |

### Venue distribution

| Venue | Count | Tier |
|---|---|---|
| ACL / EMNLP / NAACL | 3 | A* |
| NeurIPS / ICML / ICLR | 2 | A* |
| JASIST / JIS | 2 | Q1 journal |
| Workshop / preprint | 2 | unranked |
| CHI | 1 | A* |

---

## Cluster 1: LLM Capabilities for Scientific Text Processing

### Core papers
- @lee2023citextract
- @kim2024classify
- @nguyen2024domainadapt

### Consensus view

Large language models — particularly GPT-4 and instruction-tuned variants — demonstrate strong performance on structured extraction tasks (citation parsing, methodology classification) applied to scientific PDFs. Accuracy on binary or low-cardinality classification tasks consistently exceeds 90% when evaluated against human-annotated gold standards. General-purpose LLMs match or exceed domain-adapted models on these tasks (@nguyen2024domainadapt), suggesting that scale and instruction-following ability are more important than domain pretraining for surface-level extraction.

**Scope of consensus:** English-language, well-formatted academic PDFs. Performance degrades on scanned documents (@lee2023citextract, Table 5) and on fine-grained classification tasks beyond binary.

### Key disagreements

- **Domain adaptation benefit:** @nguyen2024domainadapt finds no improvement from domain adaptation, which conflicts with prior intuitions but is consistent with the scaling hypothesis. This is an emerging, contested finding.
- **Generalization to non-English:** No paper in this cluster evaluates non-English scientific text. It is unknown whether the 90%+ figures hold.

### Open questions

1. Does performance on extraction tasks transfer to reasoning-intensive tasks (e.g., inferring causal claims from methods sections)?
2. What is the failure mode distribution across scientific disciplines (STEM vs. social sciences vs. humanities)?
3. Can smaller, locally deployable models replicate these results at acceptable accuracy?

### Representative quote

> "GPT-4 achieves 94% accuracy on methodology classification, approaching the 97% human ceiling, suggesting that broad instruction-following capability suffices for this structured prediction task."
> — @kim2024classify, p.5

---

## Cluster 2: LLM-Assisted Literature Review Workflow

### Core papers
- @wang2024llmreview
- @patel2023credibility
- @huang2024recall
- @ross2024protocol

### Consensus view

Integrating LLMs into the literature review process measurably reduces time-to-synthesis (@wang2024llmreview). Structured protocols — explicit screening rubrics, evidence matrices, and role-separated prompting — improve consistency and reduce duplicate claim registration (@ross2024protocol). Human evaluators find LLM-assisted syntheses credible when assessed at abstract length and without adversarial domain expertise (@patel2023credibility).

**Scope of consensus:** Time and credibility benefits are established. Recall and completeness benefits are disputed (@huang2024recall).

### Key disagreements

- **Recall vs. efficiency trade-off:** @wang2024llmreview demonstrates time efficiency gains; @huang2024recall shows these gains do not extend to improved recall of relevant papers. Both findings are methodologically sound — they measure different outcomes. The trade-off is real: LLMs help you synthesize faster but do not reliably help you find papers you would otherwise miss.
- **Generalizability of credibility ratings:** @patel2023credibility evaluates abstract-length syntheses with non-expert raters; domain expert evaluation (@chen2024hallucination, Cluster 3) reveals error rates that challenge the credibility parity finding.

### Open questions

1. What structured prompting strategies most reliably improve synthesis completeness?
2. Can recall be improved by combining LLM-assisted synthesis with systematic Boolean search rather than replacing it?
3. How does the protocol described in @ross2024protocol scale to reviews with >500 papers?

### Representative quote

> "Participants in the LLM-assisted condition completed their synthesis in an average of 4.2 hours compared to 10.6 hours in the manual condition (60% reduction), with no significant difference in evaluator-rated quality."
> — @wang2024llmreview, Table 2, p.8

---

## Cluster 3: Reliability, Hallucination, and Quality Control

### Core papers
- @chen2024hallucination
- @zhao2024rag
- @sun2024cot

### Consensus view

Hallucination is a measurable, non-trivial problem in LLM-generated scientific text: error rates of 12–28% (depending on section type) are documented by domain experts (@chen2024hallucination). Retrieval-augmented generation provides a meaningful but partial mitigation (~40% relative reduction, @zhao2024rag). Chain-of-thought prompting improves accuracy on structured quality-assessment tasks (@sun2024cot). Taken together, the cluster converges on the view that raw LLM output requires quality-control scaffolding before it is trustworthy in high-stakes research workflows.

**Scope of consensus:** Most evidence is from English-language STEM domains. Social science and humanities are underrepresented.

### Key disagreements

- **Sufficiency of RAG as mitigation:** @zhao2024rag shows a 40% relative hallucination reduction, but the residual error rate (roughly 7–11%) may still be unacceptable for systematic reviews where every claim matters. No paper in this cluster has defined an acceptable error threshold.
- **CoT scalability:** @sun2024cot's rubric for quality assessment was not independently validated; the 79% accuracy figure may not replicate on different rubrics or domains.

### Open questions

1. Does combining RAG + CoT + human spot-checking bring hallucination rates below 5%? No experiment tests this combination.
2. Are there domain-specific patterns in hallucination (e.g., numerical distortion vs. causal inversion) that allow targeted mitigations?
3. Can LLMs reliably self-audit their own hallucinations?

### Representative quote

> "Factual errors appear in 12–18% of abstract-level summaries and in 28% of methods-section summaries, with numerical distortion accounting for 42% of all errors — suggesting that quantitative claims require especially careful human verification."
> — @chen2024hallucination, Sec 4.2, p.6

---

## Cross-cluster relationships

| Relationship | Clusters | Description |
|---|---|---|
| Enables | 1 → 2 | Extraction and classification capabilities (Cluster 1) are infrastructure for the workflow gains claimed in Cluster 2 |
| Bounds | 3 → 2 | Hallucination rates (Cluster 3) set the quality ceiling for efficiency claims (Cluster 2); gains in C001 must be qualified by C003 |
| Mitigates | 3 → 3 (internal) | RAG and CoT (Cluster 3) partially address the hallucination problems documented in the same cluster |
| Motivates | 3 → 2 | Quality concerns in Cluster 3 motivate the structured protocol work in Cluster 2 (@ross2024protocol) |

---

## Evolution over time

| Period | Dominant theme | Key shift |
|---|---|---|
| 2023 | Capability demonstration | Papers established that LLMs can perform scientific extraction tasks at near-human accuracy; optimism was high |
| Early 2024 | Workflow integration | First controlled studies tested LLMs in actual review workflows; efficiency gains confirmed but quality concerns surfaced |
| Mid–Late 2024 | Quality control and mitigation | RAG, CoT, and structured protocols emerged as responses to documented hallucination; field moved from "can it work?" to "how do we make it safe?" |

**Trajectory:** The field has moved from demonstrating capability toward establishing safeguards. The next phase (not yet represented in this library) is likely to focus on human-AI collaboration protocols and formal evaluation standards for LLM-assisted reviews.
