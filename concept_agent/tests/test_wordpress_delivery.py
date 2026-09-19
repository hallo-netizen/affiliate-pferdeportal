import sys, unittest
from pathlib import Path
OFFICE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OFFICE))
from wordpress_delivery import wordpress_delivery_bytes
class WordPressDeliveryFailClosedTest(unittest.TestCase):
    def test_internal_handoff_never_leaves_as_wordpress_file(self):
        with self.assertRaisesRegex(RuntimeError,"WORDPRESS_PACKAGE_BLOCKED"):
            wordpress_delivery_bytes({"contract":"CONCEPT_AGENT_7_ARTICLE_CHAT_HANDOFF_V1"})
    def test_unsigned_preimport_never_leaves_as_wordpress_file(self):
        with self.assertRaisesRegex(RuntimeError,"WORDPRESS_PACKAGE_BLOCKED"):
            wordpress_delivery_bytes({"contract":"PSERC_APPROVED_PRODUCTION_PACKAGE_V1"})
if __name__=="__main__": unittest.main()
