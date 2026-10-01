#!/usr/bin/env python3
"""Regenerate sitemap.xml, sitemap/index.html and robots.txt for this static site.

Run from anywhere: python scripts/build-sitemap.py
PAGES below lists every public page (path, source file); labels and descriptions come from each
page's own <title> and meta description, and each page's <lastmod> is the date of the last git
commit that touched its source file (left out if the file has no history yet). URLs always use
BASE_URL, the site's production address (from CNAME). Redirect stubs (changelog.html), the 404
page and dev-only files are deliberately not listed.

Copyright (c) StuxieDev. All Rights Reserved.
"""
import html
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://" + (ROOT / "CNAME").read_text(encoding="utf-8").strip()

# (path, source file, priority, changefreq); every file that exists is listed
PAGES = [
    ("/", "index.html", "1.0", "weekly"),
    ("/releases", "releases.html", "0.9", "weekly"),
    ("/engine", "engine.html", "0.8", "monthly"),
    ("/profiles", "profiles.html", "0.8", "weekly"),
    ("/guides", "guides/index.html", "0.8", "monthly"),
    ("/guides/install", "guides/install.html", "0.7", "monthly"),
    ("/guides/windows", "guides/windows.html", "0.7", "monthly"),
    ("/guides/linux", "guides/linux.html", "0.7", "monthly"),
    ("/guides/macos", "guides/macos.html", "0.7", "monthly"),
    ("/guides/steam", "guides/steam.html", "0.6", "monthly"),
    ("/guides/developer", "guides/developer.html", "0.6", "monthly"),
    ("/steam", "steam.html", "0.5", "monthly"),
    ("/assets/steam", "assets/steam.html", "0.4", "monthly"),
    ("/changelogs", "changelogs.html", "0.5", "weekly"),
    ("/legal", "legal/index.html", "0.3", "yearly"),
    ("/legal/privacy", "legal/privacy.html", "0.2", "yearly"),
    ("/legal/terms", "legal/terms.html", "0.2", "yearly"),
    ("/legal/cookies", "legal/cookies.html", "0.2", "yearly"),
    ("/legal/imprint", "legal/imprint.html", "0.2", "yearly"),
    ("/legal/disclaimer", "legal/disclaimer.html", "0.2", "yearly"),
    ("/legal/opt-out", "legal/opt-out.html", "0.2", "yearly"),
]
SITEMAP_DESC = "Every page on this site, with a link to the XML version."


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def meta(text: str, pattern: str) -> str:
    m = re.search(pattern, text)
    return html.unescape(m.group(1)).strip() if m else ""


def describe(path: str, src: str):
    text = read(src)
    title = meta(text, r"<title>([^<]*)</title>")
    label = "Home" if path == "/" else re.split(r" [|—] ", title)[0].strip()
    if path == "/legal":
        label = "Boring Legal Stuff"
    desc = meta(text, r'<meta name="description" content="([^"]*)"')
    return label, desc


def lastmod(rel: str) -> str:
    return subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()


def live_pages():
    return [(loc, src, prio, freq) for loc, src, prio, freq in PAGES if (ROOT / src).is_file()]


def build_xml(pages) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, src, priority, freq in pages:
        lines.append("  <url>")
        lines.append(f"    <loc>{html.escape(BASE_URL + loc)}</loc>")
        mod = lastmod(src)
        if mod:
            lines.append(f"    <lastmod>{mod}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("  <url>")
    lines.append(f"    <loc>{html.escape(BASE_URL)}/sitemap</loc>")
    lines.append("    <changefreq>monthly</changefreq>")
    lines.append("    <priority>0.1</priority>")
    lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def build_html(pages) -> str:
    """The sitemap page, in the legal hub's layout (header, theme, footer, banner)."""
    legal = read("legal/index.html")
    head_end = legal.index('<main id="top">')
    main_end = legal.index("</main>") + len("</main>")
    shell_head, shell_foot = legal[:head_end], legal[main_end:]
    site = meta(read("index.html"), r'<meta property="og:site_name" content="([^"]*)"') or "this site"
    title = f"Sitemap — {site}"
    url = BASE_URL + "/sitemap"
    shell_head = re.sub(r"<title>[^<]*</title>", lambda m: f"<title>{html.escape(title)}</title>", shell_head, count=1)
    shell_head = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + html.escape(SITEMAP_DESC) + '"', shell_head, count=1)
    shell_head = re.sub(r'(<meta property="og:description" content=")[^"]*"', lambda m: m.group(1) + html.escape(SITEMAP_DESC) + '"', shell_head, count=1)
    shell_head = re.sub(r'(<meta name="twitter:description" content=")[^"]*"', lambda m: m.group(1) + html.escape(SITEMAP_DESC) + '"', shell_head, count=1)
    shell_head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*"', lambda m: m.group(1) + html.escape(title) + '"', shell_head)
    shell_head = re.sub(r'(<link rel="canonical" href=")[^"]*"', lambda m: m.group(1) + url + '"', shell_head, count=1)
    shell_head = re.sub(r'(<meta property="og:url" content=")[^"]*"', lambda m: m.group(1) + url + '"', shell_head, count=1)
    cards = []
    for loc, src, _p, _f in pages:
        label, desc = describe(loc, src)
        cards.append(f"""        <a href="{html.escape(loc)}" class="legal-card">
          <span class="url">{html.escape(BASE_URL + loc)}</span>
          <h3>{html.escape(label)}</h3>
          <p>{html.escape(desc)}</p>
        </a>""")
    cards.append(f"""        <a href="/sitemap" class="legal-card">
          <span class="url">{html.escape(url)}</span>
          <h3>Sitemap</h3>
          <p>{html.escape(SITEMAP_DESC)}</p>
        </a>""")
    main = f"""<main id="top">

  <section class="hero profiles-hero">
    <div class="container hero-inner">
      <h1 class="page-title">Sitemap</h1>
      <p class="hero-sub">Every page on this site. Looking for the XML version? <a href="/sitemap.xml">sitemap.xml</a></p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="legal-grid">
{chr(10).join(cards)}
      </div>
    </div>
  </section>

</main>"""
    notice = "<!-- Generated by scripts/build-sitemap.py; edit the PAGES list there, then re-run it. -->\n"
    return shell_head.replace("<body>\n", "<body>\n" + notice, 1) + main + shell_foot


def main() -> None:
    pages = live_pages()
    (ROOT / "sitemap").mkdir(exist_ok=True)
    (ROOT / "sitemap" / "index.html").write_text(build_html(pages), encoding="utf-8", newline="\n")
    (ROOT / "sitemap.xml").write_text(build_xml(pages), encoding="utf-8", newline="\n")
    robots = ROOT / "robots.txt"
    line = f"Sitemap: {BASE_URL}/sitemap.xml"
    text = robots.read_text(encoding="utf-8") if robots.exists() else "User-agent: *\nAllow: /\n"
    if line not in text:
        text = text.rstrip("\n") + "\n\n" + line + "\n"
    robots.write_text(text, encoding="utf-8", newline="\n")
    print(f"Wrote sitemap.xml, sitemap/index.html and robots.txt for {BASE_URL} ({len(pages) + 1} pages)")


if __name__ == "__main__":
    main()
