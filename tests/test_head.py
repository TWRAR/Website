"""Checks the shared <head> blocks written by scripts/build-head.py: every page has the favicon tags, every real
page has a valid Discord component embed under 3,000 bytes, and the generated files are up to date.

Run with: python -m unittest discover -s tests -p "test_*.py"
"""
import importlib.util
import json
import os
import re
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
spec = importlib.util.spec_from_file_location("build_head", os.path.join(ROOT, "scripts", "build-head.py"))
bh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bh)

ALLOWED_TYPES = {1, 2, 9, 10, 11, 12, 14, 17}
BUTTON_KEYS = {"id", "type", "url", "style", "label", "emoji", "disabled"}


def walk(node):
    yield node
    for child in node.get("components", []):
        yield from walk(child)
    if "accessory" in node:
        yield from walk(node["accessory"])


def embed_of(src):
    m = re.search(r'<script id="discord:component-embed" type="application/json">(.*?)</script>', src, re.S)
    return m.group(1) if m else None


class HeadTests(unittest.TestCase):
    def setUp(self):
        self.pages = list(bh.pages())

    def test_found_pages(self):
        self.assertGreater(len(self.pages), 15)

    def test_every_page_is_up_to_date(self):
        for rel, p in self.pages:
            src = p.read_bytes().decode("utf-8")
            self.assertEqual(bh.build_page(rel, src), src, rel + ": run python scripts/build-head.py")

    def test_every_head_has_favicon_tags(self):
        for rel, p in self.pages:
            src = p.read_text(encoding="utf-8")
            for needle in ('href="/favicon.ico" sizes="48x48"', 'rel="apple-touch-icon" href="/apple-touch-icon.png"',
                           'rel="manifest" href="/site.webmanifest"', 'sizes="512x512"'):
                self.assertIn(needle, src, rel)
            self.assertNotIn('rel="shortcut icon"', src, rel)

    def test_root_files_exist(self):
        for name in ("favicon.ico", "apple-touch-icon.png", "site.webmanifest"):
            self.assertTrue(os.path.isfile(os.path.join(ROOT, name)), name)
        with open(os.path.join(ROOT, "site.webmanifest"), encoding="utf-8") as f:
            manifest = json.load(f)
        self.assertEqual(manifest["start_url"], "/")
        self.assertIn("maskable", [i.get("purpose") for i in manifest["icons"]])

    def test_embeds(self):
        for rel, p in self.pages:
            js = embed_of(p.read_text(encoding="utf-8"))
            if rel in bh.NO_EMBED:
                self.assertIsNone(js, rel)
                continue
            self.assertIsNotNone(js, rel)
            self.assertLessEqual(len(js.encode("utf-8")), 3000, rel)
            self.assertNotIn("$1", js, rel)
            root = json.loads(js.replace("<\/", "</"))["component"]
            self.assertEqual(root["type"], 17)
            nodes = list(walk(root))
            self.assertLessEqual(len(nodes) - 1, 40)
            for n in nodes[1:]:
                self.assertIn(n["type"], ALLOWED_TYPES, rel)
                self.assertNotEqual(n["type"], 17, rel)
                if n["type"] == 2:
                    self.assertEqual(n["style"], 5)
                    self.assertTrue(set(n) <= BUTTON_KEYS, rel)
                    self.assertRegex(n["url"], r"^https?://")


class EscapingTests(unittest.TestCase):
    def test_markdown_is_escaped_without_literal_dollar_one(self):
        bs = chr(92)
        out = bh.discord_md("a*b_c~d`e|f[g]h" + bs + "i")
        self.assertEqual(out, "".join(bs + c if c in "*_~`|[]" else c for c in "a*b_c~d`e|f[g]h") + bs + bs + "i")
        self.assertNotIn("$1", out)

    def test_line_start_markers_are_escaped(self):
        self.assertEqual(bh.discord_md("# x\n> y\n- z"), "\# x\n\> y\n\- z")

    def test_script_cannot_close_early(self):
        js = bh.discord_payload([{"type": 10, "content": "</script><b>"}])
        self.assertNotIn("</script>", js)
        self.assertIn("<\/script>", js)

    def test_over_limit_is_left_out(self):
        self.assertIsNone(bh.discord_payload([{"type": 10, "content": "x" * 3100}]))


if __name__ == "__main__":
    unittest.main()
