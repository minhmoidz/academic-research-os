# Academic Research OS

An evidence-first research operating system for Claude Code — covering both **literature review workflows** and **AI/ML experiment automation**, from raw idea to camera-ready paper.

> **Core rule:** No claim enters the final draft unless it has a row in `evidence/evidence_matrix.csv` with a traceable source, citation location, and confidence level.

---

## What This Is

Two integrated systems in one repo:

| Mode | Use case | Entry point |
|---|---|---|
| **A — Literature Review OS** | Systematic literature search, screening, evidence extraction, synthesis, draft | `research_protocol.md` → `research_questions/` |
| **B — AI/ML Experiment OS** | Hypothesis testing, proxy experiments, paper writing for empirical ML/AI work | `.claude/research-os/` → `/research-start` in Claude Code |

Both modes share the same anti-hallucination discipline: every claim traces to a source.

---

## Quick Start

```bash
# 1. Clone into your project
git clone https://github.com/minhmoidz/academic-research-os.git /tmp/research-os
cd your-project
bash /tmp/research-os/scripts/new-project.sh .

# 2. Define your research question
cp research_questions/RQ-001-template.md research_questions/RQ-001.md
# Edit RQ-001.md: set your question, scope, success criteria

# 3. Fill project adapter (for AI/ML experiment mode)
nano project_profile.md   # train_command, metric, dataset

# 4. Start working
claude   # Open Claude Code — it reads .claude/CLAUDE.md automatically
```

---

## Workflow Overview (Literature Review Mode)

| Step | What you do | Key file |
|---|---|---|
| 1. Define RQ | Write your research question with scope | `research_questions/RQ-NNN.md` |
| 2. Search | Run queries, log every result | `search/search_log.csv`, `search/query_bank.md` |
| 3. Screen | Apply inclusion/exclusion, score papers | `screening/screening_table.csv` |
| 4. Intake | Read paper, fill note template | `notes/paper_notes/citekey.md` |
| 5. Extract evidence | Pull claims with source + confidence | `evidence/evidence_matrix.csv` |
| 6. Identify contradictions | Compare conflicting claims | `notes/contradiction_notes/` |
| 7. Synthesize | Cluster literature, map arguments, find gaps | `synthesis/` |
| 8. Adversarial review | Challenge your conclusions | `prompts/adversarial_reviewer.md` |
| 9. Write draft | Only from evidence matrix | `outputs/draft.md` |
| 10. Validate & submit | CI/CD checks all citations and claims | `.github/workflows/validate.yml` |

---

## Directory Structure

```
academic-research-os/
│
├── research_protocol.md          ← Workflow rules + anti-hallucination checklist
├── project_profile.md            ← AI/ML project adapter (train command, metric)
│
├── research_questions/           ← One file per research question
│   └── RQ-001-template.md
│
├── search/                       ← Search strategy and logs
│   ├── query_bank.md             ← Query terms + source-specific syntax
│   ├── search_log.csv            ← Every search, logged with result counts
│   └── sources.yaml              ← Database catalog with coverage + syntax
│
├── screening/                    ← Paper selection
│   ├── inclusion_exclusion.md    ← Criteria + quality scoring rubric (0-10)
│   ├── screening_table.csv       ← Decision + score per paper
│   └── prisma_flow.md            ← PRISMA 2020 flow with Mermaid diagram
│
├── library/                      ← Bibliography management
│   ├── references.bib            ← BibTeX (citekey: authorYYYYkeyword)
│   └── papers_manifest.csv       ← Full metadata + local path + note status
│
├── notes/                        ← Structured reading notes
│   ├── paper_notes/              ← One file per paper (citekey.md)
│   │   └── paper_note_template.md
│   ├── concept_notes/            ← Cross-paper concept synthesis
│   │   └── concept_note_template.md
│   └── contradiction_notes/      ← Conflict analysis (CONTR-NNN)
│       └── contradiction_note_template.md
│
├── evidence/                     ← Central claim tracking
│   ├── evidence_matrix.csv       ← claim_id → paper → evidence → confidence
│   └── claim_registry.md         ← Full claim context with cross-references
│
├── synthesis/                    ← Literature synthesis
│   ├── literature_map.md         ← Papers clustered by theme
│   ├── argument_map.md           ← Main thesis + supporting/counter claims
│   └── gaps_and_opportunities.md ← GAP-NNN entries with priority ranking
│
├── outputs/                      ← Final deliverables
│   ├── draft.md                  ← Paper draft (every claim has Evidence comment)
│   └── slides_outline.md         ← Presentation outline with evidence pointers
│
├── prompts/                      ← LLM prompts for research tasks
│   ├── paper_extractor.md        ← Extract structured evidence from one paper
│   ├── adversarial_reviewer.md   ← Challenge your conclusions (7 attack vectors)
│   ├── synthesis_prompt.md       ← Synthesize only from evidence matrix
│   └── claim_checker.md          ← Validate a claim before it enters draft
│
├── scripts/                      ← Automation
│   ├── validate_citations.py     ← Check all citekeys exist in references.bib
│   ├── validate_evidence_matrix.py ← Validate CSV schema + draft alignment
│   ├── check_claims_without_sources.py ← Scan for unsupported claim phrases
│   ├── build_evidence_matrix.py  ← Aggregate claims from paper notes → CSV
│   └── import_zotero_bib.py     ← Merge Zotero export into references.bib
│
├── .github/workflows/
│   └── validate.yml              ← CI: structure + citations + evidence + claims
│
├── .claude/                      ← AI/ML Experiment OS (Mode B)
│   ├── research-os/              ← 34 workflow protocol files
│   └── skills/                   ← 25 invocable Claude Code commands
│
├── templates/                    ← Reusable templates for Mode B
├── examples/                     ← Sample filled-in artifacts
└── docs/                         ← Extended documentation
    └── huong-dan-tieng-viet.md   ← Full guide in Vietnamese
```

---

## CI/CD — What GitHub Actions Validates

Every push and PR runs 5 checks:

| Check | What it validates | Failure means |
|---|---|---|
| `check-structure` | Required files and dirs exist | Missing scaffold files |
| `validate-citations` | All `@citekey` in notes exist in `.bib` | Orphan citation — paper not registered |
| `validate-evidence` | CSV schema, controlled vocab, no duplicates | Matrix has invalid or missing data |
| `check-hallucination` | No "studies show" etc. without claim IDs | Unsupported claim in draft |
| `build-evidence-matrix` | Matrix passes schema validation | CSV corrupted or malformed |

Run locally before pushing:

```bash
python scripts/validate_citations.py
python scripts/validate_evidence_matrix.py
python scripts/check_claims_without_sources.py
python scripts/build_evidence_matrix.py --check
```

---

## Claude Code Commands (Mode B — AI/ML Experiment)

| Command | What it does | When to use |
|---|---|---|
| `/research-start` | Initialize project, register hypothesis | New project |
| `/gap-scout` | Find research gaps from literature | No idea yet |
| `/validate-hypothesis` | Dialectical validation (pros/cons) | Before any experiment |
| `/proxy-run` | Run 25% experiment to test viability | Before full GPU budget |
| `/hypothesis-tournament` | Compare N hypotheses via Successive Halving | Multiple candidates |
| `/experiment-loop` | Full experiment run with logging | After proxy passes |
| `/result-adequacy` | Check results are sufficient to claim | Before writing paper |
| `/paper-draft` | Write paper from evidence | After result-adequacy passes |
| `/research-status` | Show current stage and next action | Every session start |

---

## Key Principles

1. **Evidence-first:** Every claim in the draft has a row in `evidence_matrix.csv`
2. **Traceable:** claim → paper → section/page → confidence level
3. **Reproducible:** all searches logged, all screening decisions logged, all decisions auditable
4. **Anti-hallucination:** CI blocks "studies show" and similar phrases without citations
5. **Honest uncertainty:** confidence levels (high/medium/low) required on all claims

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

## Documentation

- [Vietnamese guide](docs/huong-dan-tieng-viet.md) — complete workflow in Vietnamese
- [Quickstart](docs/quickstart.md)
- [Stage gates](docs/stage-gates.md)
- [Anti-hallucination rules](docs/anti-hallucination.md)
