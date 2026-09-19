from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
OFFICE = ROOT / "concept_agent"


class IsolationTest(unittest.TestCase):
    def test_office_exists(self):
        self.assertTrue(OFFICE.is_dir())

    def test_python_has_no_relative_escape_imports(self):
        for path in OFFICE.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("isolated_system4", text)
            self.assertNotIn("startmaster", text.lower())
            self.assertNotIn("wordpress", text.lower())
            self.assertNotIn("affiliate", text.lower())
            self.assertNotIn("subprocess", text)
            self.assertNotIn("os.system", text)

    def test_no_symlinks(self):
        for path in OFFICE.rglob("*"):
            self.assertFalse(path.is_symlink(), str(path))


if __name__ == "__main__":
    unittest.main()
