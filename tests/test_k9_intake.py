import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SRC=Path(__file__).resolve().parents[1]/"k9_intake.py"
spec=importlib.util.spec_from_file_location("k9_intake",SRC)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def source(self):
        return {
            "contract":"PSERC_METADATA_ONLY_READ_ONLY_PREVIEW_V5_DUAL_STRAND",
            "mode":"READ_ONLY_METADATA_ONLY_EXACT_FIVE_FIELDS",
            "next_textmachine_metadata_batch":{
                "contract":"PSERC_TEXTMACHINE_METADATA_BATCH_V2",
                "status":"READY_FOR_TEXTMACHINE_METADATA_INTAKE",
                "item_count":1,
                "publish_allowed":False,
                "content_or_format_payload_present":False,
                "batch_sha256":"source-batch",
                "items":[{
                    "article_type":"Beratung",
                    "category":"reitplatzplaner-beratung",
                    "plan_slot":"0b401802eeed8574d9c80f7eb5e1abb03c0ac5dbf82fa8b8a95deb7abf3bec15",
                    "target_keyword":"Reitplatzplaner für Pferde",
                    "title":"Das Wichtigste über Reitplatzplaner für Pferde"
                }]
            }
        }

    def write(self,data,name="input.json"):
        p=self.root/name
        p.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8")
        return p

    def test_real_shape_becomes_native_exact_five_fields(self):
        out=m.convert(self.write(self.source()))
        self.assertEqual(out["contract"],"K9_INTAKE_V1")
        self.assertEqual(out["item_count"],1)
        self.assertFalse(out["publish_allowed"])
        item=out["items"][0]
        self.assertTrue(item["item_id"].startswith("k9-"))
        self.assertEqual(set(item["metadata"]),set(m.FIELDS))
        self.assertEqual(item["metadata"]["title"],item["title"])

    def test_same_input_has_same_batch_and_item_identity(self):
        p=self.write(self.source())
        a=m.convert(p); b=m.convert(p)
        self.assertEqual(a["batch_id"],b["batch_id"])
        self.assertEqual(a["batch_sha256"],b["batch_sha256"])
        self.assertEqual(a["items"][0]["item_id"],b["items"][0]["item_id"])

    def test_extra_field_is_blocked(self):
        d=self.source()
        d["next_textmachine_metadata_batch"]["items"][0]["extra"]="no"
        with self.assertRaisesRegex(m.IntakeError,"EXACT_FIVE_FIELDS"):
            m.convert(self.write(d))

    def test_count_mismatch_is_blocked(self):
        d=self.source()
        d["next_textmachine_metadata_batch"]["item_count"]=2
        with self.assertRaisesRegex(m.IntakeError,"COUNT_MISMATCH"):
            m.convert(self.write(d))

    def test_content_boundary_violation_is_blocked(self):
        d=self.source()
        d["next_textmachine_metadata_batch"]["content_or_format_payload_present"]=True
        with self.assertRaisesRegex(m.IntakeError,"BOUNDARY_INVALID"):
            m.convert(self.write(d))

    def test_duplicate_plan_slot_is_blocked(self):
        d=self.source()
        row=dict(d["next_textmachine_metadata_batch"]["items"][0])
        row["title"]="Anderer Titel"
        d["next_textmachine_metadata_batch"]["items"].append(row)
        d["next_textmachine_metadata_batch"]["item_count"]=2
        with self.assertRaisesRegex(m.IntakeError,"PLAN_SLOT_DUPLICATE"):
            m.convert(self.write(d))

if __name__=="__main__":
    unittest.main()
