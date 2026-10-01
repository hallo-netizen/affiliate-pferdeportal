import unittest
import k9_wordpress_export as w

class WordpressExportTests(unittest.TestCase):
    def test_contract_is_compact_02828(self):
        self.assertEqual(w.CONTRACT,"PFERDE_ATELIER_WORDPRESS_IMPORT_V1")
        self.assertEqual(w.PLUGIN_VERSION,"0.28.28")
        self.assertEqual(w.ARTICLE_KEYS,{"article_id","plan_slot","title","slug","target_keyword","category","article_type","body"})

if __name__=="__main__": unittest.main()
