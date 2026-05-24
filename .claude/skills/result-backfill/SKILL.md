# SKILL: /result-backfill
## Purpose
Backfill `evidence_ledger.md` and `claim-evidence-table.md` from existing result files when experiments were run outside the formal logging loop (e.g., before this workflow was set up, or by a collaborator). Every claim that enters the paper must be traceable to a specific result file.

---

## When to Run
- When experiments were run before the workflow was initialized and logs are not yet in results.tsv.
- When a collaborator provides result files that need to be integrated into the evidence system.
- Before running /result-adequacy, if evidence_ledger.md is incomplete.
- When the user says "I already have results — help me document them."

---

## Required Inputs
| Input | Source |
|-------|--------|
| Directory containing result files | User provides path |
| List of paper claims to map | User provides (or read from draft sections if they exist) |
| Experiment metadata (dataset, method, config) | User provides or extracted from file names/content |

---

## Steps

### Step 1 — Load Evidence Schema
Read `.claude/research-os/18_EVIDENCE_LEDGER.md` for the evidence ID format, ledger schema, and completeness requirements.

Evidence ID format: `EVID-EXP-NNN` (sequential, zero-padded to 3 digits).
Load existing `evidence_ledger.md` to determine the next available ID (do not reuse IDs).

### Step 2 — Scan Result Directory
List all files in the provided directory:
```bash
find [result_dir] -type f \( -name "*.json" -o -name "*.csv" -o -name "*.tsv" -o -name "*.log" -o -name "*.txt" \) | sort
```

For each file found, record:
- Full absolute path
- File name
- File type (JSON / CSV / TSV / log)
- File size (flag files < 100 bytes as potentially empty/corrupt)

### Step 3 — Extract Metrics from Each File
For each result file:
1. Attempt to parse it and extract metric values.
2. Look for: AUC, Accuracy, F1, loss, per-fold values, mean, std.
3. Record:
   - Which metrics are present
   - Whether per-fold values are available (or only aggregate)
   - Whether the run completed (check for error messages in log files)
   - Which dataset and method the result corresponds to (from file content or filename)

**Completeness check for 5-fold cross-validation:**
- Expect 5 fold values. If fewer: mark as `PARTIAL`.
- If only aggregate (mean/std) is available with no per-fold breakdown: mark as `AGGREGATE_ONLY` and note that variance reporting may be limited.

### Step 4 — Classify Each Run
For each result file, assign a status:
- `PASS` — metrics are present, run completed, value is above baseline.
- `FAIL` — run completed but metrics are below baseline or below TRC threshold.
- `CRASH` — run did not complete (errors in log, missing output files).
- `PARTIAL` — fewer folds than expected; usable for exploratory but not confirmatory.
- `UNKNOWN` — cannot determine status from file content alone; flag for user review.

**Do NOT create EVID entries for CRASH runs.** Log them in results.tsv with status=CRASH but exclude from evidence_ledger.md (failed runs do not constitute evidence).

### Step 5 — Create evidence_ledger.md Entries
For each PASS or AGGREGATE_ONLY result, create one EVID entry:

```markdown
## EVID-EXP-[NNN]

| Field | Value |
|-------|-------|
| Evidence ID | EVID-EXP-[NNN] |
| Run ID | [derived from filename or user-provided] |
| Timestamp | [from file metadata or user-provided] |
| Commit hash | [from git log or UNKNOWN] |
| Experiment type | EXPLORATORY / CONFIRMATORY (as specified by user) |
| Hypothesis | HYP-NNN (or NONE) |
| Dataset | [name] |
| Primary metric | [metric name] |
| Value | [value] |
| Per-fold values | [v1, v2, v3, v4, v5] or AGGREGATE_ONLY |
| Mean | [value] |
| Std | [value] |
| Direction | higher_is_better / lower_is_better |
| Baseline value | [value] or TODO_BASELINE_NEEDED |
| Delta over baseline | [value] or TODO_BASELINE_NEEDED |
| Result file path | [absolute path] |
| Config file path | [absolute path or UNKNOWN] |
| Status | PASS / PARTIAL / AGGREGATE_ONLY |
| Backfill note | Backfilled on [date] — not pre-registered in TRC |
```

### Step 6 — Backfill results.tsv
For each result file processed, add a row to results.tsv:
```
[run_id]\t[timestamp]\t[commit_hash]\t[experiment_type]\t[hypothesis_id]\t[dataset]\t[metric]\t[value]\t[direction]\t[baseline_comparison]\t[status]\t[evidence_id]\tnotes: backfilled from [file_path]
```

If results.tsv does not exist: create it with the header row first.

### Step 7 — Build claim-evidence-table.md
For each paper claim provided by the user:

```markdown
## Claim: [exact claim text]

| Field | Value |
|-------|-------|
| Claim ID | CLM-[N] |
| Claim text | "[exact wording]" |
| Mapped evidence | EVID-EXP-[NNN] |
| Evidence status | PASS / PARTIAL / AGGREGATE_ONLY |
| Sufficient for claim? | YES / PARTIAL / NO |
| Gap | [if NO or PARTIAL: what is missing] |
```

If a claim has no traceable result file: mark it `TODO_RESULT_NEEDED:` — do not draft prose for that claim.

### Step 8 — Generate Backfill Summary Report
```
RESULT BACKFILL SUMMARY
Generated: [date]
Source directory: [path]

Files scanned: [N]
  PASS:    [N] → [N] EVID entries created
  PARTIAL: [N] → [N] EVID entries created (marked PARTIAL)
  CRASH:   [N] → logged in results.tsv only (no EVID)
  UNKNOWN: [N] → flagged for user review

Claims mapped: [N] / [total_claims]
  Fully supported: [N]
  Partially supported: [N]
  TODO_RESULT_NEEDED: [N]

WARNING: Backfilled results were not pre-registered in a TRC.
If used as CONFIRMATORY evidence, they should be clearly noted as
retrospective in the paper (or a new TRC should be created retroactively
and marked RETROSPECTIVE).
```

---

## Output Files
- `evidence_ledger.md` — created or updated
- `claim-evidence-table.md` — created or updated
- `results.tsv` — updated (backfill rows added)

---

## Safety Rules
1. **Never create ledger entries from memory.** Every EVID entry must have an actual file path that exists on disk.
2. **PARTIAL results must be marked PARTIAL** — do not aggregate partial folds as if they were complete.
3. **Do not create EVID entries for CRASH runs.** Failed runs do not constitute evidence.
4. **Backfilled results must be labeled** with the `Backfill note` field — this distinguishes them from pre-registered results.
5. **If a result file is ambiguous** (cannot determine dataset, method, or metric): mark as UNKNOWN, flag for user, and do not create an EVID entry until clarified.
6. **Claims without traceable evidence get TODO_RESULT_NEEDED** — do not fill the gap with an estimate or similar result from a different experiment.
7. **Commit hash is strongly preferred** — if unknown, mark as UNKNOWN but note that reproducibility is weakened.
