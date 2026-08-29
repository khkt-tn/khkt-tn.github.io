---
journal_id: J03
experiment_id: EXP-03
title: "Xây dựng bộ dữ liệu gán nhãn trên Roboflow"
date: "2026-08-14"
status: VERIFIED
authors:
  - "Phạm Duy Quang Anh"
  - "Nguyễn Quốc Minh"
tags:
  - roboflow
  - annotation
  - dataset
evidence_level: high
last_updated: "2026-08-29"
---
<!-- Generated from scientific source; do not edit this copy directly. -->

# Xây dựng bộ dữ liệu gán nhãn trên Roboflow

<section class="journal-meta" aria-label="Thông tin bài nhật ký"><div class="journal-meta__item"><span class="journal-meta__label">Mã nhật ký</span><span class="journal-meta__value">J03</span></div><div class="journal-meta__item"><span class="journal-meta__label">Experiment</span><span class="journal-meta__value">EXP-03</span></div><div class="journal-meta__item"><span class="journal-meta__label">Ngày</span><span class="journal-meta__value">2026-08-14</span></div><div class="journal-meta__item"><span class="journal-meta__label">Trạng thái</span><span class="journal-meta__value"><span class="status-badge status-verified">Đã xác minh · VERIFIED</span></span></div><div class="journal-meta__item"><span class="journal-meta__label">Evidence</span><span class="journal-meta__value">high</span></div><div class="journal-meta__item"><span class="journal-meta__label">Cập nhật</span><span class="journal-meta__value">2026-08-29</span></div></section>


## 1. Mục tiêu

Chuyển video thành tập ảnh có bounding box nhất quán để huấn luyện và đánh giá detector cá.

## 2. Vấn đề cần giải quyết

Frame từ video cần được chọn đại diện, box phải ôm sát cá, không bỏ cá thấy rõ và không tách một cá thành nhiều box. Các frame gần nhau cũng có nguy cơ gây leakage nếu bị chia sang nhiều split.

## 3. Thiết bị, dữ liệu và phần mềm

Front dùng Roboflow workspace `phys-hus`, project `fish_front_detection`, version 1, định dạng YOLOv8. TOP dùng project `fish-top-detection`, version 2. Working copies nằm trong `data/roboflow/` và không được commit.

## 4. Phương pháp thực hiện

Nhóm trích frame, gán một class cá và export theo split do Roboflow cung cấp. Audit sau export kiểm tra số ảnh, label thiếu, box, polygon row, class distribution và cấu trúc split.

## 5. Quá trình thực hiện

Metadata local cho biết Front v1 được export ngày 14/08/2026. Audit Git ngày 17/08 ghi nhận 1.015 ảnh train và 254 ảnh valid. TOP v2 được export và audit ngày 29/08/2026.

## 6. Kết quả và quan sát

Front v1 có 1.269 ảnh và 4.883 annotation rows/boxes: train 3.888, valid 995. Không có test split dùng trong evaluation chính. Dataset có 41 polygon rows ở train và 10 ở valid; Ultralytics cảnh báo và chỉ dùng boxes cho detection.

## 7. Vấn đề phát sinh

Sự pha trộn bbox và polygon là vấn đề định dạng cần ghi lại. Metadata hiện tại cũng chưa chứng minh split theo video nguồn hoặc phân bố T1/T2, nên chưa thể tuyên bố không leakage chỉ từ số lượng ảnh.

## 8. Điều chỉnh và cải tiến

Nhóm lưu manifest, checksum `data.yaml`, source/version và bảng audit nhỏ trong Git. Các lần export sau cần khóa danh sách video nguồn theo split và sửa annotation format nhất quán trước training.

## 9. Kết luận tại thời điểm thực hiện

Dataset Front v1 và TOP v2 được xác minh đủ để tái truy xuất source/version. Front v1 đã hỗ trợ baseline detection, nhưng cảnh báo mixed annotation và thiếu test split phải đi cùng mọi báo cáo metric.

## 10. Minh chứng

- [`front_dataset_manifest.json`](https://github.com/khkt-tn/fish/blob/main/results/detection/front_dataset_manifest.json)
- [`front_dataset_audit_summary.csv`](https://github.com/khkt-tn/fish/blob/main/results/detection/front_dataset_audit_summary.csv)
- [`top_dataset_manifest.json`](https://github.com/khkt-tn/fish/blob/main/results/detection/top_dataset_manifest.json)
- [`roboflow_versions.csv`](https://github.com/khkt-tn/fish/blob/main/logs/data/roboflow_versions.csv)
- Commit [`b3b6d2fadcdd5e38f434cc2041eac51ba773943e`](https://github.com/khkt-tn/fish/commit/b3b6d2fadcdd5e38f434cc2041eac51ba773943e)

## 11. Hình ảnh đề xuất

<!-- TODO_MEDIA:
source: Roboflow project UI
timestamp: N/A
description: IMG-J03-01 màn hình annotation; IMG-J03-02 box đúng; IMG-J03-03 trường hợp chồng lấp; IMG-J03-04 split statistics
-->

## 12. Video minh họa

> 🎥 **V04 — Quá trình gán bounding box trên Roboflow**
>
> YouTube: <span class="media-waiting">Đang chờ cập nhật</span>

## 13. Đóng góp của thành viên

`TO_VERIFY_WITH_STUDENTS`: không suy ra người gán nhãn hoặc người audit từ Git author.

## 14. Công việc tiếp theo

Bổ sung evidence split theo video và hướng dẫn annotation cho các trường hợp cá chồng lấp, sát mép hoặc khó nhìn.
