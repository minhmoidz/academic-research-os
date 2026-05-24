# Project Profile

# ⚠️ Điền file này tại Stage 0, trước paper_brief.md.
# OS đọc file này để cấu hình toàn bộ experiment protocols.
# Xem .claude/research-os/33_PROJECT_PROFILE_SPEC.md để biết chi tiết từng field.

---

## Research Paradigm

task_family: "[discriminative | generative | retrieval | rl | self_supervised | structured]"
contribution_type: "[new_module | new_objective | new_architecture | new_dataset | efficiency | new_evaluation]"

---

## The Fundamental Equation
# CLAIM: "Thêm [X] vào [Y] cải thiện [Z] trên [D] thêm [Δ]"

baseline_system: |
  [Mô tả Y: baseline model + training setup. Ví dụ: "ResNet-50 pretrained on ImageNet, finetuned 100 epochs"]

proposed_change: |
  [Mô tả X: thay đổi đề xuất. Ví dụ: "Add cross-attention module after layer3"]

primary_metric: "[val_accuracy | val_auc | val_ndcg@10 | val_fid | episode_reward | ...]"
metric_direction: "[higher | lower]"
dataset: "[Tên dataset hoặc environment]"
target_delta: "[TBD — điền sau khi sign TRC ở Stage 9]"

---

## Experiment Interface
# OS giao tiếp với code của bạn qua 3 commands này.
# Xem 33_PROJECT_PROFILE_SPEC.md để biết ví dụ cho từng paradigm.

train_command: "python train.py --config {config} --output {out_dir}"
# Placeholder BẮT BUỘC: {config}, {out_dir}
# Khi OS muốn proxy run: thêm --proxy flag vào command

eval_command: "none"
# "none" nếu eval tích hợp trong train_command
# Hoặc: "python evaluate.py --model {checkpoint} --output {out_dir}"

metric_extract: "python scripts/parse_metric.py {out_dir}/results.json"
# PHẢI print một float duy nhất ra stdout. Không có text khác.

---

## Compute Profile

full_run_time: "[Xh | Xmin]"
full_run_unit: "[per_fold | per_seed | total | per_episode]"
proxy_strategy: "[reduced_epochs | reduced_data | reduced_steps | linear_probe]"
proxy_fraction: 0.25
# proxy_time (tính tự động) = full_run_time × proxy_fraction

---

## Evaluation Protocol

protocol: "[k-fold-cv | train-val-test | held-out | online-rl | human-eval]"
k: 5
# Số folds — chỉ dùng nếu protocol = k-fold-cv

seed: 42
# Multi-seed: "[42, 0, 1]"

split_level: "[patient | sample | image | document | query | episode | ...]"

---

## Kill Signals

kill_on_nan: true
kill_if: "primary_metric < baseline_metric - 0.02 after proxy"
# Thay đổi cho phù hợp với metric và paradigm của bạn

proxy_healthy_signal: ""
# OPTIONAL. Để trống nếu không có signal rõ ràng.

---

## Baseline Registration
# Điền baseline_metric SAU KHI chạy BASELINE run

baseline_config: "configs/baseline.yaml"
baseline_result_path: "results/baseline/"
baseline_metric: null
# Điền sau BASELINE run. Ví dụ: 0.612, 89.3, -150.2
