# Slide Deck Outline

<!-- Instructions for use:
     - Fill [PLACEHOLDERS] with content from the corresponding section of draft.md.
     - Every "Evidence to show" field must reference a Claim ID from claim_registry.md.
     - "Talking points" are speaker notes — write in full sentences for the presenter.
     - "Visual suggestion" describes what should appear on the slide, not what to speak.
     - Finalize slide count and order after § 4 Results are confirmed (Stage 16).
-->

**Talk title:** [TITLE PLACEHOLDER — copy from draft.md when finalized]
**Working title:** Structured LLM-Assisted Literature Review: Efficiency, Quality, and Protocol Design
**Conference / venue:** [VENUE PLACEHOLDER — fill after venue-target decision]
**Duration:** 15 min talk + 5 min Q&A (adjust slide count accordingly)
**RQ reference:** RQ-NEW (from synthesis/gaps_and_opportunities.md)
**Last updated:** YYYY-MM-DD

---

## Slide 1 — Title + Research Question

**Content to display:**
- Full paper title
- Author names and affiliations
- Venue name and date
- Research question in one line below the title: *"Does combining RAG, chain-of-thought prompting, and a structured evidence protocol reduce LLM hallucination in literature review to an acceptable level while preserving efficiency?"*

**Talking points:**
- Welcome the audience in one sentence.
- State the one thing they should remember by the end: "We will show whether the three most promising mitigations for LLM hallucination work together — and whether the combination is good enough for real research use."
- Tell them the answer will come in slide 7 — build the expectation now.

**Evidence to show:** None (title slide).

**Visual suggestion:** Clean title layout with institution logo. Include the research question as a subtitle in slightly smaller font. No bullet points.

---

## Slide 2 — Motivation: Why This Problem Matters

**Content to display:**
- "~2 million scientific papers published per year (and growing)"
- "Synthesizing 100 papers manually takes an estimated 10+ hours"
- "LLMs can cut this to ~4 hours — but at what quality cost?"
- One-line framing: *The efficiency–quality trade-off is unresolved.*

**Talking points:**
- Open with the scale of the problem: the volume of scientific literature has grown faster than any researcher's ability to read it.
- The 60% time reduction from LLM assistance (C001) sounds compelling — but it comes with a 12–28% factual error rate (C003). That is the tension this talk addresses.
- Pause after the error rate statistic. Let it land. Then say: "So the question is: can we get the efficiency without the errors?"

**Evidence to show:**
- C001: ~60% time reduction (wang2024llmreview, Table 2) — show the number prominently
- C003: 12–28% error rate (chen2024hallucination, Sec 4.2) — show alongside C001 as the counter

**Visual suggestion:** Two-column slide: LEFT column = efficiency gain (bar chart: 10.6 h manual vs. 4.2 h assisted). RIGHT column = quality cost (error rate 12–28%, highlighted in red). Draw a scale / balance icon between them to visualize the trade-off.

---

## Slide 3 — What the Literature Has Tried (Related Work Cluster 1)

**Content to display — LLM Capabilities for Scientific Text Processing:**
- LLMs achieve >90% F1 on citation extraction from structured PDFs
- GPT-4 classifies methodology (qualitative vs. quantitative) at 94% accuracy — near the human ceiling of 97%
- General LLMs match domain-adapted models: scale beats specialization
- **Scope caveat:** English STEM only; scanned PDFs drop to ~74% F1

**Talking points:**
- The first thing the field established is that LLMs can reliably extract structured information from papers. This is the foundation — without it, automation is impossible.
- The 94% classification accuracy is nearly human-level on a binary task. That is genuinely impressive and means we can trust the upstream extraction step.
- However — and this is important for later — all of this is English STEM. We will come back to that scope limitation.

**Evidence to show:**
- C002: >90% F1 citation extraction (lee2023citextract, Table 4)
- C006: 94% classification accuracy (kim2024classify, Table 1)
- C009 (low confidence, flag it): domain adaptation shows no benefit (nguyen2024domainadapt)

**Visual suggestion:** Accuracy comparison bar chart: Citation F1 (>90%) and Classification Accuracy (94%) alongside human baselines (87% kappa, 97% accuracy). Small footnote callout: "English STEM scope — generalization unknown." Timeline axis showing this work is from 2023.

---

## Slide 4 — What the Literature Has Tried (Related Work Cluster 2)

**Content to display — LLM-Assisted Workflow Studies:**
- 60% time reduction in synthesis tasks (wang2024llmreview, RCT n=24)
- Human raters find LLM syntheses equally credible to human-written ones — at abstract length
- BUT: LLMs do NOT improve recall of relevant papers vs. Boolean search
- Structured protocols reduce duplicate claim registration by 73%

**Talking points:**
- This cluster is about workflows — whether integrating LLMs into a real review process helps. The headline result is yes, it is much faster.
- The credibility finding sounds reassuring — until you realize the evaluators were not domain experts. The next cluster will show that expert evaluation tells a different story.
- The recall finding (C007) is the most underappreciated result in this field: LLMs make synthesis faster, but they do not help you find papers you would have missed. This means they must supplement, not replace, systematic Boolean search. Our protocol takes this seriously.

**Evidence to show:**
- C001: 60% time reduction — highlight as the key efficiency claim
- C005: credibility parity (patel2023credibility) — note scope limitation explicitly
- C007: no recall improvement (huang2024recall) — show as a boundary condition, not a failure
- C010: 73% reduction in duplicates (ross2024protocol)

**Visual suggestion:** Process flow diagram: [Discovery: Boolean search] → [Screening: LLM] → [Synthesis: LLM]. Highlight in green where LLM helps (screening, synthesis). Highlight in amber/warning where it does not (discovery). This visually motivates the protocol design in slide 5.

---

## Slide 5 — The Problem with Current Approaches (Cluster 3 + The Gap)

**Content to display — Reliability and the Gap:**
- Domain experts find 12–18% errors in abstract summaries; 28% in methods sections
- RAG reduces this by ~40% — but that still leaves ~7–11% errors
- CoT prompting improves quality assessment from 61% → 79%
- **The gap:** RAG and CoT have never been tested together in a structured pipeline
- No study has defined what error rate is "acceptable" for systematic reviews

**Talking points:**
- Cluster 3 is where the optimism of Cluster 2 gets stress-tested. When domain experts check the LLM's work, they find real errors — and the rate is higher in the sections that matter most (methods: 28%).
- Two mitigations exist. RAG grounds the model in source text. CoT forces step-by-step reasoning. Each helps. But — crucially — no one has tested them together. That is the gap this paper fills.
- There is a second gap that no technical solution can fix alone: the field has never agreed on what an acceptable error rate looks like. We will return to this in limitations.

**Evidence to show:**
- C003: 12–28% error rate — show the 28% methods section figure prominently
- C004: ~40% RAG reduction (zhao2024rag) — with variance (22–55%) noted
- C008: CoT 61% → 79% accuracy (sun2024cot)
- GAP-001: no joint test of RAG + CoT + protocol (from gaps_and_opportunities.md)

**Visual suggestion:** Three-row table: [Mitigation | What it fixes | Tested alone? | Tested in combination?]. RAG: yes alone, no combined. CoT: yes alone, no combined. Structured protocol: yes alone, no combined. The "no combined" column cells highlighted — that is the gap.

---

## Slide 6 — Method: The Protocol

**Content to display:**
- 4-stage pipeline diagram:
  1. Discovery: Systematic Boolean search (LLM excluded — preserves recall)
  2. Screening: LLM extraction (citation, methodology, metadata)
  3. Synthesis: RAG + CoT generation
  4. Verification: Evidence matrix + human spot-checking of high-confidence claims
- Key design choices with rationale:
  - Boolean search in Stage 1: because C007 shows LLM-only search degrades recall
  - RAG + CoT together: because each addresses a distinct failure mode from C004/C008
  - Human spot-check: because residual error rate after RAG is estimated 7–11%

**Talking points:**
- Walk through each stage in 20 seconds each.
- Emphasize that Stage 1 is intentionally LLM-free. This is a deliberate design choice based on the recall evidence — not an oversight.
- The novel contribution is Stage 3: combining RAG and CoT in a single synthesis step with a structured output protocol. No prior paper has evaluated this combination. This is what we are measuring.
- Stage 4 is the safety net. In a real research workflow, human verification of important claims is not optional — it is where the researcher's judgment remains essential.

**Evidence to show:**
- C007: rationale for Stage 1 design (no LLM in discovery)
- C004 + C008: rationale for Stage 3 design (RAG + CoT combined)
- C010: rationale for Stage 4 design (structured protocol)

**Visual suggestion:** Horizontal pipeline diagram with 4 labeled boxes connected by arrows. Color-code: blue = LLM-active stages; grey = human-only stage (Stage 1); yellow = hybrid stage (Stage 4). Below each box, one line: "Why: [C007 / C004+C008 / C010]." This makes the evidence-based design visible.

---

## Slide 7 — Key Finding 1: Hallucination Rate of the Combined Pipeline

**Content to display:**
- [TODO_RESULT_NEEDED: Insert hallucination rate (%) for each condition from § 4.1 of draft.md]
  - No mitigation baseline: ~15% (from C003 literature estimate)
  - RAG only: ~9% (estimated from C004)
  - CoT only: [TODO_RESULT_NEEDED]
  - RAG + CoT + protocol (full pipeline): [TODO_RESULT_NEEDED]
- Comparison to the "acceptable threshold" question (GAP-002)

**Talking points:**
- [TODO_RESULT_NEEDED: Write talking points after experiment results are available]
- Suggested framing when results are in: "The combined pipeline achieves [X]% hallucination — [above/below] the [Y]% threshold we proposed based on practitioner standards from [source]."
- If results are above threshold: "This shows that even the best available combination of mitigations does not yet meet the bar for high-stakes systematic reviews. This is an honest and important finding."
- If results are below threshold: "For the first time, we have an evidence-based protocol that demonstrably meets the quality bar."

**Evidence to show:**
- C003: baseline error rate (annotation: "without mitigation")
- C004: RAG-only estimate
- [TODO_RESULT_NEEDED: Empirical result from ablation experiment]

**Visual suggestion:** Grouped bar chart — four conditions on x-axis, hallucination rate (%) on y-axis. Add a horizontal dashed line at the proposed acceptable threshold. Bars decreasing left to right, with the full pipeline bar either above or below the threshold line.

---

## Slide 8 — Key Finding 2: Efficiency and Recall

**Content to display:**
- [TODO_RESULT_NEEDED: Time-to-synthesis comparison (§ 4.2)]
- [TODO_RESULT_NEEDED: Recall comparison — combined pipeline vs. Boolean-only (§ 4.4)]
- The trade-off table: time reduction vs. recall vs. error rate across conditions

**Talking points:**
- The efficiency finding answers: did adding the quality safeguards (RAG + CoT + protocol) eliminate the time savings of LLM assistance? Or do we get quality improvement without losing speed?
- The recall finding confirms whether our Stage 1 design choice (keeping Boolean search) successfully preserves recall — the central design rationale from C007.
- [TODO_RESULT_NEEDED: Fill with actual talking points once results exist]

**Evidence to show:**
- C001: reference efficiency benchmark (60% time reduction from LLM assistance alone)
- C007: reference recall benchmark (no improvement from LLM-only search)
- [TODO_RESULT_NEEDED: Empirical results from § 4.2 and § 4.4]

**Visual suggestion:** Three-column comparison table: [Condition | Time (hrs/100 papers) | Recall (%) | Hallucination (%)]. Rows: Manual, LLM-only, Full pipeline. Color-code: green = better than manual, red = worse. This lets the audience read the trade-off at a glance.

---

## Slide 9 — Contradictions and Honest Limitations

**Content to display:**
- **Contradiction 1 (CONTR-001):** Efficiency (C001) vs. recall (C007)
  - Resolution: use LLM for synthesis only; keep Boolean search for discovery
- **Contradiction 2 (CONTR-002):** Credibility parity (C005) vs. expert error rates (C003)
  - Resolution: credibility ratings measure perception, not accuracy; both can be true
- **Limitations:**
  - No agreed acceptable threshold (GAP-002) — the goalposts are not defined
  - English STEM only (GAP-004) — generalizability unknown
  - CoT rubric not independently validated (C008 caveat)

**Talking points:**
- Contradictions in the literature are a sign that the field is working on a hard problem — not a sign that the evidence is unreliable. Presenting them honestly makes your synthesis more trustworthy.
- The most important limitation is GAP-002: without an agreed threshold, claiming "good enough" is a value judgment disguised as a scientific claim. We propose one threshold based on [source] but acknowledge this needs community consensus.
- State this directly: "We do not know whether our results generalize to non-English literature or to social sciences. Future work should test this."

**Evidence to show:**
- C001 vs. C007 (CONTR-001) — show the conflicting findings side by side
- C005 vs. C003 (CONTR-002) — show the methodological explanation
- GAP-002 (no threshold exists) — show as a red "missing piece"

**Visual suggestion:** Two-panel layout. LEFT: "What prior work agrees on" (green checkmarks). RIGHT: "What is still unresolved" (amber question marks). For each contradiction, show a brief two-line summary with citekeys. Keep this honest and concise — one slide, no cramming.
<!-- Evidence: C001, C003, C005, C007 | Confirmed clusters from evidence_matrix.csv -->

---

## Slide 10 — Contribution and Novelty Claim

**Content to display:**
- **Contribution 1:** First empirical evaluation of RAG + CoT + structured protocol as a unified pipeline (GAP-001 filled)
- **Contribution 2:** [TODO_RESULT_NEEDED: quantitative result from § 4]
- **Contribution 3:** Proposed protocol design with evidence-based rationale for each stage
- Novelty statement: "To our knowledge, this is the first study to measure the combined hallucination-reduction effect of RAG, chain-of-thought prompting, and an evidence matrix protocol in a realistic literature review workflow."

**Talking points:**
- Be precise about what is novel and what is not. The individual components (RAG, CoT, structured protocol) are not new. The contribution is the joint evaluation and the integrated protocol design.
- Do not claim "proves" — say "provides evidence that" or "demonstrates that." The findings are bounded by the scope stated in slide 9.
- If results are positive: "This provides the first empirical basis for researchers to trust that a structured LLM-assisted pipeline is both faster and sufficiently accurate."
- If results are negative: "This is the first paper to empirically test — and find the limits of — the best available combination of mitigations. Negative results are contributions too."

**Evidence to show:**
- GAP-001 (the gap this paper fills — show it as "CLOSED" with the result)
- [TODO_RESULT_NEEDED: Primary empirical result from § 4.1]

**Visual suggestion:** Contribution comparison table: rows = contributions 1/2/3, columns = "Prior work" / "This paper." Use checkmarks and crosses. Bottom row: novelty statement in bold.

---

## Slide 11 — Future Work (From Gaps)

**Content to display:**
- **Priority 1 — GAP-002:** Define an acceptable hallucination threshold for AI-assisted systematic reviews — requires stakeholder survey and position paper
- **Priority 2 — GAP-003:** Resolve the efficiency vs. recall contradiction with a pre-registered recall study (3-condition design: Boolean-only / LLM-only / combined)
- **Priority 3 — GAP-004:** Test the full pipeline on non-English corpora (Spanish, Chinese, French) and social science domains
- **Priority 4 — GAP-005:** Benchmark open-source models (Llama, Mistral) as cost-accessible alternatives to GPT-4

**Talking points:**
- The most important next step is not technical — it is the threshold definition. Before the field can benchmark progress, it needs to agree on what success looks like. This is a governance problem as much as a research problem.
- The recall study is tractable: a 3-arm RCT with a clear gold-standard metric. Someone in this room could run it in six months.
- The open-source model benchmark is the most accessible entry point for resource-limited teams. Low difficulty, meaningful impact on equity.
- Close with: "The tools are here. The protocols are here. The next task is to agree on the standards."

**Evidence to show:**
- GAP-001 (closed by this paper — shown as "complete")
- GAP-002, GAP-003, GAP-004, GAP-005 — shown as open, with priority scores
- RQ-NEW from gaps_and_opportunities.md — show as the next question for the field

**Visual suggestion:** Four-row prioritized gap table: [Gap ID | Description (one line) | Difficulty | Who could do this]. GAP-001 row struck through / greyed out ("filled by this paper"). Priority badge (1–4) in the leftmost column.

---

## Q&A Preparation

Anticipated questions and prepared answers:

| Anticipated question | Prepared answer | Evidence |
|---|---|---|
| "Why use Boolean search at all — isn't LLM retrieval more flexible?" | "Because @huang2024recall (C007) shows LLM-assisted search does not improve recall vs. systematic Boolean search. Until a study shows otherwise, the risk of missed relevant literature is too high for systematic reviews." | C007 |
| "What error rate did you actually achieve?" | "[TODO_RESULT_NEEDED: insert from § 4.1 after experiment]" | § 4.1 of draft.md |
| "Isn't 10% hallucination still too high for medical reviews?" | "Yes, and we say so. GAP-002 is the unanswered question: the field has not defined the threshold. We propose one but acknowledge it needs community consensus." | GAP-002 |
| "Did you test on non-English papers?" | "No — and we flag this as GAP-004. All results are English STEM. Generalization is unknown." | GAP-004 |
| "Why not use a domain-adapted model instead of GPT-4?" | "@nguyen2024domainadapt (C009) finds no benefit from domain adaptation on these tasks. Scale appears to matter more than domain specialization for extraction and classification." | C009 (note: low confidence) |
| "Is the structured protocol really novel, or is it just good lab practice?" | "The protocol itself builds on @ross2024protocol (C010). The novelty is the joint empirical evaluation of the full pipeline, not any single component." | C010, GAP-001 |
| "What would change your conclusion?" | "If a replication of @wang2024llmreview fails in a larger pre-registered study, or if RAG + CoT post-mitigation errors remain above [X]%, the case for adoption weakens significantly." | argument_map.md § Falsifiability |
