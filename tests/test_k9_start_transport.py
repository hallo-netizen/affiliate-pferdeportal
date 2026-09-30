import copy, importlib.util, json, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("k9_intake",ROOT/"k9_intake.py")
ki=importlib.util.module_from_spec(spec); spec.loader.exec_module(ki)

TARGET={
    "title":"Transport-Test",
    "target_keyword":"Transport Test",
    "category":"reitplatzplaner-faq",
    "article_type":"FAQ",
    "plan_slot":"1"*64
}
PAYLOAD={
    "contract":"PSERC_METADATA_ONLY_READ_ONLY_PREVIEW_V5_DUAL_STRAND",
    "mode":"READ_ONLY_METADATA_ONLY_EXACT_FIVE_FIELDS",
    "next_textmachine_metadata_batch":{
        "contract":"PSERC_TEXTMACHINE_METADATA_BATCH_V2",
        "status":"READY_FOR_TEXTMACHINE_METADATA_INTAKE",
        "publish_allowed":False,
        "content_or_format_payload_present":False,
        "item_count":1,
        "batch_sha256":"2"*64,
        "items":[TARGET]
    }
}

class K9StartTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow=(ROOT/".github/workflows/k9-intake.yml").read_text(encoding="utf-8")

    def test_positive_connector_create_file_starts_auto_chain(self):
        self.assertIn("paths: ['inbox/**.json', 'inbox-auto/**.json']",self.workflow)
        self.assertIn("inbox-auto/*) auto_chain=1",self.workflow)
        self.assertIn('"run_mode":"auto_chain"',self.workflow)
        self.assertIn("text-start-pferdeatelier.yml/dispatches",self.workflow)
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"start.json"
            p.write_text(json.dumps(PAYLOAD,ensure_ascii=False),encoding="utf-8")
            out=ki.convert(p)
        self.assertEqual(out["item_count"],1)
        self.assertEqual(out["items"][0]["metadata"],TARGET)
        self.assertFalse(out["publish_allowed"])

    def test_negative_plain_inbox_is_not_auto_chain_surface(self):
        self.assertFalse("inbox/example.json".startswith("inbox-auto/"))
        self.assertTrue("inbox-auto/example.json".startswith("inbox-auto/"))

    def test_negative_invalid_payload_blocked_before_start(self):
        bad=copy.deepcopy(PAYLOAD)
        bad["mode"]="WRONG_MODE"
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"bad.json"
            p.write_text(json.dumps(bad,ensure_ascii=False),encoding="utf-8")
            with self.assertRaisesRegex(ki.IntakeError,"WORDPRESS_INPUT_MODE_INVALID"):
                ki.convert(p)

if __name__=="__main__": unittest.main()
