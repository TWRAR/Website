# Changelog

All notable changes to this project are documented here. Versioning follows
[Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`), independent
of the [Engine](https://github.com/TWRAR/Engine)'s own version.

## [1.8.4] - 2026-09-14

### Fixed
- **The footer's "Steam Artwork" link pointed at `/assets/steam`**
  (the direct .zip-download redirect) **instead of `/steam`** (the actual
  artwork landing/gallery page) — present on every single page, since the
  footer markup is duplicated per-page rather than templated. The header
  nav's own "Steam Artwork" link was already correct; only the footer
  copy had the wrong target. The three legitimate "Download the artwork
  (.zip)" buttons (on `/steam` and `/guides/steam`) still correctly point
  at `/assets/steam`.

## [1.8.3] - 2026-09-14

### Changed
- **`steam.html` no longer stores its own copy of Steam artwork.**
  `assets/steam/` here was a stale, manually-dropped duplicate that
  nothing kept in sync (this is exactly why it was still showing the
  pre-v3.6.2 icon after the Engine's chrome-dot fix) — removed it
  entirely; the page's preview images now hotlink the Engine repo's raw
  GitHub URLs directly (the single source of truth).
- **The preview gallery only showed 2 of the 6 generated assets**
  (grid capsule and hero, each standing in for a pair). Expanded to one
  card per actual file: both grid capsule orientations, the hero, and
  both logo variants, plus the small library icon.

## [1.8.2] - 2026-09-14

### Fixed
- **`releases.html`'s hero section was missing the "Download Steam
  artwork (.zip)" button** present on the sibling TS4RLS/TIGHC sites —
  added it back, linking to `/assets/steam`.
- The version badge in that same hero section had a hardcoded stale
  "Engine v2.0.2" instead of the "Engine vX.Y.Z" placeholder `versions.js`
  overwrites at runtime — corrected for consistency with the sibling
  sites (cosmetic only, since JS was already replacing the text; only
  affected the pre-JS/no-JS fallback appearance).

## [1.8.1] - 2026-09-14

### Fixed
- Synced `assets/favicon.ico`, `assets/icon.png`, `assets/logo.png`, and
  the site-root `favicon.ico` from the Engine repo's corrected icon (its
  three browser-chrome dots are now aligned to the top-left corner instead
  of drifting toward center — see the Engine's v3.6.2 changelog entry).

## [1.8.0] - 2026-09-13

### Added
- **`favicon.ico`** at the site root, written by the Engine's
  `create_project_assets.py` alongside the existing `assets/favicon.ico`
  — browsers request `/favicon.ico` directly as a fallback regardless of
  the `<link rel="icon">` tag in `<head>`.

## [1.7.2] - 2026-09-13

### Fixed
- **`dev-server.py` had no local equivalent of GitHub Pages' 404
  handling** — `404.html` already existed and is used in production, but
  a missing path returned Python's bare `http.server` error page locally
  instead. Now serves `404.html` the same way TS4RLS/TIGHC's dev servers
  already do it.

## [1.7.1] - 2026-09-12

### Fixed
- **Cache-busting `?v=` query strings were stale on every page** — stuck
  at `1.5.0` (three releases behind `VERSION.md`'s `1.7.0`), and
  `assets/steam.html` even further behind at `1.4.3`. `CONTRIBUTING.md`
  already documented bumping this on every release; it just hadn't been
  done for the last two. Bumped every reference to `?v=1.7.0`.

## [1.7.0] - 2026-09-12

### Added
- **`guides/install.html`** and **`guides/developer.html`** — deploying a
  copy of this site (GitHub Pages/custom domain/any static host) and
  running it locally (cloning alongside the Engine, `dev-server.py`, dev
  mode), adapted from TIGHC's `INSTALL.md`/`DEV_GUIDE.md` content but as
  guide pages instead of root-level markdown files, matching this site's
  own `guides/` pattern. Linked from `/guides` and from the README's
  "Local development"/"Deploying" sections.
- **`404.html`** — a custom error page (GitHub Pages serves it
  automatically for any unmatched path in production, and `dev-server.py`
  already serves `foo.html` for `/foo`, so no server-side change was
  needed here to preview it locally).

### Changed
- **`guides.html` → `guides/index.html`, `legal.html` → `legal/index.html`**
  — each hub page now lives alongside its own sub-pages instead of
  beside the folder. `steam.html` stays a flat file (it has no
  sub-pages). All internal links were already root-relative
  (`/guides`, `/legal`, ...) so nothing else needed updating; only the
  moved pages' own relative asset/script paths gained a `../`.

### Removed
- **`changelog.js`** — a stray, unreferenced one-line placeholder file
  (`changelog.html` redirects client-side and never loaded it).

### Fixed
- README's `Structure` section was an abbreviated summary rather than
  every actual file. Rewrote it to exhaustively list the current file
  set, and added a `Testing` section.

## [1.6.0] - 2026-09-12

### Added
- **CI** (`.github/workflows/ci.yml`), ported from the sibling TIGHC
  project's Website: a `node --test` unit-test job and an
  `html-validate` job over every top-level HTML page.
- **`tests/`**: `changelogs.test.js`, `versions.test.js`, and
  `releases.test.js` — unit tests for the pure logic those scripts
  already exported via `module.exports` but nothing previously
  exercised.

### Fixed
- Two inline `style="..."` attributes on `steam.html`'s preview images
  (`no-inline-style` html-validate failures) — moved into a new
  `.card-preview-img` class in `style.css`.

## [1.5.0] - 2026-09-12

### Added
- **Steam library artwork pages**, matching the sibling TS4RLS project's
  site: `/steam` (landing hub), `/guides/steam` (full asset list + how to
  apply it), and `/assets/steam` (zip-download redirect to the Engine's
  `steam_assets` branch). "Steam Artwork" added to every page's nav and
  footer. `assets/steam/*.png` copied from the Engine's
  `scripts/steam_asset_builder.py` output.

### Fixed
- `guides/windows.html`, `guides/macos.html`, `guides/linux.html` still
  told readers to run `python gui_main.py` - stale since the Engine's
  3.2.0 rename to `gui.py` (the same fix `index.html`/`engine.html` got
  in 1.4.3).

## [1.4.3] - 2026-09-12

### Added
- **Cache-busting `?v=X.Y.Z` query string** on every `assets/logo.png`,
  `assets/icon.png`, and `assets/favicon.ico` reference across every page
  (matching the TS4RLS project's convention), so a released icon/logo
  update isn't served stale from a browser or CDN cache. Documented as a
  release-flow step in `README.md`/`CONTRIBUTING.md`.

### Fixed
- `index.html`/`engine.html` still told readers to run `python
  gui_main.py` - stale since the Engine's 3.2.0 rename to `gui.py`.

## [1.4.2] - 2026-09-12

### Changed
- **Icon/logo (`assets/icon.png`, `assets/logo.png`, `assets/favicon.ico`)
  updated to match the Engine's 3.3.2 update**: the window is now an
  actual rectangle with slightly rounded corners instead of a
  heavily-rounded "squircle", and the wordmark text now aligns to the
  icon's visible window instead of sitting low against it.

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
