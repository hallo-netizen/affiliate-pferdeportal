import json, tempfile, unittest
from pathlib import Path
import k9_pserc, k9_endstempel

class ActiveIntakeScopeTest(unittest.TestCase):
    def _fixture(self, duplicate=False):
        td=tempfile.TemporaryDirectory(); root=Path(td.name)
        (root/"warehouse/intake").mkdir(parents=True)
        ledger={"items":[
            {"item_id":"old-1"},{"item_id":"old-2"},{"item_id":"new-1"},{"item_id":"new-2"}
        ]}
        old={"items":[{"item_id":"old-1"},{"item_id":"old-2"}]}
        cur={"items":[{"item_id":"new-1"},{"item_id":"new-2"}],"source_batch_sha256":"a"*64}
        (root/"warehouse/intake/K9-INTAKE-old.json").write_text(json.dumps(old))
        (root/"warehouse/intake/K9-INTAKE-current.json").write_text(json.dumps(cur))
        if duplicate:
            (root/"warehouse/intake/K9-INTAKE-duplicate.json").write_text(json.dumps(cur))
        return td,root,ledger

    def test_pserc_selects_only_suffix_intake(self):
        td,root,ledger=self._fixture()
        try:
            path,data,items=k9_pserc.active_intake_items(root,ledger)
            self.assertEqual([x["item_id"] for x in items],["new-1","new-2"])
            self.assertEqual(data["source_batch_sha256"],"a"*64)
        finally: td.cleanup()

    def test_endstempel_selects_same_suffix_intake(self):
        td,root,ledger=self._fixture()
        try:
            path,data,items=k9_endstempel.active_intake_items(root,ledger)
            self.assertEqual([x["item_id"] for x in items],["new-1","new-2"])
        finally: td.cleanup()

    def test_ambiguous_suffix_fails_closed(self):
        td,root,ledger=self._fixture(duplicate=True)
        try:
            with self.assertRaises(k9_pserc.Blocked):
                k9_pserc.active_intake_items(root,ledger)
            with self.assertRaises(k9_endstempel.Blocked):
                k9_endstempel.active_intake_items(root,ledger)
        finally: td.cleanup()

if __name__=="__main__":
    unittest.main()
