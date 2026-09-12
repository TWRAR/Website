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
