# Academic Research OS for Claude Code

A reusable Claude Code Research Operating System for evidence-first academic research, experiment tracking, prior-art checking, venue targeting, paper writing, LaTeX formatting, and multi-agent review.

---

## What This Solves

- Prevents hallucinated citations — no `\cite{}` without a verified BibTeX entry
- Prevents unsupported claims — every quantitative statement traces to a logged experiment
- Prevents premature paper writing — prose is blocked until Stage 17 Evidence Freeze passes
- Forces prior-art and SOTA checks before any novelty claim is written
- Defines minimum result requirements before confirmatory experiments run
- Separates exploratory experiments (hypothesis generation) from confirmatory experiments (paper claims)
- Maps every result to evidence IDs before the draft is written
- Gates paper drafting behind a structured evidence freeze with 4 hard checkpoints

---

## The 4 Hard Gates

**Gate 1 — Prior-Art / SOTA Check (Stage 6)**
No novelty claim may be written until a systematic prior-art check passes. Produces `prior_art_competition_table.md` and `novelty_risk_report.md`. Any contribution with threat level Critical triggers a mandatory pivot or abandonment.

**Gate 2 — Target Result Contract (Stage 9)**
Minimum acceptable results, required baselines, required datasets, and pass/fail criteria must be defined and signed off before any confirmatory experiment runs. The bar cannot be lowered after experiments begin.

**Gate 3 — Result Adequacy Gate (Stage 16)**
Six conditions are evaluated: TRC pass, prior-art beat, stability, ablation support, novelty defense, and venue fit. All six must pass. A partial pass is a full fail. Produces `result_adequacy_report.md` with one of seven decisions (A–G).

**Gate 4 — Evidence Freeze (Stage 17)**
All paper claims must be mapped to evidence IDs in `evidence_ledger.md` before prose writing begins. No sentence with a quantitative claim may be drafted without a complete evidence chain: `results.tsv → evidence_ledger.md → claim-evidence-table.md → paper.tex`.

---

## Core Workflow

```
Idea
  → Stage 1:  Idea Intake & Paper Brief
  → Stage 2:  Problem Formulation & Hypothesis Registration
  → Stage 3:  Venue Targeting
  → Stage 4:  Initial Feasibility Check
  → Stage 5:  Literature Grounding
  → Stage 6:  Prior-Art / SOTA Check         [GATE 1]
  → Stage 7:  Gap and Positioning
  → Stage 8:  Contribution Contract
  → Stage 9:  Target Result Contract          [GATE 2]
  → Stage 10: Experiment Design
  → Stage 11: Baseline / Implementation Readiness
  → Stage 12: Exploratory Experiment Loop
  → Stage 13: Result Interpretation / Direction Update
  → Stage 14: Confirmatory Experiment Planning
  → Stage 15: Confirmatory Experiment Execution
  → Stage 16: Result Adequacy Gate            [GATE 3]
  → Stage 17: Evidence Freeze                 [GATE 4]
  → Stage 18: Paper Architecture
  → Stage 19: Section Drafting
  → Stage 20: Figure and Table Design
  → Stage 21: LaTeX Formatting
  → Stage 22: Multi-Agent Review
  → Stage 23: Revision
  → Stage 24: Submission Preparation
  → Stage 25: Archive
```

---

## Quickstart

```bash
# Clone the template
git clone https://github.com/minhmoidz/academic-research-os.git

# Scaffold a new research project
mkdir my-new-paper
academic-research-os/scripts/new-project.sh my-new-paper

# Open Claude Code in your project
cd my-new-paper
claude

# Then type:
/research-status
/tool-healthcheck
/research-start
```

---

## Install Into New Project

```bash
git clone https://github.com/minhmoidz/academic-research-os.git
cd my-new-paper
../academic-research-os/scripts/new-project.sh .
claude
# then type: /research-status
```

---

## All 24 Commands

| Command | Purpose | Stage |
|---------|---------|-------|
| `/research-status` | Report current stage, artifacts, blockers, next safe action | Any |
| `/tool-healthcheck` | Verify all Research OS tools are available | Stage 0 |
| `/verify-research-os` | Verify all 29 workflow files and 21 skill files are intact | Any |
| `/resume-research-session` | Restore full project context at session start | Any |
| `/research-start` | Initialize new project: paper brief, hypothesis registry, project state | Stage 1 |
| `/venue-target` | Select target venue and define evidence requirements | Stage 3 |
| `/build-contribution-map` | Create contribution contract mapping claims to hypotheses | Stage 8 |
| `/target-result-contract` | Define binding minimum result requirements before experiments | Stage 9 |
| `/literature-review` | Build paper-qa index and literature matrix from local PDFs | Stage 5 |
| `/prior-art-check` | Assess whether prior work already addresses the contribution | Stage 6 |
| `/sota-check` | Identify best known results on target datasets | Stage 6 |
| `/plan-experiments` | Design full experiment matrix before running anything | Stage 10 |
| `/experiment-loop` | Run bounded autoresearch-style experiment loop | Stages 12, 15 |
| `/experiment-status` | Report current state of all experiments | Any |
| `/result-backfill` | Backfill evidence ledger from existing result files | Stage 17 |
| `/result-adequacy` | Stage 16 gate: evaluate results against target result contract | Stage 16 |
| `/pivot-decision` | Generate structured pivot decision when results fail | Stage 13, 16+ |
| `/create-paper-outline` | Create paper section skeleton before any prose is written | Stage 18 |
| `/draft-section [name]` | Draft a specific paper section using verified evidence only | Stage 19 |
| `/design-figure [desc]` | Create a figure or diagram for the paper | Stage 20 |
| `/format-paper` | Compile, format, and fix LaTeX layout issues | Stage 21 |
| `/review-paper` | Run all 12 review passes | Stage 22 |
| `/apply-revision-plan` | Apply fixes from review report systematically | Stage 23 |
| `/submission-check` | Complete final submission checklist before submitting | Stage 24 |

---

## Prerequisites

- Claude Code (claude.ai/code)
- paper-qa (`pip install paper-qa`)
- tectonic LaTeX compiler (`cargo install tectonic` or via package manager)
- Git

---

## Directory Structure

```
academic-research-os/
├── CLAUDE.md                        # Root-level project instructions
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .gitignore
├── .claude/
│   ├── CLAUDE.md                    # Project instructions for Claude Code
│   ├── research-os/                 # 29 workflow files (00–28)
│   │   ├── 00_OVERVIEW.md
│   │   ├── 02_RESEARCH_WORKFLOW.md
│   │   ├── 13_ANTI_HALLUCINATION_RULES.md
│   │   └── ...
│   └── skills/                      # 21 skill files
│       ├── research-start/
│       ├── experiment-loop/
│       └── ...
├── templates/                       # 17 artifact templates
│   ├── paper_brief.template.md
│   ├── project_state.template.md
│   └── ...
├── examples/
│   └── toy-research-project/        # Worked example project
├── scripts/
│   ├── new-project.sh               # Scaffold a new research project
│   ├── install.sh                   # Install OS into existing project
│   └── verify.sh                    # Verify OS integrity
└── docs/
    ├── quickstart.md
    └── installation.md
```

---

## Docs

- [Quickstart Guide](docs/quickstart.md)
- [Installation Guide](docs/installation.md)
- [Anti-Hallucination Rules](.claude/research-os/13_ANTI_HALLUCINATION_RULES.md)
- [26-Stage Workflow](.claude/research-os/02_RESEARCH_WORKFLOW.md)
- [Command Reference](.claude/research-os/11_COMMANDS.md)
- [Changelog](CHANGELOG.md)

---

## License

MIT — see [LICENSE](LICENSE)
