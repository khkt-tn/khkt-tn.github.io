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

  function getYouTubeId(url) {
    if (!url) return null;
    try {
      var parsed = new URL(url);
      var host = parsed.hostname.replace(/^www\./, "");
      var parts = parsed.pathname.split("/").filter(Boolean);
      var candidate = null;
      if (host === "youtu.be") {
        candidate = parts[0];
      } else if (host === "youtube.com" || host === "m.youtube.com") {
        if (parsed.pathname === "/watch") {
          candidate = parsed.searchParams.get("v");
        } else if (["embed", "shorts"].indexOf(parts[0]) >= 0) {
          candidate = parts[1];
        }
      }
      return /^[A-Za-z0-9_-]{11}$/.test(candidate || "")
        ? candidate
        : null;
    } catch (_error) {
      return null;
    }
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
    var grid = document.createElement("div");
    grid.className = "media-card-grid";
    Array.from(table.querySelectorAll("tbody tr")).forEach(function (row) {
      var cells = Array.from(row.children);
      if (!cells.length) return;
      var mediaId = textOf(cells[idIndex]);
      var title = textOf(cells[contentIndex]);
      var journal = textOf(cells[journalIndex]);
      var card = document.createElement("article");
      card.className = "media-card";
      card.setAttribute("data-media-id", mediaId);
      var link = row.querySelector('a[href*="youtube.com"], a[href*="youtu.be"]');
      var videoId = getYouTubeId(link ? link.href : "");
      var video = document.createElement("div");
      video.className = "media-card__video";
      if (videoId) {
        var iframe = document.createElement("iframe");
        iframe.src = "https://www.youtube-nocookie.com/embed/" + videoId;
        iframe.title = title;
        iframe.loading = "lazy";
        iframe.setAttribute("frameborder", "0");
        iframe.allow =
          "accelerometer; autoplay; clipboard-write; encrypted-media; " +
          "gyroscope; picture-in-picture; web-share";
        iframe.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
        iframe.allowFullscreen = true;
        video.appendChild(iframe);
      } else {
        video.classList.add("media-card__video--empty");
        var playIcon = document.createElement("span");
        playIcon.className = "media-card__play-icon";
        playIcon.textContent = "▶";
        var placeholder = document.createElement("span");
        placeholder.textContent = "Chưa có video";
        video.appendChild(playIcon);
        video.appendChild(placeholder);
      }
      var body = document.createElement("div");
      body.className = "media-card__body";
      var idLabel = document.createElement("span");
      idLabel.className = "media-card__id";
      idLabel.textContent = mediaId;
      var heading = document.createElement("h3");
      heading.textContent = title;
      var journalLabel = document.createElement("p");
      journalLabel.textContent = "Journal: " + journal;
      body.appendChild(idLabel);
      body.appendChild(heading);
      body.appendChild(journalLabel);
      if (videoId && link) {
        var youtubeLink = document.createElement("a");
        youtubeLink.className = "media-card__youtube-link";
        youtubeLink.href = link.href;
        youtubeLink.target = "_blank";
        youtubeLink.rel = "noopener";
        youtubeLink.textContent = "Mở trên YouTube ↗";
        body.appendChild(youtubeLink);
      }
      card.appendChild(video);
      card.appendChild(body);
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
        if (link.classList.contains("media-card__youtube-link")) return;
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
