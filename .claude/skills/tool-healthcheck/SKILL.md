# /tool-healthcheck — Tool Availability Verification Skill

## Purpose

Verify that all tools required by the Research OS are actually installed, reachable, and functional before relying on them in a stage-gate workflow. Tools that are missing or broken must be flagged before they cause a mid-stage failure.

This skill tests each tool directly via shell commands. It never assumes a tool is available — it verifies. For native Claude skills that cannot be shell-tested, it marks them as "assumed available (native Claude skill)" and notes this explicitly.

---

## When to Use This Skill

- At the beginning of a new project (`/research-start`)
- After a system update or environment change
- Before Stage 5 (pqa indexing), Stage 15 (experiments), or Stage 18 (LaTeX compilation)
- Whenever a tool fails mid-workflow

---

## Required Steps

Execute all steps in order. Do not stop at the first failure — test all tools and produce a complete report.

### Step 1: Read Tool Reference

Read `.claude/research-os/15_TOOL_HEALTHCHECK.md` to confirm the canonical tool list and expected paths for this environment.

### Step 2: Test Core CLI Tools

Run each of the following commands and record the output (version string or error):

```bash
pqa --help 2>&1 | head -3
tectonic --version 2>&1
git --version 2>&1
python3 --version 2>&1
python3 -c "import torch; print('torch', torch.__version__, 'cuda:', torch.cuda.is_available())" 2>&1
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>&1 | head -5
```

For each command:
- If it returns a version string or help text: mark WORKING
- If it returns "command not found" or error: mark MISSING with the error message

### Step 3: Test paper-qa Specifically

```bash
pqa --version 2>&1
python3 -c "import paperqa; print('paperqa version:', paperqa.__version__)" 2>&1
```

If paper-qa is working, also confirm the index directory:

```bash
ls -la .pqa/ 2>/dev/null || echo "No .pqa index found (OK if not yet indexed)"
```

### Step 4: Test tectonic LaTeX Compiler

```bash
tectonic --version 2>&1
echo '\documentclass{article}\begin{document}test\end{document}' > /tmp/tectonic_test.tex
tectonic /tmp/tectonic_test.tex 2>&1
ls /tmp/tectonic_test.pdf 2>/dev/null && echo "tectonic: PDF compilation OK" || echo "tectonic: PDF compilation FAILED"
rm -f /tmp/tectonic_test.tex /tmp/tectonic_test.pdf
```

### Step 5: Test Git

```bash
git --version 2>&1
git -C . status 2>&1 | head -3
```

### Step 6: Test academic-writing-agents Plugin

Check whether the plugin is accessible by looking for agent definitions:

```bash
ls .claude/repos/academic-writing-agents/agents/ 2>/dev/null || \
  echo "academic-writing-agents: repo not found at .claude/repos/academic-writing-agents/"
```

If the repo is not found locally, check for the plugin through the skills system:

```bash
ls ~/.claude/plugins/ 2>/dev/null | grep -i academic || echo "No academic plugin found in ~/.claude/plugins/"
```

The 12 expected agents are:
- bibliography-auditor
- brainstormer
- consistency-checker
- latex-figure-specialist
- latex-layout-auditor
- logic-reviewer
- paper-crawler
- prose-polisher
- research-analyst
- section-drafter
- technical-reviewer
- writing-reviewer

### Step 7: Check Native Claude Skills

The following are native Claude skills that are invoked as slash commands inside the Claude interface. They cannot be shell-tested. Mark all as "assumed available (native Claude skill)" unless the user reports otherwise:

| Skill | Invocation |
|-------|-----------|
| thesis-figure-skill | Invoked via Skill tool |
| latex-document-skill | Invoked via Skill tool |
| research-paper-writing | Invoked via Skill tool |
| latex-rhythm-refiner | Invoked via Skill tool |
| empirical-paper-writer | Invoked via Skill tool |
| results-backfill | Invoked via Skill tool |
| paper-from-zero | Invoked via Skill tool |
| arxiv-paper-writer | Invoked via Skill tool |
| academic-writing-agents | Invoked via Skill tool |

### Step 8: Check Optional Repo Tools

Check whether optional third-party repositories are installed:

```bash
for repo in academic-writing-skills claude-paper-review AI-research-feedback paper-audit latex-paper-skills; do
  if [ -d ".claude/repos/$repo" ]; then
    echo "FOUND: $repo at .claude/repos/$repo"
  else
    echo "MISSING: $repo"
  fi
done
```

### Step 9: Check Python ML Dependencies

```bash
python3 -c "
import importlib
deps = ['torch', 'numpy', 'sklearn', 'pandas', 'matplotlib', 'timm', 'einops']
for d in deps:
    try:
        m = importlib.import_module(d)
        v = getattr(m, '__version__', 'ok')
        print(f'  ✓ {d}: {v}')
    except ImportError:
        print(f'  ✗ {d}: NOT FOUND')
" 2>&1
```

### Step 10: Generate Report and Optionally Save

Output the full healthcheck report to the console.

Ask the user: "Save this report to `tool_healthcheck_report.md`? (yes/no)"

If yes: save the report to `tool_healthcheck_report.md` in the project root.

---

## Output Format

```
Tool Healthcheck Report
Generated: [YYYY-MM-DD HH:MM]
═══════════════════════════════════════════════════════════

WORKING TOOLS:
───────────────────────────────────────────────────────────
  ✓ pqa (paper-qa): [resolved path]
      Version: X.Y.Z
      Index present: [yes at .pqa/ | no — must run /literature-review to index]

  ✓ tectonic: [resolved path]
      Version: X.Y.Z
      Test compilation: OK

  ✓ git: version 2.34.1
      Repo status: [working tree status]

  ✓ python3: version 3.X.Y
      Location: [which python3 output]

  ✓ PyTorch: version 2.X.Y
      CUDA available: [yes | no]
      GPU: [GPU name or "none"]

  ✓ numpy: version 1.X.Y
  ✓ sklearn: version 1.X.Y
  ✓ pandas: version 2.X.Y
  ✓ matplotlib: version 3.X.Y

  ✓ thesis-figure-skill: assumed available (native Claude skill)
  ✓ latex-document-skill: assumed available (native Claude skill)
  ✓ research-paper-writing: assumed available (native Claude skill)
  ✓ latex-rhythm-refiner: assumed available (native Claude skill)
  ✓ empirical-paper-writer: assumed available (native Claude skill)
  ✓ academic-writing-agents: [N agents detected | assumed available (native Claude skill)]

MISSING OR DEGRADED TOOLS:
───────────────────────────────────────────────────────────
  ✗ nvidia-smi: command not found
      Impact: GPU monitoring unavailable; training can still run if torch.cuda.is_available()

  ✗ academic-writing-skills (repo): not found at .claude/repos/academic-writing-skills/
      Install: git clone https://github.com/bahayonghang/academic-writing-skills.git \
               .claude/repos/academic-writing-skills
      Impact: Review passes 7-9 have reduced coverage; academic-writing-agents plugin is fallback

  ✗ claude-paper-review (repo): not found at .claude/repos/claude-paper-review/
      Install: git clone https://github.com/J0nasW/claude-paper-review.git \
               .claude/repos/claude-paper-review
      Impact: /review-paper may use fallback mode (12-agent plugin)

  ✗ AI-research-feedback (repo): not found at .claude/repos/AI-research-feedback/
      Install: git clone https://github.com/claesbackman/AI-research-feedback.git \
               .claude/repos/AI-research-feedback
      Impact: Structured feedback passes unavailable; use academic-writing-agents as fallback

  ✗ paper-audit (repo): not found at .claude/repos/paper-audit/
      Install: git clone https://github.com/promptcrafted/paper-audit.git \
               .claude/repos/paper-audit
      Impact: Automated paper audit pass unavailable

  ✗ latex-paper-skills (repo): not found at .claude/repos/latex-paper-skills/
      Install: git clone https://github.com/yunshenwuchuxun/latex-paper-skills.git \
               .claude/repos/latex-paper-skills
      Impact: Specialized LaTeX formatting passes unavailable; tectonic + latex-document-skill cover basic needs

OPTIONAL TOOLS:
───────────────────────────────────────────────────────────
  ~ einops: [installed | NOT FOUND — optional for attention visualization]
  ~ timm: [installed | NOT FOUND — optional for pretrained encoders]

WORKFLOW IMPACT SUMMARY:
───────────────────────────────────────────────────────────
  Core workflow (Stages 0–17):   FULLY SUPPORTED
    Required tools: pqa ✓, tectonic ✓, git ✓, python3 ✓, pytorch [status]

  Literature Review (Stage 5):   FULLY SUPPORTED
    paper-qa ✓

  Experiments (Stage 15):        [SUPPORTED | DEGRADED — pytorch missing]
    PyTorch: [status], CUDA: [status]

  LaTeX Compilation (Stage 19):  FULLY SUPPORTED
    tectonic ✓

  Paper Review (Stages 22–24):   PARTIALLY SUPPORTED
    academic-writing-agents ✓ (12 agents)
    Missing: [N] optional review repos — fallback to 12-agent plugin

  Submission Check (Stage 25):   FULLY SUPPORTED (core tools)

RECOMMENDATIONS:
───────────────────────────────────────────────────────────
  1. [Highest priority missing tool] — install before Stage [N]
  2. [Second priority] — optional but recommended for review coverage
  3. [Any degraded tool fix]

═══════════════════════════════════════════════════════════
```

---

## Safety Rules

1. **Never assume a tool works without running the test command.** Even if the tool was working in a previous session, run the test in the current session.

2. **Never mark a tool as WORKING if the test command returns an error.** The test output must be explicitly checked.

3. **Never use a tool marked MISSING in a required stage.** If the tool is required (not optional) for the current stage, the stage cannot proceed until the tool is installed.

4. **Report impact honestly.** If a missing tool means a review pass cannot be run, say so — do not omit the limitation.

5. **Do not install tools automatically.** Provide the install command and let the user install. Some installations may require authentication, sudo, or environment configuration.

6. **For native Claude skills:** Do not attempt to test them via shell commands. Mark as "assumed available" and note that they will fail gracefully if the Skill tool is unavailable.

---

## Fallback Tool Mapping

If a tool is MISSING, use these fallbacks:

| Missing Tool | Fallback | Coverage Gap |
|-------------|---------|-------------|
| academic-writing-skills repo | academic-writing-agents plugin | Minor — same agents, different interface |
| claude-paper-review repo | academic-writing-agents:logic-reviewer + technical-reviewer | Some automated passes unavailable |
| AI-research-feedback repo | academic-writing-agents:writing-reviewer + prose-polisher | Feedback structure less systematic |
| paper-audit repo | academic-writing-agents:consistency-checker + bibliography-auditor | Manual audit required for some checks |
| latex-paper-skills repo | tectonic + latex-document-skill | LaTeX-specific optimizations unavailable |
| nvidia-smi | torch.cuda.is_available() | GPU memory monitoring unavailable |
| einops | manual attention reshape | Visualization scripts need adaptation |

---

## Project-Specific Notes

Update these notes with your own project's tool paths after running /tool-healthcheck
