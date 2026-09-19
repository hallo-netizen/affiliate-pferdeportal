from pathlib import Path
import ast
import unittest

ROOT = Path(__file__).resolve().parents[2]
OFFICE = ROOT / "concept_agent"


class IsolationTest(unittest.TestCase):
    def test_office_exists(self):
        self.assertTrue(OFFICE.is_dir())

    def test_python_imports_do_not_escape_office(self):
        forbidden_prefixes=("isolated_system4","control","protocol","startmaster","affiliate")
        for path in OFFICE.rglob("*.py"):
            tree=ast.parse(path.read_text(encoding="utf-8"),filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node,ast.Import):
                    for alias in node.names:
                        self.assertFalse(alias.name.lower().startswith(forbidden_prefixes),(path,alias.name))
                elif isinstance(node,ast.ImportFrom) and node.module:
                    self.assertFalse(node.module.lower().startswith(forbidden_prefixes),(path,node.module))

    def test_no_process_escape(self):
        for path in OFFICE.rglob("*.py"):
            text=path.read_text(encoding="utf-8")
            self.assertNotIn("subprocess",text)
            self.assertNotIn("os.system",text)
            self.assertNotIn("Popen(",text)

    def test_no_symlinks(self):
        for path in OFFICE.rglob("*"):
            self.assertFalse(path.is_symlink(),str(path))


if __name__ == "__main__":
    unittest.main()
