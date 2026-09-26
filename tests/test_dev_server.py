"""Tests for dev-server.py's /dev-sibling/ path resolution.

Run with: python -m unittest discover -s tests -p "test_*.py"
(dev-server.py has a hyphen in its name, so it's loaded by file path.)
"""
import importlib.util
import os
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "dev_server", os.path.join(HERE, "..", "dev-server.py")
)
dev_server = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dev_server)


class ResolveSiblingPathTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = os.path.realpath(self._tmp.name)
        self.sibling = os.path.join(self.root, "Engine")
        os.makedirs(os.path.join(self.sibling, "docs"))
        with open(os.path.join(self.root, "secret.txt"), "w") as f:
            f.write("outside")

    def tearDown(self):
        self._tmp.cleanup()

    def test_empty_rest_resolves_to_sibling_root(self):
        self.assertEqual(dev_server.resolve_sibling_path(self.sibling, ""), self.sibling)

    def test_normal_file_inside_sibling_is_allowed(self):
        self.assertEqual(
            dev_server.resolve_sibling_path(self.sibling, "docs/CHANGELOG.md"),
            os.path.join(self.sibling, "docs", "CHANGELOG.md"),
        )

    def test_dotdot_that_stays_inside_is_allowed(self):
        self.assertEqual(
            dev_server.resolve_sibling_path(self.sibling, "docs/../CHANGELOG.md"),
            os.path.join(self.sibling, "CHANGELOG.md"),
        )

    def test_dotdot_escaping_the_sibling_is_rejected(self):
        self.assertIsNone(dev_server.resolve_sibling_path(self.sibling, "../secret.txt"))
        self.assertIsNone(dev_server.resolve_sibling_path(self.sibling, "docs/../../secret.txt"))

    def test_sibling_prefix_lookalike_is_rejected(self):
        # "Engine-evil" shares the "Engine" string prefix but is a different dir.
        os.makedirs(os.path.join(self.root, "Engine-evil"))
        self.assertIsNone(dev_server.resolve_sibling_path(self.sibling, "../Engine-evil/x"))

    def test_rejected_path_does_not_exist(self):
        self.assertFalse(os.path.exists(dev_server.REJECTED_PATH))


if __name__ == "__main__":
    unittest.main()
