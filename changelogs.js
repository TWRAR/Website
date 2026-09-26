(function () {
  var DEV = (typeof window !== "undefined") ? window.TWRAR_DEV : undefined;
  var REPOS = DEV ? {
    engine:  DEV.repos.engine + "/CHANGELOG.md",
    website: DEV.repos.website + "/CHANGELOG.md"
  } : {
    engine:  "https://raw.githubusercontent.com/TWRAR/Engine/main/CHANGELOG.md",
    website: "https://raw.githubusercontent.com/TWRAR/Website/main/CHANGELOG.md"
  };

  var SECTION_CLASSES = {
    "added":            "cl-label-added",
    "changed":          "cl-label-changed",
    "fixed":            "cl-label-fixed",
    "removed":          "cl-label-removed",
    "breaking changes": "cl-label-breaking",
    "security":         "cl-label-security",
    "deprecated":       "cl-label-deprecated"
  };

  // Fixed display order for "### <Type>" sections within a release -
  // sections are sorted into this order at render time rather than
  // trusting the order they appear in the markdown. Unknown types
  // (e.g. "Breaking Changes") keep their relative order and go last.
  var SECTION_ORDER = ["added", "changed", "fixed", "removed", "security", "deprecated"];

  function sectionRank(title) {
    var idx = SECTION_ORDER.indexOf(String(title).trim().toLowerCase());
    return idx === -1 ? SECTION_ORDER.length : idx;
  }

  // Reorders the "### " sections inside each "## " release block of a
  // changelog's markdown into SECTION_ORDER. Anything before a release's
  // first "### " heading (prose, etc.) stays put; each section moves as a
  // whole (its heading plus every line up to the next "### "/"## ").
  function sortSections(md) {
    var lines = String(md).split("\n");
    var out = [];
    var sections = null;

    function flush() {
      if (!sections) return;
      sections
        .map(function (sec, i) { return { sec: sec, i: i }; })
        .sort(function (a, b) {
          return (sectionRank(a.sec.title) - sectionRank(b.sec.title)) || (a.i - b.i);
        })
        .forEach(function (entry) {
          var body = entry.sec.lines;
          // Keep a moved section separated from the one before it.
          var prev = out.length ? out[out.length - 1].replace(/\r$/, "") : "";
          if (prev.trim() !== "" && !/^#{1,2} /.test(prev)) {
            out.push("");
          }
          Array.prototype.push.apply(out, body);
        });
      sections = null;
    }

    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].replace(/\r$/, "");
      if (/^#{1,2} /.test(line)) {
        flush();
        out.push(lines[i]);
      } else if (/^### /.test(line)) {
        if (!sections) sections = [];
        sections.push({ title: line.replace(/^### /, ""), lines: [lines[i]] });
      } else if (sections) {
        sections[sections.length - 1].lines.push(lines[i]);
      } else {
        out.push(lines[i]);
      }
    }
    flush();
    return out.join("\n");
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function inlineFormat(text) {
    var escaped = escapeHtml(text);
    // **bold**
    escaped = escaped.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    // `code`
    escaped = escaped.replace(/`([^`]+)`/g, "<code>$1</code>");
    // [label](url)
    escaped = escaped.replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g,
      "<a href=\"$2\" target=\"_blank\" rel=\"noopener\">$1</a>");
    return escaped;
  }

  function sectionClass(title) {
    return SECTION_CLASSES[title.toLowerCase()] || "cl-label-other";
  }

  function parseChangelog(md) {
    var lines = sortSections(md).split("\n");
    var html = "";
    var inList = false;
    var inBlock = false;

    for (var i = 0; i < lines.length; i++) {
      var raw = lines[i];
      var line = raw.replace(/\r$/, "");

      if (/^## /.test(line)) {
        if (inList) { html += "</ul>"; inList = false; }
        if (inBlock) { html += "</div>"; inBlock = false; }
        var ver = line.replace(/^## /, "").trim();
        html += "<div class=\"cl-block\"><h2 class=\"cl-version\">" + escapeHtml(ver) + "</h2>";
        inBlock = true;

      } else if (/^### /.test(line)) {
        if (inList) { html += "</ul>"; inList = false; }
        var sec = line.replace(/^### /, "").trim();
        html += "<span class=\"cl-label " + sectionClass(sec) + "\">" + escapeHtml(sec) + "</span>";

      } else if (/^  - |^\t- /.test(raw)) {
        if (!inList) { html += "<ul class=\"cl-list\">"; inList = true; }
        html += "<li class=\"cl-sub\">" + inlineFormat(line.replace(/^\s+- /, "")) + "</li>";

      } else if (/^- /.test(line)) {
        if (!inList) { html += "<ul class=\"cl-list\">"; inList = true; }
        html += "<li>" + inlineFormat(line.replace(/^- /, "")) + "</li>";

      } else if (line.trim() === "") {
        if (inList) { html += "</ul>"; inList = false; }

      } else if (/^# /.test(line)) {
        // top-level heading - skip, the page has its own h1

      } else if (line.trim()) {
        if (inList) { html += "</ul>"; inList = false; }
        html += "<p class=\"cl-prose\">" + inlineFormat(line.trim()) + "</p>";
      }
    }

    if (inList) html += "</ul>";
    if (inBlock) html += "</div>";
    return html;
  }

  function loadPanel(key) {
    var panel = document.getElementById("cl-" + key);
    if (!panel || panel.dataset.loaded) return;
    panel.dataset.loaded = "1";

    fetch(REPOS[key])
      .then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status);
        return res.text();
      })
      .then(function (md) {
        panel.innerHTML = parseChangelog(md);
      })
      .catch(function (err) {
        panel.innerHTML = "<p class=\"cl-error\">Couldn't fetch changelog (" +
          escapeHtml(err.message) + ").</p>";
      });
  }

  if (typeof document !== "undefined") {
    var tabs = document.querySelectorAll(".cl-tab");
    var panels = document.querySelectorAll(".cl-panel");

    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        tabs.forEach(function (t) { t.classList.remove("active"); });
        panels.forEach(function (p) { p.classList.remove("active"); });
        tab.classList.add("active");
        var key = tab.dataset.repo;
        var panel = document.getElementById("cl-" + key);
        if (panel) panel.classList.add("active");
        loadPanel(key);
      });
    });

    loadPanel("engine");
  }

  // Exposed for unit tests - pure parsing/formatting logic only, no
  // DOM/network code is exported or invoked here.
  if (typeof module !== "undefined" && module.exports) {
    module.exports = {
      escapeHtml: escapeHtml,
      inlineFormat: inlineFormat,
      sectionClass: sectionClass,
      sectionRank: sectionRank,
      sortSections: sortSections,
      SECTION_ORDER: SECTION_ORDER,
      parseChangelog: parseChangelog
    };
  }
})();
