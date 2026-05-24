# Evidence Ledger

The evidence ledger is the authoritative index linking experiment runs to paper claims. Every quantitative claim in the paper must have an entry here before it can be written in the draft.

---

## Purpose

The claim-evidence table (`claim-evidence-table.md`) links *paper text* to *evidence*.  
The evidence ledger links *evidence* to *experiments*.  

Together they form a two-hop chain:

```
Paper claim → evidence_id → experiment run → log file → raw metric value
```

A paper claim is fully grounded when this chain is complete and unbroken.

---

## Evidence ID Format

Every piece of evidence gets a unique ID:

```
EV-[type]-[N]
```

| Type | Meaning | Example |
|------|---------|---------|
| `EXP` | Result from an experiment run | `EV-EXP-5` |
| `LIT` | Claim verified via paper-qa from literature | `EV-LIT-3` |
| `DATA` | Dataset statistic verified from data files | `EV-DATA-1` |
| `REPO` | Code fact verified from source code inspection | `EV-REPO-2` |

---

## evidence_ledger.md Format

Save as `evidence_ledger.md` in the project root.

```markdown
# Evidence Ledger

Last updated: YYYY-MM-DD

## EV-EXP-1
**Type:** Experiment result
**Experiment ID:** EXP-5
**Commit hash:** [full 40-char hash]
**results.tsv row:** 6
**Metric:** val_auc = 0.9705
**Dataset:** Dataset-A (FeatureExtractor)
**Log file:** logs/exp-5.log
**Status in results.tsv:** PASS
**Supports claim:** "ProposedModule achieves [X.XX%] AUC on Dataset-A"
**Paper location:** Table I, row "Ours (ProposedModule)", column "Dataset-A [Extractor]"
**Verified:** ✓

---

## EV-EXP-2
**Type:** Experiment result
**Experiment ID:** BASELINE
**Commit hash:** [full 40-char hash]
**results.tsv row:** 1
**Metric:** val_auc = 0.9883
**Dataset:** Dataset-A (FeatureExtractor)
**Log file:** logs/baseline.log
**Status in results.tsv:** BASELINE
**Supports claim:** "BaselineModel achieves [X.XX%] AUC on Dataset-A"
**Paper location:** Table I, row "BaselineModel", column "Dataset-A [Extractor]"
**Verified:** ✓

---

## EV-LIT-1
**Type:** Literature evidence
**paper-qa query:** "Does any prior MIL method address norm bias in group selection?"
**paper-qa answer:** [paste exact output]
**Index used:** literature-index (built YYYY-MM-DD)
**Supports claim:** "No prior work addresses the norm bias in CSS-based group selection"
**Paper location:** Introduction, paragraph 2
**Verified:** ✓

---

## EV-DATA-1
**Type:** Dataset statistic
**Dataset:** Dataset-A
**Statistic:** N = [N] samples, [K] classes ([Class1]/[Class2])
**Verified by:** `wc -l data/esca/slide_list.csv` → 152
**Command run:** 2026-05-24
**Supports claim:** "Dataset-A dataset contains [N] samples"
**Paper location:** Section IV.A, Datasets
**Verified:** ✓
```

---

## Ledger Rules

### Rule 1: One entry per distinct evidence item
Do not reuse an evidence ID for a different claim. If two claims come from the same experiment run, they get the same `EV-EXP-N` ID, but each claim entry in `claim-evidence-table.md` references it separately.

### Rule 2: Experiment evidence requires a results.tsv row
An `EV-EXP-N` entry is only valid if:
- The experiment ID (`EXP-N` or `BASELINE`) exists in `results.tsv`
- The commit hash in this entry matches `results.tsv`
- The metric value in this entry matches `results.tsv`
- The log file exists at the stated path

If any condition fails: mark the entry `Verified: ✗` and add `TODO_RESULT_NEEDED:`.

### Rule 3: Literature evidence requires a paper-qa query
An `EV-LIT-N` entry is only valid if:
- The paper-qa query and exact output are recorded
- The indexed library (index name + date) is recorded
- The supporting paper has a verified entry in `references.bib`

If the paper-qa query returns "I don't know" or low confidence: the claim cannot be made.

### Rule 4: No paper claim without an evidence ID
Before writing any of the following in the draft, it must have a complete entry in this ledger:
- Quantitative performance claims (AUC, accuracy, F1, ...)
- Ablation claims (component X contributes Y pp)
- Dataset statistics
- Novelty claims ("no prior work addresses X")
- Statements about prior work behavior

### Rule 5: Ledger is append-only
Never delete or overwrite a ledger entry. If an experiment is discarded (FAIL/CRASH), its evidence entry remains — marked with `Status in results.tsv: FAIL` — and no paper claim may use it.

---

## Ledger vs. Claim-Evidence Table

| Artifact | Answers | Required before |
|----------|---------|-----------------|
| `evidence_ledger.md` | "What experiment produced this number?" | Making the number available for claims |
| `claim-evidence-table.md` | "Which sentence in the paper uses this number?" | Writing that sentence in the draft |
| `results.tsv` | "What was the exact raw metric value and commit?" | Adding to evidence ledger |

The flow is: `results.tsv` → `evidence_ledger.md` → `claim-evidence-table.md` → `paper.tex`

---

## Quick Validation

```bash
# List all evidence IDs in the ledger
grep "^## EV-" evidence_ledger.md

# Check all EV-EXP entries have matching results.tsv rows
grep "^## EV-EXP" evidence_ledger.md | sed 's/## //' | while read evid; do
  expid=$(grep -A2 "^## $evid" evidence_ledger.md | grep "Experiment ID:" | awk '{print $3}')
  grep -q "$expid" results.tsv || echo "MISSING in results.tsv: $expid (from $evid)"
done

# List claims without evidence IDs in the claim-evidence table
grep "TODO_" claim-evidence-table.md
```
