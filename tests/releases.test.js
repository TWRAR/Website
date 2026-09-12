"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const {
  escapeHtml,
  formatBody,
  assetLabel,
  compareAssets,
  formatDate,
} = require("../releases.js");

test("escapeHtml", async (t) => {
  await t.test("escapes the HTML-significant characters", () => {
    assert.equal(escapeHtml("<script>&\"'</script>"), "&lt;script&gt;&amp;\"'&lt;/script&gt;");
  });

  await t.test("coerces non-string input", () => {
    assert.equal(escapeHtml(42), "42");
  });
});

test("formatBody", async (t) => {
  await t.test("returns empty string for empty/missing body", () => {
    assert.equal(formatBody(""), "");
    assert.equal(formatBody(undefined), "");
    assert.equal(formatBody("   \n  "), "");
  });

  await t.test("renders bold markup", () => {
    assert.equal(formatBody("**Full Changelog**"), "<p><strong>Full Changelog</strong></p>");
  });

  await t.test("autolinks a bare URL from generate_release_notes-style bodies", () => {
    const html = formatBody("**Full Changelog**: https://github.com/TWRAR/Engine/compare/v2.0.1...v2.0.2");
    assert.match(html, /<strong>Full Changelog<\/strong>/);
    assert.match(
      html,
      /<a href="https:\/\/github\.com\/TWRAR\/Engine\/compare\/v2\.0\.1\.\.\.v2\.0\.2" target="_blank" rel="noopener">https:\/\/github\.com\/TWRAR\/Engine\/compare\/v2\.0\.1\.\.\.v2\.0\.2<\/a>/
    );
  });

  await t.test("renders markdown links without double-linking the URL", () => {
    const html = formatBody("See [the docs](https://example.com/x) for details.");
    assert.equal(
      html,
      "<p>See <a href=\"https://example.com/x\" target=\"_blank\" rel=\"noopener\">the docs</a> for details.</p>"
    );
  });

  await t.test("escapes malicious content before formatting", () => {
    const html = formatBody("<img src=x onerror=alert(1)>");
    assert.doesNotMatch(html, /<img/);
    assert.match(html, /&lt;img src=x onerror=alert\(1\)&gt;/);
  });

  await t.test("splits paragraphs on blank lines and keeps single newlines as <br>", () => {
    const html = formatBody("first para\nstill first\n\nsecond para");
    assert.equal(html, "<p>first para<br>still first</p><p>second para</p>");
  });
});

test("assetLabel", async (t) => {
  await t.test("labels the current build_exe.py naming scheme by platform", () => {
    assert.equal(assetLabel("TWRAR-windows.exe"), "Windows");
    assert.equal(assetLabel("TWRAR-macos"), "macOS");
    assert.equal(assetLabel("TWRAR-linux"), "Linux");
  });

  await t.test("recognizes the .zip variant of an asset", () => {
    assert.equal(assetLabel("TWRAR-linux.zip"), "Linux");
  });

  await t.test("falls back to the raw filename for unrecognized assets", () => {
    assert.equal(assetLabel("source-code.zip"), "source-code.zip");
  });
});

test("compareAssets", async (t) => {
  await t.test("orders recognized platforms windows, macos, linux", () => {
    const assets = [{ name: "TWRAR-linux" }, { name: "TWRAR-macos" }, { name: "TWRAR-windows.exe" }];
    const sorted = assets.slice().sort(compareAssets).map((a) => a.name);
    assert.deepEqual(sorted, ["TWRAR-windows.exe", "TWRAR-macos", "TWRAR-linux"]);
  });

  await t.test("places unrecognized assets after recognized ones", () => {
    const assets = [{ name: "source-code.zip" }, { name: "TWRAR-linux" }];
    const sorted = assets.slice().sort(compareAssets).map((a) => a.name);
    assert.deepEqual(sorted, ["TWRAR-linux", "source-code.zip"]);
  });
});

test("formatDate", async (t) => {
  await t.test("formats an ISO date string", () => {
    assert.equal(formatDate("2026-09-10T00:00:00Z"), new Date("2026-09-10T00:00:00Z").toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" }));
  });

  await t.test("returns empty string for missing/invalid input", () => {
    assert.equal(formatDate(""), "");
    assert.equal(formatDate(undefined), "");
    assert.equal(formatDate("not-a-date"), "");
  });
});
