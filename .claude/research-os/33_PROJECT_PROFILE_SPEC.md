# Project Profile Specification

`project_profile.md` là file duy nhất thay đổi giữa các AI research project.
Điền một lần ở Stage 0. Toàn bộ Research OS đọc từ file này để tự cấu hình.

---

## Tại sao file này tồn tại

**Vấn đề**: Research OS không thể biết trước paradigm của project (classification vs. RL vs. generative), evaluation protocol (5-fold vs. train-val-test vs. online), hay metric (AUC vs. FID vs. reward).

**Giải pháp**: Tách workflow logic (bất biến) khỏi project config (thay đổi). OS chỉ cần đọc `project_profile.md` — không đụng vào training code.

---

## Phương trình bất biến của mọi AI paper

```
CLAIM: "Thêm [X] vào [Y] cải thiện [Z] trên [D] thêm [Δ]"

X = proposed_change   (module / objective / architecture / augmentation)
Y = baseline_system   (baseline model + training setup)
Z = primary_metric    (AUC / BLEU / FID / reward / recall@k / ...)
D = dataset           (image set / text corpus / environment / ...)
Δ = target_delta      (mức cải thiện tối thiểu — từ TRC)
```

Project profile captures X, Y, Z, D, Δ và cách đo chúng.

---

## Universal Experiment Interface

OS giao tiếp với project code qua 3 shell commands. Project PHẢI implement đúng interface này.

```bash
# 1. TRAIN — chạy một experiment
{train_command}   # placeholders: {config}, {out_dir}, --proxy (optional flag)
# Exit 0 = thành công | Exit 1 = thất bại (NaN, crash, ...)

# 2. EVAL — đánh giá checkpoint (nếu eval riêng với train)
{eval_command}    # placeholders: {checkpoint}, {out_dir}
# Exit 0 = thành công

# 3. EXTRACT — đọc metric từ output dir → in ra 1 số float
{metric_extract}  # placeholders: {out_dir}
# stdout: một float duy nhất. Ví dụ: 0.8823
```

Khi có flag `--proxy`, training script TỰ dừng sau `proxy_fraction × total_steps`. OS không biết bên trong làm gì — chỉ đọc metric sau khi script exit.

---

## Tất cả fields

### Nhóm 1: Research Paradigm

```yaml
task_family:
  # Chọn một:
  discriminative   # Classification, detection, segmentation, regression
  generative       # Diffusion, VAE, GAN, flow, autoregressive LM
  retrieval        # Dense retrieval, ranking, recommendation, RAG
  rl               # Policy learning, planning, RLHF, bandits
  self_supervised  # DINO, SimCLR, MAE, contrastive, masked prediction
  structured       # Parsing, graph prediction, seq2seq, structured output

contribution_type:
  # Chọn một:
  new_module       # Component mới thêm vào baseline architecture
  new_objective    # Loss function hoặc training objective mới
  new_architecture # Thiết kế model hoàn toàn mới
  new_dataset      # Contribution chính là dataset
  efficiency       # Cùng/tốt hơn metric với ít compute/params hơn
  new_evaluation   # Benchmark hoặc evaluation protocol mới
```

### Nhóm 2: Fundamental Equation

```yaml
baseline_system: |
  # Mô tả Y — baseline model + setup. Human-readable.
  # Ví dụ: "ResNet-50 pretrained on ImageNet, finetuned on CIFAR-10 for 100 epochs"

proposed_change: |
  # Mô tả X — thay đổi đề xuất. Human-readable.
  # Ví dụ: "Add cross-attention module between layer3 and layer4"

primary_metric: val_accuracy
  # Tên metric CHÍNH XÁC như trong training log / results file
  # Ví dụ: val_auc, val_ndcg@10, val_fid, episode_reward, val_bleu

metric_direction: higher
  # higher (accuracy, AUC, reward, BLEU, Recall)
  # lower  (loss, FID, perplexity, error rate)

dataset: "CIFAR-10"
  # Tên dataset / environment chính

target_delta: "[TBD — điền sau khi sign TRC]"
  # Mức cải thiện tối thiểu để claim có ý nghĩa
  # Ví dụ: "+2.0pp accuracy", "+5pp Recall@10", "-10 FID points"
  # KHÔNG điền trước Stage 9 (Target Result Contract)
```

### Nhóm 3: Experiment Interface

```yaml
train_command: "python train.py --config {config} --output {out_dir}"
  # Placeholders BẮT BUỘC: {config}, {out_dir}
  # Placeholder TÙY CHỌN: --proxy (khi OS muốn chạy proxy run)
  
  # Ví dụ theo paradigm:
  # Supervised:   "python train.py --config {config} --output {out_dir}"
  # RL:           "python train_ppo.py --config {config} --logdir {out_dir}"
  # Diffusion:    "python train_diffusion.py --config {config} --save_dir {out_dir}"
  # NLP ft:       "python finetune.py --config {config} --output_dir {out_dir}"
  # Self-sup:     "python pretrain.py --config {config} --output {out_dir}"

eval_command: "none"
  # Nếu eval tích hợp trong train_command: "none"
  # Nếu eval riêng biệt:
  # "python evaluate.py --model {checkpoint} --output {out_dir}"

metric_extract: "python scripts/parse_metric.py {out_dir}/results.json"
  # Phải print MỘT SỐ FLOAT ra stdout. Không có gì khác.
  # Ví dụ:
  # "grep 'val_auc' {out_dir}/log.txt | tail -1 | awk '{print $NF}'"
  # "cat {out_dir}/metrics.json | python -c \"import sys,json; d=json.load(sys.stdin); print(d['ndcg@10'])\""
  # "python -c \"import json; print(json.load(open('{out_dir}/eval.json'))['accuracy'])\""
```

### Nhóm 4: Compute Profile

```yaml
full_run_time: "2h"
  # Wall-clock time cho một complete training run
  # Ví dụ: "30min", "2h", "8h", "2d"

full_run_unit: per_fold
  # per_fold    — time per fold (k-fold CV)
  # per_seed    — time per seed (multi-seed)
  # total       — tổng time cho toàn bộ training
  # per_episode — time per episode budget (RL)

proxy_strategy: reduced_epochs
  # reduced_epochs — train proxy_fraction × total epochs (phổ biến nhất)
  # reduced_data   — train trên proxy_fraction × training data (dataset lớn)
  # reduced_steps  — proxy_fraction × total steps (LLM, RL)
  # linear_probe   — pretrain ngắn + linear evaluation (self-supervised)

proxy_fraction: 0.25
  # Fraction của full run = proxy run. Range: [0.10, 0.50]
  # Default: 0.25 (25%)
  # Với model lớn/chậm: 0.10
  # Với task không ổn định (RL): 0.50

# proxy_time tự tính: full_run_time × proxy_fraction
# Ví dụ: 2h × 0.25 = 30min
```

### Nhóm 5: Evaluation Protocol

```yaml
protocol: k-fold-cv
  # k-fold-cv      — K-fold cross-validation (medical, small datasets)
  # train-val-test — Fixed splits (large benchmarks: ImageNet, COCO, ...)
  # held-out       — Multiple val sets, one held-out test set
  # online-rl      — Online evaluation during training (RL)
  # human-eval     — Requires human annotators

k: 5
  # Số folds (chỉ dùng nếu protocol = k-fold-cv)

seed: 42
  # Primary random seed
  # Multi-seed: "[42, 0, 1]"

split_level: sample
  # Medical imaging:  patient | slide | patch
  # NLP:              document | sentence | token
  # Vision:           image | video | scene
  # RL:               episode | environment
  # Retrieval:        query | document
```

### Nhóm 6: Kill Signals (cho Proxy Protocol)

```yaml
kill_on_nan: true
  # Luôn để true. NaN loss = immediate kill.

kill_if: "primary_metric < baseline_metric - 0.02 after proxy"
  # Condition để kill proxy run. Viết dạng human-readable.
  # OS check sau khi proxy hoàn thành bằng cách so sánh metric_extract output.
  
  # Ví dụ theo paradigm:
  # Classification: "primary_metric < baseline_metric - 0.02 after proxy"
  # RL:             "mean_reward < 0 for last 10% of proxy steps"
  # Generative:     "val_fid > baseline_fid × 1.5 after proxy"
  # Retrieval:      "primary_metric < baseline_metric × 0.95 after proxy"
  # NLP:            "val_loss > baseline_val_loss × 1.1 after proxy"

proxy_healthy_signal: "train_loss decreasing for first 20% of proxy steps"
  # OPTIONAL. Leading indicator — check TRONG QUÁ TRÌNH proxy, không phải sau.
  # Nếu không healthy sớm → có thể kill trước khi proxy hoàn thành.
  # Để trống nếu không có signal rõ ràng.
```

### Nhóm 7: Baseline Registration

```yaml
baseline_config: "configs/baseline.yaml"
  # Path đến baseline config file (relative to project root)

baseline_result_path: "results/baseline/"
  # Path đến directory chứa baseline results
  # Điền sau khi chạy BASELINE run

baseline_metric: null
  # Số float — primary metric của baseline
  # Điền sau khi BASELINE run hoàn thành
  # Ví dụ: 0.612, 89.3, 245.7, -150.2 (reward)
```

---

## Ví dụ theo từng paradigm

### Supervised Classification (Vision)

```yaml
task_family: discriminative
contribution_type: new_module
baseline_system: "ResNet-50 pretrained on ImageNet, finetuned 100 epochs on CIFAR-10"
proposed_change: "Add Squeeze-and-Excitation block after each residual block"
primary_metric: val_accuracy
metric_direction: higher
dataset: "CIFAR-10"
target_delta: "[TBD]"
train_command: "python train.py --config {config} --output {out_dir}"
eval_command: "none"
metric_extract: "python scripts/parse.py {out_dir}/metrics.json val_accuracy"
full_run_time: "1h"
full_run_unit: total
proxy_strategy: reduced_epochs
proxy_fraction: 0.25
protocol: train-val-test
seed: 42
split_level: image
kill_on_nan: true
kill_if: "primary_metric < baseline_metric - 0.01 after proxy"
baseline_config: "configs/resnet50.yaml"
baseline_result_path: "results/baseline/"
baseline_metric: null
```

### Retrieval / RAG

```yaml
task_family: retrieval
contribution_type: new_module
baseline_system: "BM25 retrieval on SciDocs corpus"
proposed_change: "Cross-encoder re-ranker applied to top-50 BM25 candidates"
primary_metric: recall@10
metric_direction: higher
dataset: "SciDocs-Retrieval"
target_delta: "+5pp"
train_command: "python train_reranker.py --config {config} --output {out_dir}"
eval_command: "python evaluate.py --model {checkpoint} --output {out_dir}"
metric_extract: "python scripts/parse.py {out_dir}/eval.json recall@10"
full_run_time: "30min"
full_run_unit: total
proxy_strategy: reduced_steps
proxy_fraction: 0.25
protocol: train-val-test
seed: 42
split_level: query
kill_on_nan: true
kill_if: "primary_metric < baseline_metric × 0.95 after proxy"
baseline_config: "configs/bm25.yaml"
baseline_result_path: "results/bm25/"
baseline_metric: null
```

### Reinforcement Learning

```yaml
task_family: rl
contribution_type: new_objective
baseline_system: "PPO baseline on HalfCheetah-v2, 1M environment steps"
proposed_change: "Add auxiliary reward prediction head (auxiliary RL)"
primary_metric: episode_reward
metric_direction: higher
dataset: "HalfCheetah-v2"
target_delta: "+500 reward"
train_command: "python train_rl.py --config {config} --logdir {out_dir}"
eval_command: "none"
metric_extract: "python scripts/parse_rl.py {out_dir}/progress.csv episode_reward"
full_run_time: "4h"
full_run_unit: total
proxy_strategy: reduced_steps
proxy_fraction: 0.25
protocol: online-rl
seed: "[42, 0, 1]"
split_level: episode
kill_on_nan: true
kill_if: "mean episode_reward < 0 for last 10% of proxy steps"
proxy_healthy_signal: "episode_reward increasing trend in first 30% of proxy"
baseline_config: "configs/ppo_baseline.yaml"
baseline_result_path: "results/ppo_baseline/"
baseline_metric: null
```

### Generative (Diffusion)

```yaml
task_family: generative
contribution_type: new_module
baseline_system: "DDPM baseline on CelebA-HQ 256x256"
proposed_change: "Add cross-frame attention in UNet decoder"
primary_metric: val_fid
metric_direction: lower
dataset: "CelebA-HQ"
target_delta: "-15 FID points"
train_command: "python train_diffusion.py --config {config} --save_dir {out_dir}"
eval_command: "python compute_fid.py --model_dir {out_dir} --output {out_dir}/fid.json"
metric_extract: "python -c \"import json; print(json.load(open('{out_dir}/fid.json'))['fid'])\""
full_run_time: "12h"
full_run_unit: total
proxy_strategy: reduced_steps
proxy_fraction: 0.10
protocol: train-val-test
seed: 42
split_level: image
kill_on_nan: true
kill_if: "primary_metric > baseline_metric × 1.5 after proxy"
baseline_config: "configs/ddpm_baseline.yaml"
baseline_result_path: "results/ddpm_baseline/"
baseline_metric: null
```

### Self-Supervised Learning

```yaml
task_family: self_supervised
contribution_type: new_objective
baseline_system: "SimCLR baseline pretrained on ImageNet-100"
proposed_change: "Add prototype-based contrastive objective"
primary_metric: linear_probe_accuracy
metric_direction: higher
dataset: "ImageNet-100"
target_delta: "+3pp linear probe"
train_command: "python pretrain.py --config {config} --output {out_dir}"
eval_command: "python linear_eval.py --weights {out_dir}/weights.pth --output {out_dir}"
metric_extract: "python scripts/parse.py {out_dir}/linear_eval.json top1_accuracy"
full_run_time: "6h"
full_run_unit: total
proxy_strategy: linear_probe
proxy_fraction: 0.25
protocol: train-val-test
seed: 42
split_level: image
kill_on_nan: true
kill_if: "primary_metric < baseline_metric - 0.02 after proxy"
baseline_config: "configs/simclr.yaml"
baseline_result_path: "results/simclr_baseline/"
baseline_metric: null
```

---

## OS sử dụng file này như thế nào

| Protocol | Fields sử dụng |
|---------|----------------|
| Proxy run | `proxy_strategy`, `proxy_fraction`, `train_command`, `eval_command`, `metric_extract`, `kill_if`, `kill_on_nan` |
| Hypothesis tournament | `proxy_time` (tính từ `full_run_time × proxy_fraction`), `protocol`, `k`, `seed` |
| Result Adequacy Gate | `primary_metric`, `metric_direction`, `target_delta`, `baseline_metric` |
| Evidence ledger | `dataset`, `split_level`, `protocol`, `seed` |
| Paper writing | `task_family`, `contribution_type`, `baseline_system`, `proposed_change` |
| Gap Scout | `task_family`, `dataset`, `primary_metric` (để search đúng literature) |
| Dialectical Validation | `baseline_system`, `proposed_change` (để viết mechanistic argument đúng paradigm) |

---

## Các lỗi phổ biến khi điền

| Lỗi | Hậu quả | Fix |
|-----|---------|-----|
| `metric_extract` in thêm text ngoài số | OS parse fail | Chỉ print float, không có label/unit |
| `kill_if` quá nghiêm (tolerance nhỏ) | Kill hypothesis tốt quá sớm | Dùng tolerance ≥ 0.5× measurement noise |
| `kill_if` quá lỏng (tolerance lớn) | Chạy hết proxy mới biết thất bại | Calibrate dựa trên prior proxy experiments |
| Điền `target_delta` trước Stage 9 | TRC có thể bị bias | Để `[TBD]` cho đến khi sign TRC |
| `proxy_fraction` quá nhỏ cho RL | Signal quá noisy | RL cần ≥ 0.25, tốt nhất 0.50 |
| `train_command` không có `{out_dir}` | metric_extract không tìm được output | Luôn include `{out_dir}` placeholder |
