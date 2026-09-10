#!/usr/bin/env python3
"""TWRAR Website — local dev server.

Serves this folder the way GitHub Pages does. DEV_MODE is forced on by
default: it writes dev-config.js (gitignored, never deployed) so
versions.js fetches Engine/Website content from the sibling checkouts next
to this one (../Engine) instead of GitHub - so local edits to that repo's
CHANGELOG.md/VERSION.md show up here without pushing first - and reveals
the `#dev-banner` element every page already carries (hidden by default),
same env-banner treatment as TIGHC/Stuxs.Tools. Pass --no-dev-mode to fetch
from GitHub instead, matching production (the banner then stays hidden,
since dev-config.js is never written).
"""
import http.server
import os
import socketserver
import sys

WEB_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(WEB_DIR)
SIBLINGS = {
    "engine": os.path.join(PARENT_DIR, "Engine"),
    "website": WEB_DIR,
}


def parse_args(argv):
    port = 8000
    dev_mode = True
    for a in argv:
        if a == "--no-dev-mode":
            dev_mode = False
        elif a.isdigit():
            port = int(a)
        else:
            print("Unknown option: %s" % a, file=sys.stderr)
            sys.exit(1)
    return port, dev_mode


def write_dev_config(dev_mode, port):
    path = os.path.join(WEB_DIR, "dev-config.js")
    if not dev_mode:
        if os.path.exists(path):
            os.remove(path)
        return
    lines = [
        "// Written by dev-server.py at startup - gitignored, never deployed.",
        "window.TWRAR_DEV = {",
        "  repos: {",
        "    engine: '/dev-sibling/engine',",
        "    website: '/dev-sibling/website'",
        "  },",
        "  port: %d" % port,
        "};",
        "(function () {",
        "  var banner = document.getElementById('dev-banner');",
        "  var detail = document.getElementById('dev-banner-detail');",
        "  if (detail) {",
        "    detail.textContent = 'TWRAR Website running on :' + window.TWRAR_DEV.port +",
        "      ' \\u2014 Engine content served from local sibling checkout, not GitHub.';",
        "  }",
        "  if (banner) banner.hidden = false;",
        "})();",
        "console.log('[TWRAR dev mode] Engine/Website content is loaded from local sibling checkouts, not GitHub.');",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


class DevHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def translate_path(self, path):
        path = path.split("?", 1)[0].split("#", 1)[0]
        for key, real_dir in SIBLINGS.items():
            prefix = "/dev-sibling/" + key
            if path == prefix or path.startswith(prefix + "/"):
                rest = path[len(prefix):].lstrip("/")
                return os.path.join(real_dir, *rest.split("/")) if rest else real_dir
        return super().translate_path(path)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main():
    port, dev_mode = parse_args(sys.argv[1:])
    write_dev_config(dev_mode, port)

    print("TWRAR Website running at http://127.0.0.1:%d" % port)
    if dev_mode:
        print("DEV_MODE forced on for this run - Engine/Website content is served")
        print("from %s instead of GitHub." % PARENT_DIR)
        print("Pass --no-dev-mode to fetch from GitHub instead, matching production.")
        if not os.path.isdir(SIBLINGS["engine"]):
            print("Note: %s not found next to Website/ - engine content will 404 locally." % SIBLINGS["engine"])
    else:
        print("DEV_MODE off for this run - Engine/Website content is fetched live from GitHub, same as production.")

    with socketserver.TCPServer(("127.0.0.1", port), DevHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
