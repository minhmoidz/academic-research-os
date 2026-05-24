# Skill: /submission-check

Complete the final submission checklist before submitting the paper.

---

## Trigger

User types `/submission-check` or invokes via Skill tool.

---

## Required Input (ask if missing)

1. Path to final PDF
2. Path to references.bib
3. Path to result-map.md (or claim-evidence-table.md)
4. Target venue name and deadline

---

## Execution Steps

### Step 1: Read system files

```
Read .claude/research-os/09_SUBMISSION_CHECKLIST.md
Read .claude/research-os/08_REVIEW_AND_AUDIT_PLAYBOOK.md § Severity Levels
```

### Step 2: Run automated checks

**TODO markers:**
```bash
grep -n "TODO_" paper.tex
```
Every result must be empty or intentionally documented.

**Citation key consistency:**
```bash
grep -oP '\\cite\{\K[^}]+' paper.tex | sort -u > /tmp/tex_cites.txt
grep -oP '@\w+\{\K[^,]+' references.bib | sort -u > /tmp/bib_keys.txt
diff /tmp/tex_cites.txt /tmp/bib_keys.txt
```
All keys in .tex must be in .bib and vice versa.

**Undefined references:**
```bash
grep "?" paper.log
```

**Overfull hboxes:**
```bash
grep "Overfull" paper.log | grep -v "0\." | head -20
```

### Step 3: Run agent audits

```
Agent: academic-writing-agents:bibliography-auditor
  → Check: arXiv-only citations, missing pages, inconsistent venue names, title capitalization

Agent: academic-writing-agents:latex-layout-auditor
  → Check: float placement, last-page balance, isolated figures
```

### Step 4: Manual checklist — work through 09_SUBMISSION_CHECKLIST.md

Go through all 8 sections (A–H) and check each item.
For each item:
- ✓ Verified: mark done
- ✗ Failed: record as a finding
- N/A: document why it doesn't apply

### Step 5: Confirm 10 review passes completed

From research-state.md or session history:
- [ ] Pass 1 Logic ✓
- [ ] Pass 2 Technical ✓
- [ ] Pass 3 Claim-evidence ✓
- [ ] Pass 4 Citation ✓
- [ ] Pass 5 Writing ✓
- [ ] Pass 6 De-AI ✓
- [ ] Pass 7 Figure/table ✓
- [ ] Pass 8 LaTeX/layout ✓
- [ ] Pass 9 Paper-code alignment ✓
- [ ] Pass 10 Final skeptical ✓

### Step 6: Fill sign-off block

From `09_SUBMISSION_CHECKLIST.md § Sign-off`.

---

## Safety Rules

- No items skipped without documented justification
- No Critical review findings outstanding at sign-off
- Do not submit if any `TODO_` markers remain unresolved

---

## Output

```
Submission Checklist Summary
============================
A. Content: [N/N items ✓]
B. Citations: [N/N items ✓]
C. Results: [N/N items ✓]
D. Figures/Tables: [N/N items ✓]
E. Equations: [N/N items ✓]
F. LaTeX: [N/N items ✓]
G. Scope/Honesty: [N/N items ✓]
H. Pre-submission: [N/N items ✓]

Review passes: [N/10 completed]
Open Critical findings: [N]

Status: [READY FOR SUBMISSION / NOT READY — resolve [N] items first]
```
