---
journal_id: J05
experiment_id: EXP-05
title: "Theo dõi từng cá thể bằng ByteTrack"
date: "2026-08-17"
status: VERIFIED
authors:
  - "Phạm Duy Quang Anh"
  - "Nguyễn Quốc Minh"
tags:
  - tracking
  - bytetrack
  - trajectory
evidence_level: high
last_updated: "2026-08-29"
---
<!-- Generated from scientific source; do not edit this copy directly. -->

# Theo dõi từng cá thể bằng ByteTrack

<section class="journal-meta" aria-label="Thông tin bài nhật ký"><div class="journal-meta__item"><span class="journal-meta__label">Mã nhật ký</span><span class="journal-meta__value">J05</span></div><div class="journal-meta__item"><span class="journal-meta__label">Experiment</span><span class="journal-meta__value">EXP-05</span></div><div class="journal-meta__item"><span class="journal-meta__label">Ngày</span><span class="journal-meta__value">2026-08-17</span></div><div class="journal-meta__item"><span class="journal-meta__label">Trạng thái</span><span class="journal-meta__value"><span class="status-badge status-verified">Đã xác minh · VERIFIED</span></span></div><div class="journal-meta__item"><span class="journal-meta__label">Evidence</span><span class="journal-meta__value">high</span></div><div class="journal-meta__item"><span class="journal-meta__label">Cập nhật</span><span class="journal-meta__value">2026-08-29</span></div></section>


## 1. Mục tiêu

Nối detection giữa các frame thành track đủ liên tục để tính trajectory và đặc trưng hành vi.

## 2. Vấn đề cần giải quyết

Cá giao nhau, che khuất, đi vào nơi không nhìn thấy hoặc bị detector bỏ sót có thể làm tracker mất track, phân mảnh trajectory hoặc đổi ID. Overlay nhiều ID không tự chứng minh tracking đúng.

## 3. Thiết bị, dữ liệu và phần mềm

Front dùng cùng model SHA-256 `750b0f...7738`, video checksum cố định và các YAML ByteTrack B15/B30/B60. TOP sau đó dùng ByteTrack B15 riêng cho hai video TOP.

## 4. Phương pháp thực hiện

Ablation chỉ thay `track_buffer` 15, 30, 60 trong khi giữ threshold. Benchmark Front so ByteTrack B15 với BoT-SORT. Diagnostic gồm coverage khi cá visible, fragment, gap, lifespan, ID count và processing FPS.

## 5. Quá trình thực hiện

Trên video Front một cá, cả B15/B30/B60 có quality diagnostic gần như giống nhau; B15 được chọn tạm thời vì buffer nhỏ nhất khi hòa. Benchmark sau đó cho thấy ByteTrack và BoT-SORT có coverage giống nhau trong bài kiểm tra này, ByteTrack chạy nhanh hơn.

## 6. Kết quả và quan sát

B15 có visible track coverage 0,999143, 2 frame visible không có track, 1 excess fragment và processing khoảng 52,41 FPS trong ablation. Tuy nhiên đây là video một cá. TOP tracking về sau có 33 và 53 unique IDs, nhiều track ngắn và gap, cho thấy identity fragmentation rõ trong bài toán nhiều cá.

## 7. Vấn đề phát sinh

Benchmark một cá không đánh giá đầy đủ crossing hoặc inter-fish occlusion. MOT ground truth hiện có 200 frame/768 object rows; HOTA chưa được tính, và ba segment bị skip official metrics do identity uncertain.

## 8. Điều chỉnh và cải tiến

Nhóm tách true absence/visibility khỏi detector miss trong diagnostic Front, giữ identity uncertain thay vì đoán, và dùng `trajectory_uid` chỉ như segment kỹ thuật. Các tracker dùng cùng detector để tránh so sánh sai biến.

## 9. Kết luận tại thời điểm thực hiện

ByteTrack đã tạo trajectory phục vụ bước đặc trưng, nhưng `track_id` không phải danh tính sinh học. B15 là lựa chọn kỹ thuật tạm thời chứ không phải bằng chứng ByteTrack tối ưu cho mọi video nhiều cá.

## 10. Minh chứng

- [`front_bytetrack_ablation.csv`](https://github.com/khkt-tn/fish/blob/main/results/tracking/front_bytetrack_ablation.csv)
- [`front_tracker_benchmark.csv`](https://github.com/khkt-tn/fish/blob/main/results/tracking/front_tracker_benchmark.csv)
- [`front_mot_official_metrics_by_segment.csv`](https://github.com/khkt-tn/fish/blob/main/results/tracking/front_mot_official_metrics_by_segment.csv)
- [`top_bytetrack_baseline_summary.csv`](https://github.com/khkt-tn/fish/blob/main/results/tracking/top_bytetrack_baseline_summary.csv)
- Commits `78ed4c1`, `b0407b7`, `4c582fc`

## 11. Hình ảnh đề xuất

<!-- TODO_MEDIA:
source: local tracking overlays
timestamp: TO_VERIFY
description: IMG-J05-01 track ID; IMG-J05-02 crossing; IMG-J05-03 trajectory; IMG-J05-04 identity uncertainty/fragmentation
-->

## 12. Video minh họa

> 🎥 **V06 — ByteTrack theo dõi nhiều cá có ID**
>
> YouTube: <span class="media-waiting">Đang chờ cập nhật</span>

## 13. Đóng góp của thành viên

`TO_VERIFY_WITH_STUDENTS`: cần xác nhận người thiết kế ablation, review overlay và làm ground truth.

## 14. Công việc tiếp theo

Trong audit tái lập, xác nhận GT complete, xử lý các segment identity uncertain theo protocol và không tự điền HOTA.
