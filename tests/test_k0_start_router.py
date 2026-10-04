import json
from pathlib import Path
import unittest

BRANCH = "konzept0-portal-neutral-20261002"

class K0StartRouterTests(unittest.TestCase):
    def test_local_k0_router_is_article_production_only(self):
        text = Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("K0:start", text)
        self.assertIn("K0_CURRENT_STATE.json", text)
        self.assertNotIn("control/startmaster0107/CURRENT_STATE.json", text)
        self.assertIn("ARTICLE PRODUCTION ONLY", text)

    def test_current_binds_only_article_production(self):
        cur = json.loads(Path("K0_CURRENT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(cur["concept"], "K0")
        self.assertEqual(cur["branch"], BRANCH)
        self.assertEqual(cur["mode"], "ARTICLE_PRODUCTION_ONLY")
        self.assertEqual(cur["start_command"], "K0:start")
        self.assertEqual(cur["start_ref"], "K0_START_HERE.md")
        self.assertEqual(cur["next_action"], "RUN_CURRENT_UPLOAD_ARTICLE_PRODUCTION_ONLY")
        boundary = cur["article_run_boundary"]
        self.assertFalse(boundary["non_article_work_allowed"])
        self.assertFalse(boundary["alternate_route_allowed"])
        self.assertFalse(boundary["other_current_authority_allowed"])

if __name__ == "__main__":
    unittest.main()
