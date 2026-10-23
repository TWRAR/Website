<p align="center">
  <img src="assets/logo.png" width="500" alt="TWRAR — The Website Recorder And Replayer">
</p>

# Contributing to TWRAR Website

This repo is the static site for https://twrar.stuxie.dev. It's plain
HTML/CSS/JS with no build step - edit the files directly and preview with
`./dev-server.sh` (or `dev-server.bat`).

For the actual TWRAR tool (the GUI/CLI), see the
[Engine](https://github.com/TWRAR/Engine) repo and its own
`CONTRIBUTING.md` instead.

## Adding a legal page

The six pages under `legal/` are each their own `.html` file, linked from
`legal/index.html`'s hub grid and from every page's footer. Keep
new/edited copy in the same plain-English tone as the existing pages.

## Sitemap

`sitemap.xml`, `sitemap/index.html` and `robots.txt` are generated: after adding or removing a public page, edit the `PAGES` list in `scripts/build-sitemap.py`, run `python scripts/build-sitemap.py`, and commit the result. `python -m unittest discover -s tests` checks them.

## Release flow

1. Update `CHANGELOG.md`.
2. Bump `VERSION.md` (semantic versioning).
3. Update `README.md` if structure changed.
4. **Bump the `?v=X.Y.Z` query string** on every `assets/logo.png`,
   `assets/icon.png`, and `assets/favicon.ico` reference across every
   `.html` page (including `guides/*.html` and `legal/*.html`) to match
   the new version - this cache-busts them so a deploy's updated icon/logo
   doesn't keep getting served stale from a browser or CDN cache. Easiest
   done as a single find-and-replace of the old version string for the new
   one across all pages at once.
5. Run `commit.bat` (or `commit.sh` on POSIX) - it commits everything
   staged/unstaged as `Release vX.Y.Z` and tags `vX.Y.Z`, both read from
   `VERSION.md`.

## Versioning

This project uses [Date Versioning](https://datevers.ing). To release:

1. Add a `## vYY.MM.DD` entry at the top of `CHANGELOG.md`, with its sections in this order: Added, Changed, Fixed, Removed, Security, Deprecated.
2. Set `VERSION.md` to the same bare version (no `v`): today's **UTC** date as `YY.MM.DD`, or `YY.MM.DD-1`, `-2`… for later releases the same UTC day. Never a future date. Use UTC, not local time: just after midnight in the UK it is still the previous day in UTC.
3. Run `bash tests/version.sh`.
4. Run `./commit.sh` (or `commit.bat` on Windows). It checks the version, commits and tags `vYY.MM.DD`, and never pushes.
