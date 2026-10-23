#!/usr/bin/env python3
"""Write the shared <head> blocks into every page: the favicon tags and the Discord component embed.

Run from anywhere: python scripts/build-head.py   (re-run after changing a page's <title> or description)
Each page gets two marker-delimited blocks just before </head>, rewritten in place on every run:
  <!-- favicons --> ... <!-- /favicons -->   on every page (including the 404 and redirect stubs)
  <!-- discord -->  ... <!-- /discord -->    a <script id="discord:component-embed"> custom link preview,
                                              on real pages only (not the 404 or redirect stubs)
Old hand-written <link rel="icon"> / "shortcut icon" tags are removed.

Copyright (c) StuxieDev. All Rights Reserved.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://" + (ROOT / "CNAME").read_text(encoding="utf-8").strip()
ICON_URL = BASE_URL + "/assets/icon.png"
ACCENT = "#dc2626"
SITE_NAME = "TWRAR"
MAX_BYTES = 3000
SKIP_DIRS = {".git", "node_modules", "fontawesome", "__pycache__"}
NO_EMBED = {"404.html", "changelog.html", "assets/steam.html"}  # error page and redirect stubs

FAVICON_BLOCK = """<!-- favicons -->
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="512x512" href="/assets/icon-512.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<!-- /favicons -->"""


def discord_md(s):
    """Escape Discord markdown: inline marks and backslashes anywhere, headings/quotes/lists at a line start."""
    bs = chr(92)  # a callable replacement, so the backslash is literal (a template would read bs+$ as an escape)
    s = re.sub("[" + bs + bs + "*_~`|" + bs + "[" + bs + "]]", lambda m: bs + m.group(0), s)
    return re.sub("(?m)^[#>-]", lambda m: bs + m.group(0), s)


def page_url(rel):
    if rel == "index.html":
        return BASE_URL + "/"
    if rel.endswith("/index.html"):
        return BASE_URL + "/" + rel[: -len("/index.html")]
    return BASE_URL + "/" + rel[: -len(".html")]


def meta(src, pattern):
    m = re.search(pattern, src, re.S)
    return html.unescape(m.group(1)).strip() if m else ""


def buttons(links):
    return {"type": 1, "components": [{"type": 2, "style": 5, "label": label[:80], "url": url} for label, url in links]}


def build_components(rel, title, desc):
    url = page_url(rel)
    site = "-# [" + SITE_NAME + "](" + BASE_URL + "/)\n"
    if rel == "index.html":
        return [
            {"type": 9, "components": [{"type": 10, "content":
                "# [TWRAR](" + BASE_URL + "/)\n**The Website Recorder And Replayer**\n" + discord_md(desc)}],
             "accessory": {"type": 11, "media": {"url": ICON_URL}}},
            {"type": 14},
            {"type": 10, "content": "Free and open source. Setup guides for Windows, macOS and Linux."},
            buttons([("Releases", BASE_URL + "/releases"), ("Guides", BASE_URL + "/guides"),
                     ("GitHub", "https://github.com/TWRAR/Engine")]),
        ]
    links = [("Open", url)]
    if rel != "index.html":
        links.append(("TWRAR home", BASE_URL + "/"))
    return [
        {"type": 9, "components": [{"type": 10, "content":
            site + "## [" + discord_md(title) + "](" + url + ")\n" + discord_md(desc)}],
         "accessory": {"type": 11, "media": {"url": ICON_URL}}},
        buttons(links),
    ]


def discord_payload(components):
    payload = {"component": {"type": 17, "accent_color": int(ACCENT.lstrip("#"), 16), "components": components}}
    js = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\/")
    return js if len(js.encode("utf-8")) <= MAX_BYTES else None


def discord_block(rel, src):
    title = re.sub(r"\s+[\u2014|-]\s+.*$", "", meta(src, r"<title>(.*?)</title>")) or SITE_NAME
    desc = meta(src, r'<meta name="description" content="([^"]*)"')
    js = discord_payload(build_components(rel, title, desc))
    body = ('<!-- discord:component-embed left out: over %d bytes -->' % MAX_BYTES if js is None
            else '<script id="discord:component-embed" type="application/json">' + js + "</script>")
    return "<!-- discord -->\n" + body + "\n<!-- /discord -->"


def build_page(rel, src):
    nl = "\r\n" if "\r\n" in src else "\n"
    text = src.replace("\r\n", "\n")
    text = re.sub(r"<!-- (favicons|discord) -->.*?<!-- /\1 -->\n?", "", text, flags=re.S)
    text = re.sub(r'<link rel="(?:shortcut )?icon"[^>]*>\n', "", text)
    blocks = FAVICON_BLOCK + "\n"
    if rel not in NO_EMBED:
        blocks += discord_block(rel, text) + "\n"
    text = text.replace("</head>", blocks + "</head>", 1)
    return text.replace("\n", nl)


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if not SKIP_DIRS.intersection(p.relative_to(ROOT).parts) and "<head" in p.read_text(encoding="utf-8"):
            yield rel, p


def main():
    changed = 0
    for rel, p in pages():
        src = p.read_bytes().decode("utf-8")
        out = build_page(rel, src)
        if out != src:
            p.write_bytes(out.encode("utf-8"))
            changed += 1
    print("updated %d page(s)" % changed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
