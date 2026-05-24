# 15_TOOL_HEALTHCHECK.md — Tool Healthcheck Protocol

## Purpose

Before any research work begins, Claude must verify that all required tools are
actually installed and callable. A missing tool discovered mid-project causes wasted
effort and incorrect stage transitions. This file defines the exact test command,
expected output, failure symptoms, and recovery action for every tool in the Research OS.

**Rule:** Claude must run this healthcheck at **Stage 0** of every new project and
save the result as `tool_healthcheck_report.md` in the project root. Claude must NOT
use a tool marked **Missing** or **Untested** for any critical-path stage.

---

## Tool Inventory and Tests

### 1. pqa — PaperQA CLI

| Field | Value |
|-------|-------|
| Binary | `pqa` (locate with `which pqa`) |
| Test command | `pqa --help` |
| Expected output | Usage message listing `ask`, `index`, `search` subcommands |
| Failure symptom | `command not found`, `No such file or directory`, or import error |
| Stages required | 5 (Literature Grounding), 6 (Prior-Art/SOTA), 7 (Gap/Positioning) |
| Install/fix | `pip install paper-qa` then verify with `pqa --help` |
| Severity if missing | **Critical** — cannot do evidence-grounded literature review |

```bash
# Test command
pqa --help
```

---

### 2. tectonic — LaTeX Compiler

| Field | Value |
|-------|-------|
| Binary | `tectonic` (locate with `which tectonic`) |
| Test command | `tectonic --version` |
| Expected output | `tectonic X.Y.Z` version string |
| Failure symptom | `command not found`, permission error, or version mismatch |
| Stages required | 21 (LaTeX Formatting/PDF), 24 (Submission Check) |
| Install/fix | Download from https://tectonic-typesetting.github.io/ or `conda install -c conda-forge tectonic` |
| Severity if missing | **High** — paper cannot be compiled; fallback to system pdflatex if available |

```bash
# Test command
tectonic --version
```

---

### 3. git — Version Control

| Field | Value |
|-------|-------|
| Binary | system `git` |
| Test command | `git --version` |
| Expected output | `git version 2.X.Y` |
| Failure symptom | `command not found` |
| Stages required | 0 (readiness), 25 (Camera-Ready Archive) |
| Install/fix | `sudo apt-get install git` |
| Severity if missing | **Medium** — version control unavailable; manual backup required |

```bash
git --version
```

---

### 4. academic-writing-agents Plugin (12 agents)

| Field | Value |
|-------|-------|
| Location | `.claude/repos/academic-writing-agents/agents/` |
| Test command | Check directory exists and contains `.md` files |
| Expected output | 12 agent files: bibliography-auditor.md, brainstormer.md, consistency-checker.md, latex-figure-specialist.md, latex-layout-auditor.md, logic-reviewer.md, paper-crawler.md, prose-polisher.md, research-analyst.md, section-drafter.md, technical-reviewer.md, writing-reviewer.md |
| Failure symptom | Directory missing or fewer than 12 `.md` files |
| Stages required | 22 (Multi-Agent Review), 23 (Revision/Re-Audit) |
| Install/fix | Clone or restore the `academic-writing-agents` repo into `.claude/repos/` |
| Severity if missing | **High** — multi-agent review unavailable; must do manual review |

```bash
# Test command
ls /path/to/your/project/.claude/repos/academic-writing-agents/agents/*.md 2>/dev/null | wc -l
# Expected: 12
```

---

### 5. Python 3 Environment

| Field | Value |
|-------|-------|
| Binary | `python3` |
| Test command | `python3 --version` |
| Expected output | `Python 3.X.Y` (3.8 or higher recommended) |
| Failure symptom | `command not found` or version < 3.8 |
| Stages required | 10-16 (Experiment stages), result parsing |
| Install/fix | `conda install python=3.10` or system Python |
| Severity if missing | **Critical** — cannot run experiments or parsing scripts |

```bash
python3 --version
```

---

### 6. GPU Environment (nvidia-smi)

| Field | Value |
|-------|-------|
| Binary | `nvidia-smi` |
| Test command | `nvidia-smi` |
| Expected output | GPU table showing device name, driver version, CUDA version, memory usage |
| Failure symptom | `command not found` or `NVIDIA-SMI has failed` |
| Stages required | 12 (Exploratory Experiments), 15 (Confirmatory Experiments) |
| Install/fix | Install NVIDIA drivers; if CPU-only machine, document as CPU-only |
| Severity if missing | **Context-dependent** — only critical if experiments require GPU |

```bash
nvidia-smi
```

---

### 7. Result Parsing Scripts (project-specific)

| Field | Value |
|-------|-------|
| Location | Project root: `eval.py`, `parse_results.py`, or similar |
| Test command | `find . -name "eval.py" -o -name "parse_results.py" -o -name "aggregate_results.py" 2>/dev/null` |
| Expected output | One or more script paths found |
| Failure symptom | No files found |
| Stages required | 13 (Result Interpretation), 16 (Result Adequacy Gate) |
| Install/fix | Locate existing scripts in model subdirectories; write minimal parsing script if none exists |
| Severity if missing | **Medium** — results can be read manually from logs |

```bash
find . -maxdepth 3 -name "*.py" | grep -E "(eval|parse|result|aggregate)" | head -20
```

---

## Native Claude Skills (Cannot Be Shell-Tested)

The following are registered Claude skills invoked through the Claude harness.
They cannot be verified with shell commands. They must be assumed available unless
Claude receives an error when attempting to invoke them.

| Skill | Invocation | Stages Required | Fallback if Unavailable |
|-------|-----------|-----------------|------------------------|
| `thesis-figure-skill` | Via Skill tool | 20 (Figure Design) | Manual TikZ; use LaTeX directly |
| `latex-document` | Via Skill tool | 21 (LaTeX Formatting) | Use tectonic directly |
| `research-paper-writing` | Via Skill tool | 18-19 (Architecture, Drafting) | Manual section writing with templates |
| `empirical-paper-writer` | Via Skill tool | 18-19 | Manual section writing |
| `results-backfill` | Via Skill tool | 19 (Drafting with results) | Manual table insertion |
| `latex-rhythm-refiner` | Via Skill tool | 23 (Revision) | Manual prose polish |

**Rule:** Mark each native skill as **assumed-available** in the healthcheck report.
If a skill invocation fails during a session, update the report to **Missing** and
use the listed fallback.

---

## Tool Status Table Template

Use this template when generating `tool_healthcheck_report.md`:

```markdown
# Tool Healthcheck Report

Project: <project_name>
Date: <ISO timestamp>
Stage: 0 (System Readiness)

## Status Table

| Tool | Status | Version/Evidence | Required By Stages |
|------|--------|------------------|--------------------|
| pqa | Working / Missing / Untested | X.Y.Z | 5, 6, 7 |
| tectonic | Working / Missing / Untested | X.Y.Z | 21, 24 |
| git | Working / Missing / Untested | 2.X.Y | 0, 25 |
| academic-writing-agents | Working / Missing / Untested | 12 agents found | 22, 23 |
| Python 3 | Working / Missing / Untested | 3.X.Y | 10-16 |
| nvidia-smi | Working / Missing / Untested | Driver X.Y | 12, 15 |
| result scripts | Working / Missing / Untested | N scripts found | 13, 16 |
| thesis-figure-skill | assumed-available | native skill | 20 |
| latex-document | assumed-available | native skill | 21 |
| research-paper-writing | assumed-available | native skill | 18-19 |
| empirical-paper-writer | assumed-available | native skill | 18-19 |
| results-backfill | assumed-available | native skill | 19 |
| latex-rhythm-refiner | assumed-available | native skill | 23 |

## Working Tools and Required Stages
<list tools with status=Working and the stages they unlock>

## Missing Tools and Install Commands
<list tools with status=Missing, their install commands, and what stages are blocked>

## Untested Tools
<list tools that could not be tested and the reason>

## Native Skills (Assumed Available)
<list all native skills>

## Blocker Summary
<YES/NO: is there a Critical blocker that prevents starting Stage 1?>
<Recommended action before proceeding>
```

---

## Stage Gating Rules

| Tool Status | Claude Action |
|------------|---------------|
| Working | May use at any stage |
| Missing (Medium severity) | Must warn user; may continue with fallback |
| Missing (High severity) | Must warn user and document workaround before proceeding |
| Missing (Critical severity) | Must STOP and require fix before any dependent stage |
| Untested | Treat as Missing until confirmed Working |
| assumed-available (native skill) | May invoke; if invocation fails, use listed fallback |

---

## Running the Healthcheck

At Stage 0, Claude must:

1. Run each shell-testable command and capture output.
2. For each tool, record status as Working, Missing, or Untested.
3. Record all native skills as assumed-available.
4. Write the populated `tool_healthcheck_report.md` to project root.
5. Identify any Critical blockers.
6. If no Critical blockers: report "System ready — Stage 1 may begin."
7. If Critical blockers exist: report "System NOT ready — fix required before Stage 1."

Do not skip this step. A missing tool discovered in Stage 19 wastes all prior work.
