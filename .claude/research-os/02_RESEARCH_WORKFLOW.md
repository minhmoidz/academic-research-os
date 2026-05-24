# Master Stage-Gate Research Workflow

26 stages. Every stage must pass its gate before advancing. No shortcuts.

**Core principle:** Experiments are used to discover what is true, not to force the initial idea to be true. If evidence contradicts the hypothesis, Claude must update the research direction — not the evidence.

---

## Global Hard Gates

These rules apply regardless of stage:

| Forbidden action | Required gate before allowed |
|-----------------|------------------------------|
| Write **final paper prose** (Abstract, Introduction, Related Work, Method, Experiments, Conclusion, Limitations) | Stage 17 (Evidence Freeze) passes |
| Write Related Work from memory | Never — always requires paper-qa or verified source |
| Claim novelty ("first", "novel") | Stage 6 (Prior-Art Check) passes |
| Claim performance ("outperforms") | Stage 16 (Result Adequacy Gate) passes |
| Target a high-rank venue | Stage 9 (Target Result Contract) defined |
| Proceed to next stage | All required artifacts for current stage exist |
| No experiment (proxy or full) without APPROVED hypothesis | Stage 1.5 (Dialectical Validation) passes |
| No full run without proxy | Stage 11.5 (Proxy Protocol) PROXY_PASS status |

**Before Stage 17, Claude MAY write** (these are not "final paper prose"):
- Research notes, hypothesis notes, literature notes
- Experiment interpretation and diagnostic summaries
- TODO-based skeleton outlines (`## Section Name\n% TODO: ...`)
- Rough bullet-point outlines for planning
- Evidence ledger entries, experiment notes, decision log entries
- All artifacts listed in Stages 0-17 (templates, matrices, checklists, etc.)

The prohibition is on **final prose** (complete sentences written as if for a submission). A sentence like "Our method achieves 98.8% AUC, outperforming all baselines" is final prose — forbidden before Stage 17. A note like "TODO: write performance summary here — results are in results.tsv row EXP-12" is a research note — allowed at any stage.

**If evidence is missing:** `TODO_EVIDENCE_NEEDED:`  
**If result is missing:** `TODO_RESULT_NEEDED:`  
**If citation is missing:** `TODO_CITATION_NEEDED:`  
**If novelty uncertain:** `TODO_NOVELTY_CHECK_NEEDED:`  
**If venue fit uncertain:** `TODO_VENUE_FIT_NEEDED:`

---

## Stage 0 — System Readiness

**Goal:** Verify tools, load workflow state, and confirm which stage to resume.

**Required inputs:** Project directory

**Required outputs:**
- Tool healthcheck report (from `/tool-healthcheck`)
- `project_state.md` read or initialized
- Current stage confirmed
- Next safe action stated

**Skills/tools:**
- `/tool-healthcheck` skill → `15_TOOL_HEALTHCHECK.md`
- `/research-status` skill → reads `project_state.md`
- `12_SESSION_PROTOCOL.md`

**Pass criteria:**
- pqa available or marked as optional for this project
- LaTeX compiler confirmed (tectonic at `/opt/anaconda3/bin/tectonic`)
- academic-writing-agents plugin confirmed
- `project_state.md` exists or is created fresh

**Fail conditions:**
- Critical tools missing for the current stage (e.g., pqa missing at Stage 5)
- `project_state.md` in inconsistent state

**Forbidden:**
- Skipping healthcheck
- Assuming tools work without testing
- Starting to write prose during readiness check

**Next allowed stage:** Stage 1 (if new project) or resume from `project_state.md` current stage

---

## Stage 0.5 — Gap Scout *(Optional — skip if user has a clear idea)*

**Goal:** Autonomously discover research gaps from literature and propose hypothesis candidates when the user has no direction.

**When to use:** User has domain knowledge and access to PDFs but no specific idea. Or user wants Claude to find novel directions from the existing literature corpus.

**Required inputs:** paper-qa index on domain literature

**Required outputs:**
- `gap_scout_report.md` with ≥ 3 ranked candidates
- Top 3 candidates presented to user
- User selection logged (Human Checkpoint 1)
- Selected hypothesis registered as HYP-001 in `hypothesis_registry.md`

**Skills/tools:**
- `/gap-scout` skill → `29_GAP_SCOUT_PROTOCOL.md`
- paper-qa (pqa) for literature queries

**Pass criteria:**
- ≥ 3 gaps identified with pqa evidence
- All candidates have priority_score computed
- User has selected a direction
- Selected hypothesis registered in hypothesis_registry.md

**Fail conditions:**
- pqa index empty or unavailable → add PDFs first
- All identified gaps have high prior-art threat → run `/prior-art-check` before proceeding

**Forbidden:**
- Proposing gaps without pqa evidence
- Registering hypotheses without user confirmation
- Proceeding past this stage without user selection

**Next allowed stage:** Stage 1 (Idea Intake, with the selected direction as input)

---

## Stage 1 — Idea Intake

**Goal:** Convert a raw research idea into a structured paper brief with a falsifiable claim.

**Required inputs:** User's raw idea description

**Required outputs:**
- `paper_brief.md` (from Template 1 in `10_TEMPLATES.md`)
  - Problem statement (2-3 sentences)
  - Proposed approach (2-3 sentences)
  - Primary falsifiable claim
  - Target dataset(s) — tentative
  - Target baselines — tentative
  - Primary metric — tentative
- `project_state.md` initialized at Stage 1
- 8 idea clarification questions asked and answered (`03_IDEA_TO_PAPER_PLAYBOOK.md`)

**Skills/tools:**
- `/research-start` skill
- `03_IDEA_TO_PAPER_PLAYBOOK.md`

**Pass criteria:**
- Primary claim is falsifiable (testable with a specific metric)
- At least one real dataset is named (not invented)
- Problem is distinguishable from "we apply method X to task Y"

**Fail conditions:**
- Claim is unfalsifiable ("improves AI")
- No concrete task identified
- User cannot specify what experiment would disprove the idea

**Forbidden:**
- Writing Abstract or Introduction
- Inventing citations
- Claiming novelty before Stage 6
- Creating LaTeX files

**Next allowed stage:** Stage 2

---

## Stage 1.5 — Dialectical Validation *(Required before any experiment)*

**Goal:** Validate every hypothesis with a constructive argument + independent adversarial critique before committing compute.

**Hard rule:** No experiment (proxy or full) may run until the hypothesis has validation_status = APPROVED.

**Required inputs:**
- HYP-NNN entry in hypothesis_registry.md (status = pending)
- project_profile.md (for paradigm context)
- paper-qa index (for literature evidence)

**Required outputs:**
- `dialectical_validation.md` with full 3-step record
- hypothesis_registry.md updated: `dialectical_score`, `validation_status`

**Skills/tools:**
- `/validate-hypothesis` skill → `30_DIALECTICAL_VALIDATION.md`
- `academic-writing-agents:brainstormer` (constructive phase)
- `academic-writing-agents:research-analyst` (adversarial phase — run independently)

**Pass criteria:**
- aggregate_score ≥ 6/10
- fatal_flaw = NO
- validation_status = APPROVED in hypothesis_registry.md

**Fail conditions:**
- score < 6 → validation_status = REJECTED or REVISE
- fatal_flaw detected → must resolve before any experiment

**Forbidden:**
- Running constructive and adversarial in same subagent call
- Skipping literature search in constructive phase
- Approving hypothesis with fatal_flaw = YES
- Running experiments before this stage passes

**Next allowed stage:** Stage 2 (Research Direction Lock, if APPROVED) or hypothesis revision

---

## Stage 2 — Problem Formulation

**Goal:** Define the research question, hypothesis, and contribution candidates with precision.

**Required inputs:** `paper_brief.md`

**Required outputs:**
- `hypothesis_registry.md` initialized with HYP-001 (primary hypothesis)
  - Format: "If [mechanism] then [observation] on [task/dataset] compared to [baseline]"
- Research question: "Does [X] improve [metric] over [baseline] on [dataset]?"
- Null hypothesis H0 and alternative H1
- Minimum meaningful delta (set before experiments)
- Risk-of-overclaiming checklist completed

**Skills/tools:**
- `03_IDEA_TO_PAPER_PLAYBOOK.md`
- `22_HYPOTHESIS_REGISTRY.md`

**Pass criteria:**
- Hypothesis is falsifiable with a specific experiment
- Minimum delta is defined (e.g., ">0.5% AUC")
- At least one failure mode acknowledged

**Fail conditions:**
- Hypothesis is "our method is better" (not falsifiable)
- No minimum delta defined
- Contribution candidates listed as proven facts

**Forbidden:**
- Stating contributions as proven facts
- Skipping overclaiming risk checklist
- Writing Introduction prose

**Next allowed stage:** Stage 3

---

## Stage 3 — Venue Targeting

**Goal:** Select a target venue, define the evidence requirements that venue demands, and create a `venue_target.md`.

**Required inputs:** `paper_brief.md`, `hypothesis_registry.md`

**Required outputs:**
- `venue_target.md` with: venue name, tier (1-6), deadline, page limit, blind review status
- Venue-specific evidence requirements (novelty, baselines, datasets, ablations, metric rigor)
- `minimum_acceptable_result` field filled (tentative, confirmed at Stage 9)
- Decision logged in `decision_log.md` (DEC-001)

**Skills/tools:**
- `/venue-target` skill
- `24_VENUE_TARGETING.md`

**Pass criteria:**
- Venue is realistic given current idea and likely results
- Minimum evidence requirements are listed
- The user has confirmed the venue choice

**Fail conditions:**
- Targeting Tier-1 venue without any evidence
- Not defining minimum acceptable result for the chosen venue

**Forbidden:**
- Assuming a top-tier venue before seeing results
- Not documenting the venue choice in `decision_log.md`

**Next allowed stage:** Stage 4

---

## Stage 4 — Initial Feasibility Check

**Goal:** Assess whether the idea is computationally and technically feasible before committing to literature work.

**Required inputs:** `paper_brief.md`, `venue_target.md`

**Required outputs:**
- Feasibility assessment covering:
  - Dataset availability and access
  - Baseline reproducibility
  - Compute requirements
  - Implementation complexity
  - Timeline vs. venue deadline
- Go/No-Go recommendation
- If No-Go: specific blocking issues

**Skills/tools:**
- `/tool-healthcheck` for compute check
- Manual assessment by user + Claude

**Pass criteria:**
- Dataset accessible or obtainable within timeline
- At least one baseline runnable
- Compute available for required experiments

**Fail conditions:**
- Dataset inaccessible (behind paywall, requires special permission not obtained)
- No baseline is runnable within resource constraints
- Timeline is impossible for target venue

**Forbidden:**
- Continuing to Stage 5 with an inaccessible dataset
- Assuming compute availability without checking

**Next allowed stage:** Stage 5 (if Go) or back to Stage 1 (if No-Go: revise idea)

---

## Stage 5 — Literature Grounding

**Goal:** Find and index all relevant papers. Build a verified paper list. Do NOT write Related Work yet.

**Required inputs:** Research question, keywords (3-8 terms), PDF folder (if available)

**Required outputs:**
- `literature_list.md` — verified paper list (title, authors, year, venue, relevance)
- paper-qa index built over available PDFs
- `literature-matrix.md` — rows: papers; columns: method, dataset, metric, limitation
  - Every cell from paper-qa queries or user-provided; never from memory
  - Unknown cells marked `?`
- At least 10 relevant papers identified

**Skills/tools:**
- `/literature-review` skill
- `pqa` CLI: `pqa -i [index-name] ask "[query]"`
- `academic-writing-agents:paper-crawler` (DBLP/OpenAlex)
- `04_LITERATURE_REVIEW_PLAYBOOK.md`

**Pass criteria:**
- ≥10 papers verified to exist
- paper-qa index built (or marked as TODO if no local PDFs)
- Literature matrix has at least one column showing what prior work does NOT do

**Fail conditions:**
- Literature written from memory (no paper-qa, no verified source)
- Fewer than 10 papers identified
- No gap column in matrix

**Forbidden:**
- Writing Related Work prose
- Citing papers not on the verified list
- Filling matrix cells from memory

**Next allowed stage:** Stage 6

---

## Stage 6 — Prior-Art and SOTA Competitiveness Check

**Goal:** Determine whether prior work already addresses the contribution, and what SOTA performance levels are.

**Required inputs:** `literature-matrix.md`, research question

**Required outputs:**
- `prior_art_competition_table.md` — with threat levels for each paper
- `sota_baseline_table.md` — best known results per dataset/metric
- `novelty_risk_report.md` — overall threat assessment and differentiation strategy

**Skills/tools:**
- `/prior-art-check` skill
- `/sota-check` skill
- `25_PRIOR_ART_COMPETITION.md`
- `pqa` for evidence

**Pass criteria:**
- All papers in literature matrix assessed for threat level
- SOTA result identified for primary metric/dataset (or TODO_SOTA_NEEDED if unknown)
- Novelty threat level ≤ Medium, OR differentiation strategy documented

**Fail conditions:**
- Threat level is Critical with no differentiation strategy
- SOTA is unknown and not marked TODO
- Novelty claim made before this stage passes

**Forbidden:**
- Claiming "our approach is novel" before this check
- Ignoring papers with High/Critical threat level
- Filling SOTA table from memory

**Next allowed stage:** Stage 7 (if threat ≤ Medium or differentiation documented)  
or `/pivot-decision` (if threat = Critical and no differentiation)

---

## Stage 7 — Gap and Positioning

**Goal:** Identify and validate the research gap, and position the contribution within the literature.

**Required inputs:** `literature-matrix.md`, `prior_art_competition_table.md`

**Required outputs:**
- Gap statement: "Prior work addresses X but not Y because Z"
- paper-qa evidence that the gap exists
- Threat assessment: closest paper and how we differ
- `contribution_contract.md` outline (contributions as hypotheses, not proven facts)

**Skills/tools:**
- `pqa` for gap validation
- `academic-writing-agents:research-analyst`
- `03_IDEA_TO_PAPER_PLAYBOOK.md`

**Pass criteria:**
- Gap is verifiable from paper-qa output (not from memory)
- Closest prior paper documented with explicit differentiation

**Fail conditions:**
- Gap asserted from memory with no paper-qa evidence
- Contribution identical to closest prior paper with no differentiation

**Forbidden:**
- Writing the "no prior work has addressed X" claim without paper-qa confirmation
- Dismissing the closest competitor without analysis

**Next allowed stage:** Stage 8

---

## Stage 8 — Contribution Contract

**Goal:** Lock contribution claims before confirmatory experiments. All claims treated as hypotheses until evidence confirms them.

**Required inputs:** Gap analysis, `venue_target.md`, `hypothesis_registry.md`

**Required outputs:**
- `contribution_contract.md` with:
  - Claim 1 → hypothesis ID + evidence pointer (or `TODO_RESULT_NEEDED:`)
  - Claim 2 → ...
  - Overclaiming risk checklist completed
- All claims marked as: [HYPOTHESIS] or [CONFIRMED] or [TODO]
- No claim marked [CONFIRMED] without an evidence ID

**Skills/tools:**
- `03_IDEA_TO_PAPER_PLAYBOOK.md`
- `10_TEMPLATES.md` (Template 5: Contribution Map)

**Pass criteria:**
- Every claim has an evidence pointer or a TODO marker
- No claim marked as confirmed without experiment evidence

**Fail conditions:**
- Contribution listed as "we show X" when X is untested
- No overclaiming risk checklist

**Forbidden:**
- Writing paper contributions section as if experiments are done
- "First" claims without prior-art evidence

**Next allowed stage:** Stage 9

---

## Stage 9 — Target Result Contract

**Goal:** Define minimum acceptable results BEFORE confirmatory experiments. This contract cannot be lowered after seeing results.

**Required inputs:** `venue_target.md`, `contribution_contract.md`, `sota_baseline_table.md`

**Required outputs:**
- `target_result_contract.md` (TRC) with:
  - Minimum acceptable result (specific: metric, threshold, dataset)
  - Required baselines (confirmed runnable)
  - Required datasets (confirmed available)
  - Required ablations
  - Pass/fail conditions
  - Fallback plan if fail
  - Claim allowed if pass / forbidden if fail

**Skills/tools:**
- `/target-result-contract` skill
- `26_TARGET_RESULT_CONTRACT.md`

**Pass criteria:**
- User has confirmed the contract
- Minimum acceptable result is specific and measurable
- Fallback plan documented

**Fail conditions:**
- Contract created after seeing results (invalid — start over)
- No fallback plan

**Forbidden:**
- Modifying TRC pass/fail threshold after confirmatory experiments begin
- Leaving minimum result vague ("competitive performance")

**Next allowed stage:** Stage 10

---

## Stage 10 — Experiment Design

**Goal:** Design the complete experiment matrix before running any experiments.

**Required inputs:** `contribution_contract.md`, `target_result_contract.md`, `hypothesis_registry.md`

**Required outputs:**
- `experiment_matrix.md` with:
  - Exploratory experiments (discover what happens)
  - Diagnostic experiments (explain failures)
  - Confirmatory experiments (support paper claims, must meet TRC)
  - For each: method, config, dataset, metric, budget, editable files, protected files
- Protected files list (evaluation harness — NEVER modify)
- Experiment budget: max_runs, max_time_per_run, crash_threshold

**Skills/tools:**
- `/plan-experiments` skill
- `05_EXPERIMENT_PLAYBOOK.md`

**Pass criteria:**
- Experiment types distinguished (exploratory vs. confirmatory)
- Protected files listed
- Budget defined

**Forbidden:**
- Mixing exploratory and confirmatory experiments without distinction
- No protected files list

**Next allowed stage:** Stage 11

---

## Stage 11 — Baseline and Implementation Readiness

**Goal:** Verify that all baselines are runnable and the proposed method is implemented before running experiments.

**Required inputs:** `experiment_matrix.md`

**Required outputs:**
- Each baseline in matrix: verified runnable (or marked NOT READY)
- Proposed method code: exists and runs without crash
- Dataset splits: verified correct
- Evaluation script: runs and produces parseable output

**Pass criteria:**
- All required baselines run successfully on at least one fold/seed
- Proposed method produces a finite output (may be bad; just must not crash)
- Evaluation metric parseable from output

**Fail conditions:**
- Any required baseline cannot run
- Proposed method crashes on startup
- Dataset split is wrong

**Forbidden:**
- Claiming baseline results from another paper's table without labeling them "from [cite]"
- Running confirmatory experiments before this passes

**Next allowed stage:** Stage 12

---

## Stage 11.5 — Proxy Experiment Protocol *(Required before full experiments)*

**Goal:** Run cheap proxy experiments to eliminate weak hypotheses before committing full compute budget.

**Hard rule:** No full experiment may run without PROXY_PASS status in results.tsv.

**Required inputs:**
- All hypotheses: validation_status = APPROVED
- project_profile.md with all fields filled (including baseline_metric)
- Git clean (working tree committed)
- Baseline run completed

**Required outputs:**
- results.tsv rows for all candidates (PROXY_PASS / PROXY_KILL / PROXY_NAN)
- hypothesis_registry.md updated: `proxy_status`, `proxy_metric`
- Tournament winner if multiple candidates (see Stage 11.5b)

**Sub-stage 11.5a — Single hypothesis:**
Use `/proxy-run` for single hypothesis testing.

**Sub-stage 11.5b — Multiple hypotheses (≥ 3):**
Use `/hypothesis-tournament` for Successive Halving.

**Skills/tools:**
- `/proxy-run` skill → `31_PROXY_EXPERIMENT_PROTOCOL.md`
- `/hypothesis-tournament` skill → `32_HYPOTHESIS_TOURNAMENT.md`

**Pass criteria:**
- ≥ 1 hypothesis with PROXY_PASS status
- All proxy results logged to results.tsv with commit hash

**Fail conditions:**
- All candidates PROXY_KILL or PROXY_NAN → run `/pivot-decision`
- project_profile.metric_extract returns non-float → fix parsing script

**Forbidden:**
- Running full experiment without PROXY_PASS
- Extending proxy duration after PROXY_KILL ("needs more epochs")
- Changing config after proxy to retry PROXY_KILL

**Next allowed stage:** Stage 12 (Exploratory Experiments) for PROXY_PASS candidates

---

## Stage 12 — Exploratory Experiment Loop

**Goal:** Run exploratory experiments to discover what is true. Results may contradict the initial hypothesis — that is acceptable and expected.

**Required inputs:** `experiment_matrix.md` (exploratory rows), runnable baseline

**Required outputs:**
- `results.tsv` — every run logged (BASELINE, PASS, FAIL, CRASH)
- `experiment_notes.md` — pre-registered hypothesis per run
- `failed_runs.md` — diagnoses for all FAIL/CRASH
- `best_result.md` — current best

**Skills/tools:**
- `/experiment-loop` skill
- `20_AUTONOMOUS_EXPERIMENT_LOOP.md`
- `21_EXPERIMENT_LOG_FORMAT.md`

**Pass criteria:**
- Baseline run exists in `results.tsv`
- At least one hypothesis has status other than "pending"
- All runs (including failed) are logged

**Important behavior:**
- If results contradict HYP-001: update `hypothesis_registry.md` status → CONTRADICTED
- Run `/pivot-decision` to decide: REFINE / DIAGNOSE / PIVOT / ABANDON
- Do NOT silently discard contradicting results
- Unexpected positive findings → new hypothesis (HYP-002), not immediate contribution

**Forbidden:**
- Hiding FAIL/CRASH runs
- Changing metrics after seeing results (requires DEC entry if unavoidable)
- Treating exploratory results as confirmatory claims

**Next allowed stage:** Stage 13

---

## Stage 13 — Result Interpretation and Research Direction Update

**Goal:** Interpret exploratory results honestly and update the research direction.

**Required inputs:** `results.tsv`, `hypothesis_registry.md`, `experiment_notes.md`

**Required outputs:**
- `hypothesis_registry.md` — all explored hypotheses with status updated
- `research_direction.md` — current direction reflecting actual evidence
  - If direction changed: version bump (e.g., 1.0 → 2.0)
- Decision log entry (DEC) for any direction change
- `project_state.md` updated

**Skills/tools:**
- `23_RESEARCH_DIRECTION_UPDATE.md`
- `/pivot-decision` if direction has changed

**Pass criteria:**
- Every hypothesis in the registry has a status (not all "pending")
- `research_direction.md` reflects actual evidence, not original idea
- Any contradicted hypothesis has a logged decision

**Fail conditions:**
- Contradicted hypotheses quietly ignored
- `research_direction.md` still matches original idea after contradicting evidence

**Forbidden:**
- Forcing the paper story to match the original idea despite evidence
- Marking CONTRADICTED hypotheses as SUPPORTED
- Proceeding to confirmatory experiments with an unresolved CONTRADICTED hypothesis

**Next allowed stage:** Stage 14

---

## Stage 14 — Confirmatory Experiment Planning

**Goal:** Plan the final confirmatory experiments that will produce the paper's main results. These must satisfy the Target Result Contract.

**Required inputs:** `target_result_contract.md`, `research_direction.md`, `experiment_matrix.md` (confirmatory rows)

**Required outputs:**
- Updated `experiment_matrix.md` (confirmatory experiments only)
- Confirmatory budget: max_runs, time_budget
- Ablation design confirmed (each row isolates one variable)

**Pass criteria:**
- Each confirmatory experiment directly tests a claim in `contribution_contract.md`
- Ablation design is correct (one variable per row)
- Budget is explicit

**Forbidden:**
- Running confirmatory experiments before this plan is approved
- Designing confirmatory experiments to support the story rather than test it

**Next allowed stage:** Stage 15

---

## Stage 15 — Confirmatory Experiment Execution

**Goal:** Run confirmatory experiments, log all results, and finalize the evidence base.

**Required inputs:** Confirmatory `experiment_matrix.md`, runnable code, locked `target_result_contract.md`

**Required outputs:**
- `results.tsv` with confirmatory rows (labeled type=CONFIRMATORY)
- Ablation results complete
- Sensitivity analysis (if required by TRC)
- `evidence_ledger.md` — EVID entries for all PASS/BASELINE confirmatory runs

**Skills/tools:**
- `/experiment-loop` skill (confirmatory mode)
- `20_AUTONOMOUS_EXPERIMENT_LOOP.md`

**Hard rules:**
- All 5 folds (or required seeds) must complete — no partial averaging
- Population std or sample std: choose one and apply consistently
- Std formula cannot change after first run

**Forbidden:**
- Reporting a partial run as complete
- Running the proposed method with different preprocessing than baselines
- Changing the evaluation script during confirmatory runs

**Next allowed stage:** Stage 16

---

## Stage 16 — Result Adequacy Gate

**Goal:** Evaluate whether results are strong enough for the target venue. This is the decisive gate before paper writing.

**Required inputs:** `results.tsv`, `target_result_contract.md`, `sota_baseline_table.md`, `prior_art_competition_table.md`

**Required outputs:**
- `result_adequacy_report.md` with decision: A/B/C/D/E/F/G

**Skills/tools:**
- `/result-adequacy` skill
- `27_RESULT_ADEQUACY_GATE.md`

**Decision outcomes:**
- **A** — Strong enough for target venue → Stage 17
- **B** — Promising, needs more experiments → Stage 15
- **C** — Good but not novel enough → differentiate or `/pivot-decision`
- **D** — Novel but result too weak → more experiments or narrow scope
- **E** — Negative/inconclusive → `/pivot-decision`
- **F** — Better as lower-tier paper → update `venue_target.md`, return to Stage 9
- **G** — Should pivot → `/pivot-decision`

**Forbidden:**
- Proceeding to Stage 17 with decision B/C/D/E/F/G
- Weakening the TRC retroactively to force a pass
- Ignoring baseline comparisons that show prior work is stronger

**Next allowed stage:** Stage 17 (decision A only), or `/pivot-decision` → return to appropriate earlier stage

---

## Stage 17 — Evidence Freeze

**Goal:** Lock all evidence before paper writing begins. Every claim must trace to a verified evidence ID.

**Required inputs:** `results.tsv`, `evidence_ledger.md`, `contribution_contract.md`

**Required outputs:**
- `evidence_ledger.md` — complete (every EVID entry verified)
- `claim-evidence-table.md` — every paper claim linked to EVID
- `result_to_claim_map.md` — every table cell linked to result file
- All TODO_RESULT_NEEDED resolved or explicitly marked as future work
- All TODO_CITATION_NEEDED resolved or explicitly deferred
- `project_state.md` updated: evidence_status = FROZEN

**Skills/tools:**
- `/result-backfill` skill
- `18_EVIDENCE_LEDGER.md`

**Pass criteria:**
- Every quantitative claim has an EVID entry
- Every EVID-EXP entry has a corresponding PASS/BASELINE row in results.tsv
- No claim marked as [HYPOTHESIS] that will be presented as [CONFIRMED]

**Fail conditions:**
- Any quantitative claim without an evidence ID
- Any EVID entry pointing to a FAIL or CRASH run
- TODO_RESULT_NEEDED in contribution claims

**Forbidden:**
- Writing final paper prose before this gate passes
- Adding new results after the freeze without re-running this stage

**Next allowed stage:** Stage 18

---

## Stage 18 — Paper Architecture

**Goal:** Create the paper outline before any prose is written.

**Required inputs:** `contribution_contract.md`, `claim-evidence-table.md`, `venue_target.md`

**Required outputs:**
- Section list with 2-3 bullet goals per section
- Figure plan (which figures are needed, what each shows, what data source)
- Table plan (which tables, what content)
- Word/page budget per section
- Section order confirmed (Method first, then Experiments, Related Work, Introduction, Conclusion, Abstract last)

**Skills/tools:**
- `academic-writing-agents:section-drafter` (skeleton only)
- `06_WRITING_PLAYBOOK.md`

**Forbidden:**
- Writing actual prose during architecture
- Creating LaTeX sections with content before architecture is approved

**Next allowed stage:** Stage 19

---

## Stage 19 — Section Drafting

**Goal:** Write each section with verified evidence. Order: Method → Experiments → Analysis → Related Work → Introduction → Conclusion → Limitations → Abstract.

**Required inputs:** Paper architecture, `claim-evidence-table.md`, `literature-matrix.md`

**Required outputs:** Draft LaTeX for each section

**Skills/tools:**
- `/draft-section` skill
- `academic-writing-agents:section-drafter`
- `06_WRITING_PLAYBOOK.md`

**Hard rules per section:**
- **Method:** design choices must be explained, not just listed
- **Experiments:** only logged results from `results.tsv`; std formula consistent
- **Related Work:** from `literature-matrix.md` and paper-qa only — never from memory
- **Introduction:** must not overclaim novelty; contributions match experiments
- **Abstract:** must not exceed evidence; write last
- **Limitations:** must be specific and honest — not vague

**Forbidden:**
- Writing Related Work from memory
- Using `\cite{key}` before key exists in references.bib
- Claiming "state-of-the-art" without the comparison table showing it
- Writing Abstract before all other sections are drafted

**Next allowed stage:** Stage 20

---

## Stage 20 — Figure and Visual Design

**Goal:** Create all figures for the paper. Every figure must be grounded in real data or method description.

**Required inputs:** Figure plan from Stage 18, method description, result files

**Required outputs:** TikZ code or draw.io XML for each figure, embedded in `.tex`

**Skills/tools:**
- `thesis-figure-skill` (native Claude skill)
- `academic-writing-agents:latex-figure-specialist`
- `07_FIGURE_AND_FORMAT_PLAYBOOK.md`

**Pass criteria:**
- Every plot value matches `results.tsv` exactly
- Every architecture diagram module is described in Method section
- Every figure is `\ref{}`'d in text before it appears

**Forbidden:**
- Data values that differ from `results.tsv`
- Hardcoded hyperparameter formulas in figure boxes
- Captions that claim more than the figure shows

**Next allowed stage:** Stage 21

---

## Stage 21 — LaTeX Formatting and PDF Production

**Goal:** Compile a clean PDF in the target venue format.

**Required inputs:** Full `.tex` draft with all sections and figures

**Required outputs:** Compiled PDF, clean LaTeX log

**Skills/tools:**
- `/format-paper` skill
- `tectonic` at `/opt/anaconda3/bin/tectonic`
- `07_FIGURE_AND_FORMAT_PLAYBOOK.md`

**Forbidden:**
- Changing numerical content while fixing formatting
- Altering citation keys while fixing bibliography

**Next allowed stage:** Stage 22

---

## Stage 22 — Multi-Agent Review

**Goal:** Run all 12 review passes before submission. No shortcuts.

**12 passes (in order):**

| Pass | Agent | Finds |
|------|-------|-------|
| 1. Logic | `logic-reviewer` | Argument gaps, unsupported conclusions |
| 2. Technical | `technical-reviewer` | Math errors, method description errors |
| 3. Claim-evidence | `consistency-checker` + manual | Claims without evidence pointers |
| 4. Citation | `bibliography-auditor` | Missing/wrong citations |
| 5. Prior-art/novelty | `research-analyst` + manual | Prior work stronger than claimed |
| 6. Venue-fit | Manual | Results vs. venue expectations |
| 7. Writing/style | `writing-reviewer` | Grammar, clarity, tone |
| 8. De-AI | `prose-polisher` + manual | AI-pattern prose |
| 9. Figure/table | `latex-figure-specialist` + `consistency-checker` | Caption mismatch, data errors |
| 10. LaTeX/layout | `latex-layout-auditor` | Float placement, column balance |
| 11. Paper-code alignment | `technical-reviewer` + manual | Results match real experiments |
| 12. Final skeptical | `logic-reviewer` full re-read | Holistic quality gate |

**Skills/tools:**
- `/paper-review` skill
- `08_REVIEW_AND_AUDIT_PLAYBOOK.md`

**Output:** Review report with severity P0/P1/P2 for each finding

**Hard rules:**
- Do not rewrite immediately after review — produce report first
- Critical findings (P0) must be resolved before Stage 23
- Passes run in order

**Next allowed stage:** Stage 23

---

## Stage 23 — Revision and Re-Audit

**Goal:** Apply fixes from review report. Re-audit critical findings.

**Required inputs:** Review report from Stage 22

**Required outputs:**
- Revised `.tex` with changes applied
- Re-audit confirming P0 findings resolved
- Revision log documenting what changed and why

**Forbidden:**
- Adding new claims not supported by evidence during revision
- Removing Limitations without replacement
- Altering `\cite{}`, `\label{}`, `\ref{}`, `\eqref{}` during prose revision

**Next allowed stage:** Stage 24

---

## Stage 24 — Submission Check

**Goal:** Complete the submission checklist before submitting.

**Required inputs:** Final PDF, references.bib, `result-map.md`, review report (resolved)

**Required outputs:** Completed `09_SUBMISSION_CHECKLIST.md`

**Skills/tools:**
- `/submission-check` skill
- `09_SUBMISSION_CHECKLIST.md`
- `bibliography-auditor`, `latex-layout-auditor`

**Hard rules:**
- No unresolved P0 findings
- All TODO markers resolved or explicitly deferred
- All citations verify against references.bib
- Page count within venue limit
- PDF compiles cleanly

**Next allowed stage:** Stage 25

---

## Stage 25 — Camera-Ready Archive

**Goal:** Archive the complete submission package for reproducibility.

**Required inputs:** Final accepted/submitted PDF + all source files

**Required outputs:**
```
archive/
  main.tex, main.pdf, references.bib
  figures/, tables/, results/, configs/
  code_hashes.txt (git log)
  review_reports/
  evidence_ledger.md, claim-evidence-table.md
  result_to_claim_map.md, decision_log.md
  research_direction.md, hypothesis_registry.md
  README_ARCHIVE.md
```

**Skills/tools:**
- `/archive-paper` skill

**Forbidden:**
- Archiving without result files (reproducibility requires them)
- Deleting source files after archiving

**End of workflow.**

---

## Pivot and Return Paths

| Trigger | From Stage | Return to Stage |
|---------|-----------|-----------------|
| Feasibility fails | 4 | 1 (revise idea) |
| Prior-art threat Critical | 6 | 7 or pivot decision |
| Exploratory results contradict hypothesis | 13 | 14 (if narrow pivot) or 8 (if major pivot) or ABANDON |
| TRC not met | 16 | 15 (more experiments) or 14 (redesign) or 9 (lower venue) or PIVOT |
| Result adequacy decision B-G | 16 | as per decision |
| P0 review finding unresolvable | 22-23 | 19 or 16 or pivot |

Every pivot generates a DEC entry in `decision_log.md`.

---

## Stage-to-Artifact Map

| Stage | Artifact produced |
|-------|------------------|
| 0 | `tool_healthcheck_report.md`, `project_state.md` |
| 1 | `paper_brief.md` |
| 2 | `hypothesis_registry.md` (initialized) |
| 3 | `venue_target.md`, `decision_log.md` (DEC-001) |
| 4 | Feasibility assessment (in `project_state.md`) |
| 5 | `literature_list.md`, `literature-matrix.md` |
| 6 | `prior_art_competition_table.md`, `sota_baseline_table.md`, `novelty_risk_report.md` |
| 7 | Gap statement (in `project_state.md`) |
| 8 | `contribution_contract.md` |
| 9 | `target_result_contract.md` |
| 10 | `experiment_matrix.md` |
| 11 | Baseline verification (in `project_state.md`) |
| 12 | `results.tsv`, `experiment_notes.md`, `failed_runs.md`, `best_result.md` |
| 13 | `research_direction.md` |
| 14 | Updated `experiment_matrix.md` (confirmatory) |
| 15 | Updated `results.tsv` (confirmatory rows), `evidence_ledger.md` |
| 16 | `result_adequacy_report.md` |
| 17 | `claim-evidence-table.md`, `result_to_claim_map.md` |
| 18 | Paper outline (in `project_state.md`) |
| 19 | Draft `.tex` sections |
| 20 | TikZ/figure source files |
| 21 | Compiled PDF |
| 22 | Review report |
| 23 | Revised `.tex`, revision log |
| 24 | Completed submission checklist |
| 25 | `archive/` directory |
