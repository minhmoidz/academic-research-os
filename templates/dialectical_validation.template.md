# Dialectical Validation

hypothesis_id: HYP-[NNN]
date: [YYYY-MM-DD]
validator: Claude + academic-writing-agents
status: PENDING

---

## Step 1: Constructive Argument

### Mechanism
[Cụ thể cơ chế nào đang được khai thác. Không được vague.]

### Pathway
[Tại sao cơ chế đó dẫn đến cải thiện metric thông qua baseline system.]

### Prior Evidence (từ paper-qa)
- "[Quote ngắn từ Paper A] — [paper A] found that [mechanism] improved [metric] in [domain]"
- "[Quote ngắn từ Paper B] — [paper B] demonstrates [related pathway]"

### Prediction
[Metric sẽ thay đổi như thế nào. Số cụ thể nếu có thể. Điều kiện nào.]

### Falsification Criterion
[Kết quả thực nghiệm nào sẽ bác bỏ hypothesis này. Phải observable và specific.]

---

## Step 2: Adversarial Critique
*(Run INDEPENDENTLY — adversarial agent does NOT read Step 1)*

### Prior Failure
[Tìm paper đã thử cơ chế tương tự và thất bại. Quote evidence.]

### Condition Violation
[Liệu điều kiện dataset/task của project có thỏa mãn requirement của cơ chế không?]

### Alternative Explanation
[Nếu kết quả positive, có giải thích khác ngoài proposed mechanism không?]

---

## Step 3: Adjudication

| Criterion | Score (0-10) | Reason |
|-----------|-------------|--------|
| Mechanistic specificity | [N] | [Brief reason — is the mechanism concrete or vague?] |
| Literature support | [N] | [Brief reason — how strong is the pqa evidence?] |
| Falsifiability | [N] | [Brief reason — is the prediction testable?] |
| Adversarial resistance | [N] | [Brief reason — does argument survive critique?] |
| **Aggregate** | **[mean]** | |

fatal_flaw: [NO | YES — description of fatal flaw]

---

## Decision

decision: [APPROVED | REJECTED | REVISE]
reason: [Why this decision]
next_action: [proceed to /proxy-run | revise mechanism and re-validate | abandon HYP-NNN]

---

## Integration

After APPROVED:
- hypothesis_registry.md: set dialectical_score = [N], validation_status = APPROVED
- Proceed to /proxy-run or /hypothesis-tournament
