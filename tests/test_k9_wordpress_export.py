import unittest
import k9_wordpress_export as w

class WordpressExportTests(unittest.TestCase):
    def test_contract_is_compact_02828(self):
        self.assertEqual(w.CONTRACT,"PFERDE_ATELIER_WORDPRESS_IMPORT_V1")
        self.assertEqual(w.PLUGIN_VERSION,"0.28.28")
        self.assertEqual(w.ARTICLE_KEYS,{"article_id","plan_slot","title","slug","target_keyword","category","article_type","body"})

    def test_done_without_repair_is_valid(self):
        row={"revision":0,"stages":{"check":"DONE","repair":"NOT_REQUIRED"},"products":{"check":{}}}
        self.assertTrue(w.ledger_article_done(row))

    def test_done_after_real_repair_is_valid(self):
        row={
            "revision":1,
            "stages":{"check":"DONE","repair":"DONE"},
            "products":{"repair":{"path":"warehouse/repair/x.json"},"check":{"path":"warehouse/check/y.json"}}
        }
        self.assertTrue(w.ledger_article_done(row))

    def test_repair_done_without_revision_is_invalid(self):
        row={
            "revision":0,
            "stages":{"check":"DONE","repair":"DONE"},
            "products":{"repair":{"path":"warehouse/repair/x.json"},"check":{"path":"warehouse/check/y.json"}}
        }
        self.assertFalse(w.ledger_article_done(row))

    def test_pending_repair_is_invalid(self):
        row={"revision":1,"stages":{"check":"FAIL","repair":"PENDING"},"products":{"repair":{},"check":{}}}
        self.assertFalse(w.ledger_article_done(row))

if __name__=="__main__": unittest.main()
