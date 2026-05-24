# Writing Playbook — Section-by-Section Guide

**Tools:** `empirical-paper-writer`, `research-paper-writing`, `academic-writing-agents:section-drafter`

**Hard rule:** All claims require evidence. All citations require verified entries. All numbers trace to result files.

---

## Abstract

**Purpose:** Compress the entire paper into ~180 words. Hook, gap, fix, evidence, significance.

**Required inputs:** Final results, key numbers, method name

**Structure:**
1. Problem: what must be done (active verb, concrete stakes)
2. Existing approach + its specific, quantified failure
3. Our fix: what it does and why (one sentence, mechanism-first)
4. Why the fix needs its components (briefly)
5. Results: specific numbers (+X pp, Y× reduction), not vague qualifiers
6. Significance: what changes because of this work

**Allowed claims:** Only what results tables confirm.

**Forbidden:**
- "suggest that X can improve" (double hedge)
- "consistently" without showing it's consistent across all benchmarks
- Any AUC number not in the final result table
- "state-of-the-art" without a comparison showing it

**Required evidence:** Final result table, norm analysis numbers (if cited)

**Common mistakes:**
- Writing abstract first (write it last)
- Using AUC numbers from intermediate runs
- Burying the key result in the last sentence

**Revision checklist:**
- [ ] All numbers match the final result tables
- [ ] Gap is quantified (not "CSS has a bias" but "CSS selects easy groups in 94.1% of slides")
- [ ] Results are specific (not "improves AUC" but "+0.64, +0.74, +0.25 pp")
- [ ] No double hedges
- [ ] CSS expanded on first use

---

## Introduction

**Purpose:** Motivate the problem, identify the gap, preview the fix, list contributions, give roadmap.

**Required inputs:** Paper brief, gap analysis, contribution map, key experimental results

**Structure:**
1. Para 1: Domain framing + why the task matters (2–3 sentences max)
2. Para 2: Existing approach + specific, measurable gap (introduce the problem)
3. Para 3: Our approach overview + key mechanism (NOT a full method description)
4. Contributions: 3 bullets, each with a number or concrete qualifier
5. Roadmap: ≤ 1 sentence (or omit)

**Allowed claims:** Gap claims supported by analysis section. Contribution claims pointing to result tables.

**Forbidden:**
- Methodology details that belong in Section III
- Results that haven't been validated
- Roadmap paragraph that's 3 perfectly parallel "Section X does Y" sentences

**Required evidence:** Gap must be stated with measurement ("0.897×", "94.1%"), not as assertion.

**Common mistakes:**
- Introducing BaselineModel in too much detail (Related Work's job)
- Writing contributions as "We propose X" without saying what X achieves
- Three contribution bullets with identical grammatical structure (AI tell)

**Revision checklist:**
- [ ] Gap is measurable, not just stated
- [ ] Each contribution bullet has a number or result pointer
- [ ] Method is not over-explained (that's for Section III)
- [ ] No "Furthermore", "Moreover", "It is worth noting"

---

## Related Work

**Purpose:** Position the paper relative to prior work organized by concept. Justify why existing methods don't solve the problem.

**Required inputs:** Literature matrix (from paper-qa), references.bib

**Forbidden:** Writing from memory. Every sentence needs a citation from the verified list.

**Structure:** 2–4 subsections, each organized by concept:
- Start each subsection: what this line of work does + shared mechanism
- End each subsection: what it does NOT address (the gap)
- Differentiate proposed method explicitly at the end

**Allowed claims:** Only what paper-qa confirms about each paper.

**Forbidden:**
- "X et al. proposed Y" × N consecutive sentences with identical form
- Citing a paper before it's in references.bib
- Describing a paper's contribution more strongly than the paper itself claims
- Omitting the closest competing work

**Common mistakes:**
- Organizing by year ("In 2021... In 2022... In 2023...")
- Listing papers without synthesis
- Not explaining WHY prior methods fail on your specific problem

**Revision checklist:**
- [ ] Every citation key verified in references.bib
- [ ] Each subsection ends with gap statement
- [ ] No memory-based claims (all from paper-qa)
- [ ] Closest competing paper discussed and differentiated

---

## Method

**Purpose:** Describe the proposed method precisely enough to reproduce.

**Required inputs:** Implementation code, config files, architecture diagrams

**Structure:**
- III.A: Preliminaries (describe backbone being extended)
- III.B–E: Each proposed component with equation and figure reference
- III.F: Training objective (full loss function)

**Allowed claims:** Mechanism descriptions, architectural choices, training details.

**Forbidden:**
- Claiming the method works (that's Experiments' job)
- Forward references to results before they're established
- Describing hyperparameters without reporting sensitivity

**Required evidence:** Code must match text. Architecture in figure must match text.

**Common mistakes:**
- Not explaining WHY each component is designed as it is
- "We apply X to Y" without explaining the design motivation
- Ambiguous description of how components connect (concatenation vs. addition vs. gating)

**Revision checklist:**
- [ ] Every equation has a label and is referenced in prose
- [ ] Every component has a motivation sentence ("we do X because Y")
- [ ] Auxiliary classifier architecture explicitly stated (not implied)
- [ ] Hyperparameter values justified (not just listed)
- [ ] Figure matches text description exactly

---

## Experiments

**Purpose:** Report results that test the contributions. Every claim backed by a table row.

**Required inputs:** Result map (Phase 8), experiment matrix

**Structure:**
- IV.A: Datasets and implementation details (setup locked before experiments)
- IV.B: Comparison with baselines (Table I)
- IV.C: Ablation (Table II)
- IV.D: Analysis (figures, norm plots, qualitative)
- IV.E: Hyperparameter sensitivity (Table III or IV)

**Allowed claims:** Only what the result files show.

**Forbidden:**
- Rounding results without noting the rounding
- "Our method is better" without specifying on which dataset and metric
- Comparing against methods run with different preprocessing

**Common mistakes:**
- Discussing only favorable results (must mention where method doesn't win)
- "Consistently outperforms" when one dataset shows no improvement
- Not explaining why a method performs differently across datasets

**Revision checklist:**
- [ ] Every table number traced to a result file
- [ ] All std values computed with the same formula (population or sample, consistent)
- [ ] Every baseline confirmed to run with same protocol
- [ ] Honest about cases where method doesn't win (with explanation)
- [ ] Ablation traces gains to specific components

---

## Analysis

**Purpose:** Provide mechanistic evidence for WHY the method works.

**Required inputs:** Analysis experiments (norm plots, selection frequency counts, etc.)

**Allowed claims:** Quantitative observations that support the mechanism. Correlational evidence. Attributed causation ("we attribute X to Y" not "X is caused by Y").

**Forbidden:** Causal language without causal experiment. "CSS selects hard groups because..." without showing the mechanism.

**Common mistakes:**
- Calling correlation causation
- Selective reporting (only showing analysis that supports the hypothesis)
- Forgetting to mention AttentionModule's intermediate effect (norm gap worsens before ProposedModule corrects it)

---

## Limitations

**Purpose:** Honest accounting of what the paper does NOT show.

**Allowed claims:** Specific gaps in experimental scope (datasets, cancer types, sample sizes, statistical power).

**Forbidden:**
- Minimizing limitations to sound more confident
- Repeating ablation results that are already in the main text
- Writing 5 consecutive "The X..." sentences (parallel structure AI tell)

**Required:** Statistical power caveat if n < 30 folds. Scope qualifiers on all generalization claims.

**Common mistakes:**
- Limitations section too long and repetitive
- Not acknowledging underpowered statistical tests
- Not noting inference-time gap vs. lighter baselines if it exists

---

## Conclusion

**Purpose:** Synthesize contributions and open future directions.

**Forbidden:**
- Introducing new claims not supported by experiments
- "By combining A, B, C, D, METHOD improves..." (template completion AI tell)
- "Proves sufficient: X shifts Y toward Z" (aphorism AI tell)
- Ending with "Future work will..." × 3 bullet points

**Structure:**
1. Restate the gap (1 sentence)
2. State what ProposedModule does and show it works (2 sentences with numbers)
3. Ablation finding that generalizes (1 sentence)
4. Future directions (1–2 directions, not exhaustive list)
5. Closing: forward-looking or concrete final statement

---

## Captions

**Purpose:** Make figures and tables self-contained.

**Required:** Every figure caption must describe:
1. What is shown (axis, variable)
2. What the reader should observe
3. The conclusion that follows

**Forbidden:**
- "Figure 1 shows our method" (empty caption)
- Captions that claim more than the figure demonstrates
- Hardcoded hyperparameter values in figure captions that differ from final config

**Common mistakes:**
- Caption for a bar chart that doesn't explain the normalization baseline
- Not labeling which panel is which for multi-panel figures
