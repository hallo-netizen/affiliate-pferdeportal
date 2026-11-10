"""Proof that K0 receives the source SEO verdict without a second editorial decision.

The manifest fixture is SYNTHETIC and is not misrepresented as a real
WordPress snapshot. The three exact five-field identities are real.
"""
import copy
import json
import unittest
from pathlib import Path
from engine.core import stable
from engine.k0_portal_resolver import validate_intake
from engine.k0_seo_owner_binding import inspect,bind_context,verify_context,php_stable,Blocked

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"tests/fixtures/k0_seo_owner_manifest_SYNTHETIC_QA_20261110.json"

class SeoOwnerSourceBindingTests(unittest.TestCase):
    def setUp(self):
        self.m=json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.batch,self.owner=inspect(self.m)

    def source(self,index):
        p=ROOT/f"real_runs/k0/k0-20261110-42619ca7-{index:02d}-r2"
        return (json.loads((p/"WORDPRESS_INTAKE.json").read_text(encoding="utf-8")),
                json.loads((p/"AUTHORING_CONTEXT.json").read_text(encoding="utf-8")))

    def resign(self,m):
        m["manifest_sha256"]=stable({k:v for k,v in m.items() if k!="manifest_sha256"})
        return m

    def test_three_original_five_field_intakes_and_approved_owner(self):
        self.assertEqual(len(self.batch["items"]),3)
        self.assertEqual(len(self.owner),3)
        for i in (1,2,3):
            intake,context=self.source(i)
            self.assertEqual(len(validate_intake(intake)),1)
            original=dict(context)
            original["content_profile"]=dict(context["content_profile"])
            original["content_profile"]["search_intent"]=""
            bound=bind_context(self.m,intake,original)
            self.assertEqual(bound["content_profile"]["search_intent"],self.owner[intake["items"][0]["plan_slot"]]["search_intent"])
            self.assertEqual(bound["identity"],context["identity"])
            self.assertEqual(verify_context(self.m,intake,bound)["status"],"PASS")
            self.assertEqual(set(intake["items"][0]),{"title","target_keyword","category","article_type","plan_slot"})
            self.assertEqual(context["identity"],intake["items"][0])

    def test_wrong_editorial_intent_blocks(self):
        intake,context=self.source(2)
        context["content_profile"]["search_intent"]="SOME_OTHER_OWNER_DECISION"
        with self.assertRaisesRegex(Blocked,"INTENT_CONFLICT"):
            bind_context(self.m,intake,context)

    def test_intent_change_after_binding_blocks(self):
        intake,context=self.source(1)
        context=bind_context(self.m,intake,context)
        context["content_profile"]["search_intent"]="UNAPPROVED_REWRITE"
        with self.assertRaises(Blocked):verify_context(self.m,intake,context)

    def test_missing_or_modified_manifest_hash_blocks(self):
        bad=copy.deepcopy(self.m)
        bad["items"][0]["intent_profile"]["search_intent"]="WRONG"
        with self.assertRaisesRegex(Blocked,"MANIFEST_HASH_MISMATCH"):inspect(bad)

    def test_rehashed_manifest_cannot_mismatch_original_batch_identity(self):
        bad=copy.deepcopy(self.m)
        bad["items"][0]["metadata_binding"]["title"]="Changed title"
        self.resign(bad)
        with self.assertRaisesRegex(Blocked,"DETAIL_IDENTITY_MISMATCH"):inspect(bad)

    def test_missing_original_owner_approval_blocks_even_if_rehashed(self):
        bad=copy.deepcopy(self.m)
        bad["items"][0]["intent_profile"]["status"]="REVIEW_REQUIRED"
        self.resign(bad)
        with self.assertRaisesRegex(Blocked,"UPSTREAM_INTENT_NOT_APPROVED"):inspect(bad)

    def test_rehashed_manifest_cannot_hide_changed_original_pste_intent(self):
        bad=copy.deepcopy(self.m)
        bad["items"][0]["intent_profile"]["search_intent"]="FABRICATED_SEO_REDECISION"
        self.resign(bad)
        with self.assertRaisesRegex(Blocked,"ORIGINAL_PSTE_PROFILE_HASH_MISMATCH"):
            inspect(bad)

    def test_genuine_php_hash_formats_for_seo_probabilities(self):
        # Known hashes from the original PSERC_Stable_Json implementation.
        self.assertEqual(php_stable({"v":1e-5}),"f32d38a5e40c0a0a6fca0425a6764b7edab87ccefaec35ed85165b9033d664ba")
        self.assertEqual(php_stable({"v":1e20}),"e2f957556683366624e5e003e8fe15765bd75f85eca7819707c5fc0c8e437142")
        self.assertEqual(php_stable({"v":0.3}),"8d3104ead3049f23ce96b16520ba7db77fb39748e92e9c6020869803c8eb3fab")

    def test_tampered_single_article_plan_slot_blocks(self):
        intake,context=self.source(1)
        intake["items"][0]["plan_slot"]=self.batch["items"][1]["plan_slot"]
        from engine.k0_portal_resolver import stable as json_stable
        import hashlib
        intake["batch_sha256"]=hashlib.sha256(json_stable({k:v for k,v in intake.items() if k!="batch_sha256"}).encode("utf-8")).hexdigest()
        with self.assertRaisesRegex(Blocked,"SINGLE_ITEM_NOT_IN_SOURCE_BATCH"):bind_context(self.m,intake,context)

    def test_profile_source_provenance_cannot_be_replaced(self):
        intake,ctx=self.source(3)
        bound=bind_context(self.m,intake,ctx)
        bound["content_profile"]["seo_owner_profile_sha256"]="0"*64
        with self.assertRaisesRegex(Blocked,"SOURCE_PROVENANCE_CONFLICT"):bind_context(self.m,intake,bound)

    def test_five_field_metadata_stays_byte_identical(self):
        original=json.loads((ROOT/"real_runs/k0/batch-20261110-42619ca7/BATCH_INTAKE.json").read_text(encoding="utf-8"))
        self.assertEqual(original,self.batch)

if __name__=="__main__":
    unittest.main()
