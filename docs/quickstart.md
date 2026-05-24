# Quickstart Guide

## Overview

The Academic Research OS is a structured 26-stage workflow for conducting rigorous, evidence-first academic research. It integrates Claude Code, paper-qa (pqa), tectonic, and a set of slash commands to guide a project from raw idea to camera-ready submission without hallucinating results or novelty claims.

This guide gets you running in under 30 minutes.

---

## 1. Prerequisites

Before starting, ensure the following tools are installed and accessible from your shell:

| Tool | Purpose | Minimum Version |
|------|---------|-----------------|
| Claude Code | AI assistant and workflow driver | Latest |
| paper-qa (`pqa`) | Retrieval-augmented literature search | 4.0+ |
| tectonic | LaTeX compiler (PDF output) | 0.15+ |
| git | Version control for artifact tracking | 2.30+ |

To verify all prerequisites at once, open Claude Code inside your project directory and run:

```
/tool-healthcheck
```

If any tool is missing, see the [Installation Guide](installation.md) before continuing.

---

## 2. Three Ways to Use This OS

### (a) Fresh Project

You have a research idea and no existing code or results. Start here:

```bash
# Clone the template
git clone https://github.com/your-org/academic-research-os my-project
cd my-project

# Run the new-project setup script
bash scripts/new-project.sh
```

The setup script creates `project_state.md`, `research_direction.md`, `experiment-plan.md`, and the `.claude/` config directory. You begin at Stage 0.

### (b) Existing Project

You have code, partial results, or a draft and want to graft the OS onto it. Copy the `.claude/` directory into your project root:

```bash
cp -r /path/to/academic-research-os/.claude /path/to/your-project/
cd /path/to/your-project
claude  # open Claude Code
```

Then run `/research-status` to detect which stages are already satisfied and which artifacts are missing. The OS will tell you the earliest unmet gate and the next safe action.

### (c) Template Clone via GitHub

Use the "Use this template" button on the GitHub repository page. This creates a fresh repository under your account with all workflow files intact but no project-specific content. Then follow the fresh-project path above.

---

## 3. First Session Walkthrough

Open Claude Code inside your project directory. You will be prompted to read `.claude/research-os/12_SESSION_PROTOCOL.md` automatically if it is present.

**Step 1 — Report current stage.**
Claude reads `project_state.md` and tells you: "You are at Stage 0. No artifacts are present."

**Step 2 — Identify blockers.**
Run `/research-status`. Claude scans for required artifact files and reports which are missing, which are present, and what the next safe action is.

**Step 3 — Confirm before writing.**
The OS will not write any paper prose or create artifacts without your explicit confirmation. After Claude proposes the next action, type `yes` or press Enter to proceed, or give a different instruction.

**Step 4 — Work through Stage 0.**
For a fresh project, Stage 0 is the Research Question draft. Claude will ask you to describe your idea in 2-3 sentences and will create `research_direction.md` from your input.

**Step 5 — Update state.**
At the end of the session, run `/update-state` or ask Claude to update `project_state.md`. This ensures the next session picks up correctly.

---

## 4. The First 5 Commands

These five commands are used in almost every session. Learn them first.

### `/research-status`

Scans the project for required artifacts, checks which stages are complete, and reports the current stage, the next incomplete gate, and any missing files. Run this at the start of every session.

```
/research-status
```

Expected output: a numbered list of completed stages (green check), incomplete stages (yellow dash), and failed gates (red X), followed by a recommended next action.

### `/tool-healthcheck`

Checks that pqa, tectonic, git, and any registered plugins are installed and reachable. Does not modify any files.

```
/tool-healthcheck
```

Run this if a tool command fails unexpectedly or after a new machine setup.

### `/verify-research-os`

Checks the integrity of the `.claude/research-os/` system files themselves: that all 26 stage definitions are present, that hook files are intact, and that no system file has been accidentally modified. Different from `/tool-healthcheck`, which checks external tools.

```
/verify-research-os
```

Run this after cloning or after any manual edits to `.claude/`.

### `/research-start`

Begins a new research project interactively. Asks for a working title, research question, and domain, then creates `research_direction.md` and initializes `project_state.md` at Stage 0. Only run once per project.

```
/research-start
```

Do not run this on an existing project — it will overwrite `project_state.md`.

### `/venue-target`

Helps you select a publication venue. Presents the 6-tier classification system, asks for your preliminary results profile, and writes `venue_target.md`. Safe to run early as a planning artifact, but the venue is not binding until Stage 9 (Target Result Contract).

```
/venue-target
```

Running `/venue-target` before having any experiment results is allowed but outputs a provisional tier with a warning.

---

## 5. Common First-Session Mistakes

**Mistake 1: Writing prose before Stage 17.**
The OS does not permit paper prose in `paper.tex` before the Evidence Freeze (Stage 17). If you ask Claude to "write the introduction," it will refuse and explain which stages must be completed first. Do not try to override this.

**Mistake 2: Skipping `/research-status`.**
Starting work without running `/research-status` means you may duplicate completed work or attempt a stage whose prerequisites are unmet. Always run it first.

**Mistake 3: Running `/research-start` on an existing project.**
This overwrites `project_state.md`. If you have an existing project, use `/research-status` instead to detect the current stage.

**Mistake 4: Claiming novelty before Stage 6.**
Statements like "our method is the first to..." are blocked before the Prior-Art/SOTA Check gate (Stage 6) passes. Use the placeholder `TODO_NOVELTY_CHECK_NEEDED:` until the gate is cleared.

**Mistake 5: Averaging results from different fold counts.**
The OS enforces consistent fold counts across all reported results. If baseline A used 3 folds and your method used 5 folds, the comparison is invalid. Use matching fold counts or document the discrepancy explicitly.

**Mistake 6: Not updating `project_state.md` at session end.**
The OS cannot resume correctly if `project_state.md` is stale. Always update it before closing Claude Code.
