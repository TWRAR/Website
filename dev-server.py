#!/usr/bin/env python3
"""TWRAR Website — local dev server.

Serves this folder the way GitHub Pages does. DEV_MODE is forced on by
default: every .html response gets a fixed dev banner injected right after
<body>, so it's obvious at a glance you're looking at a local build and not
production. Pass --no-dev-mode to serve the files untouched, matching
production exactly.
"""
import http.server
import os
import socketserver
import sys

WEB_DIR = os.path.dirname(os.path.abspath(__file__))

DEV_BANNER = (
    b'<div style="position:sticky;top:0;z-index:9999;background:#dc2626;'
    b'color:#fff;font:600 13px/1.4 system-ui,sans-serif;text-align:center;'
    b'padding:6px 12px">DEV MODE - local build, not production - '
    b'<a href="https://twrar.stuxie.dev" style="color:#fff;text-decoration:underline">'
    b'twrar.stuxie.dev</a></div>'
)


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


def make_handler(dev_mode):
    class DevHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=WEB_DIR, **kwargs)

        def do_GET(self):
            path = self.translate_path(self.path)
            if os.path.isdir(path):
                path = os.path.join(path, "index.html")
            if dev_mode and os.path.isfile(path) and path.endswith(".html"):
                with open(path, "rb") as f:
                    body = f.read()
                body_tag = body.find(b"<body")
                if body_tag != -1:
                    tag_end = body.find(b">", body_tag)
                    if tag_end != -1:
                        insert_at = tag_end + 1
                        body = body[:insert_at] + DEV_BANNER + body[insert_at:]
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            return super().do_GET()

        def log_message(self, fmt, *args):
            sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    return DevHandler


def main():
    port, dev_mode = parse_args(sys.argv[1:])

    print("TWRAR Website running at http://127.0.0.1:%d" % port)
    if dev_mode:
        print("DEV_MODE forced on for this run - every page gets a dev banner.")
        print("Pass --no-dev-mode to serve pages untouched, matching production.")
    else:
        print("DEV_MODE off for this run - pages are served as-is, same as production.")

    with socketserver.TCPServer(("127.0.0.1", port), make_handler(dev_mode)) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
