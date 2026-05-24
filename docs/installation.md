# Installation Guide

## Overview

This guide walks through installing every tool the Academic Research OS depends on, verifying the installation, and setting up a new project from scratch.

---

## 1. Installing Claude Code

Claude Code is the primary interface for the Research OS. All slash commands, stage gating, and artifact management run inside Claude Code.

**Install:**
Visit [claude.ai/code](https://claude.ai/code) and follow the platform-specific instructions. Claude Code is available as a CLI tool installable via npm:

```bash
npm install -g @anthropic-ai/claude-code
```

**Verify:**
```bash
claude --version
```

Claude Code requires an Anthropic API key. Set it in your environment:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Add the export to your shell profile (`~/.bashrc`, `~/.zshrc`, or `~/.profile`) to persist across sessions.

---

## 2. Installing paper-qa (pqa)

paper-qa is the retrieval-augmented question-answering system used for literature search, prior-art checking, and evidence retrieval from local PDFs.

**Install:**
```bash
pip install paper-qa
```

For a specific minimum version (recommended):
```bash
pip install "paper-qa>=4.0"
```

**Verify:**
```bash
pqa --help
```

You should see the pqa command-line help with subcommands including `ask`, `build`, and `index`.

**API key for pqa:**
paper-qa uses an LLM backend. Set your OpenAI API key (or compatible provider):

```bash
export OPENAI_API_KEY="sk-..."
```

If you prefer a different backend, consult the [paper-qa documentation](https://github.com/Future-House/paper-qa) for configuration options.

**Building a literature index:**
Place your PDF papers in a directory (e.g., `papers/`) and build the index:

```bash
pqa build papers/
```

Then query it:
```bash
pqa ask "What methods exist for retrieval-augmented agents in scientific literature analysis?"
```

---

## 3. Installing tectonic

tectonic is a self-contained LaTeX compiler that downloads packages on demand. It is the preferred compiler for the Research OS because it avoids platform-specific TeX distribution issues.

### macOS (Homebrew)

```bash
brew install tectonic
```

### Ubuntu / Debian (apt)

```bash
sudo apt-get install tectonic
```

If tectonic is not in your distribution's package index, use the cargo method below.

### Any Platform (cargo / Rust)

```bash
# Install Rust if not present
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install tectonic
cargo install tectonic
```

### Pre-built Binary

Pre-built binaries for Linux and macOS are available on the [tectonic releases page](https://github.com/tectonic-typesetting/tectonic/releases). Download, extract, and place the binary in a directory on your `PATH`.

**Verify:**
```bash
tectonic --version
```

**Test compilation:**
```bash
echo '\documentclass{article}\begin{document}Hello.\end{document}' > /tmp/test.tex
tectonic /tmp/test.tex
ls /tmp/test.pdf   # should exist
```

---

## 4. Installing the academic-writing-agents Plugin

The `academic-writing-agents` plugin provides Claude Code skills for citation validation, prose rhythm refinement, and paper-qa integration.

**From the `.claude/repos/` directory:**

If you cloned the full template repository, the plugin source is already at `.claude/repos/academic-writing-agents/`. Register it with Claude Code:

```bash
claude plugins install .claude/repos/academic-writing-agents/
```

**From a remote source:**

```bash
claude plugins install https://github.com/your-org/academic-writing-agents
```

**Verify:**
Inside Claude Code, run:
```
/tool-healthcheck
```

The healthcheck output will include a line for `academic-writing-agents` showing `OK` or a specific error.

---

## 5. Verifying the Full Installation

Once all tools are installed, open Claude Code in your project directory and run:

```
/tool-healthcheck
```

Expected output:

```
[OK] claude-code       vX.Y.Z
[OK] pqa               4.x.x
[OK] tectonic          0.x.x
[OK] git               2.x.x
[OK] academic-writing-agents plugin   loaded
```

If any line shows `[FAIL]` or `[NOT FOUND]`, see the Troubleshooting section below.

---

## 6. Setting Up a New Project

The `scripts/new-project.sh` script initializes all required artifact files for a new research project.

**Usage:**
```bash
bash scripts/new-project.sh
```

The script prompts for:
- Project name (used in directory and artifact filenames)
- Working title (written to `research_direction.md`)
- Primary researcher name

It creates:
- `project_state.md` — current stage tracker
- `research_direction.md` — working hypothesis and research question
- `experiment-plan.md` — blank template with required fields
- `evidence_ledger.md` — blank evidence tracking file
- `decision_log.md` — blank decision history
- `results/` — directory for experiment outputs
- `papers/` — directory for PDF literature

After the script completes, open Claude Code:
```bash
claude
```

Then run `/research-status` to confirm Stage 0 is active.

---

## 7. Troubleshooting

### pqa not found

**Symptom:** `command not found: pqa`

**Causes and fixes:**
- pip installed pqa into a Python environment that is not on `PATH`. Activate the correct environment (`conda activate myenv` or `source venv/bin/activate`) and retry.
- The `Scripts/` or `bin/` directory of the Python environment is not on `PATH`. Add it: `export PATH="$HOME/.local/bin:$PATH"`.
- Multiple Python versions are present and the wrong pip was used. Use `python -m pip install paper-qa` and then `python -m pqa --help`.

### tectonic not found

**Symptom:** `command not found: tectonic` or `/tool-healthcheck` reports tectonic FAIL.

**Causes and fixes:**
- Cargo-installed binaries are in `~/.cargo/bin/`. Add to PATH: `export PATH="$HOME/.cargo/bin:$PATH"`.
- Homebrew installed to a non-standard prefix (Apple Silicon Macs use `/opt/homebrew/bin/`). Add: `export PATH="/opt/homebrew/bin:$PATH"`.
- The installation failed silently. Re-run `cargo install tectonic` and check for errors.

**Alternative:** If tectonic cannot be installed, you may use pdflatex with the flag `--compiler=pdflatex` on compile commands. See the [FAQ](faq.md) for details.

### Plugin not loading

**Symptom:** `/tool-healthcheck` reports `academic-writing-agents: NOT FOUND` or skills from the plugin are unavailable.

**Causes and fixes:**
- The plugin was installed in a different Claude Code profile. Run `claude plugins list` to see installed plugins.
- The plugin directory path was wrong during install. Re-run `claude plugins install` with the correct absolute path.
- The plugin has a syntax error. Check `claude plugins validate .claude/repos/academic-writing-agents/` for errors.

### ANTHROPIC_API_KEY not set

**Symptom:** Claude Code starts but immediately errors with `401 Unauthorized` or `API key not found`.

**Fix:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
claude
```

To persist: add the export line to your shell profile and run `source ~/.bashrc` (or equivalent).
