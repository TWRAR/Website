(function () {
  var REPOS = {
    engine:  "TWRAR/Engine",
    website: "TWRAR/Website"
  };
  var DEV = (typeof window !== "undefined") ? window.TWRAR_DEV : undefined;

  function fetchVersion(key) {
    var url = DEV
      ? DEV.repos[key] + "/VERSION.md"
      : "https://raw.githubusercontent.com/" + REPOS[key] + "/main/VERSION.md";
    return fetch(url)
      .then(function (r) { return r.ok ? r.text() : null; })
      .then(function (t) { return t ? t.trim() : null; })
      .catch(function () { return null; });
  }

  function versionText(prefix, ver) {
    return (prefix || "") + "v" + ver;
  }

  if (typeof document !== "undefined") {
    Promise.all([fetchVersion("engine"), fetchVersion("website")])
      .then(function (vers) {
        var map = { engine: vers[0], website: vers[1] };
        window.TWRAR_VERSIONS = map;

        document.querySelectorAll("[data-version]").forEach(function (el) {
          var ver = map[el.dataset.version];
          if (!ver) return;
          el.textContent = versionText(el.dataset.versionPrefix, ver);
        });

        // Inline version spans inside tab buttons (changelogs page)
        document.querySelectorAll("[data-version-inline]").forEach(function (el) {
          var ver = map[el.dataset.versionInline];
          if (ver) el.textContent = " v" + ver;
        });

        document.dispatchEvent(new CustomEvent("twrar-versions", { detail: map }));
      });
  }

  // Exposed for unit tests - pure fetch/format helpers only, no DOM code.
  if (typeof module !== "undefined" && module.exports) {
    module.exports = {
      fetchVersion: fetchVersion,
      versionText: versionText,
      REPOS: REPOS
    };
  }
})();
