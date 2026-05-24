# Skill: /review-paper

Run all 10 review passes from the Review and Audit Playbook.

---

## Trigger

User types `/review-paper` or invokes via Skill tool.

---

## Required Input (ask if missing)

1. Path to compiled PDF
2. Path to .tex source file
3. Which passes to run (default: all 10, or specify subset)

---

## Execution Steps

### Step 1: Read system file

```
Read .claude/research-os/08_REVIEW_AND_AUDIT_PLAYBOOK.md
```

### Step 2: Run passes in order

Run each requested pass using the agent specified in the playbook.
**Do not skip passes or run them out of order.**

| Pass | Agent | Must complete before |
|------|-------|---------------------|
| 1. Logic | `academic-writing-agents:logic-reviewer` | All other passes |
| 2. Technical | `academic-writing-agents:technical-reviewer` | Passes 3–10 |
| 3. Claim-evidence | `academic-writing-agents:consistency-checker` | Passes 4–10 |
| 4. Citation | `academic-writing-agents:bibliography-auditor` | Pass 10 |
| 5. Writing/style | `academic-writing-agents:writing-reviewer` | Pass 6 |
| 6. De-AI | `academic-writing-agents:prose-polisher` | Pass 10 |
| 7. Figure/table | `academic-writing-agents:latex-figure-specialist` | Pass 8 |
| 8. LaTeX/layout | `academic-writing-agents:latex-layout-auditor` | Pass 10 |
| 9. Paper-code alignment | Manual + `technical-reviewer` | Pass 10 |
| 10. Final skeptical | `academic-writing-agents:logic-reviewer` | — |

### Step 3: Compile findings into Section Review Report

Use Template 9 from `10_TEMPLATES.md`.

For each pass:
- List Critical findings (must fix before submission)
- List Major findings (should fix)
- List Minor findings (optional)

### Step 4: Report status

```
Pass 1 (Logic): [N Critical, M Minor]
Pass 2 (Technical): [N Critical, M Minor]
...
Pass 10 (Final): [N Critical, M Minor]

Overall: [N] Critical findings unresolved
Status: [Ready for submission / Needs revision]
```

---

## Safety Rules

- Run passes in order: logic before style, style before de-AI
- Critical findings must be resolved before any submission claim
- Do not change numerical content while fixing style issues (Pass 5/6)
- Do not alter citation keys while fixing bibliography (Pass 4)
- Pass 9 (paper-code alignment) requires inspecting actual result files — not memory

---

## Output

Section Review Report for each pass + overall status.
If any Critical findings: list them with location and recommended fix.
