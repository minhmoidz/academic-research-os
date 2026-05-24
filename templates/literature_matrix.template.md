# Literature Matrix

Built from paper-qa queries on [YYYY-MM-DD]. NOT from memory.

---

## Rules

- Every cell must be filled from a paper-qa query or left as `?` if not in the available PDF.
- Never fill a cell from training-data knowledge without a paper-qa query backing it.
- If paper-qa is unavailable, mark cells as `TODO_EVIDENCE_NEEDED:`.
- The "Addresses gap?" column must state specifically why a paper does or does not address the gap.

---

## Standard Matrix

| Paper (cite key) | Method type | Dataset | Key metric | Key limitation | Addresses our gap? |
|-----------------|-------------|---------|-----------|----------------|-------------------|
| [cite-key-1] | [e.g., dense retrieval] | [dataset name] | [metric = value] | [What this paper cannot do] | No — because [specific reason] |
| [cite-key-2] | [e.g., re-ranking] | [dataset name] | [metric = value] | [What this paper cannot do] | Partially — but [specific gap remaining] |
| [cite-key-3] | [method type] | [dataset name] | [metric = value] | [limitation] | Yes — but only for [restricted setting] |

---

## Gap Column Summary

No prior work addresses: [gap statement — one specific sentence]

Evidence from paper-qa:
```
Query: "Does any paper address [gap]?"
Answer: [paste paper-qa output verbatim]
Index: [index name, built YYYY-MM-DD]
```

---

## Domain-Specific Columns (Optional)

Add columns relevant to your specific research gap. Examples:
- For retrieval papers: "retrieval model", "re-ranking step", "query expansion"
- For NLP papers: "pre-training data", "fine-tuning protocol", "evaluation language"
- For systems papers: "throughput", "latency", "hardware"

---

## paper-qa Queries Used

Record each query used to fill the matrix, in order:

| Query | Result summary | Used in row |
|-------|---------------|-------------|
| "[pqa query text]" | [one-line summary of answer] | [cite-key] |
