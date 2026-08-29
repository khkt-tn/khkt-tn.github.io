(function () {
  "use strict";

  function populateStats() {
    var root = document.querySelector("[data-journal-index]");
    if (!root) return;

    fetch(root.getAttribute("data-journal-index"))
      .then(function (response) {
        if (!response.ok) throw new Error("Journal index unavailable");
        return response.json();
      })
      .then(function (data) {
        var values = Object.assign({ count: data.count }, data.status_counts);
        document.querySelectorAll("[data-stat]").forEach(function (element) {
          var key = element.getAttribute("data-stat");
          element.textContent = String(values[key] || 0);
        });
      })
      .catch(function () {
        document.querySelectorAll("[data-stat]").forEach(function (element) {
          element.textContent = "—";
        });
      });
  }

  function setupJournalFilters() {
    var buttons = Array.from(
      document.querySelectorAll("[data-journal-filter]")
    );
    var cards = Array.from(document.querySelectorAll("[data-journal-card]"));
    var result = document.querySelector("[data-filter-result]");
    if (!buttons.length || !cards.length) return;

    function applyFilter(status) {
      var visible = 0;
      cards.forEach(function (card) {
        var show =
          status === "ALL" || card.getAttribute("data-status") === status;
        card.hidden = !show;
        if (show) visible += 1;
      });
      buttons.forEach(function (button) {
        var active = button.getAttribute("data-journal-filter") === status;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-pressed", String(active));
      });
      if (result) result.textContent = "Hiển thị " + visible + " bài.";
    }

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        applyFilter(button.getAttribute("data-journal-filter"));
      });
    });
    applyFilter("ALL");
  }

  function textOf(cell) {
    return cell ? cell.textContent.trim() : "";
  }

  function enhanceTimeline() {
    var page = document.querySelector(".source-research-timeline");
    if (!page) return;
    var tables = Array.from(page.querySelectorAll("table"));
    var table = tables.find(function (candidate) {
      var headings = Array.from(candidate.querySelectorAll("th"))
        .map(textOf)
        .join(" ")
        .toLowerCase();
      return headings.indexOf("ngày") >= 0 && headings.indexOf("xác minh") >= 0;
    });
    if (!table) return;

    var headers = Array.from(table.querySelectorAll("thead th")).map(function (
      heading
    ) {
      return textOf(heading).toLowerCase();
    });
    var dateIndex = headers.findIndex(function (heading) {
      return heading.indexOf("ngày") >= 0;
    });
    var activityIndex = headers.findIndex(function (heading) {
      return heading.indexOf("hoạt động") >= 0;
    });
    var statusIndex = headers.findIndex(function (heading) {
      return heading.indexOf("xác minh") >= 0;
    });
    var sourceIndex = headers.findIndex(function (heading) {
      return heading.indexOf("nguồn") >= 0;
    });
    var list = document.createElement("ol");
    list.className = "timeline-list";
    Array.from(table.querySelectorAll("tbody tr")).forEach(function (row) {
      var cells = Array.from(row.children);
      if (cells.length < 3) return;
      var status = textOf(cells[statusIndex]).toUpperCase();
      var item = document.createElement("li");
      item.className = "timeline-item";
      item.setAttribute("data-status", status);
      item.innerHTML =
        '<span class="timeline-marker" aria-hidden="true"></span>' +
        '<div class="timeline-card"><strong>' +
        textOf(cells[dateIndex]) +
        " · " +
        textOf(cells[activityIndex]) +
        "</strong><span>" +
        textOf(cells[statusIndex]) +
        " · " +
        textOf(cells[sourceIndex]) +
        "</span></div>";
      list.appendChild(item);
    });
    if (list.children.length) {
      var wrapper = table.closest(".md-typeset__table") || table;
      wrapper.replaceWith(list);
    }
  }

  function enhanceMedia() {
    var page = document.querySelector(".source-media-index");
    if (!page) return;
    var table = Array.from(page.querySelectorAll("table")).find(function (
      candidate
    ) {
      return /^V\d{2}$/.test(
        textOf(candidate.querySelector("tbody tr td:first-child"))
      );
    });
    if (!table) return;

    var headers = Array.from(table.querySelectorAll("thead th")).map(function (
      heading
    ) {
      return textOf(heading).toLowerCase();
    });
    function column(name) {
      return headers.findIndex(function (heading) {
        return heading.indexOf(name) >= 0;
      });
    }
    var idIndex = column("id");
    var contentIndex = column("nội dung");
    var journalIndex = column("bài sử dụng");
    var statusIndex = column("trạng thái");
    var grid = document.createElement("div");
    grid.className = "media-card-grid";
    Array.from(table.querySelectorAll("tbody tr")).forEach(function (row) {
      var cells = Array.from(row.children);
      if (!cells.length) return;
      var card = document.createElement("article");
      card.className = "media-card";
      var link = row.querySelector('a[href*="youtube.com"], a[href*="youtu.be"]');
      var statusText = cells.map(textOf).join(" ");
      card.innerHTML =
        '<span class="media-card__id">' +
        textOf(cells[idIndex]) +
        "</span><h3>" +
        textOf(cells[contentIndex]) +
        "</h3><p>" +
        "Journal: " +
        textOf(cells[journalIndex]) +
        "</p>" +
        (link
          ? '<a class="youtube-link" href="' +
            link.href +
            '" target="_blank" rel="noopener">Xem trên YouTube ↗</a>'
          : '<span class="status-badge status-todo">' +
            (statusText.indexOf("chờ") >= 0 ||
            statusText.indexOf("TODO") >= 0 ||
            statusText.indexOf("Đang") >= 0
              ? "Chờ video"
              : textOf(cells[statusIndex])) +
            "</span>");
      grid.appendChild(card);
    });
    if (grid.children.length) {
      var wrapper = table.closest(".md-typeset__table") || table;
      wrapper.replaceWith(grid);
    }
  }

  function enhanceYouTubeLinks() {
    document
      .querySelectorAll(
        '.md-content a[href*="youtube.com"], .md-content a[href*="youtu.be"]'
      )
      .forEach(function (link) {
        link.classList.add("youtube-link");
        link.setAttribute("target", "_blank");
        link.setAttribute("rel", "noopener");
      });
  }

  function addFooterLinks() {
    var footer = document.querySelector(".md-footer-meta__inner");
    if (!footer || footer.querySelector(".site-footer-links")) return;
    var nav = document.createElement("nav");
    nav.className = "site-footer-links";
    nav.setAttribute("aria-label", "Liên kết cuối trang");
    nav.innerHTML =
      '<a href="/journal/">Nhật ký</a>' +
      '<a href="/timeline/">Timeline</a>' +
      '<a href="/evidence/">Minh chứng</a>' +
      '<a href="https://github.com/khkt-tn/fish" rel="noopener">GitHub</a>';
    footer.appendChild(nav);
  }

  function initialize() {
    populateStats();
    setupJournalFilters();
    enhanceTimeline();
    enhanceMedia();
    enhanceYouTubeLinks();
    addFooterLinks();
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(initialize);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize);
  } else {
    initialize();
  }
})();
