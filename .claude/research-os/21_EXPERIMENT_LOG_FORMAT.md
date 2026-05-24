# Experiment Log Format

Standard file formats for all experiment tracking artifacts. All files live in the project root (or a `logs/` subdirectory as noted).

---

## 1. results.tsv

**Path:** `results.tsv`  
**Purpose:** Authoritative record of every experiment run. One row per run.  
**Format:** Tab-separated values, UTF-8, no trailing whitespace.

### Header (required, do not modify)
```
exp_id	commit_hash	metric_value	peak_memory_mb	runtime_s	status	description
```

### Column definitions

| Column | Type | Rules |
|--------|------|-------|
| `exp_id` | string | `BASELINE` for the baseline run; `EXP-N` (N=1,2,3...) for all others |
| `commit_hash` | string | Full 40-char git commit hash. Never abbreviated. |
| `metric_value` | float or `NaN` | Primary metric value. `NaN` for CRASH runs. Never estimated. |
| `peak_memory_mb` | float or `NaN` | Peak GPU/RAM usage in MB. `NaN` if not measurable. |
| `runtime_s` | float | Wall-clock time in seconds for the full run. |
| `status` | string | One of: `BASELINE`, `PASS`, `FAIL`, `CRASH` |
| `description` | string | One-line hypothesis for this experiment. No tabs. |

### Status values

| Status | Meaning |
|--------|---------|
| `BASELINE` | Unmodified code, first run — reference for all comparisons |
| `PASS` | Run completed, metric improved or matched — commit KEPT |
| `FAIL` | Run completed, metric did not improve — commit REVERTED |
| `CRASH` | Run did not complete (exit code ≠ 0, NaN loss, parse failure) — commit REVERTED |

### Example
```
exp_id	commit_hash	metric_value	peak_memory_mb	runtime_s	status	description
BASELINE	a3f2c1d9e8b7a6c5d4e3f2a1b9c8d7e6f5a4b3c2	[X.XXXX]	4821.3	298.4	BASELINE	unmodified [baseline-model] with default config
EXP-1	b4e3d2c1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5	0.8891	4823.1	301.2	PASS	add dropout=0.1 to attention — expected regularization benefit
EXP-2	c5f4e3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6	NaN	NaN	12.3	CRASH	reduce lr to 1e-5 — expected slower convergence; crashed: NaN loss at step 4
EXP-3	d6a5f4e3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7	0.8841	4820.7	299.8	FAIL	increase batch size to 64 — expected faster convergence; metric worse than EXP-1 best
```

### Rules
- Never edit a row after it is written (append-only)
- Never fill `metric_value` from memory or estimation
- The `BASELINE` row must exist before any `EXP-N` row

---

## 2. experiment_notes.md

**Path:** `experiment_notes.md`  
**Purpose:** Human-readable record of the hypothesis and reasoning for each experiment. Written BEFORE the experiment runs.

### Format

```markdown
# Experiment Notes

## BASELINE
**Objective:** Establish reference metric on unmodified code.
**Files changed:** None.
**Expected outcome:** N/A — this is the reference.
**Result:** metric_value=[value] (from results.tsv)

---

## EXP-1
**Date:** YYYY-MM-DD HH:MM
**Hypothesis:** [What change] because [why it might help].
**Files changed:** [file1, file2]
**Key change:** [describe the diff in plain language]
**Expected effect on metric:** [direction and rough magnitude]
**Actual result:** [PASS|FAIL|CRASH] — metric_value=[value]
**Keep/discard reason:** [one sentence]

---
```

### Rules
- The `Hypothesis` line must be written before the run (pre-registration)
- The `Actual result` line is filled after the run
- Do not retroactively rewrite the hypothesis to match the result

---

## 3. failed_runs.md

**Path:** `failed_runs.md`  
**Purpose:** Consolidated record of all FAIL and CRASH experiments with diagnoses.

### Format

```markdown
# Failed Runs

## EXP-[N] — [status: FAIL or CRASH]
**Commit:** [full hash]
**Metric:** [value or NaN]
**Failure reason:** [one sentence — what went wrong]
**Diagnosis:** [root cause, if known]
**Action taken:** reverted via `git revert [hash]`

---
```

### Rules
- Every FAIL and CRASH row in `results.tsv` must have a corresponding entry here
- "Failure reason" must be from log file evidence, not from speculation
- If the root cause is unknown, write "unknown — log at logs/exp-[N].log"

---

## 4. best_result.md

**Path:** `best_result.md`  
**Purpose:** Single-file record of the current best experiment. Updated whenever a PASS experiment beats the previous best.

### Format

```markdown
# Best Result

**As of:** YYYY-MM-DD HH:MM  
**Experiment:** [exp_id]  
**Commit:** [full hash]  
**Metric:** [metric_name] = [value]  
**Delta over baseline:** [+/- value] ([direction])  
**Description:** [hypothesis from experiment_notes.md]  
**Files changed from baseline:**  
- [file1]: [what changed]  
- [file2]: [what changed]  

**Reproducibility:**  
- Seed: [value]  
- Hardware: [GPU model]  
- Runtime: [seconds]  

**Status:** This result IS / IS NOT in experiment_matrix.md (row [N])
```

### Rules
- Only one entry in this file at a time (overwrite on each update)
- The commit hash must exactly match a PASS row in `results.tsv`
- Never write "best result" in the paper without cross-checking this file

---

## 5. result_to_claim_map.md

**Path:** `result_to_claim_map.md`  
**Purpose:** Maps every paper claim to the experiment that produced it. Required before any performance claim enters the draft.

### Format

```markdown
# Result-to-Claim Map

| Claim (as will appear in paper) | Experiment ID | Commit hash | results.tsv row | Verified? |
|--------------------------------|---------------|-------------|-----------------|----------|
| "Our method achieves [X]% on [dataset]" | EXP-5 | [hash] | row 6 | ✓ |
| "Component A contributes [Y] pp improvement" | EXP-7 | [hash] | row 8 | ✓ |
| "[Method] outperforms [baseline] by [Z]%" | BASELINE vs EXP-5 | both hashes | rows 1,6 | ✓ |

## Unmapped claims (resolve before paper writing)
- TODO_RESULT_NEEDED: [claim that needs an experiment]
```

### Rules
- A paper claim may not be written until it has a row in this table
- The "Claim" column must be the exact text that will appear in the paper (no paraphrasing)
- Commit hashes in this table must match `results.tsv` exactly
- Any claim without a row here is a `TODO_RESULT_NEEDED:` until mapped

---

## Log File Convention

**Path:** `logs/exp-[N].log`  
**Purpose:** Full stdout/stderr capture for each experiment run.  
**Retention:** Keep all log files. Never delete — they are the primary evidence.

```bash
# How to create (inside the loop):
python train.py 2>&1 | tee logs/exp-${N}.log
```

The log file is the primary evidence for the metric value in `results.tsv`. If the log is deleted, the result is unverifiable and must be removed from `results.tsv`.

---

## File Relationships

```
experiment_notes.md     ← hypothesis written BEFORE each run
      ↓
[run experiment]
      ↓
logs/exp-N.log          ← raw stdout/stderr from the run
      ↓
results.tsv             ← parsed metric, status, commit hash
      ↓
failed_runs.md          ← diagnosis for FAIL/CRASH rows
best_result.md          ← current best (updated on PASS)
      ↓
result_to_claim_map.md  ← claim ↔ experiment linkage
      ↓
evidence_ledger.md      ← structured evidence IDs for paper writing
      ↓
claim_evidence_table.md ← final paper claim ↔ evidence
```

---

## Validation Commands

```bash
# Count experiments run
wc -l results.tsv

# Check all FAIL/CRASH rows have failed_runs.md entries
grep "FAIL\|CRASH" results.tsv | awk '{print $1}' | while read id; do
  grep -q "$id" failed_runs.md || echo "MISSING from failed_runs.md: $id"
done

# Check no NaN values in PASS rows
grep "PASS" results.tsv | awk -F'\t' '$3 == "NaN" {print "NaN in PASS row:", $0}'

# Check all claim map commits exist in results.tsv
awk -F'|' 'NR>2 {print $3}' result_to_claim_map.md | tr -d ' ' | while read h; do
  grep -q "$h" results.tsv || echo "Hash not in results.tsv: $h"
done
```
