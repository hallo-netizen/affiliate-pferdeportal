import json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch

import k9_terminal_preflight as t

class TerminalPreflightTests(unittest.TestCase):
    def fixture(self,root,repair="NOT_REQUIRED",revision=0):
        (root/"state").mkdir(parents=True)
        status={
            "active_job":None,"remaining":0,"repair_required":0,
            "total":1,"fully_done":1
        }
        item={
            "item_id":"I1","revision":revision,
            "metadata":{"title":"T","target_keyword":"K","category":"c","article_type":"FAQ","plan_slot":"S1"},
            "stages":{"check":"DONE","repair":repair},
            "products":{"check":{"path":"c"}}
        }
        if repair=="DONE":
            item["products"]["repair"]={"path":"r"}
        (root/"state/STATUS.json").write_text(json.dumps(status))
        (root/"state/ledger.json").write_text(json.dumps({"contract":"K9_LEDGER_V1","items":[item]}))
        return item

    def test_terminal_preflight_passes_exact_ready_state(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); item=self.fixture(root)
            intake={"item_count":1,"batch_sha256":"B"}
            pserc={"contract":"K9_PSERC_RESULT_V1","status":"PASS","bridge_status":"PSERC_FINAL_INTEGRITY_ONLY_PASS","article_count":1,"publish_allowed":False}
            out=root/"pserc.json"
            with patch.object(t.k9_pserc,"active_intake_items",return_value=(Path("x"),intake,[item])),                  patch.object(t.k9_pserc,"run",return_value=pserc),                  patch.object(t.k9_wordpress_export,"ledger_article_done",return_value=True):
                result=t.run(root,Path("ppm"),Path("pserc"),out)
            self.assertEqual(result["status"],"PASS")
            self.assertEqual(result["wordpress_ledger_readiness"],"PASS")
            self.assertTrue(out.is_file())

    def test_terminal_preflight_blocks_wordpress_ledger_state_before_finalizer(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); item=self.fixture(root,repair="PENDING")
            intake={"item_count":1,"batch_sha256":"B"}
            with patch.object(t.k9_pserc,"active_intake_items",return_value=(Path("x"),intake,[item])),                  patch.object(t.k9_wordpress_export,"ledger_article_done",return_value=False):
                with self.assertRaisesRegex(t.Blocked,"TERMINAL_WORDPRESS_LEDGER_STATE_INVALID"):
                    t.run(root,Path("ppm"),Path("pserc"),root/"out.json")

    def test_terminal_preflight_blocks_pserc_before_finalizer(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); item=self.fixture(root)
            intake={"item_count":1,"batch_sha256":"B"}
            bad={"contract":"K9_PSERC_RESULT_V1","status":"BLOCKED","bridge_status":"NO","article_count":1}
            with patch.object(t.k9_pserc,"active_intake_items",return_value=(Path("x"),intake,[item])),                  patch.object(t.k9_pserc,"run",return_value=bad),                  patch.object(t.k9_wordpress_export,"ledger_article_done",return_value=True):
                with self.assertRaisesRegex(t.Blocked,"TERMINAL_PSERC_NOT_PASS"):
                    t.run(root,Path("ppm"),Path("pserc"),root/"out.json")

if __name__=="__main__": unittest.main()
