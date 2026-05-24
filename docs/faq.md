# Frequently Asked Questions

---

## Setup and Tools

**1. Can I use this OS without paper-qa?**

Yes, but with reduced capability. paper-qa powers the prior-art check (`/prior-art-check`), SOTA check (`/sota-check`), and Related Work verification. Without it, you must perform these checks manually and mark unverified cells with `TODO_EVIDENCE_NEEDED:`. The experiment loop, evidence tracking, and all writing stages still work fully without paper-qa.

**2. Can I use pdflatex instead of tectonic?**

Yes. Tectonic is the default recommendation because it auto-downloads packages and produces clean output, but any LaTeX compiler works. Update the compile command in `12_SESSION_PROTOCOL.md` and the `paper-format` skill to use `pdflatex` or `xelatex`. The OS has no hard dependency on tectonic.

**3. What if I already have results — do I still need to go through all 26 stages?**

You can start at a later stage, but you must backfill the required artifacts for earlier stages before the gates will pass. At minimum, you need: `paper_brief.md` (Stage 1), `hypothesis_registry.md` with pre-registered hypotheses (Stage 2), `prior_art_competition_table.md` (Stage 6), `sota_baseline_table.md` (Stage 6), `target_result_contract.md` (Stage 9), and `results.tsv` with logged runs (Stage 12+). Run `/result-backfill` to create evidence ledger entries from existing result files.

**4. Can I use this for non-ML papers?**

Yes. The workflow is designed for empirical ML/AI papers but the core principles — evidence tracing, prior-art checking, gate-based progression, anti-hallucination rules — apply to any empirical research paper. The experiment loop and result adequacy gate assume a numeric metric, so for qualitative papers you would adapt those stages to use qualitative criteria.

---

## Gates and Contracts

**5. What happens if my results don't meet the Target Result Contract?**

Run `/result-adequacy`. If the decision is not A (Proceed), run `/pivot-decision` to choose one of 9 options: RUN_MORE_EXPERIMENTS, NARROW_CLAIM, CHANGE_VENUE, PIVOT_ANALYSIS, PIVOT_ROBUSTNESS, PIVOT_BENCHMARK, PIVOT_SYSTEM, or ABANDON. You may not lower the TRC threshold retroactively without logging a DEC entry and a justification.

**6. Can I run confirmatory experiments before finishing the prior-art check?**

No. The prior-art check (Gate 1, Stage 6) must pass before confirmatory experiments begin. Running confirmatory experiments without knowing the prior-art landscape risks discovering after the fact that your contribution was already published — wasting expensive compute. Exploratory experiments are allowed at any stage.

**7. What is the difference between `/research-status` and `/verify-research-os`?**

`/research-status` reports your *research project* state: current stage, completed artifacts, open TODOs, active blockers, next safe action. It reads `project_state.md`. `/verify-research-os` reports the *OS infrastructure* state: are all 29 workflow files present, are all 21 skill files present, is CLAUDE.md correctly wired. Run `/research-status` every session. Run `/verify-research-os` when you suspect a file is missing or after a git pull.

**8. What is the difference between `/tool-healthcheck` and `/verify-research-os`?**

`/tool-healthcheck` tests binary tool *availability*: does `pqa` run, does `tectonic` compile a test file, is `git` accessible. `/verify-research-os` tests OS *file integrity*: are all the workflow and skill files in place. Both should be run when setting up on a new machine.

---

## Hypotheses and Experiments

**9. How do I add a new hypothesis mid-project?**

Open `hypothesis_registry.md` and add a new HYP-NNN entry with status `pending`. Log the addition in `decision_log.md` with category `NEW_HYPOTHESIS`. Update `project_state.md`. Then design an experiment to test it. Never mark a hypothesis `supported` before running the experiment.

**10. What is the simplicity criterion in the experiment loop?**

When two experiment variants produce equal metric values, prefer the one with fewer lines of code. Specifically: if discarding a change (reverting to baseline) produces the same metric as keeping the change, discard it. Complexity is a liability — it makes the codebase harder to maintain and harder to explain in the paper's method section.

---

## Writing Rules

**11. Can I write rough notes and outlines before Stage 17?**

Yes. Before the Evidence Freeze (Stage 17), you may write: research notes, hypothesis notes, literature notes, experiment interpretation, rough bullet-point outlines, TODO-based skeleton outlines (section headers with `% TODO:` placeholders), and all stage artifacts (matrices, checklists, ledger entries). What is forbidden is **final paper prose** — complete sentences written as if for a submission. A skeleton like `## Method\n% TODO: describe [ProposedModule] here` is allowed. The sentence "Our method achieves 89.3% accuracy, outperforming all baselines" is not.

**12. What does "Evidence Freeze" actually freeze?**

The Evidence Freeze (Stage 17) locks the `evidence_ledger.md`. After freezing, every claim in the paper draft must already have a corresponding EVID entry pointing to a PASS or BASELINE row in `results.tsv`. New experiments may not be run after the freeze without explicitly unfreezing (which requires a DEC log entry and re-running the result adequacy gate).

---

## Pivots and Direction Changes

**13. How do I handle a result that contradicts my hypothesis?**

Immediately update `hypothesis_registry.md` to mark the hypothesis `contradicted`. Run `/pivot-decision` to get a structured recommendation. Log the decision in `decision_log.md`. Do not proceed as if the contradiction did not happen. Do not "adjust" the result. Do not cherry-pick a fold that shows positive results. The system is designed to help you find the real story — which may differ from the initial idea.

**14. When should I use `/pivot-decision`?**

Use `/pivot-decision` whenever: (a) a hypothesis is marked CONTRADICTED, (b) the result adequacy gate returns Decision B-G, (c) a prior-art threat is Critical, or (d) you are considering changing the venue or metric. The command produces a structured recommendation with one of 9 decisions and logs it to `decision_log.md`.

**15. Can I lower the Target Result Contract threshold if results are weak?**

Only before confirmatory experiments begin. If you have not yet run any confirmatory experiment, you may revise the TRC with a DEC log entry explaining why the threshold was set incorrectly. If confirmatory experiments have already run, lowering the threshold is **forbidden** — it constitutes retroactively moving the goalposts, which is a research integrity violation. In that case, use `/pivot-decision` instead.
