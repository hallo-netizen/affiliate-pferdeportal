import importlib.util, json, tempfile, unittest
from pathlib import Path

SRC=Path(__file__).resolve().parents[1]/"k9_intake.py"
spec=importlib.util.spec_from_file_location("k9_intake",SRC)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
    def tearDown(self): self.tmp.cleanup()
    def batch(self):
        d={"contract":m.BATCH_CONTRACT,"status":"READY_FOR_TEXTMACHINE_METADATA_INTAKE","item_count":1,"maximum_articles":0,"maximum_articles_per_type":0,"publish_allowed":False,"content_or_format_payload_present":False,"items":[{"article_type":"Beratung","category":"reitplatzplaner-beratung","plan_slot":"0b401802eeed8574d9c80f7eb5e1abb03c0ac5dbf82fa8b8a95deb7abf3bec15","target_keyword":"Reitplatzplaner für Pferde","title":"Das Wichtigste über Reitplatzplaner für Pferde"}]}
        d["batch_sha256"]=m.stable(d); return d
    def source(self): return {"contract":m.SOURCE_CONTRACT,"mode":"READ_ONLY_METADATA_ONLY_EXACT_FIVE_FIELDS","next_textmachine_metadata_batch":self.batch()}
    def write(self,data,name="input.json"):
        p=self.root/name; p.write_text(json.dumps(data,ensure_ascii=False),encoding="utf-8"); return p
    def test_legacy_snapshot_becomes_native_exact_five_fields(self):
        out=m.convert(self.write(self.source())); self.assertEqual(out["item_count"],1); self.assertEqual(out["source_kind"],"WORDPRESS_LEGACY_SNAPSHOT_EXACT_FIVE_FIELDS"); self.assertEqual(set(out["items"][0]["metadata"]),set(m.FIELDS))
    def test_compact_batch_is_accepted_directly(self):
        b=self.batch(); out=m.convert(self.write(b,"compact.json")); self.assertEqual(out["source_kind"],"WORDPRESS_COMPACT_EXACT_FIVE_FIELDS"); self.assertEqual(out["source_batch_sha256"],b["batch_sha256"])
    def test_batch_hash_tamper_is_blocked(self):
        b=self.batch(); b["items"][0]["title"]="Manipuliert"
        with self.assertRaisesRegex(m.IntakeError,"SHA_MISMATCH"): m.convert(self.write(b))
    def test_extra_field_is_blocked(self):
        b=self.batch(); b["items"][0]["extra"]="no"; core=dict(b); core.pop("batch_sha256"); b["batch_sha256"]=m.stable(core)
        with self.assertRaisesRegex(m.IntakeError,"EXACT_FIVE_FIELDS"): m.convert(self.write(b))
    def test_duplicate_plan_slot_is_blocked(self):
        b=self.batch(); row=dict(b["items"][0]); row["title"]="Anderer Titel"; b["items"].append(row); b["item_count"]=2; core=dict(b); core.pop("batch_sha256"); b["batch_sha256"]=m.stable(core)
        with self.assertRaisesRegex(m.IntakeError,"PLAN_SLOT_DUPLICATE"): m.convert(self.write(b))

if __name__=="__main__": unittest.main()
