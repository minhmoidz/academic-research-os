# Bounded Experiment Loop

## 1. What It Is

The Bounded Experiment Loop is an automated experiment management pattern adapted from autoresearch-style agent workflows. It allows Claude Code to propose, execute, log, and evaluate a sequence of experimental configurations without requiring manual intervention for each run — while maintaining full reproducibility and preventing the AI agent from modifying protected files or fabricating results.

"Bounded" means the loop operates within pre-defined constraints: a fixed budget of runs, a fixed set of editable files, and a fixed evaluation metric. The loop cannot expand its own scope, extend its own budget, or change the success criterion during execution.

---

## 2. When to Use It vs. Manual Experiments

**Use the experiment loop when:**
- You have more than 3 configurations to compare
- Each configuration requires only code changes within the editable file list
- You want reproducible, logged results without manual record-keeping
- You are running ablations (systematically removing or varying components)

**Use manual experiments when:**
- A configuration requires architectural changes not anticipated in `experiment-plan.md`
- You need to inspect intermediate outputs interactively before deciding on the next run
- The experiment requires external infrastructure (data collection, human annotation) that cannot be scripted
- You are debugging a single failing configuration

**Important:** Even manual experiments must be logged to `results.tsv` in the same format as loop-generated results. The evidence ledger draws from `results.tsv` regardless of how the result was produced.

---

## 3. The experiment-plan.md Setup

Before running the loop, create or update `experiment-plan.md` with the following required fields:

```markdown
# Experiment Plan

## Objective
[One sentence describing what the loop is trying to discover or verify.]
Example: Determine whether adding a re-ranking step to a retrieval-augmented agent
improves citation recall on the ScientificQA benchmark.

## Hypothesis
[Falsifiable prediction with expected direction and estimated effect size.]
Example: Re-ranking retrieved passages by citation count will increase recall@10 by
at least 5 percentage points compared to the baseline retrieval-only agent.

## Editable Files
[List of files the loop is permitted to modify. Only these files may be changed.]
- src/agent/retriever.py
- src/agent/reranker.py
- configs/experiment.yaml

## Protected Files
[List of files the loop must never modify.]
- src/data/dataset_loader.py
- src/eval/evaluator.py
- data/scientificqa_test.json

## Primary Metric
recall@10

## Secondary Metrics
precision@10, MRR

## Budget
Max runs: 12
Max wall time: 4 hours

## Baseline Configuration
configs/baseline.yaml (no re-ranking)

## Evaluation Command
python eval/run_eval.py --config {config_file} --output results/{run_id}/
```

All fields are required. The loop will refuse to start if `experiment-plan.md` is missing any field or if the baseline configuration is not specified.

---

## 4. The Main Loop

Each iteration of the experiment loop follows this fixed sequence:

```
1. HYPOTHESIS
   └── Propose the next configuration to test, based on prior results.
       First iteration always uses the baseline configuration.

2. MODIFY
   └── Edit only files in the Editable Files list.
       Record the diff in results/{run_id}/config_diff.txt.

3. COMMIT
   └── git commit -m "loop: run {run_id} — {one-line description}"
       This ensures every configuration is reproducible via git.

4. RUN
   └── Execute the evaluation command from experiment-plan.md.
       Capture stdout, stderr, and the metric output file.

5. PARSE
   └── Extract the primary metric value from the evaluation output.
       If parsing fails, log run_id as FAILED and do not invent a value.

6. LOG
   └── Append one row to results.tsv (see format below).

7. KEEP / DISCARD
   └── If the run improves over the current best on the primary metric:
       mark as KEEP and update best_config.yaml.
       Otherwise: mark as DISCARD.
       Either way, the result is logged — discarded runs are not deleted.

8. CHECK BUDGET
   └── If runs exhausted or wall time exceeded: exit loop.
       Otherwise: return to step 1 with updated context.
```

**Simplicity criterion:** When two configurations achieve the same primary metric value (within measurement noise), prefer the simpler configuration — the one with fewer changed lines, fewer hyperparameters, or fewer components. This prevents the loop from accumulating unnecessary complexity.

---

## 5. The results.tsv Format

Every run, whether loop-generated or manual, must be appended to `results.tsv` in the following tab-separated format:

```
run_id	timestamp	config_file	primary_metric	primary_value	secondary_metrics	status	notes
```

Example rows:

```
run-001	2024-11-15T14:23:01Z	configs/baseline.yaml	recall@10	0.612	precision@10=0.541,MRR=0.678	KEEP	baseline
run-002	2024-11-15T14:51:17Z	configs/rerank_v1.yaml	recall@10	0.651	precision@10=0.573,MRR=0.701	KEEP	reranker with count threshold=5
run-003	2024-11-15T15:12:44Z	configs/rerank_v2.yaml	recall@10	0.648	precision@10=0.569,MRR=0.698	DISCARD	reranker with count threshold=3; no improvement
run-004	2024-11-15T15:40:09Z	configs/rerank_v3.yaml	recall@10	FAILED	N/A	FAILED	eval crash: KeyError in passage_scorer.py line 87
```

**Rules for results.tsv:**
- Never delete rows — append only
- Never edit a value after it is written (use a new row with a correction note instead)
- FAILED runs must have a non-empty notes field explaining the failure
- All folds must be averaged before writing — do not write per-fold rows to the primary file (keep per-fold data in `results/{run_id}/folds.tsv`)
- Timestamps must be UTC ISO 8601

---

## 6. The Evidence Output

After the loop completes, two evidence artifacts are produced or updated:

### evidence_ledger.md

Each run marked KEEP generates a candidate ledger entry. The loop auto-populates a draft entry; the researcher reviews and approves it before the Evidence Freeze. Format:

```markdown
## EVID-EXP-2

- **Type:** Experimental result
- **Run ID:** run-002
- **Config:** configs/rerank_v1.yaml (diff: results/run-002/config_diff.txt)
- **Dataset:** ScientificQA test split (N=1,200 queries)
- **Metric:** recall@10 = 0.651 ± 0.018 (5-fold)
- **Baseline:** EVID-EXP-1 (recall@10 = 0.612 ± 0.021)
- **Delta:** +0.039 (+6.4%)
- **Status:** APPROVED
- **Supports claims:** C-3, C-5
```

### result_to_claim_map.md

A preliminary mapping from evidence IDs to the claims they support. This becomes `claim-evidence-table.md` after the outline is written. It ensures that no result is "orphaned" (run but never cited) and no claim is "floating" (written but not backed by evidence).

---

## 7. Common Pitfalls

**Pitfall 1: Modifying protected files.**
The loop may propose changes to protected files if Claude has not been given the explicit protected list. Always fill the `Protected Files` section in `experiment-plan.md` before starting. The evaluator, data loader, and test set must always be protected.

**Pitfall 2: Skipping the baseline.**
The first run must always be the baseline configuration. Results are meaningless without a baseline to compare against, and evidence IDs without a baseline entry cannot be entered in the ledger.

**Pitfall 3: Partial fold averaging.**
If a 5-fold experiment crashes on fold 3, the result from folds 1–2 must not be averaged and written to `results.tsv` as a "partial" result. Log the run as FAILED. A partial result is not a valid experimental result.

**Pitfall 4: Treating DISCARD as deleted.**
Discarded runs remain in `results.tsv`. They are evidence that a configuration was tried and did not improve performance. If a reviewer asks "did you try X?", a DISCARD row for X is a complete answer. Deleting DISCARD rows destroys that evidence.

**Pitfall 5: Retroactively changing the primary metric.**
If recall@10 is the primary metric in `experiment-plan.md` but results are stronger on precision@10, do not switch the primary metric without re-running Gate 3 and logging a `/pivot-decision`. Reporting whichever metric looks best post-hoc is outcome bias.

**Pitfall 6: Ignoring the simplicity criterion.**
If two configurations achieve equivalent performance, the loop should prefer the simpler one. Accumulating complexity (more hyperparameters, more components) for no measurable gain makes the method harder to reproduce and harder to explain in the paper.
