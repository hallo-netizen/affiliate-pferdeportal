import json
from pathlib import Path
import unittest

BRANCH="konzept0-portal-neutral-20261002"

class K0StartRouterTests(unittest.TestCase):
    def test_local_k0_router_is_present_and_pins_k0(self):
        p=Path("K0_START_HERE.md")
        self.assertTrue(p.is_file(),"K0_START_HERE.md missing")
        text=p.read_text(encoding="utf-8")
        self.assertIn("K0:start",text)
        self.assertIn(BRANCH,text)
        self.assertIn("K0_CURRENT_STATE.json",text)
        self.assertNotIn("control/startmaster0107/CURRENT_STATE.json",text)

    def test_current_binds_only_k0_router(self):
        cur=json.loads(Path("K0_CURRENT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(cur["concept"],"K0")
        self.assertEqual(cur["branch"],BRANCH)
        self.assertEqual(cur["work_binding"]["start_command"],"K0:start")
        self.assertEqual(cur["work_binding"]["start_ref"],"K0_START_HERE.md")
        self.assertFalse(cur["work_binding"]["alternate_route_allowed"])
        self.assertFalse(cur["old_chat_or_archive_authority"])

if __name__=="__main__":
    unittest.main()
