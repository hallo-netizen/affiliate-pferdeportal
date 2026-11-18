"""Regression proof for the technical WordPress-to-K0 binding only.

Run: python -m unittest tests.test_wp_k0_wordpress_source
This does not replace the unchanged K0 quality/LanguageTool/security tests.
"""
from __future__ import annotations
import copy
import hashlib
import unittest
from engine.wp_order_identity_receipt import inspect,resolve_current_intake,stable_sha,Blocked
from engine.k0_wp_upload import unpack

class WordPressSourceContractTest(unittest.TestCase):
    def setUp(self):
        order_id="TXE-28fe244e1ca82a090e8d175fa8a236d6"
        title="Horseware-Regendecken und ihre Unterschiede bei Schnitt und Ausstattung"
        aid="article:"+hashlib.sha256(("texterstellung-k0-v1|oliver-beil.de|"+order_id).encode()).hexdigest()[:24]
        slot=hashlib.sha256(("pserc-plan-slot-v2|"+aid).encode()).hexdigest()
        self.row={"title":title,"target_keyword":"horseware regendecken","category":"pferdedecken-regendecken-vergleich","article_type":"Vergleich","plan_slot":slot}
        batch={"contract":"PSERC_TEXTMACHINE_METADATA_BATCH_V2","status":"READY_FOR_TEXTMACHINE_METADATA_INTAKE","item_count":1,"publish_allowed":False,"content_or_format_payload_present":False,"items":[self.row]}
        batch["batch_sha256"]=stable_sha(batch)
        receipt={"contract":"WP_K0_SOURCE_RECEIPT_V1","source":"CENTRAL_WORDPRESS_ORDER_REGISTRY","site_host":"oliver-beil.de","publish_allowed":False,"next_textmachine_metadata_batch":batch,"items":[{"metadata_binding":self.row,"order_id":order_id,"article_id":aid,"search_intent":"Markenberatung"}]}
        receipt["manifest_sha256"]=stable_sha(receipt)
        self.package={"contract":"WP_K0_UPLOAD_PACKAGE_V1","publish_allowed":False,"k0_intake":batch,"word_press_order_receipt":receipt}
    def resign(self,r):
        r.pop("manifest_sha256",None);r["manifest_sha256"]=stable_sha(r)
    def test_original_order_one_article(self):
        docs=unpack(self.package)
        self.assertEqual(len(docs),1)
        self.assertEqual(resolve_current_intake(*docs[0])["bindings"][self.row["plan_slot"]],self.package["word_press_order_receipt"]["items"][0]["article_id"])
    def test_wrong_original_order_is_blocked(self):
        r=copy.deepcopy(self.package["word_press_order_receipt"])
        r["items"][0]["order_id"]="TXE-"+"0"*32;self.resign(r)
        with self.assertRaises(Blocked):inspect(r)
    def test_missing_upstream_intent_is_blocked(self):
        r=copy.deepcopy(self.package["word_press_order_receipt"])
        r["items"][0]["search_intent"]="";self.resign(r)
        with self.assertRaises(Blocked):inspect(r)
    def test_mismatched_category_is_blocked(self):
        r=copy.deepcopy(self.package["word_press_order_receipt"])
        r["items"][0]["metadata_binding"]["category"]="other";self.resign(r)
        with self.assertRaises(Blocked):inspect(r)
    def test_mismatched_source_batch_is_blocked(self):
        p=copy.deepcopy(self.package)
        p["k0_intake"]["items"][0]["title"]="wrong"
        with self.assertRaises(Exception):unpack(p)
    def test_publish_is_blocked(self):
        p=copy.deepcopy(self.package);p["publish_allowed"]=True
        with self.assertRaises(Exception):unpack(p)
    def test_sixth_editorial_field_is_blocked(self):
        p=copy.deepcopy(self.package);p["k0_intake"]["items"][0]["intent"]="forbidden"
        with self.assertRaises(Exception):unpack(p)
    def test_replay_is_identical(self):
        self.assertEqual(unpack(self.package),unpack(self.package))


    def test_existing_wordpress_receipt_is_the_k0_source_manifest(self):
        import json
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from engine.k0_wp_upload import write_runs
        from engine.k0_seo_owner_binding import inspect as k0_inspect, bind_context
        with TemporaryDirectory() as temp:
            source=Path(temp)/"upload.json"
            source.write_text(json.dumps(self.package,ensure_ascii=False),encoding="utf-8")
            runs=write_runs(source,Path(temp)/"runs")
            self.assertEqual(len(runs),1)
            self.assertEqual(sorted(p.name for p in runs[0].iterdir()),["PSERC_SOURCE_MANIFEST.json","WORDPRESS_INTAKE.json"])
            manifest=json.loads((runs[0]/"PSERC_SOURCE_MANIFEST.json").read_text())
            intake=json.loads((runs[0]/"WORDPRESS_INTAKE.json").read_text())
            self.assertEqual(manifest["contract"],"WP_K0_SOURCE_RECEIPT_V1")
            batch,owners=k0_inspect(manifest)
            self.assertEqual(batch,self.package["k0_intake"])
            self.assertEqual(owners[self.row["plan_slot"]]["search_intent"],"Markenberatung")
            bound=bind_context(manifest,intake,{"identity":self.row,"content_profile":{"search_intent":"UNVERIFIED_HINT"}})
            self.assertEqual(bound["content_profile"]["search_intent"],"Markenberatung")
            self.assertEqual(bound["content_profile"]["seo_owner_manifest_sha256"],manifest["manifest_sha256"])

    def test_current_wp_bundle_one_two_three_and_safe_repeat(self):
        import json
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from engine.k0_wp_upload import write_runs
        from engine.k0_seo_owner_binding import inspect as k0_inspect
        site="pferde-atelier.de"
        for count in (1,2,3):
            rows=[]; details=[]
            for i in range(count):
                order="TXE-"+format(i+1,"032x")
                aid="article:"+hashlib.sha256(("texterstellung-k0-v1|"+site+"|"+order).encode()).hexdigest()[:24]
                slot=hashlib.sha256(("pserc-plan-slot-v2|"+aid).encode()).hexdigest()
                row={"title":"K0 Musterartikel "+str(i+1),"target_keyword":"musterkeyword "+str(i+1),
                     "category":"pferdegesundheit-verstehen","article_type":"FAQ","plan_slot":slot}
                rows.append(row);details.append({"metadata_binding":row,"order_id":order,"article_id":aid,"search_intent":"Bereits entschiedener FAQ-Intent"})
            batch={"contract":"PSERC_TEXTMACHINE_METADATA_BATCH_V2",
                   "status":"READY_FOR_TEXTMACHINE_METADATA_INTAKE","item_count":count,
                   "publish_allowed":False,"content_or_format_payload_present":False,"items":rows}
            batch["batch_sha256"]=stable_sha(batch)
            receipt={"contract":"WP_K0_SOURCE_RECEIPT_V1","source":"CENTRAL_WORDPRESS_ORDER_REGISTRY",
                     "site_host":site,"publish_allowed":False,"next_textmachine_metadata_batch":batch,"items":details}
            receipt["manifest_sha256"]=stable_sha(receipt)
            package={"contract":"WP_K0_UPLOAD_PACKAGE_V1","publish_allowed":False,
                     "k0_intake":batch,"word_press_order_receipt":receipt}
            with TemporaryDirectory() as temp:
                source=Path(temp)/"upload.json"
                source.write_text(json.dumps(package,ensure_ascii=False),encoding="utf-8")
                target=Path(temp)/"jobs"
                first=write_runs(source,target)
                second=write_runs(source,target)
                self.assertEqual(first,second)
                self.assertEqual(len(first),count)
                observed=[]
                for run in first:
                    one=json.loads((run/"WORDPRESS_INTAKE.json").read_text())
                    proven=json.loads((run/"PSERC_SOURCE_MANIFEST.json").read_text())
                    self.assertEqual(len(one["items"]),1)
                    self.assertEqual(k0_inspect(proven)[0],batch)
                    observed.append(one["items"][0]["plan_slot"])
                self.assertEqual(observed,[row["plan_slot"] for row in rows])
                self.assertEqual(len(observed),len(set(observed)))
                self.assertFalse(package["publish_allowed"])

    def test_real_archived_k0_wrote_two_verified_wordpress_drafts(self):
        import json
        from pathlib import Path
        from engine.wordpress_batch_export import combine
        root=Path("real_runs/k0")
        archived=root/"k0-20261116-txe-4a2e4870-01"
        source=json.loads((archived/"PSERC_SOURCE_MANIFEST.json").read_text())
        full=source["next_textmachine_metadata_batch"]
        records=[json.loads((root/f"k0-20261116-txe-4a2e4870-0{i}"/"WORDPRESS_SINGLE.json").read_text())
                 for i in (1,2)]
        finished=combine(full,records)
        self.assertEqual(finished["article_count"],2)
        self.assertFalse(finished["publish_allowed"])
        self.assertEqual([a["plan_slot"] for a in finished["articles"]],
                         [a["plan_slot"] for a in full["items"]])
        for a in finished["articles"]:
            self.assertEqual(a["production_context"]["production_plan_item"]["canonical_article_id"],a["article_id"])
            self.assertEqual(a["languagetool"]["status"],"PASS")
            self.assertEqual(a["ppm679"]["status"],"PASS")
            self.assertTrue(a["body"])
        original=json.loads((root/"batch-20261116-txe-4a2e4870"/"WORDPRESS_BATCH.json").read_text())
        self.assertEqual(original["article_count"],2)
        self.assertEqual(original["batch_sha256"],finished["batch_sha256"])

if __name__=="__main__":unittest.main()
