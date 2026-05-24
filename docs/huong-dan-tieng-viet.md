# Hướng Dẫn Sử Dụng Academic Research OS (Tiếng Việt)

> Hệ thống hỗ trợ nghiên cứu AI từ ý tưởng → paper hoàn chỉnh, chạy trong Claude Code.

---

## Mục lục

1. [Research OS là gì?](#1-research-os-là-gì)
2. [Cài đặt](#2-cài-đặt)
3. [Bắt đầu project mới](#3-bắt-đầu-project-mới)
4. [Điền project_profile.md](#4-điền-project_profilemd)
5. [Quy trình đầy đủ từng bước](#5-quy-trình-đầy-đủ-từng-bước)
6. [Tất cả lệnh và tác dụng](#6-tất-cả-lệnh-và-tác-dụng)
7. [Khi nào dùng lệnh nào?](#7-khi-nào-dùng-lệnh-nào)
8. [Các tình huống thường gặp](#8-các-tình-huống-thường-gặp)
9. [Câu hỏi thường gặp](#9-câu-hỏi-thường-gặp)

---

## 1. Research OS là gì?

Research OS là một bộ file hướng dẫn cài vào dự án của bạn. Khi bạn mở dự án trong **Claude Code**, Claude sẽ đọc các file này và hoạt động như một **research assistant chuyên nghiệp** — tự biết phải làm gì ở từng bước, không bịa kết quả, không viết paper trước khi có dữ liệu.

**Vấn đề nó giải quyết:**
- Không biết bắt đầu từ đâu khi nghiên cứu
- Chạy experiment tốn GPU mà không biết có work không
- Viết paper xong mới phát hiện bị prior work làm rồi
- Claude "bịa" kết quả hoặc citation

**Cách nó hoạt động:**
```
Bạn gõ lệnh → Claude đọc file hướng dẫn → thực hiện đúng quy trình → nhắc bạn bước tiếp theo
```

---

## 2. Cài đặt

### Yêu cầu
- [Claude Code](https://claude.ai/code) (CLI hoặc VS Code extension)
- Python 3.8+
- Git

### Cài vào project của bạn

```bash
# Bước 1: Clone Research OS
git clone https://github.com/minhmoidz/academic-research-os.git /tmp/research-os

# Bước 2: Chạy script cài đặt vào project của bạn
cd /path/to/your-project
bash /tmp/research-os/scripts/new-project.sh .
```

Script sẽ tự tạo:
```
your-project/
├── .claude/
│   ├── CLAUDE.md              ← Hướng dẫn cho Claude
│   ├── research-os/           ← 34 file quy trình
│   └── skills/                ← 25 lệnh có thể gọi
├── project_profile.md         ← BẠN CẦN ĐIỀN FILE NÀY
├── project_state.md           ← Tự cập nhật sau mỗi session
└── templates/                 ← Các template cần dùng
```

### Cài tools hỗ trợ (khuyến nghị)

```bash
# paper-qa — tìm kiếm trong literature (quan trọng nhất)
pip install paper-qa

# tectonic — compile LaTeX (nếu viết paper bằng LaTeX)
cargo install tectonic
# hoặc: conda install -c conda-forge tectonic
```

---

## 3. Bắt đầu project mới

Sau khi cài xong, mở Claude Code trong thư mục project:

```bash
cd your-project
claude  # hoặc mở VS Code + Claude Code extension
```

Claude sẽ tự đọc `.claude/CLAUDE.md` và biết đây là research project.

**Gõ lệnh đầu tiên:**
```
/research-start
```

Claude sẽ hỏi bạn:
- Ý tưởng nghiên cứu là gì?
- Dataset nào?
- Metric đo lường là gì?
- Baseline model là gì?

Sau đó Claude tự tạo các file cần thiết và báo bước tiếp theo.

---

## 4. Điền project_profile.md

Đây là file quan trọng nhất — điền **1 lần** để toàn bộ OS hiểu dự án của bạn.

Mở file `project_profile.md` và điền:

```yaml
## Research Paradigm
task_family: "discriminative"        # discriminative / generative / retrieval / rl / self_supervised
contribution_type: "new_module"      # new_module / new_objective / new_architecture / efficiency

## The Fundamental Equation
baseline_system: |
  ResNet-50 pretrained on ImageNet, finetuned 100 epochs   # ← baseline của bạn là gì?

proposed_change: |
  Thêm cross-attention module sau layer 3                   # ← bạn muốn thêm gì?

primary_metric: "val_accuracy"       # metric chính (val_auc, val_fid, episode_reward, ...)
metric_direction: "higher"           # higher hoặc lower
dataset: "CIFAR-10"                  # dataset của bạn

## Experiment Interface  (3 lệnh này OS dùng để chạy code của bạn)
train_command: "python train.py --config {config} --output {out_dir}"
eval_command: "none"                 # "none" nếu eval tích hợp trong train
metric_extract: "python scripts/parse_metric.py {out_dir}/results.json"
# metric_extract PHẢI in ra 1 số float duy nhất, ví dụ: 0.8823

## Compute Profile
full_run_time: "2h"                  # bao lâu để train 1 lần đầy đủ?
proxy_fraction: 0.25                 # proxy chạy 25% — thay đổi nếu cần

## Evaluation Protocol
protocol: "train-val-test"           # k-fold-cv / train-val-test / online-rl
seed: 42
```

**Ví dụ theo từng loại project:**

| Loại project | task_family | protocol | metric thường dùng |
|---|---|---|---|
| Classification ảnh | discriminative | train-val-test | val_accuracy, val_auc |
| Medical imaging | discriminative | k-fold-cv | val_auc, val_f1 |
| Text generation | generative | train-val-test | val_loss, val_bleu |
| Retrieval/RAG | retrieval | train-val-test | recall@10, ndcg@10 |
| RL | rl | online-rl | episode_reward |
| Self-supervised | self_supervised | train-val-test | linear_probe_accuracy |

---

## 5. Quy trình đầy đủ từng bước

### Khi bạn đã có ý tưởng

```
Bước 1  /research-start          Khai báo ý tưởng, dataset, metric
Bước 2  /prior-art-check         Check xem ai đã làm chưa (dùng paper-qa)
Bước 3  /sota-check              Xem SOTA hiện tại là bao nhiêu
Bước 4  /validate-hypothesis     Claude tranh luận pros/cons — xác nhận ý tưởng đủ tốt
Bước 5  /plan-experiments        Lên danh sách experiments (baseline + ablation + proposed)
Bước 6  /proxy-run               Chạy thử 25% để xem có work không (tiết kiệm GPU)
         → Nếu PROXY_PASS        Tiếp tục bước 7
         → Nếu PROXY_KILL        Ý tưởng không work → /pivot-decision
Bước 7  /experiment-loop         Chạy đầy đủ, tự log kết quả vào results.tsv
Bước 8  /result-adequacy         Check kết quả có đủ để claim không
Bước 9  /paper-draft             Viết paper (chỉ được viết sau bước 8 pass)
Bước 10 /submission-audit        Kiểm tra lần cuối trước nộp
```

### Khi bạn chưa có ý tưởng

```
Bước 0  /gap-scout               Claude tự tìm 3-5 hướng nghiên cứu từ literature
                                  → Bạn chọn 1 hướng
         (tiếp tục từ Bước 2)
```

### Khi có nhiều ý tưởng muốn so sánh

```
         /hypothesis-tournament  So sánh N ý tưởng bằng Successive Halving
                                  Round 0: chạy proxy tất cả (25%)
                                  Round 1: chạy 1-fold cho top 50%
                                  Round 2: chạy 3-fold cho top 50%
                                  Chung kết: chạy đầy đủ cho winner
                                  → Tiết kiệm 57%+ GPU so với test lần lượt
```

---

## 6. Tất cả lệnh và tác dụng

### Khởi động & kiểm tra

| Lệnh | Tác dụng | Dùng khi nào |
|---|---|---|
| `/research-start` | Khởi động project, khai báo ý tưởng | Đầu mỗi project mới |
| `/research-status` | Xem project đang ở stage nào, còn thiếu gì | Đầu mỗi session làm việc |
| `/verify-research-os` | Kiểm tra OS cài đúng chưa | Sau khi cài lần đầu |
| `/tool-healthcheck` | Kiểm tra paper-qa, tectonic, GPU có hoạt động không | Khi tool bị lỗi |

### Nghiên cứu & ý tưởng

| Lệnh | Tác dụng | Dùng khi nào |
|---|---|---|
| `/gap-scout` | Tự tìm research gaps từ literature | Khi chưa có ý tưởng |
| `/prior-art-check` | Check xem ai đã làm idea này chưa | Trước khi commit vào idea |
| `/sota-check` | Xem SOTA hiện tại bao nhiêu | Trước khi đặt target |
| `/validate-hypothesis` | Tranh luận pros/cons của ý tưởng | Trước khi chạy bất kỳ experiment nào |
| `/venue-target` | Chọn conference/journal phù hợp | Sau khi có ý tưởng rõ ràng |
| `/target-result-contract` | Đặt mức kết quả tối thiểu cần đạt | Trước confirmatory experiments |

### Experiments

| Lệnh | Tác dụng | Dùng khi nào |
|---|---|---|
| `/plan-experiments` | Lên danh sách experiments cần chạy | Sau khi validate hypothesis |
| `/proxy-run` | Chạy thử 25% để xem có work không | Trước mỗi full experiment |
| `/hypothesis-tournament` | So sánh N ý tưởng cùng lúc, chọn winner | Khi có ≥2 ý tưởng cạnh tranh |
| `/experiment-loop` | Chạy experiments đầy đủ, tự log kết quả | Khi đã có PROXY_PASS |
| `/experiment-status` | Xem tiến độ experiments hiện tại | Trong khi chạy |

### Viết paper

| Lệnh | Tác dụng | Dùng khi nào |
|---|---|---|
| `/result-adequacy` | Check kết quả có đủ để viết paper không | Sau khi chạy xong experiments |
| `/result-backfill` | Điền kết quả thật vào paper draft | Sau khi có results |
| `/paper-draft` | Viết paper section by section | Sau khi result-adequacy PASS |
| `/literature-review` | Viết Related Work từ paper-qa | Trong khi viết paper |
| `/pivot-decision` | Quyết định xử lý khi kết quả không như kỳ vọng | Khi experiments fail |

### Review & nộp bài

| Lệnh | Tác dụng | Dùng khi nào |
|---|---|---|
| `/submission-audit` | Kiểm tra toàn diện trước nộp | 1-2 ngày trước deadline |
| `/archive-paper` | Lưu trữ paper sau khi nộp | Sau khi submit |

### Tự động hóa

| Lệnh | Tác dụng |
|---|---|
| `/auto-research` | Chạy toàn bộ pipeline tự động (gap-scout → validate → proxy → experiments → draft) với 3 điểm dừng để bạn xác nhận |

---

## 7. Khi nào dùng lệnh nào?

### Đầu mỗi session làm việc — luôn gõ:
```
/research-status
```
Claude sẽ báo: đang ở stage nào, cần làm gì tiếp theo, còn thiếu artifact nào.

### Quyết định có nên chạy experiment không:
```
/validate-hypothesis    ← BẮT BUỘC trước mọi experiment
```
Nếu score < 6/10 → không chạy, sửa lại ý tưởng trước.

### Muốn tiết kiệm GPU:
```
/proxy-run              ← chạy 25% trước
```
Nếu PROXY_KILL → không chạy full, tiết kiệm 75% GPU.

### Kết quả không như kỳ vọng:
```
/pivot-decision         ← Claude gợi ý 9 hướng xử lý
```
Không bao giờ "ép" story vào kết quả không đủ.

---

## 8. Các tình huống thường gặp

### Tình huống 1: Bắt đầu từ zero, chưa có idea

```
Bạn: /gap-scout
Claude: [chạy paper-qa tìm gaps trong lĩnh vực của bạn]
        → Đề xuất 5 hướng: TYPE1 (Unexplored Combination), TYPE2 (Contradictory Results)...
        → "Bạn muốn theo hướng nào?"
Bạn: [chọn 1 hướng]
Claude: [đăng ký hypothesis, chuyển sang validate]
```

### Tình huống 2: Có idea, muốn check xem có mới không

```
Bạn: /prior-art-check
Claude: [chạy paper-qa với 9 query templates]
        → Báo cáo: threat level LOW/MEDIUM/HIGH/CRITICAL
        → Nếu CRITICAL: ai đó đã làm y chang → cần pivot
        → Nếu MEDIUM: có điểm khác biệt → tiếp tục nhưng cần argue rõ novelty
```

### Tình huống 3: Experiments chạy xong, kết quả kém hơn baseline

```
Bạn: /pivot-decision
Claude: Phân tích 9 hướng xử lý:
        1. PROCEED — kết quả đủ tốt theo TRC
        2. NARROW — thu hẹp claim
        3. REFRAME — đổi góc nhìn contribution
        4. DIAGNOSE — chạy thêm ablation để hiểu tại sao
        5. PIVOT — đổi hypothesis hoàn toàn
        6-9. ...
        → Gợi ý hướng phù hợp nhất
```

### Tình huống 4: Muốn so sánh 3 variant của model

```
Bạn: /hypothesis-tournament
Claude: [đăng ký 3 hypothesis: HYP-001, HYP-002, HYP-003]
        Round 0: chạy proxy (25%) cho cả 3
        → HYP-001: 0.82, HYP-002: 0.79, HYP-003: 0.71
        → Eliminate HYP-003
        Round 1: chạy 1-fold cho HYP-001, HYP-002
        → HYP-001 win
        → Chạy full confirmatory cho HYP-001
```

### Tình huống 5: Đã có kết quả, muốn viết paper

```
Bạn: /result-adequacy
Claude: Check 6 điều kiện:
        ✓ TRC compliance (kết quả đạt threshold đã cam kết)
        ✓ SOTA gap (beat baseline đủ nhiều)
        ✓ Ablation complete
        ✓ Cross-dataset stability
        ✓ Statistical validity
        ✓ Claim-result alignment
        → Decision A: PROCEED → /paper-draft
        → Decision B-G: cần thêm experiments trước
```

---

## 9. Câu hỏi thường gặp

**Q: Tôi không có paper-qa, có dùng được không?**

Được, nhưng các lệnh `/gap-scout`, `/prior-art-check`, `/sota-check`, `/literature-review` sẽ không hoạt động tốt. Cài bằng `pip install paper-qa` và index paper collection của bạn trước.

---

**Q: `metric_extract` cần viết như thế nào?**

Phải in ra **đúng 1 số float** ra stdout. Ví dụ:

```python
# scripts/parse_metric.py
import json, sys
data = json.load(open(sys.argv[1]))
print(data["val_accuracy"])   # chỉ print số, không có text gì khác
```

Hoặc dùng bash:
```bash
metric_extract: "grep 'val_auc' {out_dir}/log.txt | tail -1 | awk '{print $NF}'"
```

---

**Q: proxy_fraction bao nhiêu là hợp lý?**

| Loại model | Khuyến nghị |
|---|---|
| Classification thông thường | 0.25 (25%) |
| Model lớn, train lâu | 0.10 (10%) |
| RL (noisy) | 0.50 (50%) |
| Self-supervised | 0.25, dùng `linear_probe` strategy |

---

**Q: Khi nào mới được viết paper?**

Chỉ sau khi `/result-adequacy` trả về **Decision A**. Trước đó có thể viết research notes, hypothesis notes, outline có TODO markers — nhưng không viết Abstract/Introduction/Related Work/Experiments chính thức.

---

**Q: Tôi dùng framework khác (JAX, Julia, R) có được không?**

Được. `train_command`, `eval_command`, `metric_extract` trong `project_profile.md` là shell commands tùy ý — gọi bất cứ ngôn ngữ/framework nào cũng được, miễn là:
- `train_command` exit 0 khi thành công
- `metric_extract` in ra 1 số float duy nhất

---

**Q: Có thể bỏ qua bước nào không?**

Có thể bỏ qua các bước optional (Gap Scout nếu đã có idea, Venue Target nếu chưa cần). Nhưng **4 gates này bắt buộc**:

| Gate | Lệnh | Không qua = không được làm gì |
|---|---|---|
| Stage 6 | `/prior-art-check` | Không được confirm hypothesis |
| Stage 9 | `/target-result-contract` | Không được chạy confirmatory experiments |
| Stage 16 | `/result-adequacy` | Không được viết paper prose |
| Stage 17 | Evidence Freeze | Không được submit |

---

**Q: Dùng với Claude Code version nào?**

Bất kỳ version nào hỗ trợ custom skills (`.claude/skills/`). Khuyến nghị dùng model **Claude Sonnet** hoặc **Claude Opus** để có chất lượng reasoning tốt nhất cho validation và adversarial critique.

---

## Tóm tắt nhanh

```
Chưa có idea:     /gap-scout → chọn direction → /validate-hypothesis
Có idea rồi:      /prior-art-check → /validate-hypothesis → /plan-experiments
Trước chạy GPU:   /proxy-run (tiết kiệm 75% nếu fail)
Nhiều ý tưởng:    /hypothesis-tournament (tiết kiệm 57%+ GPU)
Đủ kết quả rồi:  /result-adequacy → /paper-draft
Mỗi sáng vào:    /research-status (xem cần làm gì tiếp)
```
