# Hypothesis Registry

Project: [project_name]
Last updated: [YYYY-MM-DD]
Total hypotheses: [N]
Supported: [N] | Partially supported: [N] | Contradicted: [N] |
Inconclusive: [N] | Pending: [N] | Testing: [N] | Abandoned: [N]

---

## Core Principle

A hypothesis is a falsifiable prediction written in ignorance of its outcome.
If you already know the result when you write the hypothesis, it is not a hypothesis — it is a description.
Descriptions do not constitute scientific contribution.

**Rule:** The `date_registered` must predate the experiment start date. Claude must not update a hypothesis `status` field until a real logged result in `results.tsv` exists for the testing experiment.

---

## Status Transitions

```
[pending]
    |
    | (experiment started)
    v
[testing]
    |
    +-------> [supported]            — metric exceeds success_criterion
    |
    +-------> [partially_supported]  — metric moves in predicted direction
    |                                  but does not reach success_criterion
    +-------> [contradicted]         — metric moves opposite to prediction
    |                                  or success_criterion definitively not met
    +-------> [inconclusive]         — result is noisy, invalid, or underpowered
```

Transitions are one-way. A `contradicted` hypothesis cannot be moved back to `pending`.

---

## Entry Template

Copy this block and fill it in before running each experiment.

```markdown
## HYP-[NNN]

- **hypothesis_id:** HYP-[NNN]
- **date_registered:** [YYYY-MM-DD]  ← must be BEFORE the experiment starts
- **stage_registered:** [stage number: 2, 4, 8, 12, or 13]
- **hypothesis_text:** >
    If [intervention X] is applied to [model/system Y] under [condition Z], then [outcome metric]
    will [increase/decrease] by at least [delta] compared to [baseline].
- **motivation:** >
    [2-3 sentences explaining why this is expected based on prior work or domain knowledge.
    No result values may be cited here — only reasoning and references to prior work.]
- **expected_observation:** >
    [Metric name] on [dataset] will [increase/decrease] from approximately [baseline value] to
    at least [target value] when comparing [ablated model A] vs [ablated model B].
- **experiment_assigned:** EXP-[N]
- **metric:** [e.g., val_auc, test_accuracy, recall_at_10, ndcg_at_10]
- **success_criterion:** [e.g., "Recall@10 >= 0.75 on Dataset-A (5-fold mean)"]
- **failure_criterion:** [e.g., "Recall@10 < 0.70, or no improvement over baseline in 3/5 folds"]
- **possible_outcomes:**
    - supports: [metric meets success_criterion]
    - partially_supports: [metric improves but does not reach threshold]
    - contradicts: [metric degrades or shows no effect]
    - inconclusive: [high variance, experiment error, or confound found]
- **current_status:** pending
- **evidence:** none yet
- **decision:** none yet
- **next_action:** Run EXP-[N]; do not update status until experiment log entry exists.
```

---

## Registered Hypotheses

(Add hypothesis entries below, in order of registration. Use `---` as a separator.)
