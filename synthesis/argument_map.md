# Argument Map

<!-- Purpose: make the logical structure of the paper's thesis explicit.
     Every claim in this map must trace to a Claim ID in claim_registry.md.
     Every counterargument must trace to a Contradiction Note in contradiction_notes/.
     
     This document is the bridge between the evidence matrix and the draft.
     Before writing any section of draft.md, verify the argument structure here first.
     If an argument cannot be traced to a Claim ID, it MUST NOT appear in the draft. -->

<!-- Last updated: 2026-05-25 -->

---

## Main thesis

> **LLM-assisted literature review, when implemented with structured quality-control protocols (RAG, chain-of-thought prompting, and evidence matrix tracking), provides a net benefit for research synthesis — reducing time to synthesis without an unacceptable increase in factual error rate — compared to unassisted manual review.**

**Thesis confidence:** medium

**Rationale for confidence level:** The efficiency gain is strongly evidenced (C001, high confidence). The quality mitigation is moderately evidenced (C004, medium confidence; C008, medium confidence). The claim that the net benefit is "acceptable" requires a threshold judgment that the current literature has not defined. Until a study directly tests the full pipeline (RAG + CoT + structured protocol), the combined mitigation effect remains an inference rather than a measured result.

**What would change this conclusion (falsifiability):**
1. A direct comparison study showing that RAG + CoT does NOT reduce hallucination rates below an agreed acceptable threshold (e.g., < 5%) would require weakening the thesis to "conditionally beneficial."
2. A recall study showing that LLM-assisted workflows systematically miss entire literature sub-fields (not just individual papers) would require narrowing the thesis to synthesis-only, excluding discovery tasks.
3. A replication failure of @wang2024llmreview's 60% time-reduction finding in a larger, pre-registered study would undermine the efficiency pillar.

---

## Supporting arguments

### SA-1: LLM-assisted review is substantially faster than manual review

**Summary:** Integrating LLMs into the review pipeline reduces synthesis time by ~60%, a practically meaningful efficiency gain.

**Claim trace:** C001 (high confidence, @wang2024llmreview, RCT, n=24)

**Mechanism:** LLMs accelerate abstract screening, relevance scoring, and initial summary generation — tasks that are cognitively demanding but structurally repetitive for humans.

**Scope:** Applies to synthesis tasks. Does not apply to paper discovery / recall (see CA-1).

**Confidence:** high

**Draft location:** § Introduction ¶2 (motivation), § Related Work — Cluster 2

---

### SA-2: Structured extraction infrastructure makes the pipeline reliable

**Summary:** LLMs perform high-accuracy citation extraction and methodology classification, providing the structured inputs that the synthesis workflow requires.

**Claim trace:** C002 (high confidence, @lee2023citextract, F1 > 90%), C006 (high confidence, @kim2024classify, 94% accuracy)

**Mechanism:** Reliable extraction is a prerequisite for efficient synthesis. If extraction is noisy, the time savings of SA-1 are offset by downstream error correction. C002 and C006 together show the prerequisite is met for well-formatted PDFs.

**Scope limitation:** Scanned or non-standard PDFs reduce extraction F1 to ~74% (C002 footnote). Studies limited to English-language documents.

**Confidence:** high (within scope)

**Draft location:** § Related Work — Cluster 1, § Method (pipeline description)

---

### SA-3: Quality-control mitigations substantially reduce hallucination cost

**Summary:** RAG reduces hallucination by ~40% and chain-of-thought prompting improves evidence quality assessment accuracy by 18 percentage points, making the quality cost of LLM assistance manageable.

**Claim trace:** C004 (medium confidence, @zhao2024rag), C008 (medium confidence, @sun2024cot)

**Mechanism:** RAG grounds generation in retrieved source text, reducing the model's reliance on parametric memory. CoT forces the model to reason step-by-step through quality criteria before rendering a judgment, reducing classification shortcuts.

**Combined effect:** No single study tests RAG + CoT together. The combined mitigation effect is inferred from two independent results — this is the weakest inferential link in the argument.

**Confidence:** medium

**Draft location:** § Method (protocol design rationale), § Discussion ¶1 (quality assurance)

---

### SA-4: Structured protocols produce outputs that humans judge as credible

**Summary:** When implemented with proper structure, LLM-assisted syntheses receive credibility ratings from human evaluators that are statistically equivalent to human-written syntheses.

**Claim trace:** C005 (medium confidence, @patel2023credibility, n=40), C010 (medium confidence, @ross2024protocol)

**Scope limitation:** C005 evaluates abstract-length syntheses only; full-section credibility is untested. C010 is a single-institution case study without a control condition.

**Confidence:** medium (at abstract length); low (for full-section synthesis)

**Draft location:** § Results / Findings ¶2, § Discussion ¶3

---

## Counterarguments

### CA-1: LLM assistance does not improve — and may harm — literature discovery recall

**Summary:** Using LLMs for paper screening does not significantly improve the recall of relevant papers compared to manual keyword search, meaning the pipeline may miss important literature.

**Claim trace:** C007 (medium confidence, @huang2024recall)

**Contradiction note:** CONTR-001 (`contradiction_notes/CONTR-001.md`)

**Why this is a genuine challenge:** If the LLM-assisted workflow is used as a replacement for systematic Boolean search, papers outside the LLM's training distribution may be systematically missed. The 60% time saving in SA-1 partially reflects a reduction in thoroughness, not only in cognitive load.

**Rebuttal (RB-1):** The thesis claims that LLM assistance improves *synthesis*, not *discovery*. If LLM-assisted search is used as a supplement to, rather than a replacement for, systematic Boolean search, CA-1 does not undermine the thesis. The protocol described in @ross2024protocol explicitly combines both approaches.

**Residual limitation after rebuttal:** Users who replace systematic search with LLM-assisted search alone will see degraded recall. This must be flagged as a misuse case in the draft's limitations section.

---

### CA-2: LLM-generated scientific summaries contain factual errors at a rate that domain experts find unacceptable

**Summary:** Even with LLM assistance, summaries contain factual errors at 12–28% depending on section type — a rate that may be too high for systematic reviews where every claim requires accurate representation.

**Claim trace:** C003 (high confidence, @chen2024hallucination)

**Contradiction note:** CONTR-002 (`contradiction_notes/CONTR-002.md`)

**Why this is a genuine challenge:** C003 is a high-confidence finding from domain experts, which makes it the strongest evidence against the thesis. The 28% error rate in methods sections is especially damaging, as methods are often the most critical section for evidence synthesis.

**Rebuttal (RB-2):** SA-3 addresses this with C004 and C008: RAG reduces hallucination by ~40% (bringing the 12–18% rate to roughly 7–11%), and CoT prompting further improves accuracy. With a structured review protocol (@ross2024protocol), human spot-checking is explicitly built in for high-stakes claims. The combined mitigation may bring error rates to an acceptable level — but this remains to be demonstrated empirically (honest limitation).

**Residual limitation after rebuttal:** No study has measured the post-mitigation error rate in a realistic full-pipeline deployment. CA-2 should be acknowledged in the limitations section even after RB-2 is presented.

---

### CA-3: Credibility equivalence may reflect evaluator limitations rather than true quality parity

**Summary:** The finding that human evaluators rate LLM syntheses as equally credible to human-written ones (C005) may reflect the difficulty of detecting subtle errors without domain expertise, rather than genuine quality equivalence.

**Claim trace:** C005 (medium confidence, @patel2023credibility) vs. C003 (high confidence, @chen2024hallucination)

**Contradiction note:** CONTR-002 (`contradiction_notes/CONTR-002.md`)

**Why this is a genuine challenge:** CA-2 and CA-3 together suggest that non-expert credibility ratings are not a reliable proxy for factual accuracy. If SA-4 relies on credibility ratings, and those ratings are insensitive to the errors documented in C003, SA-4 is a weaker argument than it appears.

**Rebuttal (RB-3):** SA-4 is presented as evidence about perceived usability, not factual accuracy. The draft should clearly distinguish these two dimensions: "LLM-assisted syntheses are perceived as credible (C005), though this perception does not guarantee the absence of errors (C003), which is why the quality-control protocol described in § Method is essential."

**Residual limitation after rebuttal:** SA-4 should be deprioritized in the draft; RB-3 largely concedes the point. SA-1, SA-2, and SA-3 carry the thesis.

---

## Confidence assessment for the thesis

| Pillar | Argument | Confidence | Key evidence |
|---|---|---|---|
| Efficiency gain | SA-1 | high | C001 (RCT) |
| Infrastructure reliability | SA-2 | high (within scope) | C002, C006 |
| Quality mitigation | SA-3 | medium | C004, C008 (no joint test) |
| Net acceptability | SA-4 | medium–low | C005, C010 (scope-limited) |

**Overall thesis confidence: medium**

The efficiency and infrastructure pillars are strongly supported. The quality mitigation pillar is moderately supported but relies on inference from two independent studies rather than a direct test. The net acceptability pillar is the weakest and should be hedged in the draft.

---

## What would change this conclusion

| Scenario | Impact on thesis |
|---|---|
| Replication failure of @wang2024llmreview | Would eliminate SA-1; thesis requires major revision |
| Study showing RAG + CoT < 5% hallucination rate | Would upgrade SA-3 to high confidence; thesis strengthens |
| Study showing RAG + CoT still > 15% hallucination | Would require narrowing thesis: "beneficial only with mandatory human verification" |
| Large-scale recall study confirming C007 | Would require explicit restriction: "synthesis only, not discovery" |
| Pre-registered replication of C005 with domain experts | Would clarify whether SA-4 survives expert scrutiny |
