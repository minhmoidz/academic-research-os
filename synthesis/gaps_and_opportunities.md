# Research Gaps and Opportunities

<!-- Purpose: systematically catalog where the literature falls short, prioritize those gaps,
     and derive actionable research questions.
     
     Gap taxonomy (from Research OS Stage 6):
       1. Unexplored Combination — two existing techniques never tested together
       2. Contradictory Results — two high-quality papers reach opposite conclusions
       3. Missing Baseline — a claim is made without comparison to a relevant alternative
       4. Efficiency Gap — a method works but is too slow/expensive for practical use
       5. Generalization Gap — a finding holds in one domain/language/scale but not others
     
     Priority scores (1–5): 5 = field-defining, blocks multiple downstream papers;
                             1 = incremental, unlikely to change practice. -->

<!-- Last updated: 2026-05-25 -->

---

## Gap inventory

---

### GAP-001 — Untested combination of RAG + CoT + structured protocol in a single pipeline

**Gap type:** Unexplored Combination

**Description:** RAG reduces hallucination by ~40% (@zhao2024rag, C004). Chain-of-thought prompting improves quality-assessment accuracy by 18 pp (@sun2024cot, C008). Structured evidence matrix protocols reduce duplicate claims by 73% (@ross2024protocol, C010). These three mitigations have been studied in isolation — no study tests them in combination in a unified literature review pipeline.

**Evidence this gap exists:**
- @zhao2024rag (C004) tests RAG alone; no CoT
- @sun2024cot (C008) tests CoT alone; no RAG
- @ross2024protocol (C010) tests the protocol; neither RAG nor CoT is evaluated as a component
- The synthesis in argument_map.md § SA-3 explicitly flags this as an inferential gap rather than a measured result

**Why it matters:** The thesis of this project depends on the combined mitigation effect. If RAG + CoT together do not reduce hallucination below ~10%, the quality case for LLM-assisted review is much weaker than currently argued. This gap directly bounds the confidence of the main thesis.

**Difficulty:** medium — requires building and evaluating a unified pipeline, but all components are off-the-shelf. The main challenge is designing a realistic benchmark with ground-truth hallucination labels.

**Potential approach:** Conduct a 2x2 factorial experiment (RAG on/off × CoT on/off) on a hallucination benchmark (e.g., FELM or a new scientific-text benchmark), with structured protocol as a fixed condition. Report hallucination rates by error category (C003's taxonomy: numerical distortion, method misattribution, causal inversion).

**Priority score:** 5/5

---

### GAP-002 — No agreed acceptable hallucination threshold for systematic reviews

**Gap type:** Missing Baseline

**Description:** @chen2024hallucination documents 12–28% error rates and frames them as problematic, but no paper in the field has formally defined an acceptable error rate threshold for LLM-assisted systematic reviews. Without a threshold, it is impossible to say whether the post-mitigation error rate (estimated ~7–11% after RAG) is "good enough."

**Evidence this gap exists:**
- @chen2024hallucination (C003) reports rates but does not propose a threshold
- @zhao2024rag (C004) reports improvement but does not evaluate against a threshold
- Cochrane systematic review standards (outside this library) define thresholds for inter-rater agreement but not for AI error rates — a direct analogy is not established

**Why it matters:** Without a threshold, research in this area cannot declare success or failure. Every mitigation study produces a relative improvement figure but cannot say whether the result is fit for purpose. This gap makes the entire field's progress hard to evaluate.

**Difficulty:** high — threshold definition requires stakeholder consensus (researchers, journal editors, ethics boards), not just empirical measurement. This is partly a governance and norms problem, not only a technical one.

**Potential approach:** Survey systematic review practitioners and journal editors to elicit acceptable error rate thresholds across disciplines. Publish a position paper proposing a tiered standard (e.g., < 5% for medical systematic reviews, < 10% for exploratory reviews in STEM).

**Priority score:** 4/5

---

### GAP-003 — Contradictory findings on whether LLM assistance improves recall

**Gap type:** Contradictory Results

**Description:** @wang2024llmreview (C001) shows 60% time reduction and implies quality is maintained; @huang2024recall (C007) shows LLM assistance does not improve recall of relevant papers. These use different metrics (time and quality rating vs. recall), but both studies frame themselves as evaluating "LLM-assisted literature review." The contradiction has not been formally reconciled.

**Evidence this gap exists:**
- See contradiction note CONTR-001
- No meta-analysis or direct comparison study exists
- Argument map § CA-1 discusses the boundary conditions but notes no empirical test of the "supplement not replace" recommendation

**Why it matters:** If practitioners conflate the two use cases (synthesis acceleration vs. discovery assistance), they will misapply LLM tools and miss relevant literature. The field needs a clear delineation, supported by empirical evidence, of what LLM assistance does and does not improve.

**Difficulty:** medium — a well-designed comparative study (Boolean search alone vs. LLM-assisted vs. LLM + Boolean combined) would directly address this. The challenge is recruiting sufficient participants and defining a gold-standard recall metric.

**Potential approach:** Pre-registered recall study with three conditions: (1) systematic Boolean search only, (2) LLM-assisted search only, (3) LLM-assisted search supplementing Boolean search. Measure recall against a gold standard (e.g., Cochrane review reference list). Report both recall and time.

**Priority score:** 4/5

---

### GAP-004 — Near-zero evaluation of LLM-assisted review in non-English and non-STEM domains

**Gap type:** Generalization Gap

**Description:** All 10 papers in this library evaluate English-language, STEM-domain documents. No study evaluates performance on non-English scientific literature, social science, humanities, or low-resource domains.

**Evidence this gap exists:**
- literature_map.md § all clusters: "English-language" is noted as a scope limitation in every cluster
- @lee2023citextract (C002) explicitly reports lower F1 on non-standard formats; non-English is not evaluated
- @kim2024classify (C006): test set drawn from Web of Science English corpus only

**Why it matters:** Scientific literature is global. Research teams in non-English-speaking countries, and researchers working on social science or humanities questions, cannot rely on the current evidence base to evaluate LLM-assisted review tools. Tools that work in English STEM may fail in other contexts due to training data imbalance.

**Difficulty:** medium — requires assembling non-English test corpora and recruiting domain-appropriate evaluators. Primary difficulty is the scarcity of ground-truth annotations for non-English scientific text.

**Potential approach:** Select three non-English scientific corpora (e.g., Spanish-language medical literature, Chinese-language computer science, French-language social science). Apply the full pipeline from @ross2024protocol with multilingual LLMs (e.g., GPT-4-turbo, mT5). Report performance broken down by language and domain.

**Priority score:** 3/5

---

### GAP-005 — LLM-assisted review tools are too expensive for researchers without institutional API access

**Gap type:** Efficiency Gap

**Description:** All studies in this library use GPT-4 or equivalent closed-source models via API. The cost per 100-paper review is not reported in any study. Researchers at institutions without API subscriptions or with limited budgets cannot replicate the reported workflows.

**Evidence this gap exists:**
- @wang2024llmreview (C001): GPT-4 used; cost not reported
- @zhao2024rag (C004): GPT-4 used; cost not reported
- No study evaluates open-source model alternatives (Llama, Mistral, etc.) on the same tasks

**Why it matters:** The efficiency gains (SA-1) are only accessible to well-resourced researchers. If the tools rely on closed-source APIs with significant per-token costs, the equity implications are serious and the practical adoption rate among independent researchers is limited.

**Difficulty:** low — open-source models can be evaluated on the same benchmarks as closed-source models without requiring new data collection. The main challenge is compute access for inference, not study design.

**Potential approach:** Systematic benchmark of open-source models (Llama 3, Mistral, Qwen2) versus GPT-4 on the extraction, classification, and summarization tasks from Clusters 1–3. Report accuracy, cost per 100 papers, and inference time. Identify the accuracy–cost Pareto frontier.

**Priority score:** 3/5

---

## Prioritized gap ranking

| Rank | Gap ID | Type | Priority | Difficulty | Blocking thesis? |
|---|---|---|---|---|---|
| 1 | GAP-001 | Unexplored Combination | 5/5 | medium | yes — SA-3 depends on this |
| 2 | GAP-002 | Missing Baseline | 4/5 | high | yes — no way to claim "net benefit" without a threshold |
| 3 | GAP-003 | Contradictory Results | 4/5 | medium | partial — CA-1 rebuttal needs empirical support |
| 4 | GAP-004 | Generalization Gap | 3/5 | medium | no — out of scope for current RQ but important for impact |
| 5 | GAP-005 | Efficiency Gap | 3/5 | low | no — but affects adoption relevance |

---

## Suggested next research question

Derived from GAP-001 (highest priority):

> **RQ-NEW: Does a combined RAG + chain-of-thought + evidence matrix protocol, implemented as a unified pipeline, reduce hallucination rates in LLM-assisted scientific summarization to below 10%, and does this enable the efficiency gains of LLM-assisted review to be achieved without an unacceptable increase in factual error rate?**

**Why this is the right next question:**
- It directly addresses the weakest inferential link in the current argument (SA-3)
- It is tractable: all components exist, the experiment design is clear
- Answering it positively would upgrade thesis confidence from medium to high
- Answering it negatively would require revising the thesis and is an equally valuable scientific contribution

**Suggested study design:** See GAP-001 § Potential approach above.
