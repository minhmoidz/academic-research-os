# Venue Targeting Guide

## Overview

Venue targeting determines which publication you will submit to — and therefore what evidence standards your results must meet. The OS enforces a structured approach to venue selection to prevent the most common mistake: choosing a prestigious venue aspirationally before running any experiments, then reverse-engineering claims to fit.

The venue target is formalized in `venue_target.md` and is binding from the moment the Target Result Contract (Gate 2) is signed.

---

## 1. The 6-Tier Classification System

| Tier | Description | Examples | Typical Acceptance Rate |
|------|-------------|----------|------------------------|
| 1 | Top-tier full paper venues (ML/AI/domain-specific A*) | NeurIPS, ICML, ICLR, ACL, CVPR, Nature, Science | 15–25% |
| 2 | Strong full paper venues (A-ranked conferences, top domain journals) | EMNLP, ECCV, ICCV, AAAI, IJCAI, IEEE TPAMI, JMLR | 20–30% |
| 3 | Solid mid-tier full paper venues (B-ranked conferences, respected journals) | COLING, EACL, BMVC, IEEE Access (selective), ECML-PKDD | 25–40% |
| 4 | Workshop papers, short papers at Tier 1–2 venues | NeurIPS workshops, ACL Findings, CVPR workshops | 35–55% |
| 5 | Regional / domain-specific conferences and application journals | IEEE-EMBC, regional AI conferences, domain IEEE Transactions | 40–60% |
| 6 | Preprint / technical report (no peer review) | arXiv, institutional reports | N/A |

Tier assignment is based on the contribution's combination of novelty, empirical breadth, and theoretical grounding — not on the researcher's career stage or aspiration.

---

## 2. How to Pick the Right Tier

Run `/venue-target` and answer the following four questions. Claude uses your answers to recommend a tier range:

1. **Novelty level:** Is the proposed approach a new paradigm (high), a meaningful improvement on an established approach (medium), or an application of known methods to a new domain (applied)?
2. **Empirical breadth:** How many datasets, baselines, and ablations are planned?
3. **Theoretical grounding:** Does the paper include formal proofs, complexity analysis, or statistical guarantees?
4. **Comparison strength:** Can you run comparisons against all published SOTA methods at your target tier, or only a subset?

For example, a paper on retrieval-augmented agents for scientific literature analysis that introduces a new re-ranking mechanism tested on 2 datasets with 4 baselines and 3 ablations, with no formal proofs, typically fits Tier 2–3. A paper with a single-dataset experiment and 2 baselines fits Tier 4–5.

If you are unsure, start with a conservative tier. Reviewing the target venue's recent proceedings for accepted paper profiles is more reliable than any heuristic.

---

## 3. What Each Tier Requires

### Tier 1

- At least 2 primary benchmarks with full SOTA comparison
- Ablation study with at least 3 components varied
- Statistical significance testing (e.g., paired t-test, bootstrap confidence intervals)
- At least 5 competitive baselines including the most recent published method
- Clear theoretical motivation (not required to be a formal proof, but must be arguable)
- Reproducibility: code release or detailed pseudocode

### Tier 2

- At least 2 benchmarks or 1 large-scale benchmark
- Ablation study with at least 2 components varied
- Comparison against at least 3 strong baselines
- No formal proof required, but a clear explanation of why the method works

### Tier 3

- At least 1 benchmark with comparison against 2+ baselines
- Some ablation (even 1 component is acceptable)
- Results clearly better than baselines, not just competitive

### Tier 4

- Preliminary results on 1 dataset acceptable
- 1–2 baselines acceptable
- Position papers with no experiments acceptable if argumentation is strong

### Tier 5

- Application results: correctness and utility over novelty
- Reproduction of existing methods on a new domain is acceptable

### Tier 6

- No peer review standard; self-assessed quality

---

## 4. The venue_target.md Artifact

`venue_target.md` is created by `/venue-target` and updated by `/pivot-decision` if the venue changes. It contains:

```markdown
# Venue Target

## Target Venue
[Conference or journal name]

## Tier
[1–6]

## Rationale
[2–3 sentences explaining why this tier and venue match the contribution profile]

## Required Evidence for Acceptance (this venue)
- Primary metric: [metric name]
- Minimum datasets: [N]
- Minimum baselines: [N]
- Ablations required: [yes/no, description]
- Statistical tests required: [yes/no, type]

## Deadline
[Submission deadline if known; "TBD" if not]

## Status
[PROVISIONAL | SIGNED | DOWNGRADED]

## Change Log
[Dates and reasons for any status changes]
```

The artifact transitions from PROVISIONAL (before Gate 2) to SIGNED (at Gate 2) to DOWNGRADED (if a `/pivot-decision` lowers the tier after Gate 3).

---

## 5. When to Downgrade a Venue (and How to Log It)

Downgrade the venue target when Gate 3 returns Decision E (results are real but below the threshold required for the signed tier). Do not downgrade preemptively based on anxiety — only downgrade based on Gate 3 evidence.

**How to downgrade:**

1. Run `/pivot-decision` and select "venue downgrade" as the pivot type.
2. State the original tier, the new tier, and the specific evidence that triggered the downgrade.
3. Update `venue_target.md`: change the tier and set status to DOWNGRADED.
4. Update `result_contract.md`: lower the minimum threshold to match the new tier's requirements.
5. Re-evaluate Gate 3 with the updated contract.

The decision log entry must include:
- The Gate 3 decision that triggered the downgrade (Decision E)
- The original minimum threshold and the actual result achieved
- The new venue and its evidence requirements

Downgrading is not a failure. Publishing a rigorous paper at Tier 3 is more valuable to the research community than submitting an overclaimed paper to Tier 1 and receiving repeated rejections.

---

## 6. Common Mistakes

**Mistake 1: Targeting Tier 1 before running any experiments.**
Running `/venue-target` before Stage 12 (Pilot Experiment) produces a PROVISIONAL tier assessment with no empirical basis. Using a Tier 1 provisional target to design the experiment loop — for example, by requiring 5 baselines before running any experiments — wastes resources on infrastructure before validating the core idea. Start with a conservative tier and upgrade if results justify it.

**Mistake 2: Changing the venue without logging the decision.**
Switching from CVPR to a workshop without a `/pivot-decision` entry means the change has no rationale on record. Reviewers, collaborators, and your future self cannot reconstruct why the target changed.

**Mistake 3: Conflating venue prestige with contribution quality.**
Tier 1 papers are not inherently better science than Tier 3 papers. They require more evidence, not better ideas. A contribution that belongs at Tier 3 — because it has one dataset and three baselines — is not improved by targeting Tier 1. It will receive "insufficient evaluation" rejections and waste review cycles.

**Mistake 4: Not checking the venue's specific requirements.**
The tier system is an approximation. Each venue has idiosyncratic requirements (e.g., double-blind review, page limits, formatting style, code release policy). Always read the venue's call for papers and review criteria before signing the contract.

**Mistake 5: Targeting a venue whose deadline has passed.**
Confirm the submission deadline before signing the contract at Gate 2. If the next deadline is more than 12 months away, consider whether a closer lower-tier venue serves the project better.
