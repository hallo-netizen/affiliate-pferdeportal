import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from engine.wordpress_batch_export import combine, BatchBlocked

def single(idx,title,keyword,category,article_type,article_id):
    slot=hashlib.sha256(("pserc-plan-slot-v2|"+article_id).encode()).hexdigest()
    body=f'<article class="ppm-generated ppm-type-{article_type.lower()}" data-article-type="{article_type}"><section data-block="intro"><p>Einleitung {idx}.</p></section><section data-block="conclusion"><h2>Fazit</h2><p>Fazit {idx}.</p></section></article>'
    sha=hashlib.sha256(body.encode()).hexdigest()
    row={
      "index":0,"article_id":article_id,"title":title,"target_keyword":keyword,
      "category":category,"article_type":article_type,"plan_slot":slot,
      "final_draft_sha256":sha,"revision_count":1,"body":body,
      "production_context":{
        "fact_pack":{"contract":"canonical_fact_pack_v1","status":"SOURCE_VERIFIED_PRODUCTION_READY","sources":[],"claims":[]},
        "production_plan_item":{
          "canonical_article_id":article_id,"article_type":article_type,"target_keyword":keyword,"topic":title,
          "canonical_article":{"title":title,"article_type":article_type,"slug":"test","body_html":body,"body_html_sha256":sha},
          "quality_binding":{"wordpress_category":{"id":1,"slug":category,"taxonomy":"category"}},
          "runtime_order":{"article_type":article_type,"title":title,"slug":"test","subject_scope":title,"subject_label":keyword,"allowed_fact_ids":[]}
        }
      },
      "languagetool":{"status":"PASS","finding_count":0,"engine":"LanguageTool 6.8"},
      "ppm679":{"status":"PASS","ppm_version":"6.7.9","technical_status":"TECHNICAL_CHECK_OK","content_quality_status":"CONTENT_QUALITY_CHECK_OK","fail_closed_aggregate_status":"PASS","content_sha256":sha}
    }
    return {
      "contract":"SYSTEM4_WORDPRESS_HANDOFF_V1","batch_sha256":"a"*64,"article_count":1,
      "publish_allowed":False,"signing_deferred":True,"batch_gate_status":"SYSTEM4_BATCH_FULL_PASS_COLLECTED",
      "no_legacy_status":"PASS","test_suite_status":"PASS",
      "wordpress_review":{"file_format":"JSON","mime_type":"application/json",
        "intended_next_step":"WORDPRESS_DIRECT_IMPORT","direct_wordpress_upload_ready":True,
        "direct_upload_block_reason":None,"required_downstream_components":[]},
      "articles":[row]
    }

def intake(rows):
    return {
      "contract":"PSERC_TEXTMACHINE_METADATA_BATCH_V2","status":"READY_FOR_TEXTMACHINE_METADATA_INTAKE",
      "item_count":len(rows),"maximum_articles":0,"maximum_articles_per_type":0,"publish_allowed":False,
      "content_or_format_payload_present":False,"batch_sha256":"a"*64,"items":rows,
    }

class BatchExportTests(unittest.TestCase):
    def make_three(self):
        specs=[
          ("A?","A","faq-a","FAQ","article:111111111111111111111111"),
          ("B?","B","faq-b","FAQ","article:222222222222222222222222"),
          ("C?","C","faq-c","FAQ","article:333333333333333333333333"),
        ]
        docs=[single(i,*x) for i,x in enumerate(specs)]
        rows=[{k:d["articles"][0][k] for k in ("article_type","category","plan_slot","target_keyword","title")} for d in docs]
        return intake(rows),docs

    def test_positive_three_article_batch_preserves_input_order(self):
        i,docs=self.make_three()
        out=combine(i,[docs[2],docs[0],docs[1]])
        self.assertEqual(out["contract"],"SYSTEM4_WORDPRESS_HANDOFF_V1")
        self.assertEqual(out["article_count"],3)
        self.assertEqual([x["title"] for x in out["articles"]],["A?","B?","C?"])
        self.assertTrue(all(hashlib.sha256(("pserc-plan-slot-v2|"+x["article_id"]).encode()).hexdigest()==x["plan_slot"] for x in out["articles"]))
        self.assertFalse(out["publish_allowed"])

    def test_article_id_slot_mismatch_blocks(self):
        i,docs=self.make_three()
        docs[0]["articles"][0]["article_id"]="article:aaaaaaaaaaaaaaaaaaaaaaaa"
        with self.assertRaisesRegex(BatchBlocked,"SINGLE_ARTICLE_ID_PLAN_SLOT_MISMATCH"):
            combine(i,docs)

    def test_nested_canonical_id_mismatch_blocks(self):
        i,docs=self.make_three()
        docs[0]["articles"][0]["production_context"]["production_plan_item"]["canonical_article_id"]="article:aaaaaaaaaaaaaaaaaaaaaaaa"
        with self.assertRaisesRegex(BatchBlocked,"SINGLE_NESTED_CANONICAL_ID_MISMATCH"):
            combine(i,docs)

    def test_missing_article_blocks(self):
        i,docs=self.make_three()
        with self.assertRaisesRegex(BatchBlocked,"BATCH_SINGLE_COUNT_MISMATCH"):
            combine(i,docs[:2])

    def test_wrong_wordpress_import_readiness_blocks(self):
        i,docs=self.make_three()
        docs[1]["wordpress_review"]["direct_wordpress_upload_ready"]=False
        with self.assertRaisesRegex(BatchBlocked,"SINGLE_WORDPRESS_IMPORT_NOT_READY"):
            combine(i,docs)

    def test_mismatched_wordpress_format_blocks(self):
        i,docs=self.make_three()
        docs[0]["wordpress_review"]["mime_type"]="application/zip"
        with self.assertRaisesRegex(BatchBlocked,"SINGLE_WORDPRESS_IMPORT_NOT_READY"):
            combine(i,docs)

    def test_failed_quality_status_blocks(self):
        i,docs=self.make_three()
        docs[2]["articles"][0]["ppm679"]["status"]="FAIL"
        with self.assertRaisesRegex(BatchBlocked,"SINGLE_PPM679_NOT_PASS"):
            combine(i,docs)

    def test_duplicate_input_identity_blocks(self):
        i,docs=self.make_three()
        i["items"][2]=dict(i["items"][0])
        with self.assertRaisesRegex(BatchBlocked,"BATCH_INTAKE_DUPLICATE_OR_INVALID"):
            combine(i,docs)

    def test_file_is_one_verified_wordpress_batch_and_wrong_filename_blocks(self):
        i,docs=self.make_three()
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            intake_path=root/"WORDPRESS_INTAKE.json"
            intake_path.write_text(json.dumps(i,ensure_ascii=False),encoding="utf-8")
            singles=[]
            for number,doc in enumerate(docs):
                path=root/f"single-{number}.json"
                path.write_text(json.dumps(doc,ensure_ascii=False),encoding="utf-8")
                singles.append(str(path))
            output=root/"WORDPRESS_BATCH.json"
            command=[sys.executable,"-m","engine.wordpress_batch_export",str(intake_path),str(output),*singles]
            ok=subprocess.run(command,capture_output=True,text=True)
            self.assertEqual(ok.returncode,0,ok.stdout+ok.stderr)
            emitted=json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(emitted["article_count"],3)
            self.assertTrue(emitted["wordpress_review"]["direct_wordpress_upload_ready"])
            self.assertEqual([x["title"] for x in emitted["articles"]],["A?","B?","C?"])
            wrong=root/"NOT_WORDPRESS_BATCH.json"
            rejected=subprocess.run([sys.executable,"-m","engine.wordpress_batch_export",str(intake_path),str(wrong),*singles],capture_output=True,text=True)
            self.assertNotEqual(rejected.returncode,0)
            self.assertIn("BATCH_OUTPUT_FILENAME_INVALID",rejected.stdout)
            self.assertFalse(wrong.exists())

if __name__=="__main__":
    unittest.main()
