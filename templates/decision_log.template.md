# decision_log.md
# Append-only — do not modify or delete prior entries.
# Decision ID format: DEC-YYYY-MM-DD-NNN

Project: [project_name]
Started: [YYYY-MM-DD]

---

## Entry Template

Copy this block and fill it in for each new decision. Append below the last entry.
Never modify prior entries. If a decision is reversed, add a new entry with category `reversal`.

```
---

### DEC-YYYY-MM-DD-NNN

decision_id: DEC-YYYY-MM-DD-NNN
date: YYYY-MM-DD
session_number: [integer]
stage: [0-25]
category: [framing | pivot | venue | baseline | metric | result-interpretation | claim-softening | abandon | contribution | writing | reversal | budget]
impact_level: [Low | Medium | High | Critical]

**Context:**
[2-3 sentences describing the situation that prompted this decision.
What was observed, what was uncertain, and why a decision was needed.]

**Decision Made:**
[One clear, unambiguous sentence stating what was decided.]

**Options Considered:**
1. [Option A — the chosen option]
2. [Option B]
3. [Option C, if applicable]

**Evidence Used:**
- [Data, result, or literature that supported this decision.]
- [E.g., "EXP-005 ablation showed component X alone gives +1.8pp on Dataset-A."]
- [If no evidence: state "judgment call — no empirical evidence available."]

**Risk:**
[What could go wrong if this decision is wrong? What is the worst case?]

**Consequence:**
[What changes as a result of this decision? Affects: [claims / experiments / venue / writing / direction]]

**Reversible:** [Yes — how to reverse / No — why not]
```

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

## Rules

1. **Append-only.** Never delete or overwrite a prior entry.
2. **Every pivot must have an entry.** A research pivot (changing the core approach, hypothesis, or claim) is the highest-priority decision type.
3. **Every venue change must have an entry.**
4. **Every metric change (after seeing results) must have an entry.**
5. **Every claim removal or softening must have an entry.**
6. **Log before acting.** Write the entry before making the change, not after.

---

## Log Begins Below

(Append entries here in chronological order, oldest first.)
