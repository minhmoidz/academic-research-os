# Repository and Tool Map

All tools in the Research OS ecosystem. Run `/tool-healthcheck` to verify current status.

---

## Status Legend

| Status | Meaning |
|--------|---------|
| ✓ ACTIVE | Installed locally and verified working |
| ~ NATIVE | Native Claude skill — available without installation |
| ✗ MISSING | Not installed locally; install command provided |

---

## Tool 1: academic-writing-agents

**URL:** https://github.com/andrehuang/academic-writing-agents  
**Status:** check with `/tool-healthcheck` — installed at `.claude/repos/academic-writing-agents/`  
**Plugin:** v2.0.0, 12 agents

**Agents:**

| Agent | Role | Stage(s) |
|-------|------|----------|
| `logic-reviewer` | Argument flow, narrative, conclusions | 22 Pass 1, 22 Pass 12 |
| `technical-reviewer` | Math, methodology, dimension errors | 22 Pass 2, 22 Pass 11 |
| `consistency-checker` | Claim-evidence cross-check | 22 Pass 3 |
| `bibliography-auditor` | Citations, bib entries, venue names | 22 Pass 4 |
| `research-analyst` | Gap analysis, positioning | 6-7 |
| `brainstormer` | Ideas, framings | 1-2 |
| `paper-crawler` | DBLP/OpenAlex literature search | 5 |
| `writing-reviewer` | Grammar, clarity, tone | 22 Pass 7 |
| `prose-polisher` | De-AI, rhythm, variety | 22 Pass 8 |
| `latex-figure-specialist` | TikZ, pgfplots, captions | 22 Pass 9 |
| `latex-layout-auditor` | Float placement, column balance | 22 Pass 10 |
| `section-drafter` | Section skeleton, LaTeX structure | 18-19 |

**Invoke:** `academic-writing-agents:[agent-name]` via the Agent tool.

---

## Tool 2: paper-qa

**URL:** https://github.com/Future-House/paper-qa  
**Status:** check with `/tool-healthcheck` — install path varies; use `which pqa` to locate

**Role:** Evidence engine for local PDFs. Required for literature grounding and prior-art checks.

**Key commands:**
```bash
pqa -i my-index index /path/to/pdfs/
pqa -i my-index ask "What methods address [topic]?"
pqa -i my-index ask "Does any paper address [specific gap]?"
pqa -i my-index ask "Best result on [dataset] for [metric]?"
```

**Stages:** 5 (literature matrix), 6 (prior-art/SOTA), 7 (gap validation), 19 (Related Work verification)

**Rule:** Never fill a literature matrix cell from memory. Use paper-qa or mark `?`.

---

## Tool 3: thesis-figure-skill

**URL:** https://github.com/0xE1337/thesis-figure-skill  
**Status:** ~ NATIVE — Claude native skill

**Role:** Architecture diagrams, method diagrams, TikZ code for paper figures.

**Stages:** 20 (figure design)

---

## Tool 4: latex-document-skill

**URL:** https://github.com/ndpvt-web/latex-document-skill  
**Status:** ~ NATIVE — Claude native skill

**Role:** LaTeX/PDF production, BibTeX, tables, compilation, pgfplots charts.

**Stages:** 21 (formatting), 24 (final PDF)

---

## Tool 5: Research-Paper-Writing-Skills

**URL:** https://github.com/Master-cai/Research-Paper-Writing-Skills  
**Status:** ~ NATIVE — Claude native skill (`research-paper-writing`)

**Role:** Section-level academic writing guidance.

**Stages:** 19 (section drafting), 23 (revision)

---

## Tool 6: empirical-paper-writer

**Status:** ~ NATIVE — Claude native skill

**Role:** Specialized for empirical ML paper sections (Experiments, Analysis, Ablation).

**Stages:** 19

---

## Tool 7: latex-rhythm-refiner

**Status:** ~ NATIVE — Claude native skill

**Role:** Sentence-level rhythm and variety improvement after writing.

**Stages:** 22 Pass 8 (de-AI review)

---

## Tool 8: latex-paper-skills

**URL:** https://github.com/yunshenwuchuxun/latex-paper-skills  
**Status:** ✗ MISSING

**Install:** `git clone https://github.com/yunshenwuchuxun/latex-paper-skills.git .claude/repos/latex-paper-skills`

**Role when installed:** End-to-end paper workflow, contribution mapping, evidence matrix.

**Fallback:** `academic-writing-agents:section-drafter` + `03_IDEA_TO_PAPER_PLAYBOOK.md`

---

## Tool 9: academic-writing-skills

**URL:** https://github.com/bahayonghang/academic-writing-skills  
**Status:** ✗ MISSING

**Install:** `git clone https://github.com/bahayonghang/academic-writing-skills.git .claude/repos/academic-writing-skills`

**Role when installed:** Grammar/style polish, de-AI editing, format validation.

**Fallback:** `academic-writing-agents:writing-reviewer` + `academic-writing-agents:prose-polisher`

---

## Tool 10: claude-paper-review

**URL:** https://github.com/J0nasW/claude-paper-review  
**Status:** ✗ MISSING

**Install:** `git clone https://github.com/J0nasW/claude-paper-review.git .claude/repos/claude-paper-review`

**Role when installed:** Pre-submission referee-style review.

**Fallback:** `logic-reviewer` + `technical-reviewer` (academic-writing-agents)

---

## Tool 11: AI-research-feedback

**URL:** https://github.com/claesbackman/AI-research-feedback  
**Status:** ✗ MISSING

**Install:** `git clone https://github.com/claesbackman/AI-research-feedback.git .claude/repos/AI-research-feedback`

**Role when installed:** Paper-code-result alignment, reproducibility review.

**Fallback:** Manual review using `13_ANTI_HALLUCINATION_RULES.md` Rules 11-13

---

## Tool 12: paper-audit

**URL:** https://github.com/promptcrafted/paper-audit  
**Status:** ✗ MISSING

**Install:** `git clone https://github.com/promptcrafted/paper-audit.git .claude/repos/paper-audit`

**Role when installed:** Adversarial final audit — numbers, consistency, claims.

**Fallback:** 12-pass review protocol in `08_REVIEW_AND_AUDIT_PLAYBOOK.md`

---

## Tool 13: autoresearch (patterns integrated)

**URL:** https://github.com/karpathy/autoresearch  
**Status:** ✗ NOT installed — patterns extracted and adapted into Research OS

**Patterns integrated:**
- Fixed evaluation harness (protected files — DO NOT CHANGE)
- One editable file per experiment
- Fixed time budget per run (platform-independent comparison)
- Git branch per session
- TSV result log: run_id, commit, metric, status, description
- Keep/discard on metric improvement
- Simplicity criterion: deletion outweighs minor gain from added complexity
- Crash-fast on NaN/divergence (exit 1)

**Adaptation:** `20_AUTONOMOUS_EXPERIMENT_LOOP.md` adds: hard budget, user-defined metric/direction, pre-registered hypotheses, evidence ledger updates, paper-claim gate. The original "never stop" behavior is replaced with a bounded experiment loop.

**Optional local clone** (recommended if running real auto-loop experiments so Claude can re-read the original source):
```bash
git clone https://github.com/karpathy/autoresearch.git .claude/repos/autoresearch
```
Not required for normal Research OS use — all necessary patterns are already in `20_AUTONOMOUS_EXPERIMENT_LOOP.md`.

---

## Infrastructure Tools

| Tool | Path | Status |
|------|------|--------|
| tectonic | install path varies; use `which tectonic` to locate | check with `/tool-healthcheck` |
| pqa | install path varies; use `which pqa` to locate | check with `/tool-healthcheck` |
| git | system | check with `/tool-healthcheck` |
| Python 3 | system or conda environment | check with `/tool-healthcheck` |
| nvidia-smi | system | verify before GPU experiments |

---

## Quick Reference: Which Tool for Which Task

| Task | Primary | Fallback |
|------|---------|---------|
| Literature search | `paper-crawler` + `pqa` | Manual + DBLP |
| Prior-art check | `pqa` queries | Manual literature search |
| SOTA check | `pqa` + manual | User-provided |
| Experiment loop | `/experiment-loop` skill | Manual runs |
| Logic review | `logic-reviewer` | Manual |
| Technical review | `technical-reviewer` | Manual |
| Citation audit | `bibliography-auditor` | grep + manual |
| Writing review | `writing-reviewer` | Manual |
| De-AI polish | `prose-polisher` | Manual |
| Figure review | `latex-figure-specialist` | `consistency-checker` |
| Layout review | `latex-layout-auditor` | Manual PDF inspection |
| Architecture figures | `thesis-figure-skill` | TikZ manual |
| Section drafting | `research-paper-writing` + `section-drafter` | Manual |
| LaTeX compile | `tectonic` | pdflatex fallback |
