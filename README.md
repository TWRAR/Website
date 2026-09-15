<p align="center">
  <img src="assets/logo.png" width="300" alt="TWRAR — The Website Recorder And Replayer">
</p>

# TWRAR Website

Source for [twrar.stuxie.dev](https://twrar.stuxie.dev), the landing site
for [TWRAR](https://github.com/TWRAR) (The Website Recorder And Replayer).

See [CHANGELOG.md](CHANGELOG.md) for release history.

Website: https://twrar.stuxie.dev  
Repository: https://github.com/TWRAR/Website  
License: [GPL-3.0-or-later](LICENSE.md)

---

## Structure

Plain HTML/CSS/JS, no build step, deployed via GitHub Pages (see `CNAME`):

```
index.html               # landing page — what TWRAR is, features, how it works, get started
engine.html               # install/usage docs for the Engine
changelogs.html           # tabbed changelog viewer (Engine / Website)
changelogs.js             # fetches and renders CHANGELOG.md from each repo for changelogs.html
changelog.html            # redirect alias for /changelogs (singular → plural)
releases.html             # TWRAR Engine releases, fetched live from the GitHub Releases API
releases.js               # fetches and renders TWRAR/Engine's GitHub releases for releases.html
steam.html                # Steam library artwork landing hub (no sub-pages, so no /steam folder)
404.html                  # custom error page, served automatically by GitHub Pages
favicon.ico               # site-root copy browsers fall back to regardless of <link rel="icon">
style.css                 # shared styles
script.js                 # mobile nav toggle and the light/dark theme toggle
versions.js               # fetches VERSION.md from Engine/Website on load, populates version badges
CNAME                     # custom domain (twrar.stuxie.dev) for GitHub Pages

legal/index.html          # "Boring Legal Stuff" hub, linking to legal/*.html
legal/privacy.html
legal/terms.html
legal/cookies.html
legal/imprint.html
legal/disclaimer.html
legal/opt-out.html

guides/index.html         # setup guides hub, linking to guides/*.html
guides/windows.html
guides/macos.html
guides/linux.html
guides/steam.html         # full "add TWRAR to Steam" artwork guide
guides/install.html       # deploying a copy of this site (see Deploying below)
guides/developer.html     # running this site locally (see Local development below)

assets/icon.png           # copied from the Engine repo's assets/
assets/logo.png
assets/favicon.ico
assets/steam.html         # /assets/steam — redirects to the Engine's TWRAR Steam assets zip
assets/steam/*.png        # generated Steam library artwork (6 files), copied from the
                          # Engine's scripts/steam_asset_builder.py output
assets/fontawesome/       # Font Awesome Free (vendored, self-hosted — see its own LICENSE.txt)

tests/changelogs.test.js  # node:test unit tests for changelogs.js
tests/releases.test.js    # node:test unit tests for releases.js
tests/versions.test.js    # node:test unit tests for versions.js
.github/workflows/ci.yml  # runs `node --test` and html-validate on every push/PR

dev-server.py             # local dev server shared by dev-server.sh/.bat (see Local development below)
dev-server.sh             # Unix wrapper for dev-server.py
dev-server.bat            # Windows wrapper for dev-server.py

CHANGELOG.md / VERSION.md / CONTRIBUTING.md / LICENSE.md
commit.sh / commit.bat    # commit + tag a release, reading the version from VERSION.md
.gitignore
```

## Local development

See [/guides/developer](https://twrar.stuxie.dev/guides/developer) to run
the site locally.

```
./dev-server.sh       # or dev-server.bat on Windows
```

Serves this folder at `http://127.0.0.1:8000` with a dev banner injected
into every page, so it's obvious you're not looking at production. Pass
`--no-dev-mode` to serve pages untouched instead:

```
./dev-server.sh --no-dev-mode
```

## Deploying

GitHub Pages is configured to serve from this repo's root on `main` — just
push. The `CNAME` file points the custom domain at GitHub Pages; don't
remove it unless the domain setup is changing too. See
[/guides/install](https://twrar.stuxie.dev/guides/install) for
self-hosting elsewhere.

## Testing

The parsing/formatting logic in `changelogs.js`, `releases.js`, and
`versions.js` (changelog Markdown parsing, release-notes formatting and
asset labeling/sorting, version-string handling) has unit tests under
`tests/`, using Node's built-in test runner — no extra dependencies
required:

```
node --test
```

CI (`.github/workflows/ci.yml`) runs these tests and validates the
top-level HTML pages with [html-validate](https://html-validate.org/) on
every push and pull request.

## Release flow

1. Update `CHANGELOG.md`.
2. Bump `VERSION.md` (semantic versioning).
3. Update `README.md` if structure changed.
4. Bump the `?v=X.Y.Z` query string on every `logo.png`/`icon.png`/
   `favicon.ico` reference across all pages (see `CONTRIBUTING.md`).
5. Run `commit.bat` (or `commit.sh` on POSIX) - it commits everything
   staged/unstaged as `Release vX.Y.Z` and tags `vX.Y.Z`, both read from
   `VERSION.md`.

---

*Written & Maintained by <img src="https://global.media.stuxie.dev/icon.png" height="14" alt="StuxieDev" valign="middle"> [StuxieDev](https://stuxie.dev).*

*[A StuxieDev Project](https://projects.stuxie.dev)*
