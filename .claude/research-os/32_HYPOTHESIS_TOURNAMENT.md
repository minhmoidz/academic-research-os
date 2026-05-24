# 32 — Hypothesis Tournament Protocol

**Stage:** 11.5 (after Stage 10 Proxy Protocol, before Stage 12 Exploratory Experiments)  
**Trigger:** ≥ 3 APPROVED hypothesis candidates need to be compared efficiently.  
**Output:** Single winning hypothesis, ranked tournament log, updated `hypothesis_registry.md`

---

## 1. When to Use the Hypothesis Tournament

Use this protocol when ALL of the following conditions are met:

- There are **≥ 3 hypothesis candidates** that have passed Dialectical Validation (Stage 8)
- All candidates have `validation_status: APPROVED` in `hypothesis_registry.md`
- The baseline has been run and `baseline_metric` is recorded
- Compute budget is sufficient for at least 2 tournament rounds (estimate using Section 4 below)

Do NOT use this protocol to evaluate a single hypothesis — use the standard proxy → full pipeline instead.

---

## 2. Successive Halving Rounds

The tournament uses **Successive Halving**: each round eliminates the bottom 50% of candidates, concentrating compute on survivors.

### Round 0 — PROXY (all candidates, ideally in parallel)

```
Duration:  proxy_time per candidate (from project_profile.md)
Metric:    primary_metric after proxy run
Config:    same as individual proxy protocol — reduced epochs/steps/data fraction
Fold:      fold-0 only
Seed:      seed from project_profile.md (same for all)
Kill:      bottom 50% by metric; any PROXY_NAN or PROXY_OOM also killed
Survivors: top 50% (minimum 1)
```

### Round 1 — 1-FOLD FULL (survivors only)

```
Duration:  full_run_time × 1 fold
Metric:    primary_metric after fold-0 full run
Fold:      fold-0 (same fold as Round 0)
Seed:      same
Kill:      bottom 50% of survivors
Survivors: top 50%
```

### Round 2 — 3-FOLD (survivors, if >1 remaining after Round 1)

```
Duration:  full_run_time × 3 folds
Metric:    mean primary_metric over folds 0, 1, 2
Folds:     0, 1, 2 (same for all candidates in this round)
Seed:      same
Kill:      bottom 50%
Survivors: top 50% (often just 1)
Skip:      if only 1 candidate survived Round 1, skip directly to Round 3
```

### Round 3 — FULL K-FOLD (winner, confirmatory)

```
Duration:  full_run_time × K folds (K from project_profile.md)
Metric:    mean ± std primary_metric over all K folds
Folds:     all K folds
Seed:      same
→ This is the CONFIRMATORY experiment feeding into Stage 16 Result Adequacy Gate
```

---

## 3. Fair Comparison Rules (Mandatory)

Violation of any rule below **invalidates the tournament round** and requires a re-run.

| Rule | Requirement |
|------|-------------|
| Same fold per round | All candidates in a given round must run on the same fold(s) |
| Same seed | All candidates use the identical random seed throughout |
| Same preprocessing | Data loading, augmentation, normalization must be identical |
| Same eval protocol | Metric computation, threshold, averaging must be identical |
| Config freeze | A candidate's config is frozen at Round 0 and cannot change in later rounds |
| No cherry-picking folds | Cannot assign different folds to different candidates within a round |
| No mid-round kills | Do not kill a candidate before all Round N results are collected |

**If a candidate crashes or returns NaN:** log as `PROXY_NAN` or `RUN_FAIL`, count as the lowest score (not excluded from the count). The candidate is eliminated in the kill step, but the round is not re-run for the failed candidate.

---

## 4. Budget Calculation

Compute total budget before starting. Present to user for approval (Human Checkpoint 2).

```
N   = number of candidates entering Round 0
P   = proxy_time per candidate (from project_profile.md)
F   = full_run_time per fold per candidate (from project_profile.md)
K   = number of folds for full protocol (from project_profile.md)

proxy_budget   = N × P
round1_budget  = ceil(N / 2) × F × 1
round2_budget  = ceil(N / 4) × F × 3     [0 if ceil(N/2) == 1]
full_budget    = 1 × F × K

total_tournament = proxy_budget + round1_budget + round2_budget + full_budget

naive_full_cost  = N × F × K
savings_pct      = (1 - total_tournament / naive_full_cost) × 100
```

**Worked example** (N=8, P=30 min, F=2 h, K=5):

```
proxy:   8 × 30 min          =  4 h
round1:  4 × 2 h × 1 fold   =  8 h
round2:  2 × 2 h × 3 folds  = 12 h
full:    1 × 2 h × 5 folds  = 10 h
TOTAL:                         34 h

Naive (all 8 full):            80 h
Savings:                       57.5 %
```

---

## 5. Tournament Log Format

Append all tournament runs to `results.tsv` using the naming convention below. Do not create a separate file.

```
exp_id                       commit    metric   mem_gb  time_min  status        description
HYP-001-ROUND0-PROXY         abc1234   0.681    4.2     28        PROXY_PASS    tournament round 0, fold-0
HYP-002-ROUND0-PROXY         abc1234   0.612    4.1     27        PROXY_PASS    tournament round 0, fold-0
HYP-003-ROUND0-PROXY         abc1234   0.724    4.3     29        PROXY_PASS    tournament round 0, fold-0
HYP-004-ROUND0-PROXY         abc1234   NaN      —       —         PROXY_NAN     tournament round 0 — OOM at batch 12
HYP-001-ROUND1               def5678   0.701    4.2     118       PASS          tournament round 1, fold-0
HYP-003-ROUND1               def5678   0.739    4.3     120       PASS          tournament round 1, fold-0
HYP-003-ROUND2               ghi9012   0.731    4.3     362       PASS          tournament round 2, folds 0-2 mean
HYP-003-CONFIRMATORY         jkl3456   0.738    4.3     605       PASS          tournament winner, full K-fold
```

After the confirmatory run, add a summary comment in `hypothesis_registry.md`:

```yaml
HYP-003:
  validation_status: CONFIRMED
  tournament_rank: 1
  confirmatory_metric: 0.738 ± 0.011
  tournament_date: YYYY-MM-DD

HYP-001:
  validation_status: TOURNAMENT_ELIMINATED
  tournament_rank: 2
  eliminated_round: 2
  final_metric_at_elimination: 0.701 (round 1)

HYP-002:
  validation_status: TOURNAMENT_ELIMINATED
  tournament_rank: 3
  eliminated_round: 1
  final_metric_at_elimination: 0.612 (round 0)

HYP-004:
  validation_status: TOURNAMENT_ELIMINATED
  tournament_rank: 4
  eliminated_round: 0
  final_metric_at_elimination: NaN (PROXY_NAN)
```

---

## 6. Declaring the Winner

```
Winner = candidate with highest mean primary_metric over full K-fold confirmatory run

If winner metric > baseline_metric:
  → Winner advances to Stage 16 (Result Adequacy Gate)
  → Record in evidence_ledger.md as CONFIRMATORY evidence

If winner metric ≤ baseline_metric (ALL candidates fail to beat baseline):
  → Log: "Tournament winner does not beat baseline."
  → Run /pivot-decision
  → Do NOT draft paper claiming improvements over baseline
```

---

## 7. Forbidden Patterns

The following actions corrupt tournament integrity and are explicitly prohibited:

- **Config modification between rounds** for the same candidate — the config is frozen at Round 0 commit hash.
- **Different folds for different candidates** in the same round — all must share the same fold(s).
- **"Just one more fold"** extension for a losing candidate — strictly follow the halving schedule.
- **Starting Round 1 before all Round 0 results are collected** — comparison requires all results before killing.
- **Retroactive proxy kill adjustment** — once the kill threshold is applied, do not revise it.
- **Running confirmatory on a non-winner** — only the single winner of the halving bracket gets K-fold confirmation.
- **Selectively reporting** only the winner's metrics without logging the full tournament table.

---

## 8. Human Checkpoints

### Human Checkpoint 2 — Budget Approval (before Round 0)

Present:
- Number of candidates entering tournament
- Estimated total budget in hours
- Savings vs naive approach
- Expected timeline

Wait for explicit "y" / "proceed" / "yes" from user before running any experiment.

### Human Checkpoint 3 — Winner Confirmation (after Round 3)

Present:
- Full tournament ranking table
- Winner's confirmatory metric vs baseline
- Delta significance assessment
- Recommendation for next stage

Wait for user confirmation before updating `hypothesis_registry.md` as CONFIRMED and before routing to Stage 16.

---

## 9. Integration with Research OS Stages

```
Stage 10 — Proxy Protocol (individual candidates)
    ↓ [≥3 candidates survive proxy individually]
Stage 11.5 — Hypothesis Tournament (/hypothesis-tournament)
    Round 0: PROXY — all candidates
    Round 1: 1-fold — survivors
    Round 2: 3-fold — survivors (if >1)
    Round 3: K-fold — winner (CONFIRMATORY)
    ↓
Stage 12 — Exploratory Experiments (winner only)
    ↓
Stage 13 — Ablation Study (winner configuration)
    ↓
Stage 16 — Result Adequacy Gate
```

If only 1 or 2 candidates exist after Stage 8 validation, skip the tournament and run each through the standard proxy → full pipeline sequentially.
