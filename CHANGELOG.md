# Changelog

All notable changes to this project are documented here. Versioning follows
[Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`), independent
of the [Engine](https://github.com/TWRAR/Engine)'s own version.

## [1.4.1] - 2026-09-12

### Changed
- **Icon/logo (`assets/icon.png`, `assets/logo.png`, `assets/favicon.ico`)
  updated to match the Engine's new browser-window icon** (chrome/tab bar
  across the top, recording dot + play triangle + cursor inside it) instead
  of a plain rounded square. `favicon.ico` is now generated from the same
  glyph as the app icon (via the Engine's `scripts/generate_icon.py`)
  instead of being maintained by hand.

## [1.4.0] - 2026-09-10

### Added
- **Guides section** (`/guides` hub + `/guides/windows`,
  `/guides/macos`, `/guides/linux`): platform-specific setup notes -
  installation, browser detection behavior, and troubleshooting per OS.
  Linked from the header nav and every page's footer.

### Fixed
- `dev-server.py`'s pretty-URL logic 301-redirected `/legal` and
  `/guides` into their same-named subdirectory instead of serving
  `legal.html`/`guides.html`, since a same-named directory existing took
  priority in the fallback check. Now prefers the sibling `.html` file
  whenever the request doesn't end in `/`, matching how GitHub Pages
  actually resolves this in production.

## [1.3.0] - 2026-09-10

### Changed
- Removed all CLI/hotkeys copy from `index.html` and `engine.html`,
  following Engine v3.0.0's discontinuation of the CLI (GUI-only from
  here on). The Macros feature card/section stays; only the CLI/hotkeys
  half of it is gone.
- Hero/badge copy now says "Windows · macOS · Linux" everywhere,
  matching Engine's new cross-platform release builds.
- `releases.js`'s asset parser now matches the real release-workflow
  naming (`TWRAR-<platform>[.exe|.zip]`) instead of flat Windows-only
  names.
- Background now carries a subtle warm red tint in both themes, and "A
  StuxieDev Project" (footer bottom bar) is muted instead of
  accent-colored, underlining only on hover.

### Added
- Releases page now carries a disclaimer that the CLI was discontinued
  in Engine v3.0.0 and is no longer built or supported.

### Fixed
- The dev-mode banner was showing unconditionally, including in
  production: `.env-banner` was missing a `[hidden] { display: none; }`
  override, so its own `display: flex` rule beat the browser's native
  `hidden` attribute.

## [1.2.0] - 2026-09-10

### Added
- **Engine page** (`/engine`): installation, GUI walkthrough, CLI usage,
  and config shape reference.
- **Releases page** (`/releases` + `releases.js`): live release list
  fetched from the Engine repo's GitHub Releases, with asset download
  links.
- **Changelogs page** (`/changelogs` + `changelogs.js`): tabbed live
  changelog viewer for Engine and Website, matching TIGHC's viewer.
  `/changelog` (singular) redirects to it, matching TIGHC's alias.
- Header nav now links to Engine/Changelogs/Releases on every page;
  footer's Project column links to Changelogs too.
- `dev-server.py` now resolves pretty URLs (`/engine` → `engine.html`)
  locally, matching GitHub Pages' production behavior.

### Fixed
- The dev-mode banner was showing unconditionally, including in
  production: `.env-banner` was missing a `[hidden] { display: none; }`
  override, so its own `display: flex` rule beat the browser's native
  `hidden` attribute. Also reverted its color back to TIGHC/TS4RLS's
  amber/black (an earlier red recolor was wrong).

### Changed
- Background now carries a subtle warm red tint in both themes,
  matching how TIGHC (purple) and TS4RLS (green) tint theirs, instead
  of a neutral gray.
- "A StuxieDev Project" (footer bottom bar) is now muted instead of
  accent-colored, and only underlines on hover.

## [1.1.1] - 2026-09-10

### Changed
- Synced the updated wordmark logo (`assets/logo.png`) from Engine: bold
  tagline in the same red as the icon/acronym.

## [1.1.0] - 2026-09-10

### Added
- FontAwesome 7.3.1 (vendored locally under `assets/fontawesome/`) for
  icons throughout the header, footer, and dev-mode banner.
- `versions.js`: fetches `VERSION.md` live from the Engine and Website
  GitHub repos and fills in the hero/footer version badges.
- Hero version/platform badges, a numbered "How it works" section, and
  a "Get started" section with a clone-and-run code block, matching the
  TIGHC/TS4RLS site layout.
- A real dev-mode banner (hidden `#dev-banner` element on every page,
  revealed by a generated `dev-config.js`), matching TIGHC's current
  implementation, plus sibling-checkout serving (`/dev-sibling/engine`)
  so local Engine content shows up without pushing first.

### Changed
- Rebuilt to match the TIGHC/TS4RLS site structure and CSS system more
  closely: generic `.grid`/`.grid-2`/`.grid-3`/`.card` classes instead of
  bespoke `.feature-grid`/`.feature-card`, and legal sub-pages now use
  the shared hero + `.legal-prose`/`.legal-meta`/`.legal-back` pattern
  instead of a bespoke `.legal-doc` layout.
- Footer "More" column now includes "Written & Maintained by StuxieDev";
  "A StuxieDev Project" moved to its own line in the footer's bottom bar
  on every page (previously only on the homepage).
- `dev-server.py` rewritten to match TIGHC's actual current approach
  (hidden banner + sibling-repo serving) instead of raw HTML injection.

## [1.0.0] - 2026-09-10

### Added
- Initial landing page (`index.html`/`style.css`/`script.js`), red-themed,
  with light/dark mode support.
- The required "Boring Legal Stuff" hub (`legal.html`) and its six
  sub-pages: privacy, terms, cookies, imprint, disclaimer, opt-out.
- `dev-server.py` (+ `dev-server.sh`/`dev-server.bat`): local dev server
  with a forced DEV_MODE banner and a `--no-dev-mode` opt-out.
- `CNAME` for `twrar.stuxie.dev`.
