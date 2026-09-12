"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const { escapeHtml, inlineFormat, sectionClass, parseChangelog } = require("../changelogs.js");

test("escapeHtml", async (t) => {
  await t.test("escapes the HTML-significant characters", () => {
    assert.equal(escapeHtml("<script>&\"'</script>"), "&lt;script&gt;&amp;\"'&lt;/script&gt;");
  });

  await t.test("leaves plain text untouched", () => {
    assert.equal(escapeHtml("hello world"), "hello world");
  });

  await t.test("handles empty string", () => {
    assert.equal(escapeHtml(""), "");
  });

  await t.test("coerces non-string input", () => {
    assert.equal(escapeHtml(42), "42");
  });
});

test("inlineFormat", async (t) => {
  await t.test("renders bold markup", () => {
    assert.equal(inlineFormat("this is **bold** text"), "this is <strong>bold</strong> text");
  });

  await t.test("renders inline code", () => {
    assert.equal(inlineFormat("run `npm test`"), "run <code>npm test</code>");
  });

  await t.test("renders markdown links with target=_blank", () => {
    assert.equal(
      inlineFormat("see [docs](https://example.com/x)"),
      "see <a href=\"https://example.com/x\" target=\"_blank\" rel=\"noopener\">docs</a>"
    );
  });

  await t.test("escapes HTML before applying markdown formatting", () => {
    assert.equal(
      inlineFormat("<b>**bold**</b>"),
      "&lt;b&gt;<strong>bold</strong>&lt;/b&gt;"
    );
  });

  await t.test("does not linkify non-http(s) URLs", () => {
    assert.equal(inlineFormat("[bad](javascript:alert(1))"), "[bad](javascript:alert(1))");
  });

  await t.test("leaves plain prose alone", () => {
    assert.equal(inlineFormat("just plain text"), "just plain text");
  });
});

test("sectionClass", async (t) => {
  await t.test("maps known section titles case-insensitively", () => {
    assert.equal(sectionClass("Added"), "cl-label-added");
    assert.equal(sectionClass("FIXED"), "cl-label-fixed");
    assert.equal(sectionClass("Breaking Changes"), "cl-label-breaking");
    assert.equal(sectionClass("security"), "cl-label-security");
  });

  await t.test("falls back to cl-label-other for unknown sections", () => {
    assert.equal(sectionClass("Deprecated"), "cl-label-other");
    assert.equal(sectionClass(""), "cl-label-other");
  });
});

test("parseChangelog", async (t) => {
  await t.test("parses a version heading, section, and list items", () => {
    const md = [
      "## 1.2.4",
      "",
      "### Added",
      "- one thing",
      "- another thing",
    ].join("\n");

    const html = parseChangelog(md);
    assert.match(html, /<h2 class="cl-version">1\.2\.4<\/h2>/);
    assert.match(html, /<span class="cl-label cl-label-added">Added<\/span>/);
    assert.match(html, /<li>one thing<\/li>/);
    assert.match(html, /<li>another thing<\/li>/);
    assert.match(html, /^<div class="cl-block">/);
    assert.match(html, /<\/div>$/);
  });

  await t.test("renders nested sub-bullets (2-space and tab indented) as cl-sub items", () => {
    const md = [
      "## 1.0.0",
      "### Fixed",
      "- top level",
      "  - nested with spaces",
      "\t- nested with tab",
    ].join("\n");

    const html = parseChangelog(md);
    assert.match(html, /<li>top level<\/li>/);
    assert.match(html, /<li class="cl-sub">nested with spaces<\/li>/);
    assert.match(html, /<li class="cl-sub">nested with tab<\/li>/);
  });

  await t.test("closes an open list before starting a new section or block", () => {
    const md = [
      "## 1.0.0",
      "### Added",
      "- item a",
      "### Fixed",
      "- item b",
    ].join("\n");

    const html = parseChangelog(md);
    // list is closed exactly once between the two sections
    assert.equal((html.match(/<\/ul>/g) || []).length, 2);
    assert.equal((html.match(/<ul class="cl-list">/g) || []).length, 2);
  });

  await t.test("skips the top-level H1 heading", () => {
    const md = "# Changelog\n\nSome intro prose.\n";
    const html = parseChangelog(md);
    assert.doesNotMatch(html, /Changelog<\/h1>/);
    assert.match(html, /<p class="cl-prose">Some intro prose\.<\/p>/);
  });

  await t.test("blank lines close an open list without starting a new block", () => {
    const md = [
      "## 1.0.0",
      "### Added",
      "- item",
      "",
      "some prose after a blank line",
    ].join("\n");

    const html = parseChangelog(md);
    assert.match(html, /<\/ul><p class="cl-prose">some prose after a blank line<\/p>/);
  });

  await t.test("handles an entirely empty changelog", () => {
    assert.equal(parseChangelog(""), "");
  });

  await t.test("handles a changelog with only a version heading and no body", () => {
    const html = parseChangelog("## 2.0.0");
    assert.equal(html, "<div class=\"cl-block\"><h2 class=\"cl-version\">2.0.0</h2></div>");
  });

  await t.test("handles CRLF line endings", () => {
    const md = "## 1.0.0\r\n### Added\r\n- item\r\n";
    const html = parseChangelog(md);
    assert.match(html, /<h2 class="cl-version">1\.0\.0<\/h2>/);
    assert.match(html, /<li>item<\/li>/);
  });

  await t.test("escapes malicious content embedded in a changelog entry", () => {
    const md = "## 1.0.0\n### Added\n- <img src=x onerror=alert(1)>\n";
    const html = parseChangelog(md);
    assert.doesNotMatch(html, /<img/);
    assert.match(html, /&lt;img src=x onerror=alert\(1\)&gt;/);
  });
});
