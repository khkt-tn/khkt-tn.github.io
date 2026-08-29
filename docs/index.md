---
title: Trang chủ
hide:
  - toc
---

<div class="home-page" data-journal-index="assets/data/journal_index.json" markdown>

<section class="research-hero">
  <div class="research-hero__content">
    <p class="eyebrow">FISH AI RESEARCH · NHẬT KÝ KHOA HỌC</p>
    <h1>PHÂN TÍCH HÀNH VI CÁ CẢNH<br>SỬ DỤNG TRÍ TUỆ NHÂN TẠO<br>TỪ DỮ LIỆU HÌNH ẢNH VÀ MÔI TRƯỜNG</h1>
    <p class="research-hero__lead">Hệ thống kết hợp thị giác máy tính, theo dõi đa cá thể, dữ liệu cảm biến môi trường và hệ thống nhúng nhằm định lượng và phân tích hành vi cá cảnh.</p>
    <div class="hero-actions">
      <a class="button button--primary" href="journal/">Xem nhật ký nghiên cứu</a>
      <a class="button button--secondary" href="results/">Xem kết quả</a>
    </div>
  </div>
  <aside class="author-panel" aria-label="Nhóm thực hiện">
    <span class="author-panel__label">HỌC SINH THỰC HIỆN</span>
    <strong>Phạm Duy Quang Anh</strong>
    <strong>Nguyễn Quốc Minh</strong>
    <span>K37 Toán</span>
    <span>THPT Chuyên Thái Nguyên</span>
  </aside>
</section>

<section class="home-section stats-section" aria-labelledby="stats-heading">
  <div class="section-heading">
    <p class="eyebrow">TIẾN ĐỘ CÓ THỂ KIỂM TRA</p>
    <h2 id="stats-heading">Nhật ký trong một lần đọc</h2>
    <p>Số liệu dưới đây được sinh trực tiếp từ YAML front matter của J01–J16.</p>
  </div>
  <div class="stats-grid" aria-live="polite">
    <article class="stat-card">
      <span class="stat-card__label">NHẬT KÝ</span>
      <strong data-stat="count">—</strong>
      <span>bài</span>
    </article>
    <article class="stat-card stat-card--verified">
      <span class="stat-card__label">VERIFIED</span>
      <strong data-stat="VERIFIED">—</strong>
      <span>bài</span>
    </article>
    <article class="stat-card stat-card--partial">
      <span class="stat-card__label">PARTIAL</span>
      <strong data-stat="PARTIAL">—</strong>
      <span>bài</span>
    </article>
    <article class="stat-card stat-card--planned">
      <span class="stat-card__label">PLANNED</span>
      <strong data-stat="PLANNED">—</strong>
      <span>bài</span>
    </article>
  </div>
</section>

<section class="home-section" aria-labelledby="pipeline-heading">
  <div class="section-heading">
    <p class="eyebrow">QUY TRÌNH NGHIÊN CỨU</p>
    <h2 id="pipeline-heading">Từ quan sát đến phân tích khoa học</h2>
  </div>
  <div class="pipeline" role="list" aria-label="Pipeline nghiên cứu">
    <div class="pipeline-step" role="listitem"><span>01</span><strong>CAMERA + SENSOR</strong></div>
    <div class="pipeline-step" role="listitem"><span>02</span><strong>DATASET</strong></div>
    <div class="pipeline-step" role="listitem"><span>03</span><strong>YOLO DETECTION</strong></div>
    <div class="pipeline-step" role="listitem"><span>04</span><strong>BYTETRACK</strong></div>
    <div class="pipeline-step" role="listitem"><span>05</span><strong>BEHAVIOR FEATURES</strong></div>
    <div class="pipeline-step" role="listitem"><span>06</span><strong>ENVIRONMENT SYNC</strong></div>
    <div class="pipeline-step" role="listitem"><span>07</span><strong>SCIENTIFIC ANALYSIS</strong></div>
  </div>
</section>

<section class="home-section research-story" aria-labelledby="story-heading">
  <div class="section-heading">
    <p class="eyebrow">CÂU CHUYỆN NGHIÊN CỨU</p>
    <h2 id="story-heading">Dữ liệu, AI, hành vi và môi trường</h2>
  </div>
  <div class="story-grid">
    <article>
      <span class="story-number">01</span>
      <h3>Dữ liệu quan sát</h3>
      <p>Video TOP/FRONT và dữ liệu cảm biến tạo nên hai nguồn quan sát của hệ thống.</p>
    </article>
    <article>
      <span class="story-number">02</span>
      <h3>AI làm nhiệm vụ gì?</h3>
      <p>YOLO phát hiện cá; ByteTrack hỗ trợ theo dõi để hình thành trajectory theo thời gian.</p>
    </article>
    <article>
      <span class="story-number">03</span>
      <h3>Định lượng hành vi</h3>
      <p>Trajectory được chuyển thành các đặc trưng quan sát được, không suy diễn trạng thái sinh học khi chưa có ground truth.</p>
    </article>
    <article>
      <span class="story-number">04</span>
      <h3>Đối chiếu môi trường</h3>
      <p>Dữ liệu hành vi và môi trường được đồng bộ theo timestamp để phục vụ phân tích mối liên hệ.</p>
    </article>
  </div>
</section>

<section class="home-section" aria-labelledby="experiments-heading">
  <div class="section-heading section-heading--split">
    <div>
      <p class="eyebrow">08 CỤM THÍ NGHIỆM</p>
      <h2 id="experiments-heading">Hành trình thực nghiệm</h2>
    </div>
    <a class="text-link" href="experiments/">Xem toàn bộ thí nghiệm →</a>
  </div>
  <div class="experiment-grid experiment-grid--compact">
    <a class="experiment-card" href="journal/J01_data_acquisition/"><span>EXP-01</span><strong>Thu nhận dữ liệu</strong></a>
    <a class="experiment-card" href="journal/J02_top_front_data_collection/"><span>EXP-02</span><strong>Dữ liệu đa góc nhìn</strong></a>
    <a class="experiment-card" href="journal/J03_roboflow_dataset/"><span>EXP-03</span><strong>Dataset và annotation</strong></a>
    <a class="experiment-card" href="journal/J04_yolo_detection/"><span>EXP-04</span><strong>Phát hiện cá</strong></a>
    <a class="experiment-card" href="journal/J05_fish_tracking/"><span>EXP-05</span><strong>Tracking và hành vi</strong></a>
    <a class="experiment-card" href="journal/J07_raspberry_pi_coral/"><span>EXP-06</span><strong>Triển khai hệ thống nhúng</strong></a>
    <a class="experiment-card" href="journal/J09_sensor_behavior_sync/"><span>EXP-07</span><strong>Đồng bộ môi trường</strong></a>
    <a class="experiment-card" href="journal/J10_environment_behavior_analysis/"><span>EXP-08</span><strong>Phân tích môi trường – hành vi</strong></a>
  </div>
</section>

<section class="evidence-callout">
  <div>
    <p class="eyebrow">EVIDENCE-FIRST</p>
    <h2>Trạng thái nào cũng có ý nghĩa</h2>
    <p><strong>VERIFIED</strong>, <strong>PARTIAL</strong>, <strong>TO_VERIFY</strong> và <strong>PLANNED</strong> được giữ nguyên từ nhật ký nguồn. Git, notebook, log, bảng kết quả và plot được dùng làm đường dẫn kiểm chứng — không thay thế câu chuyện nghiên cứu.</p>
  </div>
  <a class="button button--secondary" href="evidence/">Mở chỉ mục minh chứng</a>
</section>

</div>
