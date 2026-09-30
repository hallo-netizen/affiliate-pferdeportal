import copy, importlib.util, json, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("k9_intake",ROOT/"k9_intake.py")
ki=importlib.util.module_from_spec(spec); spec.loader.exec_module(ki)

class K9StartTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current=json.loads((ROOT/"CURRENT_STATE.json").read_text(encoding="utf-8"))
        cls.workflow=(ROOT/".github/workflows/k9-intake.yml").read_text(encoding="utf-8")
        cls.ledger=json.loads((ROOT/"state/ledger.json").read_text(encoding="utf-8"))

    def test_positive_connector_create_file_starts_auto_chain(self):
        s=self.current["confirmation_start"]
        self.assertEqual(s["connector_action"],"CREATE_FILE")
        self.assertEqual(s["path_prefix"],"inbox-auto/")
        self.assertIs(s["external_workflow_dispatch_required"],False)
        self.assertIn("paths: ['inbox/**.json', 'inbox-auto/**.json']",self.workflow)
        self.assertIn("inbox-auto/*) auto_chain=1",self.workflow)
        self.assertIn('"run_mode":"auto_chain"',self.workflow)
        self.assertIn("text-start-pferdeatelier.yml/dispatches",self.workflow)
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"start.json"
            p.write_text(json.dumps(s["exact_payload"],ensure_ascii=False),encoding="utf-8")
            out=ki.convert(p)
        self.assertEqual(out["item_count"],1)
        self.assertEqual(out["items"][0]["metadata"],s["exact_target"])
        self.assertFalse(out["publish_allowed"])

    def test_negative_plain_inbox_is_not_auto_chain_surface(self):
        self.assertFalse("inbox/example.json".startswith("inbox-auto/"))
        self.assertTrue("inbox-auto/example.json".startswith("inbox-auto/"))

    def test_negative_invalid_payload_blocked_before_start(self):
        bad=copy.deepcopy(self.current["confirmation_start"]["exact_payload"])
        bad["mode"]="WRONG_MODE"
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"bad.json"
            p.write_text(json.dumps(bad,ensure_ascii=False),encoding="utf-8")
            with self.assertRaisesRegex(ki.IntakeError,"WORDPRESS_INPUT_MODE_INVALID"):
                ki.convert(p)

    def test_confirmation_target_is_not_completed(self):
        slot=self.current["confirmation_start"]["exact_target"]["plan_slot"]
        completed={x["metadata"]["plan_slot"] for x in self.ledger.get("items",[]) if x.get("stages",{}).get("check")=="DONE"}
        self.assertNotIn(slot,completed)

if __name__=="__main__": unittest.main()
