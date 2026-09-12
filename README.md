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

- `index.html` / `style.css` / `script.js` — the landing page
- `legal.html` + `legal/*.html` — the required "Boring Legal Stuff" hub and
  its six sub-pages (privacy, terms, cookies, imprint, disclaimer, opt-out)
- `assets/` — logo, icon, favicon (copied from
  [Engine](https://github.com/TWRAR/Engine)'s `assets/`)

## Local development

```
./dev-server.sh       # or dev-server.bat on Windows
```

Serves this folder at `http://127.0.0.1:8000` with a dev banner injected
into every page, so it's obvious you're not looking at production. Pass
`--no-dev-mode` to serve pages untouched instead:

```
./dev-server.sh --no-dev-mode
```

## Release flow

1. Update `CHANGELOG.md`.
2. Bump `VERSION.md` (semantic versioning).
3. Update `README.md` if structure changed.
4. Run `commit.bat` (or `commit.sh` on POSIX) - it commits everything
   staged/unstaged as `Release vX.Y.Z` and tags `vX.Y.Z`, both read from
   `VERSION.md`.

---

*Written & Maintained by <img src="https://github.com/StuxieDev.png" height="14" alt="StuxieDev" valign="middle"> [StuxieDev](https://stuxie.dev).*

*[A StuxieDev Project](https://projects.stuxie.dev)*
