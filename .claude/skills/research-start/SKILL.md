# Skill: /research-start

Initialize a new research project with proper state tracking.

---

## Trigger

User types `/research-start` or invokes via Skill tool.

---

## Required Input (ask if missing)

1. Project directory path
2. Working title
3. Target venue (e.g., "MICCAI 2026", "IEEE TMI")
4. Page limit

---

## Execution Steps

### Step 1: Read system files

```
Read .claude/research-os/12_SESSION_PROTOCOL.md
Read .claude/research-os/03_IDEA_TO_PAPER_PLAYBOOK.md
Read .claude/research-os/10_TEMPLATES.md
```

### Step 2: Ask the 8 Idea Clarification Questions

From `03_IDEA_TO_PAPER_PLAYBOOK.md § Section 1`, ask the user:

1. What is the problem your method addresses?
2. Why does the current best approach fail on this problem?
3. What does your method do differently?
4. What is the primary falsifiable claim?
5. What datasets and metrics will you use?
6. Who are the baselines, and are they runnable?
7. What is the minimum meaningful improvement to claim success?
8. What is the key figure that shows your method working?

Wait for answers before proceeding.

### Step 3: Initialize paper-brief.md

Fill Template 1 from `10_TEMPLATES.md` using the user's answers.
Save as `paper-brief.md` in the project directory.

### Step 4: Initialize research-state.md

From `12_SESSION_PROTOCOL.md § research-state.md Format`:
- Set Current Phase: 1
- Set Phase History: Phase 1 In Progress
- Set Next Step: "Complete idea formalization (Phase 2)"
- Evidence Gate: all unchecked

### Step 5: Create literature/ folder

```bash
mkdir -p literature/
```

### Step 6: Report

Tell the user:
- Files created: paper-brief.md, research-state.md, literature/
- Current phase: 1 (Idea Capture)
- Next action: Run /idea-to-plan to formalize the hypothesis and contribution map

---

## Safety Rules

- Do NOT write any paper prose
- Do NOT generate or invent any citations
- Do NOT run experiments
- Do NOT fill in result numbers
- Ask the 8 questions before creating any file

---

## Output

```
✓ paper-brief.md created
✓ research-state.md initialized (Phase 1)
✓ literature/ folder created

Next: /idea-to-plan to build the contribution map and hypothesis.
```
