# Session Protocol

Follow this protocol at the start and end of every research session.

---

## Session Start — 11 Steps (Required Before Any Work)

### Step 1: Load CLAUDE.md
```
Read .claude/CLAUDE.md
```
Confirm: Academic Research Operating System section present.

### Step 2: Load session protocol
```
Read .claude/research-os/12_SESSION_PROTOCOL.md     ← this file
```

### Step 3: Load workflow
```
Read .claude/research-os/02_RESEARCH_WORKFLOW.md
```
Confirm: 26-stage workflow loaded.

### Step 4: Load anti-hallucination rules
```
Read .claude/research-os/13_ANTI_HALLUCINATION_RULES.md
```
Confirm: Rules 1–13 loaded.

### Step 5: Read project state
```
Read project_state.md                               ← in project root
```
If missing: report "Stage 0 not started" and ask user to run `/research-start`.

### Step 6: Detect current stage
From `project_state.md`:
- `current_stage` field → confirms which of the 26 stages applies
- `completed_stages` → what has been done
- If `project_state.md` is missing: current stage = 0

### Step 7: Detect available artifacts
Check which stage-required artifacts exist in the project root:
```bash
ls paper_brief.md venue_target.md hypothesis_registry.md \
   literature-matrix.md prior_art_competition_table.md \
   sota_baseline_table.md contribution_contract.md \
   target_result_contract.md experiment_matrix.md \
   results.tsv evidence_ledger.md claim-evidence-table.md \
   research_direction.md result_adequacy_report.md \
   decision_log.md 2>/dev/null
```

### Step 8: Detect missing artifacts
Compare detected artifacts against requirements for the current stage (see Stage-to-Artifact Map in `02_RESEARCH_WORKFLOW.md`). List everything missing.

### Step 9: Detect active TODO markers
```bash
grep -rn "TODO_" *.tex *.md 2>/dev/null | wc -l
grep -rn "TODO_" *.tex *.md 2>/dev/null | head -20
```

### Step 10: Check evidence gate
If current stage ≥ 17 (Evidence Freeze):
- [ ] `claim-evidence-table.md` exists
- [ ] `evidence_ledger.md` has entries for all paper claims
- [ ] No EVID entry pointing to a FAIL/CRASH run
- [ ] `result_to_claim_map.md` exists

If current stage ≥ 19 (Section Drafting):
- [ ] Evidence Freeze passed (project_state.md: evidence_status = FROZEN)
- [ ] `literature-matrix.md` exists (for Related Work)
- [ ] `results.tsv` confirmatory rows exist

### Step 11: Report status and wait for user confirmation

Output the status report in this format:

```
═══════════════════════════════════════════════════════
Research OS Session Start Report
═══════════════════════════════════════════════════════
Workflow loaded: YES (26 stages)
Anti-hallucination rules: YES (13 rules)

Current stage: [N] — [Stage Name]
Last updated: [timestamp from project_state.md]
Session count: [N]

Artifacts present:
  ✓ paper_brief.md
  ✓ hypothesis_registry.md (N hypotheses)
  ✓ results.tsv (N runs)
  ✗ target_result_contract.md — MISSING (required for Stage 9)
  ✗ result_adequacy_report.md — MISSING (required for Stage 16)

Active TODO markers: [N total]
  TODO_RESULT_NEEDED: [N occurrences]
  TODO_CITATION_NEEDED: [N occurrences]
  TODO_EVIDENCE_NEEDED: [N occurrences]

Current gate: [Stage N — Gate Name]
Active blockers: [list or "none"]
Next safe action: [one specific recommended action]
═══════════════════════════════════════════════════════
```

**Do not write any content until the user confirms the next action.**

---

## During the Session

### When writing prose (Stage 19+):
1. Check `claim-evidence-table.md` for every claim in the section
2. Confirm result files exist for all quantitative claims
3. Confirm `\cite{}` keys exist in references.bib before using them
4. Run paper-qa for any Related Work claim

### When editing existing prose:
1. Note all `\cite{}`, `\label{}`, `\ref{}`, `\eqref{}` in the section
2. These must be preserved exactly — no key changes during revision
3. If a numerical claim looks wrong: flag it, do not silently "fix" it

### When a hypothesis is contradicted:
1. Update `hypothesis_registry.md` → mark status: CONTRADICTED
2. Run `/pivot-decision`
3. Log decision in `decision_log.md`
4. Update `research_direction.md` (version bump)
5. Update `project_state.md`
6. Do NOT proceed to Stage 14 with an unresolved CONTRADICTED hypothesis

### When results come in:
1. Append to `results.tsv` immediately (append-only)
2. Update `best_result.md` if PASS
3. Log FAIL/CRASH in `failed_runs.md`
4. Never cherry-pick — all runs are logged

---

## Session End (Required Before Closing)

### Step 1: Update project_state.md
```markdown
current_stage: [N]
last_updated: [ISO timestamp]
session_count: [N+1]
completed_stages: [..., stage just completed if applicable]
completed_artifacts: [updated list]
missing_artifacts: [updated list]
active_blockers: [updated list]
next_safe_action: [recommended first action for next session]
```

### Step 2: Count open TODOs
```bash
grep -rn "TODO_" *.tex *.md 2>/dev/null | wc -l
```
Record count in `project_state.md: active_todo_markers`.

### Step 3: Verify LaTeX compiles (if `.tex` was edited)
```bash
tectonic [paper.tex]
```
If compilation fails: note the error in `project_state.md` and resolve before claiming the session is complete.

### Step 4: Check for new Critical findings
If any P0 review finding was introduced during this session (e.g., by reviewing a new section), log it in `project_state.md: active_blockers`.

---

## research-state.md vs project_state.md

| File | Format | Purpose |
|------|--------|---------|
| `project_state.md` | Full template from `16_PROJECT_STATE.md` | Complete project state — updated every session |
| `research-state.md` | Legacy simple format | Older projects; superseded by `project_state.md` in this version |

For new projects: use `project_state.md`.
For legacy projects: create `project_state.md` from the template and migrate key fields.

---

## Rules for Session Continuity

1. **Never start from scratch** — always read `project_state.md` first
2. **Never assume state** — if `project_state.md` says Stage 12, do not skip to Stage 19
3. **Never write final paper prose before Stage 17 Evidence Freeze passes** — "final paper prose" means complete sentences intended for a submission draft (Abstract, Introduction, Related Work, Method, Experiments, Conclusion, Limitations). Before Stage 17, Claude MAY write: research notes, hypothesis notes, literature notes, experiment interpretation, rough bullet-point outlines, TODO-based skeleton outlines, and all stage artifacts (matrices, checklists, templates, evidence ledger entries).
4. **Never close a session with a P0 finding unresolved** — document it if you cannot fix it immediately
5. **Always update `project_state.md` before closing**
6. **Never force the paper story** — if contradicting evidence exists, update the direction
