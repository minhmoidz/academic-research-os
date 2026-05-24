# SKILL: /archive-paper
## Purpose
Create a complete, self-contained camera-ready archive after paper submission. The archive must be sufficient for: reproducing all results, verifying all claims, auditing all evidence, and recovering the full paper from scratch if original files are lost.

---

## When to Run
- After paper submission (immediately post-submission).
- After a major revision round is submitted.
- As a pre-submission dry-run (produces archive/ but does not finalize it).

---

## Required Inputs
| Input | Source | If Missing |
|-------|--------|------------|
| main.tex | project root | BLOCK — cannot archive without LaTeX source |
| main.pdf | project root | Attempt recompile; BLOCK if compile fails |
| references.bib | project root | BLOCK — bibliography required |
| results.tsv | project root | WARN — archive proceeds but note is added |
| Submission metadata | User provides: venue, date, paper ID | Required for README_ARCHIVE.md |

---

## Steps

### Step 1 — Pre-Archive Verification
Before creating any files, verify:
1. Does `main.pdf` exist and is it current? If not: recompile with tectonic.
   ```bash
   tectonic main.tex
   ```
   If compile fails: BLOCK and report error. Do not archive a broken PDF.
2. Does `results.tsv` exist with at least one CONFIRMATORY PASS row? If not: WARN and note in archive README.
3. Does `evidence_ledger.md` exist? If not: WARN and note.
4. Is git initialized in the project root? Run `git status` to check.

### Step 2 — Create Archive Directory Structure
```bash
ARCHIVE_DIR="archive/submission_[venue]_[YYYYMMDD]"
mkdir -p $ARCHIVE_DIR/figures
mkdir -p $ARCHIVE_DIR/tables
mkdir -p $ARCHIVE_DIR/results
mkdir -p $ARCHIVE_DIR/configs
mkdir -p $ARCHIVE_DIR/review_reports
mkdir -p $ARCHIVE_DIR/evidence
mkdir -p $ARCHIVE_DIR/decisions
```

Never overwrite an existing archive directory. If the target directory exists: append `_v2`, `_v3`, etc.

### Step 3 — Copy Paper Source Files
```bash
cp main.tex $ARCHIVE_DIR/
cp main.pdf $ARCHIVE_DIR/
cp references.bib $ARCHIVE_DIR/
# Copy any supplementary files
cp supplement.tex $ARCHIVE_DIR/ 2>/dev/null || true
cp supplement.pdf $ARCHIVE_DIR/ 2>/dev/null || true
# Copy any style/class files required for compilation
cp *.sty $ARCHIVE_DIR/ 2>/dev/null || true
cp *.cls $ARCHIVE_DIR/ 2>/dev/null || true
```

### Step 4 — Copy Figure Source Files
Copy all figure source files into `archive/figures/`:
- TikZ source files (`.tex` files in a figures/ subdirectory)
- pgfplots data files (`.tsv`, `.csv` used by pgfplots)
- Python/matplotlib scripts (`.py` files that generate figures)
- Raw image files (`.pdf`, `.png`, `.eps`) used in the paper

```bash
# Find and copy all figure sources
find ./figures -type f | while read f; do
  cp "$f" "$ARCHIVE_DIR/figures/"
done
# Also include any standalone figure .tex files
find . -maxdepth 2 -name "fig_*.tex" -exec cp {} "$ARCHIVE_DIR/figures/" \;
```

### Step 5 — Copy Table Source Files
Copy all table source files into `archive/tables/`:
- `.tex` files containing tabular environments
- `.csv`/`.tsv` data files used to populate tables
- Python/pandas scripts that generate table content

```bash
find . -maxdepth 2 \( -name "tab_*.tex" -o -name "table_*.tex" \) \
  -exec cp {} "$ARCHIVE_DIR/tables/" \;
```

### Step 6 — Copy Result Files
Copy result files into `archive/results/` (one level deep — do not recurse into all subdirectories):
```bash
cp results.tsv $ARCHIVE_DIR/results/ 2>/dev/null || true
cp evidence_ledger.md $ARCHIVE_DIR/results/ 2>/dev/null || true
cp claim-evidence-table.md $ARCHIVE_DIR/results/ 2>/dev/null || true
cp result_to_claim_map.md $ARCHIVE_DIR/results/ 2>/dev/null || true
cp best_result.md $ARCHIVE_DIR/results/ 2>/dev/null || true
cp result_adequacy_report.md $ARCHIVE_DIR/results/ 2>/dev/null || true
cp sota_baseline_table.md $ARCHIVE_DIR/results/ 2>/dev/null || true
# Copy model output files (JSON/log files in results/ subdirectory)
find ./results -maxdepth 1 -type f -exec cp {} "$ARCHIVE_DIR/results/" \;
```

### Step 7 — Copy Config Files
Copy all configuration files used for main results:
```bash
find . -maxdepth 2 \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.cfg" -o -name "*.ini" \) \
  ! -path "./.claude/*" \
  -exec cp {} "$ARCHIVE_DIR/configs/" \;
```

### Step 8 — Record Git History
Capture the code state at submission time:
```bash
git log --oneline -20 > "$ARCHIVE_DIR/code_hashes.txt" 2>/dev/null || \
  echo "Git not initialized or no commits" > "$ARCHIVE_DIR/code_hashes.txt"

git log -1 --format="Submission commit: %H%nDate: %ad%nMessage: %s" \
  >> "$ARCHIVE_DIR/code_hashes.txt" 2>/dev/null || true

git diff HEAD > "$ARCHIVE_DIR/uncommitted_changes.diff" 2>/dev/null || true
```

### Step 9 — Copy Review Reports and Decision Documents
```bash
cp target_result_contract.md $ARCHIVE_DIR/decisions/ 2>/dev/null || true
cp decision_log.md $ARCHIVE_DIR/decisions/ 2>/dev/null || true
cp research_direction.md $ARCHIVE_DIR/decisions/ 2>/dev/null || true
cp hypothesis_registry.md $ARCHIVE_DIR/decisions/ 2>/dev/null || true
cp venue_target.md $ARCHIVE_DIR/decisions/ 2>/dev/null || true

# Copy review reports
find . -maxdepth 1 -name "*review*" -o -name "*audit*" | \
  xargs -I{} cp {} "$ARCHIVE_DIR/review_reports/" 2>/dev/null || true
```

### Step 10 — Write archive/README_ARCHIVE.md
Create a human-readable index of the archive:

```markdown
# Archive README

## Paper Metadata
- **Title:** [paper title]
- **Authors:** [author list]
- **Venue:** [venue name]
- **Submission date:** [date]
- **Paper ID:** [if assigned]
- **Revision:** [initial submission / revision 1 / camera-ready]

## How to Reproduce Main Results
1. Checkout commit: `git checkout [commit_hash]`
2. Install dependencies: `[command]`
3. Run: `[command for main result]`
4. Expected output: [metric]=[value] on [dataset]

## Result File to Table Cell Mapping
| Table | Row | Column | Result File | Evidence ID |
|-------|-----|--------|-------------|-------------|
| Table I | Our method | Dataset-A AUC | results/[file] | EVID-EXP-001 |
| Table I | Our method | Dataset-B AUC | results/[file] | EVID-EXP-002 |
[add all rows]

## Config Files Used for Main Results
| Experiment | Config File |
|-----------|-------------|
| Main result | configs/[file] |
| Ablation A | configs/[file] |

## Git Commit at Submission
See `code_hashes.txt` for full log.
Main commit: [hash] — [message]

## Archive Contents
```
archive/
├── main.tex            — LaTeX source
├── main.pdf            — Submitted PDF
├── references.bib      — Bibliography
├── figures/            — All figure sources
├── tables/             — All table sources
├── results/            — Result files and evidence ledger
├── configs/            — Training/eval configs
├── review_reports/     — Internal review reports
├── decisions/          — TRC, decision log, hypothesis registry
├── code_hashes.txt     — Git history at submission
└── README_ARCHIVE.md   — This file
```
```

### Step 11 — Create Zip Archive (if zip available)
```bash
cd $(dirname $ARCHIVE_DIR) && \
  zip -r "$(basename $ARCHIVE_DIR).zip" "$(basename $ARCHIVE_DIR)/" && \
  echo "Archive zip created: $(basename $ARCHIVE_DIR).zip"
```

### Step 12 — Final Verification Checklist
Verify archive completeness:
- [ ] main.tex present and compiles
- [ ] main.pdf present and matches compiled output
- [ ] references.bib present
- [ ] results.tsv present with CONFIRMATORY PASS rows
- [ ] evidence_ledger.md present
- [ ] claim-evidence-table.md present
- [ ] README_ARCHIVE.md has result-to-table mapping filled in
- [ ] git commit hash recorded
- [ ] No .env or credential files included (check: `find $ARCHIVE_DIR -name ".env" -o -name "*.key"`)

Report any missing items to the user before declaring archive complete.

---

## Output Files
- `archive/submission_[venue]_[YYYYMMDD]/` — full archive directory
- `archive/submission_[venue]_[YYYYMMDD].zip` — compressed archive (if zip available)

---

## Safety Rules
1. **Never delete original files when archiving.** The archive is a copy — originals remain in place.
2. **Verify PDF compiles before archiving.** An archive with a broken PDF is not useful for camera-ready submission.
3. **Verify all result files referenced in the paper are present** before declaring the archive complete.
4. **Archive is append-only.** Do not overwrite a previous archive — create a new versioned directory.
5. **Never include credential files, .env files, or API keys** in the archive. Scan and report any found.
6. **README_ARCHIVE.md must have the result-to-table mapping filled in** — a generic or empty mapping defeats the purpose of the archive.
7. **If git is not initialized:** warn prominently; the archive is weakened without commit tracking; recommend initializing git before next submission.
