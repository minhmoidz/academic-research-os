# 17_DECISION_LOG.md — Decision Log Protocol

## Purpose

`decision_log.md` is an **append-only** record of all significant research decisions
made during a project. It enables retrospective audit, pivot tracking, and ensures that
no decision is made implicitly. Every major fork in the research path — changing venue,
reframing a claim, dropping a baseline, narrowing a hypothesis — must be logged here
before the change is acted upon.

The decision log is not a journal of actions taken. It is a record of choices made
when multiple options were available and the outcome was uncertain.

---

## Rules (Non-Negotiable)

1. **Append-only.** Never delete, modify, or overwrite a prior entry. If a decision
   is reversed, add a new entry with category `reversal` referencing the original ID.
2. **Every pivot must have an entry.** A research pivot (changing the core approach,
   hypothesis, or claim) is the highest-priority decision type. If a pivot happens
   without a log entry, the research OS is in an invalid state.
3. **Every venue change must have an entry.** Include the old venue, new venue,
   reason, and consequence to the paper structure.
4. **Every metric change (after seeing results) must have an entry.** If the primary
   evaluation metric is changed after experiments have started, it must be logged as
   a potential p-hacking risk, and the justification must reference pre-experiment reasoning.
5. **Every claim removal or softening must have an entry.** If a contribution claim
   is removed from the paper or its language is weakened (e.g., "surpasses" →
   "performs comparably"), log it with the reason.
6. **Every experiment budget increase must have an entry.** If the number of GPU
   hours, folds, or datasets is increased beyond the original plan, log the reason
   and the new total.
7. **Log before acting.** Write the entry before making the change, not after.
   The act of writing the entry forces explicit reasoning.
8. **Impact levels:** Low = cosmetic or organizational; Medium = affects one section
   or one experiment; High = affects multiple sections or the primary claim;
   Critical = affects the core thesis, venue, or go/no-go decision.

---

## Decision ID Format

```
DEC-YYYY-MM-DD-NNN
```

- `YYYY-MM-DD`: date the decision was made
- `NNN`: three-digit sequence number within that date (001, 002, ...)
- Example: `DEC-2026-05-24-001`

If multiple decisions are made in one session, increment NNN sequentially.

---

## Decision Categories

| Category | When to Use |
|----------|------------|
| `framing` | Changing how the problem or contribution is described, without changing the method |
| `pivot` | Changing the core approach, method, or hypothesis |
| `venue` | Changing the target publication venue |
| `baseline` | Adding, removing, or changing a baseline model |
| `metric` | Changing or adding a primary or secondary evaluation metric |
| `result-interpretation` | Deciding how to interpret ambiguous or surprising results |
| `claim-softening` | Weakening or removing a contribution claim |
| `abandon` | Stopping work on a line of inquiry, module, or experiment |
| `contribution` | Adding a new contribution claim (requires evidence gate check) |
| `writing` | Structural writing decisions (section order, page budget, figure placement) |
| `reversal` | Reversing a prior decision; must reference the original DEC-ID |
| `budget` | Increasing experiment compute, time, or data budget |

---

## Entry Template

```markdown
---

### <DEC-YYYY-MM-DD-NNN>

decision_id: DEC-YYYY-MM-DD-NNN
date: YYYY-MM-DD
session_number: <integer>
stage: <0-25>
category: <category from list above>
impact_level: <Low | Medium | High | Critical>

**Context:**
<2-3 sentences describing the situation that prompted this decision.
What was observed, what was uncertain, and why a decision was needed.>

**Decision Made:**
<One clear, unambiguous sentence stating what was decided.>

**Options Considered:**
1. <Option A — the chosen option>
2. <Option B>
3. <Option C, if applicable>

**Evidence Used:**
- <Data, result, or literature that supported this decision.>
- <E.g., "EXP-031 ablation showed [ProposedModule] alone gives +1.8 AUC on [Dataset-A].">
- <If no evidence: state "judgment call — no empirical evidence available.">

**Risk:**
<What could go wrong if this decision is wrong? What is the worst case?>

**Consequence:**
<What changes as a result of this decision? Affects: [claims / experiments / venue / writing / direction]>

**Reversible:** <Yes — how to reverse / No — why not>
```

---

## Example Entries

### Example 1: Pivot After Weak Exploratory Results

```markdown
---

### DEC-2026-05-10-003

decision_id: DEC-2026-05-10-003
date: 2026-05-10
session_number: 7
stage: 13
category: pivot
impact_level: High

**Context:**
Exploratory experiments (EXP-012 through EXP-028) showed that the AttentionModule alone
improved AUC by only 0.3 pp on Dataset-A, which is below the 1.0 pp threshold set
in the result contract. However, EXP-031 (ProposedModule ablation) showed a 1.8 pp improvement.
The original hypothesis treated all four modules as equally important contributors.

**Decision Made:**
The hypothesis is narrowed: ProposedModule is identified as the primary contributor, and the
paper's framing will emphasize hierarchical reasoning over cross-patch attention.

**Options Considered:**
1. Narrow hypothesis to emphasize ProposedModule as primary driver (chosen).
2. Continue ablating AttentionModule with more hyperparameter search (2 additional GPU days).
3. Abandon AttentionModule entirely and simplify the method to ProposedModule+LS only.

**Evidence Used:**
- EXP-031: ProposedModule ablation, Dataset-A, AUC = 0.923 ± 0.009 vs baseline 0.905 ± 0.011.
- EXP-017: AttentionModule-only ablation, Dataset-A, AUC = 0.908 ± 0.013 vs baseline 0.905 ± 0.011.
- Result contract threshold: primary metric improvement ≥ 1.0 pp AUC on Dataset-A.

**Risk:**
If ProposedModule's gain does not replicate in confirmatory experiments, the narrowed hypothesis
will fail the Result Adequacy Gate and a further pivot or venue downgrade will be required.

**Consequence:**
Affects: claims, writing, direction.
Contribution Contract Claim C1 revised from "four-module synergy" to "ProposedModule-driven
hierarchical reasoning with supporting AttentionModule+regularization."
Paper_outline.md Section III will lead with ProposedModule description.

**Reversible:** Yes — revert to original equal-emphasis framing if confirmatory
ProposedModule results do not replicate.
```

---

### Example 2: Venue Downgrade

```markdown
---

### DEC-2026-06-15-001

decision_id: DEC-2026-06-15-001
date: 2026-06-15
session_number: 14
stage: 24
category: venue
impact_level: Critical

**Context:**
The paper is 9 pages with 5 figures and 3 tables. The target venue (MICCAI 2026)
enforces an 8-page limit with figures included. Cutting the paper to 8 pages would
require removing the ablation table (Table III) or the dataset comparison figure
(Fig. 4), both of which are essential to the core argument.

**Decision Made:**
The target venue is changed from MICCAI 2026 to IEEE Transactions on Medical Imaging,
which has no page limit and a higher impact factor for benchmark comparison papers.

**Options Considered:**
1. Change to IEEE TMI (no page limit, IF ~11) — chosen.
2. Cut paper to 8 pages and submit to MICCAI (loses ablation).
3. Submit to MedIA (Medical Image Analysis) — similar scope, slower review.

**Evidence Used:**
- MICCAI 2026 CFP: confirmed 8-page limit inclusive of references.
- TMI scope statement: explicitly covers the paper's domain.
- Prior work (b3, b7) both published in TMI confirming venue appropriateness.

**Risk:**
TMI review cycle is 3-6 months vs MICCAI 4 months. Project timeline extends.
Risk of a more thorough review requiring additional experiments.

**Consequence:**
Affects: venue, writing.
Format changes: two-column IEEE format, no page limit, longer related work section acceptable.
Deadline changes from MICCAI submission (2026-03-01) to TMI rolling submission.

**Reversible:** Yes — revert to MICCAI format and cut ablation if TMI review cycle
is unacceptable to the team.
```

---

### Example 3: Claim Narrowing After Reviewer Concern

```markdown
---

### DEC-2026-07-02-002

decision_id: DEC-2026-07-02-002
date: 2026-07-02
session_number: 19
stage: 23
category: claim-softening
impact_level: Medium

**Context:**
During the logic-reviewer pass (Stage 22), it was flagged that Contribution Claim C3
states "YourMethod achieves state-of-the-art performance on Dataset-B" but the
result contract only required improvement over the five listed baselines, not over
all published methods. Two papers published after the literature freeze (b15, b16)
report higher AUC on Dataset-B.

**Decision Made:**
Claim C3 is softened from "state-of-the-art on Dataset-B" to "best among the five
baselines evaluated, with competitive performance on Dataset-B."

**Options Considered:**
1. Soften the claim to match actual evidence (chosen).
2. Index b15 and b16 with paper-qa and run additional experiments to compare.
3. Remove Claim C3 entirely and rely only on Dataset-A results.

**Evidence Used:**
- b15 (Author et al., 2026): Dataset-B AUC = 0.941 vs our 0.931 ± 0.008.
- b16 (Author et al., 2026): Dataset-B AUC = 0.938 vs our 0.931 ± 0.008.
- Our result contract: threshold was "exceed all five listed baselines," not "exceed all published work."

**Risk:**
Softened claim is less impactful but defensible. Risk: reviewers may still ask
about b15 and b16 in rebuttal.

**Consequence:**
Affects: claims, writing.
Introduction and Conclusion must be revised to remove "state-of-the-art on Dataset-B."
Abstract revised. Fig. 5 caption revised.

**Reversible:** No — the factual situation (b15, b16 exist) cannot change.
```

---

## Quick Reference: What Goes in the Log

**YES — log this:**
- Choosing one hypothesis framing over another
- Deciding to use dataset A instead of dataset B
- Dropping a baseline because it failed to reproduce
- Softening "outperforms" to "performs comparably"
- Adding a new experiment after seeing initial results
- Changing the primary metric from F1 to AUC
- Deciding the paper is ready for submission despite an unresolved minor issue
- Any pivot in research direction
- Any venue change
- Any increase in compute budget beyond the original plan

**NO — do not log this:**
- Fixing a typo
- Reformatting a table
- Adjusting a figure's color scheme
- Running a planned experiment from the experiment plan
- Updating project_state.md after a session

---

## File Location

Save `decision_log.md` in the project root directory alongside `project_state.md`.
The log begins with the header below and grows with each appended entry.

```markdown
# decision_log.md
# Append-only — do not modify or delete prior entries.
# Decision ID format: DEC-YYYY-MM-DD-NNN

Project: <project_name>
Started: <ISO date>

---
```
