---
title: "Minh chứng"
---

<!-- Generated from scientific source; do not edit this copy directly. -->

<div class="source-page source-evidence-index" markdown>

# Chỉ mục minh chứng

<nav class="evidence-map" aria-label="Nhóm minh chứng">
  <a href="#git-evidence"><span>01</span><strong>Git</strong></a>
  <a href="#dataset-evidence"><span>02</span><strong>Dataset</strong></a>
  <a href="#model-evidence"><span>03</span><strong>Model</strong></a>
  <a href="#tracking-evidence"><span>04</span><strong>Tracking</strong></a>
  <a href="#model-evidence"><span>05</span><strong>Behavior</strong></a>
  <a href="#environment-evidence"><span>06</span><strong>Environment</strong></a>
  <a href="#environment-evidence"><span>07</span><strong>Notebook</strong></a>
</nav>


## Git evidence

| Commit | Ngày UTC | Hoạt động | Bài |
| --- | --- | --- | --- |
| [`b3b6d2fadcdd5e38f434cc2041eac51ba773943e`](https://github.com/khkt-tn/fish/commit/b3b6d2fadcdd5e38f434cc2041eac51ba773943e) | 17/08/2026 | Audit dataset Front | J03 |
| [`7e23b580488fe650fb3b379ca97f686d5b8ce9af`](https://github.com/khkt-tn/fish/commit/7e23b580488fe650fb3b379ca97f686d5b8ce9af) | 17/08/2026 | Train YOLOv8n Front | J04 |
| [`4cfac689c08d0f3f25bdee9cb8aac99d3202b9ee`](https://github.com/khkt-tn/fish/commit/4cfac689c08d0f3f25bdee9cb8aac99d3202b9ee) | 17/08/2026 | Evaluate YOLOv8n Front | J04 |
| [`78ed4c11909367c4eef4724991449f74994d917f`](https://github.com/khkt-tn/fish/commit/78ed4c11909367c4eef4724991449f74994d917f) | 17/08/2026 | ByteTrack ablation | J05 |
| [`b0407b726d665e6f7798f35d9c9c6786242bd6fc`](https://github.com/khkt-tn/fish/commit/b0407b726d665e6f7798f35d9c9c6786242bd6fc) | 17/08/2026 | Tracker benchmark | J05 |
| [`622a94b808af2173b584cb6c5148603f93bac19c`](https://github.com/khkt-tn/fish/commit/622a94b808af2173b584cb6c5148603f93bac19c) | 19/08/2026 | Front behavior artifacts và Coral demo code | J06–J08 |
| [`4c582fc012f8e37bf7dd003e034aa7ee1676bed3`](https://github.com/khkt-tn/fish/commit/4c582fc012f8e37bf7dd003e034aa7ee1676bed3) | 29/08/2026 | TOP detection/tracking | J02, J04–J06 |
| [`cc74ce9c4e7873380a0f88d360817f29b472bcd6`](https://github.com/khkt-tn/fish/commit/cc74ce9c4e7873380a0f88d360817f29b472bcd6) | 29/08/2026 | TOP behavior features | J06, J09 |
| [`dbc51a9fec769a9f1754d5ba479f5b77317b39fd`](https://github.com/khkt-tn/fish/commit/dbc51a9fec769a9f1754d5ba479f5b77317b39fd) | 29/08/2026 | Environment–behavior analysis | J09–J10 |

## Model evidence

| Model | Config/log | Result | Bài |
| --- | --- | --- | --- |
| Front YOLOv8n | [`FRONT_DET_YOLOV8N_EVAL_001`](https://github.com/khkt-tn/fish/blob/main/logs/detection/FRONT_DET_YOLOV8N_EVAL_001/summary.json) | [`front_yolov8n_validation_metrics.csv`](https://github.com/khkt-tn/fish/blob/main/results/detection/front_yolov8n_validation_metrics.csv) | J04 |
| Front Random Forest | [`FRONT_BEHAVIOR_MODELS_001`](https://github.com/khkt-tn/fish/blob/main/logs/behavior/FRONT_BEHAVIOR_MODELS_001/summary.json) | [`front_behavior_model_comparison.csv`](https://github.com/khkt-tn/fish/blob/main/results/behavior/front_behavior_model_comparison.csv) | J06 |
| TOP YOLOv8n | [`TOP_DET_YOLOV8N_EVAL_001`](https://github.com/khkt-tn/fish/blob/main/logs/detection/TOP_DET_YOLOV8N_EVAL_001/summary.json) | [`top_yolov8n_validation_metrics.csv`](https://github.com/khkt-tn/fish/blob/main/results/detection/top_yolov8n_validation_metrics.csv) | J04 |

## Dataset evidence

| Dataset/version | Metadata | Audit | Bài |
| --- | --- | --- | --- |
| Front Roboflow v1 | [`roboflow_versions.csv`](https://github.com/khkt-tn/fish/blob/main/logs/data/roboflow_versions.csv) | [`front_dataset_manifest.json`](https://github.com/khkt-tn/fish/blob/main/results/detection/front_dataset_manifest.json) | J03 |
| TOP Roboflow v2 | [`roboflow_versions.csv`](https://github.com/khkt-tn/fish/blob/main/logs/data/roboflow_versions.csv) | [`top_dataset_manifest.json`](https://github.com/khkt-tn/fish/blob/main/results/detection/top_dataset_manifest.json) | J03 |

## Tracking evidence

| Nội dung | Evidence | Bài |
| --- | --- | --- |
| ByteTrack B15/B30/B60 | [`front_bytetrack_ablation.csv`](https://github.com/khkt-tn/fish/blob/main/results/tracking/front_bytetrack_ablation.csv) | J05 |
| ByteTrack và BoT-SORT | [`front_tracker_benchmark.csv`](https://github.com/khkt-tn/fish/blob/main/results/tracking/front_tracker_benchmark.csv) | J05 |
| TOP ByteTrack B15 | [`top_bytetrack_baseline_summary.csv`](https://github.com/khkt-tn/fish/blob/main/results/tracking/top_bytetrack_baseline_summary.csv) | J05–J06 |
| MOT theo segment | [`front_mot_official_metrics_by_segment.csv`](https://github.com/khkt-tn/fish/blob/main/results/tracking/front_mot_official_metrics_by_segment.csv) | J05, J11 |

## Environment evidence

| Artifact | Vai trò | Bài |
| --- | --- | --- |
| [`16_environment_behavior_analysis.ipynb`](https://github.com/khkt-tn/fish/blob/main/notebooks/16_environment_behavior_analysis.ipynb) | Notebook phân tích | J09–J10 |
| [`TOP_ENV_BEHAVIOR_001/summary.json`](https://github.com/khkt-tn/fish/blob/main/logs/environment/TOP_ENV_BEHAVIOR_001/summary.json) | Provenance, giới hạn, quyết định | J09–J10 |
| [`environment_session_summary.csv`](https://github.com/khkt-tn/fish/blob/main/results/environment/environment_session_summary.csv) | Hai phiên và sensor đầu/cuối | J09–J10 |
| [`environment_behavior_summary.csv`](https://github.com/khkt-tn/fish/blob/main/results/environment/environment_behavior_summary.csv) | Tóm tắt cá thể và nhóm | J10 |
| [`environment_behavior_comparison.csv`](https://github.com/khkt-tn/fish/blob/main/results/environment/environment_behavior_comparison.csv) | Sáu so sánh mô tả | J10 |

Chi tiết hơn được tách trong thư mục [`evidence/`](https://github.com/khkt-tn/fish/tree/main/research_diary/evidence).

</div>
