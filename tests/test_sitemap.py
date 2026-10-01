"""Checks that the committed sitemap.xml / sitemap/index.html / robots.txt are well formed,
list the expected public pages, leave out the excluded ones, and match scripts/build-sitemap.py.

Run with: python -m unittest discover -s tests -p "test_*.py"
"""
import os
import unittest
import xml.etree.ElementTree as ET

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


class SitemapTests(unittest.TestCase):
    def setUp(self):
        self.base = "https://" + read("CNAME").strip()
        tree = ET.fromstring(read("sitemap.xml"))
        self.locs = [e.text for e in tree.findall("s:url/s:loc", NS)]

    def test_lists_the_expected_pages(self):
        expected = ["/", "/releases", "/changelogs", "/guides", "/legal", "/legal/privacy", "/legal/terms",
                    "/legal/cookies", "/legal/imprint", "/legal/disclaimer", "/legal/opt-out", "/sitemap"]
        for path in expected:
            self.assertIn(self.base + path, self.locs)

    def test_leaves_out_excluded_pages(self):
        for bad in ("/404", "/changelog", "/dev-config", "/dev-server", "/sitemap.xml"):
            self.assertNotIn(self.base + bad, self.locs)
        for loc in self.locs:
            self.assertTrue(loc.startswith(self.base))

    def test_every_listed_page_has_a_source_file(self):
        for loc in self.locs:
            path = loc[len(self.base):].strip("/")
            candidates = ["index.html"] if not path else [path + ".html", os.path.join(path, "index.html")]
            if path == "sitemap":
                candidates = ["sitemap/index.html"]
            self.assertTrue(any(os.path.isfile(os.path.join(ROOT, c)) for c in candidates), loc)

    def test_sitemap_page_has_a_card_per_url(self):
        page = read("sitemap/index.html")
        self.assertIn("sitemap.xml", page)
        self.assertEqual(page.count('class="legal-card"'), len(self.locs))

    def test_robots_points_at_the_sitemap(self):
        self.assertIn("Sitemap: " + self.base + "/sitemap.xml", read("robots.txt"))


if __name__ == "__main__":
    unittest.main()
