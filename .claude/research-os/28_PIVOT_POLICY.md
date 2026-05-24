# Pivot Policy — Research Direction Change Protocol

## Core Principle

A pivot is not a failure. It is the research process working correctly.

Experiments are designed to discover what is true about a system. When the truth is different from the original hypothesis, the responsible action is to update the research direction — not to force weak or negative evidence into a positive story.

**Forcing a negative or weak result into a positive story is the failure.** It produces misleading papers, wastes reviewer and reader time, and harms the research community. The Research OS exists to prevent this.

---

## When a Pivot Is Required

A pivot is required when the Result Adequacy Gate (Stage 16) returns any decision other than A. Specifically:

| Gate Decision | Pivot Type Required |
|--------------|-------------------|
| A | No pivot — PROCEED |
| B | RUN_MORE_EXPERIMENTS |
| C | Differentiate or narrow (novelty threat) |
| D | NARROW_CLAIM |
| E | PIVOT_ANALYSIS or ABANDON |
| F | CHANGE_VENUE |
| G | Full direction pivot — ABANDON or restart |

---

## The 9 Allowed Decisions

### 1. PROCEED

**Meaning:** Results are strong, novelty is confirmed, venue is appropriate.

**Trigger conditions:**
- TRC pass = yes (all conditions)
- gap_over_prior > 0 on all claimed datasets
- threat_level = None, Low, or Medium
- Required baselines all covered
- Venue fit confirmed

**Evidence required:**
- Completed RAR with Decision A
- All TRC pass conditions individually verified
- Prior-art competition table shows no Critical threat

**Risks:** None specific to the pivot policy. Standard paper writing risks apply.

**Next action:** Proceed to Stage 17 (Evidence Freeze). Run `/evidence-freeze`.

**Claims forbidden:** None removed by PROCEED — only those already forbidden by TRC fail conditions.

**New TRC needed:** No.

---

### 2. RUN_MORE_EXPERIMENTS

**Meaning:** Results are promising but not yet at the required threshold. A bounded additional experiment set may close the gap.

**Trigger conditions (all required):**
- Gap to TRC threshold ≤ 2.0pp AUC
- Failure is not due to fundamental method weakness (not negative results)
- A specific bounded experiment plan can be written

**Evidence required before choosing this:**
- Identified specific reason why threshold was not reached (e.g., insufficient seeds, data preprocessing issue, suboptimal hyperparameter)
- Written plan for additional experiments with a fixed budget
- Commitment to report ALL runs from the new plan (no cherry-picking)

**Risks:**
- If additional experiments still don't meet threshold, must downgrade to D or G — cannot keep running indefinitely
- Maximum 2 iterations of RUN_MORE_EXPERIMENTS before requiring a different decision

**Next action:**
1. Write new experiment plan in `experiment_plan.md`
2. Log DEC entry: "Decision B: running additional experiments [list] to close gap of [X]pp"
3. Return to Stage 14 (Confirmatory Experiment Planning)
4. Run at Stage 15, re-evaluate at Stage 16

**Claims forbidden:** Any performance claim before new Stage 16 pass.

**New TRC needed:** No — same TRC applies to the additional runs.

---

### 3. NARROW_CLAIM

**Meaning:** Results are only valid in a narrower setting than originally claimed.

**Trigger conditions:**
- Method improves results on a specific subset (e.g., one dataset, one cancer type, one slide type) but not globally
- Main claim as written is too broad for the evidence

**Evidence required before choosing this:**
- Identify the specific setting where improvement holds (with exact AUC values)
- Confirm the setting is still scientifically interesting and publishable
- Confirm the narrowed claim is still falsifiable and testable

**Risks:**
- Narrowed scope may be too narrow for the target venue → may also need CHANGE_VENUE
- Must be honest about what the method does NOT improve

**Next action:**
1. Rewrite `main_claim` in a new TRC (TRC-NNN+1) with narrow scope
2. Log DEC entry with rationale
3. Re-evaluate venue fit
4. If venue still appropriate: return to Stage 16 with new TRC
5. If venue too ambitious: also apply CHANGE_VENUE

**Claims forbidden after NARROW_CLAIM:**
- "generalizes to" any setting outside the confirmed narrow scope
- "robust across datasets" if improvement only on one dataset
- "state-of-the-art" if claim is narrow (typically not SOTA framing)

**New TRC needed:** Yes — new TRC with narrowed main_claim and updated pass conditions.

---

### 4. CHANGE_VENUE

**Meaning:** Results are real and positive but do not meet the bar for the original target venue.

**Trigger conditions:**
- TRC pass = yes but gap_over_prior is positive and smaller than venue expectation
- venue_readiness = no in the RAR
- Results appropriate for a workshop, domain-specific journal, or lower-tier conference

**Evidence required before choosing this:**
- Specific understanding of the target venue's typical accepted result magnitude
- A lower-tier venue that is genuinely appropriate for this work
- Confirmation that the paper's contribution is real (not negative) — just appropriately scoped

**Risks:**
- Venue downgrade may reduce impact visibility
- If the lower venue also rejects, may need to downgrade again or pivot further

**Next action:**
1. Update `venue_target.md` with new venue, tier, and deadline
2. Create new TRC with thresholds appropriate for the new venue
3. Return to Stage 16 with new TRC to confirm pass for the new venue
4. Log DEC entry: "Decision F: venue downgraded from [old] to [new]. Reason: [result magnitude]"

**Claims forbidden:** Claims calibrated to higher-tier standards that are not supported by evidence.

**New TRC needed:** Yes — new TRC with updated venue and appropriate thresholds.

---

### 5. PIVOT_ANALYSIS

**Meaning:** Negative or inconclusive results contain a genuine insight about why the approach fails or what the failure reveals about the task.

**Trigger conditions:**
- gap_over_baseline is negative or negligible
- Failure is reproducible and not a bug
- Failure mode reveals something non-obvious about the task, dataset, or modeling assumption

**Evidence required before choosing this:**
- Identification of the specific failure mode with evidence (not speculation)
- Argument for why the failure mode is interesting to the community
- Preliminary analysis showing the failure is systematic, not random

**Risks:**
- Analysis papers are harder to get accepted without a positive result
- Must be very careful not to overstate the insight
- Reviewers may ask for a method that fixes the problem (requires more experiments)

**Next action:**
1. Write a new paper_brief.md with analysis framing
2. Identify the specific insight claim (what does the failure reveal?)
3. Create new TRC with the analysis claim as the main_claim
4. Plan additional analysis experiments (interpretability, failure cases, etc.)
5. Log DEC entry with rationale

**Claims forbidden after PIVOT_ANALYSIS:**
- Any positive performance claim for the original method
- Framing that implies the method is useful for deployment
- Any comparison that makes the method appear competitive

**New TRC needed:** Yes — completely new TRC for the analysis claim.

---

### 6. PIVOT_ROBUSTNESS

**Meaning:** The method does not improve the primary performance metric but demonstrates meaningfully lower variance (better stability) across folds or seeds.

**Trigger conditions:**
- gap_over_baseline for primary metric is < +0.5pp (below TRC threshold)
- BUT cross-fold std is ≥ [Z%] lower than the best baseline
- Stability difference is consistent across both datasets

**Evidence required before choosing this:**
- Per-fold results for both our method and the strongest baseline
- Statistical evidence that the std reduction is meaningful (not noise)
- Argument for why stability matters in the research context (e.g., Dataset-A slide scarcity)

**Risks:**
- Stability papers are less common in MIL; may face reviewer skepticism
- Must demonstrate the stability improvement is clinically meaningful

**Next action:**
1. Reframe paper around reliability and stability
2. New main_claim: "X reduces cross-fold AUC variance by Y× on Dataset-A, improving deployment reliability in low-resource settings"
3. Create new TRC with stability thresholds
4. Plan additional robustness experiments (out-of-distribution slides, edge cases)

**Claims forbidden after PIVOT_ROBUSTNESS:**
- "improves AUC by X" (if that improvement is below TRC threshold)
- "state-of-the-art performance" (performance pivot is not SOTA framing)

**New TRC needed:** Yes — new TRC with stability-focused main_claim and std-based pass conditions.

---

### 7. PIVOT_BENCHMARK

**Meaning:** The experiments reveal significant gaps or problems in existing benchmark datasets or protocols that are themselves worth reporting.

**Trigger conditions:**
- Experiments reveal that baseline reproducibility under identical protocol produces substantially different results than published numbers
- Dataset has quality issues (label noise, slide quality variation) that explain conflicting results
- Evaluation protocol inconsistencies explain why prior methods appear stronger in papers than in reproduction

**Evidence required before choosing this:**
- Quantitative evidence of the benchmark gap (our reproduction vs. published numbers for at least 3 baselines)
- Specific protocol differences identified (not just "results differ")
- At least one proposed fix or recommendation

**Risks:**
- Benchmark papers require contacting original authors for clarification (should be done before submission)
- May be seen as indirect criticism; must be framed constructively

**Next action:**
1. Systematically reproduce all required baselines under identical protocol
2. Document deviations between reproduction and published numbers
3. Create a benchmark analysis paper framing
4. New main_claim focuses on the protocol analysis, not method performance

**Claims forbidden after PIVOT_BENCHMARK:**
- Claims about the proposed method's performance (it becomes context, not contribution)
- Accusations of misconduct — only factual documentation of differences

**New TRC needed:** Yes — benchmark-focused TRC.

---

### 8. PIVOT_SYSTEM

**Meaning:** The method works well in practical deployment but does not achieve SOTA on standard benchmarks.

**Trigger conditions:**
- Strong practical results (speed, memory, ease of integration) even if primary metric is below threshold
- Method has clear engineering advantages that benchmark metrics don't capture
- Target application has specific constraints (e.g., real-time inference, edge deployment) that the method addresses

**Evidence required before choosing this:**
- Concrete practical advantage measured (e.g., inference time, GPU memory, FLOPs)
- Real use-case framing (who would use this and why)
- At least one benchmark where the speed/efficiency advantage is demonstrated quantitatively

**Risks:**
- System papers are typically published in different venues (systems conferences, applied ML workshops)
- Must be honest that the method is not SOTA on standard metrics

**Next action:**
1. Identify appropriate system/application venue
2. New main_claim focuses on practical advantages with honest performance context
3. Add engineering experiments (benchmark inference time, memory, integration tests)
4. Create new TRC for system framing

**Claims forbidden after PIVOT_SYSTEM:**
- "state-of-the-art" on standard benchmarks
- Performance comparisons that omit the baselines the method loses to

**New TRC needed:** Yes — system-focused TRC with practical metric thresholds.

---

### 9. ABANDON

**Meaning:** Results are weak, no interesting insight emerges, and no defensible pivot is available.

**Trigger conditions (any):**
- gap_over_prior is significantly negative (> -2.0pp) with no redeeming finding
- No ablation shows positive contribution
- PIVOT_ANALYSIS: failure mode is trivial or well-known
- PIVOT_ROBUSTNESS: std improvement is negligible
- Two iterations of RUN_MORE_EXPERIMENTS failed to improve results

**Evidence required before choosing ABANDON:**
- Honest assessment that no pivot produces a genuine publishable contribution
- All ablation variants tested
- At least one alternative baseline tried

**Next action:**
1. Log final DEC entry: "Decision 9 — ABANDON. Reason: [specific reason]. Date: [date]."
2. Mark all hypotheses as REJECTED in `hypothesis_registry.md`
3. Archive the experiment logs and results (do not delete — data may be useful later)
4. Update `project_state.md` to CLOSED
5. Do not write any paper draft

**What ABANDON is not:**
- It is not a judgment on the researcher's ability
- It is not permanent — the approach may work with a different dataset, different backbone, or different framing
- It is not a reason to write a paper anyway — that would violate the core principle

---

## Forbidden Pivots — What Claude Must Never Do

These are the actions Claude is strictly prohibited from performing regardless of user request:

### Forbidden Pivot 1: Metric Redefinition
**What it is:** Silently switching to a different metric after seeing that the original metric doesn't show improvement.
**Example:** Original TRC requires AUC improvement. After seeing AUC is flat, reporting Accuracy instead without updating the TRC.
**Why forbidden:** This is post-hoc metric selection — a form of p-hacking.
**Correct action:** If Accuracy is genuinely a better metric, create a new TRC at Stage 14 before running new experiments.

### Forbidden Pivot 2: Cherry-Picking Runs
**What it is:** Running 20 experiments and reporting only the 3 that worked.
**Example:** Running 5 different hyperparameter settings and reporting the best one as "our result."
**Why forbidden:** The reported result does not represent the method's typical behavior.
**Correct action:** Report all runs. If hyperparameter sensitivity is high, report the sensitivity analysis. Mean and std must include all runs.

### Forbidden Pivot 3: "Competitive" Framing for Worse Results
**What it is:** Writing "our method is competitive with X" when our method is actually worse than X.
**Example:** Method achieves [X.XXX] AUC; best baseline achieves 0.922 AUC. Writing "comparable performance."
**Why forbidden:** "Competitive" implies parity. Using it to describe worse results is misleading.
**Correct action:** Report the gap honestly. If the method has other advantages (speed, interpretability), report those as separate contributions with their own evidence.

### Forbidden Pivot 4: Dropping Losing Baselines
**What it is:** Removing a baseline from the comparison table because it beats the proposed method.
**Example:** BaselineModel achieves higher AUC than ours. We remove BaselineModel from Table I.
**Why forbidden:** Baselines required by the TRC must appear in the paper. Dropping them hides unfavorable results.
**Correct action:** Report all required baselines. If the method loses to one baseline, acknowledge it and analyze why.

### Forbidden Pivot 5: Test/Validation Set Confusion
**What it is:** Reporting validation set results as if they are held-out test set results.
**Example:** In 5-fold CV, selecting the fold with the best validation AUC and reporting it as "our result."
**Why forbidden:** This inflates apparent performance and does not generalize.
**Correct action:** Report the mean across all 5 folds. Per-fold results must be in the supplementary or appendix.

---

## Pivot Execution Protocol

When a pivot is required, follow these steps exactly:

```
Step 1: Run /result-adequacy
        → Classifies outcome (Decision A–G)
        → Generates result_adequacy_report.md

Step 2: Run /pivot-decision (if Decision != A)
        → Generates pivot options with evidence requirements
        → User selects pivot type

Step 3: Log decision in decision_log.md
        Format: DEC-NNN: [date] [decision type] [reason] [what changes]

Step 4: Update hypothesis_registry.md
        → Mark affected hypotheses as REJECTED, NARROWED, or REDIRECTED
        → Note which evidence led to the change

Step 5: Update research_direction.md
        → Version bump (v1.0 → v1.1 for narrow pivots, v2.0 for major pivots)
        → Record new direction with rationale

Step 6: Update venue_target.md (if venue changes)
        → New venue name, tier, deadline
        → Reason for change

Step 7: Create new target_result_contract.md (if pivot changes claims)
        → New contract_id (TRC-NNN+1)
        → Mark old TRC as SUPERSEDED
        → Link to DEC entry

Step 8: Update project_state.md
        → Current stage, last action, next step, decision history

Step 9a: If PROCEED → move to Stage 17 (Evidence Freeze)
Step 9b: If more experiments → return to Stage 14 (Confirmatory Planning)
Step 9c: If analysis/robustness/benchmark/system pivot → return to Stage 8 (Problem Reformulation)
Step 9d: If ABANDON → close project, archive results
```

---

## Decision Log Format

Every pivot decision must be logged as a DEC entry in `decision_log.md`:

```markdown
## DEC-001
date: YYYY-MM-DD
decision_type: [NARROW_CLAIM | RUN_MORE_EXPERIMENTS | CHANGE_VENUE | PIVOT_ANALYSIS | PIVOT_ROBUSTNESS | PIVOT_BENCHMARK | PIVOT_SYSTEM | ABANDON]
triggered_by: RAR-001 (Stage 16 gate failure)
old_trc: TRC-001 (now SUPERSEDED)
new_trc: TRC-002 (if applicable)
old_main_claim: "[paste old claim]"
new_main_claim: "[paste new claim, or NONE if abandoning]"
reason: >
  [Specific numeric reason. E.g.: "Mean AUC on Dataset-A was [X.XXX], which is
   below the TRC threshold of >[threshold]. Gap over BaselineModel was +[Ypp], below the
   required +0.5pp. No ablation component individually exceeded +0.4pp. The
   method shows consistently lower cross-fold std ([Ypp] vs [Ypp] for BaselineModel),
   which warrants a PIVOT_ROBUSTNESS framing."]
experiments_already_run: [list EXP-NNN IDs]
claims_now_forbidden: [list specific phrases forbidden after this decision]
```

---

## Reference: Case Studies

### Case 1 — Strong Result, Proceed

**Situation:** ProposedModule module achieves [X.XXX] AUC on Dataset-A (std [Ypp]), beating BaselineModel by +[Ypp]. All 4 ablations positive. Prior-art threat = Low.

**Decision:** PROCEED.

**Requirements met:** TRC pass (AUC > [threshold], std < 1.0pp, gap > +0.5pp), novelty confirmed, venue fit confirmed.

**Claims allowed:** "The proposed method achieves [X.XXX] AUC on Dataset-A, exceeding BaselineModel by [Ypp] under 5-fold cross-validation."

---

### Case 2 — Prior Art Already Did It

**Situation:** After running experiments, prior-art check reveals a 2024 paper used the same hypergraph regularization idea on the same dataset with similar results.

**Decision:** NARROW_CLAIM or PIVOT_ANALYSIS.

**Required actions:** Read the prior paper carefully via paper-qa. Identify specific technical differences. If genuine difference exists, narrow the contribution to what is new. If no genuine difference, pivot to analysis of when hypergraph regularization helps vs. hurts.

**Claims forbidden:** "first to use hypergraph regularization for MIL", "novel approach", "state-of-the-art" on the task where prior art matched.

---

### Case 3 — Accuracy Flat, Variance Lower

**Situation:** Our method achieves [X.XXX] AUC (std [Ypp]). BaselineModel achieves [X.XXX] AUC (std [Ypp]). AUC improvement is negative, but variance is [Z%] lower.

**Decision:** PIVOT_ROBUSTNESS.

**New main_claim:** "The proposed method reduces cross-fold AUC variance by [Z%] compared to BaselineModel on Dataset-A ([Ypp] vs [Ypp] std), improving reliability for deployment."

**Claims forbidden:** "improves AUC", "outperforms BaselineModel on primary metric".

**New TRC needed:** Yes. TRC-002 with main_claim = stability, pass condition = "cross-fold std ≤ [Ypp] AND std reduction ≥ [Z%] vs. BaselineModel."

---

### Case 4 — Only Works on One Dataset

**Situation:** Our method achieves +[Ypp] AUC on Dataset-A but -[Ypp] on Dataset-B.

**Decision:** NARROW_CLAIM.

**New main_claim:** "The proposed method improves AUC by [Ypp] on Dataset-A under 5-fold CV. Results on Dataset-B do not show improvement, suggesting the method is most effective for small, niche datasets."

**Claims forbidden:** "generalizes across domains", "robust across datasets", "outperforms on both GenericBenchmark datasets."

---

### Case 5 — Method Slower but More Interpretable

**Situation:** Our method matches BaselineModel on AUC but is 2× slower. However, attention maps align better with expert annotations.

**Decision:** PIVOT_SYSTEM or CHANGE_VENUE.

**New framing:** "The proposed method matches BaselineModel performance with improved interpretability (attention-annotation alignment: +15% IoU) at the cost of 2× inference time. We analyze the accuracy-interpretability tradeoff for deployment."

**Claims forbidden:** "state-of-the-art", "efficient", "faster than baselines".

---

### Case 6 — Completely Negative Result

**Situation:** Our method achieves -[Ypp] AUC vs. BaselineModel on Dataset-A and -[Ypp] on Dataset-B. All ablation variants also negative. No clear failure mode insight.

**Decision:** ABANDON.

**Next action:** Log DEC-NNN. Archive results. Close project. Do not write a paper. Do not try to spin the negative result.

**What not to do:** Write "our exploration shows that hypergraph regularization is not suitable, which is itself a contribution." This framing requires genuine insight, not just negative numbers.
