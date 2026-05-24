# 24 — Venue Targeting

**Purpose:** Define how to select and commit to a target venue, specify what evidence is required
for each venue tier, and establish the protocol for venue changes when results do not meet the
original target.

---

## Core Principle

> Venue selection must drive evidence requirements, not follow them.
> Claude must define what evidence is needed to reach a target venue BEFORE confirmatory
> experiments run. After experiments, Claude must honestly assess whether the evidence meets
> those requirements, and recommend a downgrade, additional experiments, or narrowing if it does
> not. Assuming a positive result is sufficient for a top-tier venue is a planning error.

---

## Venue Tier Classification

### Tier 1 — Top-tier Venues (A* ranking)

Conferences and journals at the frontier of their field. Acceptance rates typically 15-25%.
Reviewers expect significant novelty, strong empirical support, and broad impact.

**Conferences:** NeurIPS, ICML, ICLR, CVPR, ECCV, ICCV, ACL, EMNLP, SIGKDD, AAAI, IJCAI,
MICCAI (main track)

**Journals:** Nature Machine Intelligence, JMLR, IEEE TPAMI (for substantial extended work)

---

### Tier 2 — Strong Venues (A ranking)

High-quality venues with significant community reach. Acceptance rates 20-35%.
Reviewers expect clear novelty and solid empirical evidence.

**Conferences:** BMVC, WACV, COLING, EACL, NAACL, MIDL (main track), ISBI (top papers)

**Journals:** IEEE TPAMI (shorter papers), IJCV, Medical Image Analysis, IEEE TMI, Pattern
Recognition

---

### Tier 3 — Domain-Specific Venues (B ranking)

Specialized venues with strong community but narrower scope. Acceptance rates 30-45%.
Reviewers value domain relevance and methodological soundness.

**Conferences:** MIDL (extended abstracts), ISBI, MIUA, CLEF, regional AI/ML conferences,
EMNLP Findings, ACL Findings

**Journals:** Computerized Medical Imaging and Graphics, Artificial Intelligence in Medicine,
Journal of Digital Imaging

---

### Tier 4 — Workshops

Workshops at Tier 1-2 venues. High acceptance rates (40-60%). Good for preliminary results,
position papers, and work-in-progress.

**Examples:** MICCAI workshops (MIL4MIL, COMPAY), NeurIPS workshops, CVPR workshops

---

### Tier 5 — arXiv / Preprint

No peer review. Used for dissemination, priority establishment, or supplementary material.
Not a substitute for peer-reviewed publication.

---

### Tier 6 — Thesis / Internal Report

Non-public or limited-distribution documents. No external review standard required.

---

## Evidence Requirements by Tier

| Requirement | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|-------------|--------|--------|--------|--------|
| **Novelty** | Strong methodological or theoretical novelty beyond incremental improvements | Clear differentiation from prior work; novel application or meaningful extension | Domain-specific novelty; clear improvement over standard methods in the field | Preliminary novel idea; conceptual novelty acceptable |
| **Baseline strength** | Must beat very recent SOTA (≤2 years); include all strong baselines | Must beat published SOTA; at least 3 strong recent baselines | Must beat standard baselines for the domain; 2+ established methods | Comparable to representative baselines; full comparison not required |
| **Dataset coverage** | ≥3 standard benchmarks, including at least one held-out test set | ≥2 standard benchmarks; held-out evaluation preferred | ≥1 domain-relevant benchmark; cross-dataset preferred | ≥1 dataset; exploratory setting acceptable |
| **Ablation depth** | Full component-by-component ablation; interaction effects; hyperparameter sensitivity | Component ablation for all design choices; at least one sensitivity study | Ablation of key design choices; simplification acceptable | Minimal ablation; "what if" analysis acceptable |
| **Statistical rigor** | Multiple seeds (≥5); report mean ± std; significance tests encouraged | Multiple seeds (≥3); report mean ± std; consistent across runs | ≥3 seeds preferred; variance reported | Single run acceptable for preliminary work |
| **Analysis depth** | Failure mode analysis, qualitative examples, computational cost, limitations section | At least one deeper analysis (attention maps, error analysis, or efficiency); limitations | Discussion of limitations; one supporting visualization | Brief discussion of limitations; informal analysis acceptable |
| **Reproducibility** | Code release expected; hyperparameter table required; data splits specified | Code release encouraged; sufficient detail to reproduce | Sufficient methodological detail; hyperparameters documented | Method sketch sufficient |
| **Writing standard** | Publication-ready; no ambiguous claims; every claim cited or ablated | Near-publication-ready; minor revision expected | Clear and correct; domain terminology consistent | Preliminary draft standard |

---

## Realistic Comparison: MICCAI (Tier 1) vs. ISBI (Tier 3)

### Submitting to MICCAI (Tier 1)

**What reviewers will check:**
- Is the method meaningfully different from prior MIL methods (BaselineMethod, AnotherMethod, ComparisonMethod)?
- Are all strong GenericDataset baselines included (2022-2024)?
- Is the result statistically stable across 5 folds with low variance?
- Is there an ablation for every module claimed as a contribution?
- Does the paper acknowledge failure modes and limitations?

**Minimum acceptable result for competitive consideration:**
- Beat 3+ strong recent baselines (published 2022-2024) on 2+ standard benchmarks
- AUC improvement ≥ 1.5pp over the strongest baseline, stable across seeds
- No single-dataset results as primary evidence

**Common rejection reasons at TIER 1:**
- "Baseline comparisons are outdated or incomplete"
- "Ablation does not support all claimed contributions"
- "Results are marginal or only shown on one dataset"
- "Method is incremental over [concurrent paper X]"
- "No analysis of failure cases or computational cost"

### Submitting to ISBI (Tier 3)

**What reviewers will check:**
- Is the problem medically or technically relevant?
- Is the method reasonable and clearly described?
- Is there at least one comparison to a standard method?

**Minimum acceptable result:**
- Beat one established baseline on one relevant dataset
- AUC improvement ≥ 0.5pp; or demonstrate a new capability not previously shown

**Common rejection reasons at TIER 3:**
- "Evaluation is too limited to draw conclusions"
- "The method is not described in sufficient detail to reproduce"
- "No comparison to any existing approach"

---

## Template: `venue_target.md`

Create this file in the project root at Stage 3, before experiments begin.

```markdown
# Venue Target

Project: [Project name]
Decision made at stage: 3
Last updated: YYYY-MM-DD

---

## Primary Target

- **target_venue:** [e.g., MICCAI 2026]
- **venue_tier:** [1-6]
- **paper_type:** [empirical / survey / system / theory / benchmark]
- **submission_deadline:** YYYY-MM-DD
- **page_limit:** [e.g., 8 pages (+ references)]
- **blind_review:** [yes / no]

---

## Candidate Venues (Ordered Fallbacks)

1. [Primary venue] — Tier N
2. [First fallback] — Tier N
3. [Second fallback] — Tier N
4. [Workshop option] — Tier 4

---

## Evidence Requirements for Primary Venue

- **required_novelty_level:** >
    [Specific description: e.g., "Method must differ from ComparisonMethod in at least one structural
    way beyond hyperparameter tuning; difference must be ablated and justified."]

- **required_empirical_strength:** >
    [Quantitative: e.g., "Beat at least 3 baselines published 2022-2024 on 2 of the 3 target
    datasets (Dataset-A, Dataset-B, Dataset-C) by at least 1.5pp AUC."]

- **required_baselines:** >
    - BaselineModel (2024)
    - ComparisonMethod (2024)
    - AnotherMethod (2021)
    - ACMIL (2023)
    - DSMIL (2021)

- **required_datasets:** >
    - Dataset-A (primary)
    - Dataset-B (secondary)

- **required_ablations:** >
    [List every module that will be claimed as a contribution. Each needs its own ablation row.]
    - AttentionModule module (on/off)
    - ProposedModule module (on/off)
    - CLS token (on/off)
    - LS module (on/off)
    - Full model vs. BaselineModel backbone

- **required_analysis:** >
    [e.g., "Attention map visualization for AttentionModule; computational cost vs. performance tradeoff;
    per-class analysis; failure case examples."]

---

## Result Contract

- **minimum_acceptable_result:** >
    [Specific threshold: e.g., "val_auc ≥ 0.900 on Dataset-A; val_auc ≥ 0.960 on Dataset-B;
    both must exceed BaselineModel by ≥ 1.5pp."]

---

## Risk Assessment

- **known_risks:**
    - [e.g., "Concurrent work at NeurIPS 2025 uses similar attention-gating in MIL"]
    - [e.g., "Dataset-B baseline is already very high (>0.95), limiting headroom for improvement"]
    - [e.g., "ProposedModule graph construction is computationally expensive; reviewers may object"]

- **recommended_path:** >
    [If primary venue is not reached, what is the fallback strategy? Be specific.]
    "If AUC does not beat BaselineModel by ≥ 1.5pp on both datasets, downgrade to MIDL (Tier 2)
    and reframe as an ablation analysis of attention-gating strategies in Mamba MIL."
```

---

## Hard Rules

1. **Venue must be selected at Stage 3**, before any confirmatory experiments. Selecting a venue
   after seeing results is venue-shopping and invalidates the evidence requirements.

2. **Venue selection drives the target result contract.** The `minimum_acceptable_result` in
   `venue_target.md` must match the requirements for the chosen tier. If the venue changes, the
   result contract must be updated.

3. **If results do not meet venue requirements, Claude must recommend:**
   - Downgrade to a lower tier, OR
   - Run additional experiments to meet the evidence threshold, OR
   - Narrow the scope of the contribution claim.
   Claude must NOT assume that a positive result is automatically sufficient for the original
   target venue.

4. **Claude must define venue-specific evidence requirements BEFORE running confirmatory
   experiments.** The requirements in `venue_target.md` are fixed at Stage 3. They are not
   adjusted to match results observed at Stage 12.

5. **Any venue change requires a DEC entry in `decision_log.md`**, with the reason, the
   triggering evidence, and the new venue requirements.

---

## Venue Change Protocol

When a venue change is warranted (results below threshold, scope narrowed, etc.):

```
Step 1: Identify the triggering evidence (EXP-N, HYP-N, or prior-art finding).
Step 2: Create DEC-NNN in decision_log.md with:
        - Old venue and why it was the target
        - New venue and why it is appropriate
        - Evidence that triggered the change
        - How evidence requirements change
Step 3: Update venue_target.md:
        - Increment direction_version (see 23_RESEARCH_DIRECTION_UPDATE.md)
        - Update candidate_venues, required_empirical_strength, minimum_acceptable_result
Step 4: Update contribution_contract.md if the venue change requires narrowing claims.
Step 5: Update research_direction.md pivot_recommendation field.
Step 6: Notify the researcher with a summary of the change and the new path.
```

---

## Interaction with Other System Files

| File | Relationship |
|------|-------------|
| `hypothesis_registry.md` | Supported hypotheses must meet venue evidence requirements |
| `research_direction.md` | Direction updates may trigger venue downgrade |
| `contribution_contract.md` | Claims must be strong enough for the chosen venue tier |
| `25_PRIOR_ART_COMPETITION.md` | Threat level High/Critical may require venue adjustment |
| `09_SUBMISSION_CHECKLIST.md` | Venue requirements drive the checklist at submission |
| `decision_log.md` | All venue changes logged permanently here |
