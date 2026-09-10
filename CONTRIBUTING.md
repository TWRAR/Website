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
`legal.html`'s hub grid and from every page's footer. Keep new/edited
copy in the same plain-English tone as the existing pages.

## Release flow

1. Update `CHANGELOG.md`.
2. Bump `VERSION.md` (semantic versioning).
3. Update `README.md` if structure changed.
4. Run `commit.bat` (or `commit.sh` on POSIX) - it commits everything
   staged/unstaged as `Release vX.Y.Z` and tags `vX.Y.Z`, both read from
   `VERSION.md`.
