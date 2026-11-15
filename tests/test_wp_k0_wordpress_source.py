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

if __name__=="__main__":unittest.main()
