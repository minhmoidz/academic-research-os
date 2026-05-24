# Evidence Ledger

Last updated: [YYYY-MM-DD]

---

## Purpose

The evidence ledger is the authoritative index linking experiment runs to paper claims.
Every quantitative claim in the paper must have an entry here before it can be written in the draft.

The two-hop evidence chain is:
```
Paper claim → evidence_id → experiment run → log file → raw metric value
```

A paper claim is fully grounded only when this chain is complete and unbroken.

---

## Evidence ID Format

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

## Entry Templates

Copy the appropriate template for each new evidence item. Append below the last entry.

### Experiment Evidence (EV-EXP-N)

```markdown
## EV-EXP-[N]
**Type:** Experiment result
**Experiment ID:** EXP-[N]
**Commit hash:** [full 40-char git commit hash — never abbreviated]
**results.tsv row:** [row number]
**Metric:** [metric_name] = [value]
**Dataset:** [dataset name and setting]
**Log file:** logs/exp-[N].log
**Status in results.tsv:** [PASS | BASELINE]
**Supports claim:** "[exact claim text as it will appear in the paper]"
**Paper location:** [Table X, row "...", column "..." / Section Y, paragraph Z]
**Verified:** [✓ | ✗ — add TODO_RESULT_NEEDED: if ✗]
```

---

### Literature Evidence (EV-LIT-N)

```markdown
## EV-LIT-[N]
**Type:** Literature evidence
**paper-qa query:** "[exact query string used]"
**paper-qa answer:** [paste exact output — do not paraphrase]
**Index used:** [index name] (built [YYYY-MM-DD])
**Supports claim:** "[exact claim text as it will appear in the paper]"
**Paper location:** [section and paragraph]
**Verified:** [✓ | ✗]
```

---

### Dataset Evidence (EV-DATA-N)

```markdown
## EV-DATA-[N]
**Type:** Dataset statistic
**Dataset:** [dataset name]
**Statistic:** [e.g., N = 500 papers, 2 splits]
**Verified by:** [command run, e.g., `wc -l data/dataset.csv` → 500]
**Command run:** [YYYY-MM-DD]
**Supports claim:** "[exact claim text]"
**Paper location:** [Section X.A, Datasets paragraph]
**Verified:** [✓ | ✗]
```

---

## Ledger Rules

1. **One entry per distinct evidence item.** Do not reuse an evidence ID for a different claim.
2. **Experiment evidence requires a results.tsv row.** An `EV-EXP-N` entry is only valid if the experiment ID exists in `results.tsv`, the commit hash matches, and the metric value matches.
3. **Literature evidence requires a paper-qa query.** Record the exact query and exact output.
4. **No paper claim without an evidence ID.** Before writing any quantitative claim, ablation claim, dataset statistic, or novelty claim in the draft, it must have a complete entry here.
5. **Ledger is append-only.** Never delete or overwrite a prior entry.

---

## Entries

(Add entries below, in order of creation. Use `---` as a separator between entries.)
