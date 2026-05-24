# Skill: /draft-section

Draft a specific paper section using verified evidence only.

---

## Trigger

User types `/draft-section [section-name]` or invokes via Skill tool.

---

## Required Input (ask if missing)

1. Section name (Abstract / Introduction / Related Work / Method / Experiments / Analysis / Limitations / Conclusion)
2. Claim-evidence table rows for this section (from claim-evidence-table.md)
3. Relevant literature matrix rows (for Related Work)
4. List of already-approved sections (for consistency)

---

## Pre-flight Check (run before drafting)

Verify each item:

- [ ] claim-evidence-table.md exists and has entries for this section
- [ ] All result files cited in the table are accessible
- [ ] All citation keys for this section exist in references.bib
- [ ] Evidence gate passed (see research-state.md)

If any item fails: stop and report. Do not draft.

---

## Execution Steps

### Step 1: Read system files

```
Read .claude/research-os/06_WRITING_PLAYBOOK.md (section for [section-name])
Read .claude/research-os/13_ANTI_HALLUCINATION_RULES.md
```

### Step 2: For Related Work sections — run paper-qa

```bash
pqa -i [index-name] ask "How does [cited paper] address [topic]?"
```

Fill Related Work claims from paper-qa output. Never from memory.

### Step 3: Draft the section

Follow `06_WRITING_PLAYBOOK.md` for the specific section.

Required conventions:
- IEEE conference LaTeX format (IEEEtran)
- `\cite{key}` for all citations (key must exist in references.bib)
- `\label{sec:X}` and `\ref{sec:X}` for cross-references
- `\eqref{eq:X}` for equation references
- `\footnotesize` inside TikZ figures and tables
- No forbidden phrases from `06_WRITING_PLAYBOOK.md § Blacklisted phrases`

### Step 4: Tag all unresolved items

For any claim without a source:
```
TODO_RESULT_NEEDED: [description of what number is missing]
TODO_CITATION_NEEDED: [description of what paper is needed]
TODO_EVIDENCE_NEEDED: [description of what paper-qa should verify]
```

Never fill a TODO with a fabricated value.

### Step 5: Update claim-evidence-table.md

For each claim written, add a row:
```
| [Section] | [para N] | "[claim quoted]" | [result file or paper-qa query] | ✓ / TODO |
```

---

## Safety Rules

- No result stated without a verified source file
- No citation used without a verified references.bib entry
- No Related Work written from memory — paper-qa only
- All LaTeX commands (`\cite`, `\label`, `\ref`, `\eqref`) must be preserved exactly during any later revision

---

## Output

Drafted LaTeX for the section, followed by:
```
Claim-evidence table updated: [N] claims added, [M] TODOs created
Citations used: [list of \cite{key} keys]
TODO markers: [list any open TODOs]
```
