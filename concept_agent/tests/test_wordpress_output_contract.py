import copy, json, sys, unittest
from pathlib import Path
OFFICE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OFFICE))
from wordpress_output_contract import validate_wordpress_package

FIXTURE=OFFICE/"fixtures"/"wordpress_endstempel_signed_fixture.json"

class WordPressOutputContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pkg=json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_signed_fixture_passes(self):
        self.assertEqual([],validate_wordpress_package(self.pkg))

    def test_concept_agent_chat_handoff_is_rejected(self):
        bad={"contract":"CONCEPT_AGENT_7_ARTICLE_CHAT_HANDOFF_V1"}
        self.assertIn("WP_PACKAGE_CONTRACT_INVALID",validate_wordpress_package(bad))

    def test_article_mutation_breaks_hash(self):
        bad=copy.deepcopy(self.pkg)
        bad["article_manifest"]["articles"][0]["content_utf8"]+="X"
        errors=validate_wordpress_package(bad,verify_signature=False)
        self.assertTrue(any(x.startswith("WP_ARTICLE_HASH_INVALID:") for x in errors))

    def test_signature_is_mandatory(self):
        bad=copy.deepcopy(self.pkg)
        bad["signature_b64"]="AA=="
        errors=validate_wordpress_package(bad)
        self.assertTrue("WP_SIGNATURE_ENCODING_INVALID" in errors or "WP_SIGNATURE_INVALID" in errors)

    def test_publish_allowed_must_stay_false(self):
        bad=copy.deepcopy(self.pkg); bad["publish_allowed"]=True
        self.assertIn("WP_PUBLISH_ALLOWED_MUST_BE_FALSE",validate_wordpress_package(bad,verify_signature=False))

if __name__=="__main__": unittest.main()
