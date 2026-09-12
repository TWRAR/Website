"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const { fetchVersion, versionText, REPOS } = require("../versions.js");

function withMockFetch(impl, fn) {
  const original = global.fetch;
  global.fetch = impl;
  return Promise.resolve()
    .then(fn)
    .finally(() => {
      global.fetch = original;
    });
}

test("fetchVersion", async (t) => {
  await t.test("resolves the trimmed VERSION.md contents on success", () => {
    return withMockFetch(
      (url) => {
        assert.equal(url, "https://raw.githubusercontent.com/" + REPOS.engine + "/main/VERSION.md");
        return Promise.resolve({ ok: true, text: () => Promise.resolve("  1.2.4\n") });
      },
      () => fetchVersion("engine").then((v) => assert.equal(v, "1.2.4"))
    );
  });

  await t.test("resolves null on a non-ok HTTP response", () => {
    return withMockFetch(
      () => Promise.resolve({ ok: false, status: 404, text: () => Promise.resolve("") }),
      () => fetchVersion("website").then((v) => assert.equal(v, null))
    );
  });

  await t.test("resolves null when the fetch itself rejects (network error)", () => {
    return withMockFetch(
      () => Promise.reject(new Error("network down")),
      () => fetchVersion("website").then((v) => assert.equal(v, null))
    );
  });

  await t.test("trims a whitespace-only VERSION.md down to an empty string", () => {
    // Note: only a falsy body (e.g. a 0-byte file) yields null here — any
    // non-empty text, even all whitespace, is truthy and gets trim()'d.
    return withMockFetch(
      () => Promise.resolve({ ok: true, text: () => Promise.resolve("   \n  ") }),
      () => fetchVersion("engine").then((v) => assert.equal(v, ""))
    );
  });

  await t.test("resolves null for a genuinely empty response body", () => {
    return withMockFetch(
      () => Promise.resolve({ ok: true, text: () => Promise.resolve("") }),
      () => fetchVersion("engine").then((v) => assert.equal(v, null))
    );
  });

  await t.test("builds a request URL per repo key", () => {
    const requested = [];
    return withMockFetch(
      (url) => {
        requested.push(url);
        return Promise.resolve({ ok: true, text: () => Promise.resolve("9.9.9") });
      },
      () =>
        Promise.all([fetchVersion("engine"), fetchVersion("website")]).then(
          () => {
            assert.equal(requested.length, 2);
            assert.ok(requested[0].includes(REPOS.engine));
            assert.ok(requested[1].includes(REPOS.website));
          }
        )
    );
  });
});

test("versionText", async (t) => {
  await t.test("prefixes the version with v", () => {
    assert.equal(versionText("", "1.2.4"), "v1.2.4");
  });

  await t.test("prepends a caller-supplied prefix", () => {
    assert.equal(versionText("Engine ", "2.0.0"), "Engine v2.0.0");
  });

  await t.test("treats a missing prefix as empty", () => {
    assert.equal(versionText(undefined, "1.0.0"), "v1.0.0");
    assert.equal(versionText(null, "1.0.0"), "v1.0.0");
  });
});
