# Changelog

All notable changes to this project are documented here. Versioning follows
[Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`), independent
of the [Engine](https://github.com/TWRAR/Engine)'s own version.

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
