import json, unittest
from unittest.mock import patch
import k9_write_packager as w

class WriterCollectAllTests(unittest.TestCase):
    def test_batch_collects_all_item_failures(self):
        drafts=[
            {"item_id":"A","content_html":"x"},
            {"item_id":"B","content_html":"y"},
        ]
        def fail(job,entry,rules,rules_sha,row,lt_jar=None):
            raise w.PackError("FAIL_"+row["item_id"])
        with patch.object(w,"_build_single",side_effect=fail):
            with self.assertRaises(w.PackError) as cm:
                w.build_rows({}, {}, {}, "sha", drafts)
        reason=str(cm.exception)
        self.assertIn("WRITER_BATCH_ALL_FINDINGS",reason)
        self.assertIn('"item_id":"A"',reason)
        self.assertIn('"item_id":"B"',reason)
        self.assertIn("FAIL_A",reason)
        self.assertIn("FAIL_B",reason)

if __name__=="__main__": unittest.main()
