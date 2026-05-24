# Result Adequacy Gate — Stage 16

## Purpose

The Result Adequacy Gate is the critical checkpoint between experiment completion and paper writing. It is a structured evaluation that determines whether the experimental evidence is sufficient, novel, and stable enough to support the intended paper's claims at the intended venue.

**Claude must not draft any final paper prose — abstract, introduction, contributions, conclusion, or method claims — before this gate passes with Decision A.**

---

## What Is Evaluated at Stage 16

Six conditions are evaluated, in order:

1. **TRC Pass** — Does our result meet every pass condition in the active Target Result Contract?
2. **Prior-Art Beat** — Does our result beat the best known published result on this task?
3. **Stability** — Is the result stable across seeds and folds (low variance)?
4. **Ablation Support** — Do ablation experiments individually confirm each contribution claim?
5. **Novelty Defense** — Is the novelty claim still defensible after prior-art check?
6. **Venue Fit** — Is the target venue still appropriate given the actual result magnitude?

Failing any one condition triggers a specific decision outcome. All six must be addressed before the gate can pass.

---

## Result Adequacy Report (RAR) Template

Save as: `result_adequacy_report.md` in the project root.

```markdown
# Result Adequacy Report

report_id: RAR-001
date: YYYY-MM-DD
evaluator: Claude Research OS — Stage 16

## Paper Context

target_venue: [e.g., MICCAI 2025]
venue_tier: [A* | A | B | Workshop]
paper_type: [empirical | method | system | analysis | survey]
contract_id: TRC-001  # which TRC this evaluates against

## Main Claim Being Evaluated

claim: >
  [Paste the main_claim from the active TRC here verbatim]

## Our Result

our_result:
  metric: AUC
  value: 0.XXX
  std: 0.0XX
  dataset: Dataset-A
  protocol: 5-fold CV, population std (÷5), seed=42
  experiment_id: EXP-NNN  # from results.tsv
  source_file: results/ours/fold_results.csv

## Strongest Baseline Result

strongest_baseline_result:
  value: 0.XXX
  std: 0.0XX
  method: BaselineModel
  protocol: same 5-fold CV as ours
  source: our reproduction, EXP-NNN

## Best Prior Published Result

best_prior_result:
  value: 0.XXX
  method: [method name]
  paper: [paper title — must be real, verified]
  source: [paper-qa query output | user-provided table | DBLP]
  note: TODO_EVIDENCE_NEEDED if not yet verified

## Gap Analysis

gap_over_baseline:
  absolute: +X.Xpp AUC
  relative: +X.X%
  significant: [yes/no — is this above TRC required_gap?]

gap_over_prior:
  absolute: [+X.Xpp | -X.Xpp]
  significant: [yes/no — is this meaningful for the venue?]
  note: If negative, Decision A is blocked regardless of TRC pass.

## Variance and Stability

variance_stability:
  cross_fold_std: 0.0XX AUC
  max_fold_deviation: X.Xpp from mean
  meets_trc_stability: [yes/no — is std < TRC minimum_acceptable_stability?]
  per_fold_results:
    - fold: 1
      auc: 0.XXX
    - fold: 2
      auc: 0.XXX
    - fold: 3
      auc: 0.XXX
    - fold: 4
      auc: 0.XXX
    - fold: 5
      auc: 0.XXX

## Ablation Support

ablation_support:
  - component: AttentionModule module
    ablation_result: [AUC without AttentionModule] = 0.XXX
    contribution: +X.Xpp over backbone
    supports_claim: [yes/no]
    source: EXP-NNN

  - component: CLS module
    ablation_result: [AUC without CLS] = 0.XXX
    contribution: +X.Xpp over backbone
    supports_claim: [yes/no]
    source: EXP-NNN

  - component: ProposedModule module
    ablation_result: [AUC without ProposedModule] = 0.XXX
    contribution: +X.Xpp over backbone
    supports_claim: [yes/no]
    source: EXP-NNN

  - component: LS module
    ablation_result: [AUC without LS] = 0.XXX
    contribution: +X.Xpp over backbone
    supports_claim: [yes/no]
    source: EXP-NNN

  components_confirmed: [N of 4]
  meets_trc_ablation: [yes/no — is N >= TRC required minimum?]

## Robustness Support

robustness_support:
  cross_dataset:
    tcga_esca_auc: 0.XXX
    tcga_lung_auc: 0.XXX
    consistent_trend: [yes/no]
  sensitivity:
    hyperparameter_tested: [name]
    range_tested: [e.g., ±20%]
    auc_range: [min–max across range]
    sensitive: [yes/no]
  meets_trc_robustness: [yes/no]

## Novelty Support

novelty_support:
  prior_art_check_file: prior_art_competition_table.md
  threat_level: [None | Low | Medium | High | Critical]
  closest_prior: [method name + paper]
  differentiation: >
    [One paragraph explaining how our method differs from the closest prior.
     Must reference a specific technical or empirical difference.]
  novelty_defensible: [yes/no]

## Venue Readiness

venue_readiness:
  verdict: [yes/no]
  reason: >
    [Does the magnitude of improvement (gap_over_prior) justify submission to
     the target venue? Consider typical acceptance thresholds for this venue.]

## TRC Pass Evaluation

trc_pass_conditions:
  - condition: "Mean AUC on Dataset-A > [threshold]"
    result: [our AUC value]
    met: [yes/no]
  - condition: "Cross-fold AUC std < 1.0pp"
    result: [our std value]
    met: [yes/no]
  - condition: "AUC gain over BaselineModel >= +0.5pp"
    result: [our gap value]
    met: [yes/no]
  - condition: "At least 3 of 4 ablations positive"
    result: [N of 4 positive]
    met: [yes/no]
  - condition: "Dataset-B non-negative vs BaselineModel"
    result: [our gap on Lung]
    met: [yes/no]
  - condition: "All 5 baselines reproduced"
    result: [list any missing baselines]
    met: [yes/no]

trc_pass: [yes/no — ALL conditions above must be yes]

## Risk Assessment

risk_level: [Low | Medium | High | Critical]

risk_factors:
  - factor: [e.g., "One ablation shows marginal negative (−0.1pp)"]
    severity: [Low | Medium | High]
    mitigation: [e.g., "Report with confidence intervals; reframe as negligible"]

## Decision

decision: [A | B | C | D | E | F | G]
decision_text: [full text of decision — see decision guide below]
rationale: >
  [2–4 sentences explaining why this decision was reached, referencing specific
   numbers from the report above]

## Next Action

next_action: >
  [Specific instruction: which stage to proceed to, or which skill to run]
```

---

## Decision Guide

Each decision has specific trigger conditions, requirements, and consequences.

### Decision A — Proceed to Paper Writing

**Verdict:** Strong enough for target venue. Proceed to Stage 17 (Evidence Freeze).

**Requirements (all must be true):**
- `trc_pass = yes`
- `gap_over_prior` is positive (we beat the best known prior)
- `threat_level` is None, Low, or Medium (novelty defensible)
- All required baselines covered
- Venue tier appropriate to result magnitude
- At least 3 of 4 ablations positive

**What happens next:** Stage 17 Evidence Freeze → Stage 18 Writing

**Claude's action:** Confirm Decision A in `result_adequacy_report.md`, update `project_state.md` to Stage 17, run `/evidence-freeze` if available.

---

### Decision B — Return to Experiments

**Verdict:** TRC pass condition not met, but results are promising. More experiments needed.

**Trigger:** TRC pass = no, but gap_over_prior > 0 and results are close to threshold.

**Requirements before choosing B:**
- Gap to threshold must be ≤ 2.0pp AUC (larger gaps require D or G)
- A specific, bounded additional experiment plan must be written
- New experiment budget must be defined (e.g., "3 more seeds, report all")
- No cherry-picking: all runs under the new plan must be reported

**What happens next:** Return to Stage 14, define new experiments, run at Stage 15, re-evaluate at Stage 16.

**Claude's action:** Write a new experiment plan in `experiment_plan.md`, update `project_state.md`.

---

### Decision C — Differentiate or Pivot (Novelty Threat)

**Verdict:** TRC passed, but prior-art threat is High or Critical.

**Trigger:** `trc_pass = yes` but `threat_level = High or Critical`.

**What this means:** Another paper appears to have addressed the same contribution. The novelty claim as written is not defensible.

**Required actions:**
- Re-read the closest prior paper carefully (not from memory — from paper-qa)
- Identify a genuine technical difference our method has
- Either: reframe the contribution to emphasize the specific difference
- Or: run `/prior-art-check` again with refined queries to find the true gap
- If no genuine difference found after careful analysis: → Decision G

**Forbidden after Decision C:** "first to", "novel", "state-of-the-art" until novelty is re-confirmed.

---

### Decision D — Narrow Scope (Novelty Confirmed, Metric Weak)

**Verdict:** Novelty is defensible but main metric is below TRC minimum.

**Trigger:** `novelty_support.novelty_defensible = yes` but `trc_pass = no` because minimum_acceptable_result not reached.

**What this means:** The contribution is genuine but the performance improvement is too small to support the original claim.

**Options:**
- Option D1: Narrow the claim to a specific setting where the improvement holds (e.g., "only on rare cancers with sparse slides")
- Option D2: Reframe as a stability/robustness contribution if std is lower
- Option D3: Change the primary metric to one where the improvement is clearer, if scientifically justified

**New TRC required** before any of these options is pursued. The new TRC must be created before additional experiments.

**Forbidden after Decision D:** Claims about the original primary metric that don't hold.

---

### Decision E — Negative Result / Analysis Paper

**Verdict:** No positive result on primary metric. Possible analysis contribution.

**Trigger:** `gap_over_prior` is negative, `gap_over_baseline` is negative or negligible.

**Before choosing E, verify:**
- The failure is reproducible (not a bug or preprocessing error)
- The baseline reproduction is correct
- The failure mode is interesting and not trivially explained

**If failure mode is interesting:** Frame as an analysis paper examining why the approach fails and what that reveals about the task.

**If failure mode is trivial:** → Decision G (ABANDON).

**Forbidden after Decision E:** Any performance claim about the method. The paper must be framed as analysis throughout.

---

### Decision F — Venue Downgrade

**Verdict:** Results are real and positive, but not competitive for the target venue. A smaller venue is appropriate.

**Trigger:** `trc_pass = yes` but `gap_over_prior` is positive and small (< +0.5pp on a competitive benchmark) or venue_readiness = no.

**What this means:** The result is publishable but at a lower-tier venue (workshop, domain-specific journal, arXiv).

**Required actions:**
- Update `venue_target.md` with the new venue
- Create new TRC-NNN for the new venue's thresholds
- Proceed to Stage 17 only after new TRC created and confirmed

**Forbidden:** Submitting to the original higher-tier venue with a result that doesn't meet that venue's standards.

---

### Decision G — Pivot Direction

**Verdict:** Fundamental mismatch between method, results, and research question.

**Trigger:** Any of the following:
- `gap_over_prior` is significantly negative (> -2.0pp)
- No ablation shows positive contribution
- Novelty threat is Critical and no differentiation is possible
- Decision E applies but failure mode is not interesting

**What this means:** The research direction needs to change substantially.

**Required actions:**
1. Run `/pivot-decision` to generate pivot options
2. Log a DEC entry in `decision_log.md` with full rationale
3. Mark affected hypotheses REJECTED in `hypothesis_registry.md`
4. Update `research_direction.md` with version bump
5. If pivoting to new direction: create new paper_brief.md and TRC from Stage 1
6. If ABANDONING: log final decision, close project

---

## Hard Rules for Claude at Stage 16

1. **Claude must NOT draft abstract, introduction, or contributions before Decision A is logged.**

2. **Claude must NOT retroactively weaken the TRC to force a pass.** If the user requests this, Claude must refuse and log the request as a DEC entry.

3. **Claude must NOT ignore any required baseline.** If a baseline is missing, the gate cannot pass regardless of other results.

4. **Claude must NOT write "our method outperforms [X]" if `gap_over_prior` is negative for X.**

5. **Claude must NOT report validation set results as if they are test set results.** The RAR must specify which split was used for each number.

6. **If `gap_over_prior` is negative for any baseline included in required_baselines, this must be disclosed in the paper.** It cannot be omitted.

7. **A partial TRC pass is a full TRC fail.** Every pass condition must be met individually.

---

## What Happens if the Gate Fails

If Decision is B, C, D, E, F, or G:

1. Claude runs the appropriate pivot action (see `28_PIVOT_POLICY.md`)
2. Claude logs a DEC entry in `decision_log.md`
3. Claude updates `project_state.md` to the appropriate stage
4. Claude does NOT draft any paper prose
5. Claude waits for user confirmation before taking further action

The gate failure is not a problem — it means the research system is working correctly. The problem is proceeding to write prose on results that don't support the claims.
