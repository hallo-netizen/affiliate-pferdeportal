from __future__ import annotations

import hashlib
import unittest
from unittest.mock import patch

from concept_agent.konzept8_verbot.engine import k8_progress_guard, k8_wordpress_export


class K8WordPressExportTest(unittest.TestCase):
    def _binding_and_checkpoint(self):
        slot="a"*64
        body="<article>" + ("wort " * 760) + "</article>"
        raw=body.encode("utf-8")
        draft_sha=hashlib.sha256(raw).hexdigest()
        binding={
            "contract":k8_progress_guard.BINDING_CONTRACT,
            "status":"AUTHORING_READY",
            "batch_sha256":"b"*64,
            "item_count":1,
            "items":[{
                "item_index":0,
                "identity":{
                    "item_index":0,
                    "title":"Testtitel",
                    "target_keyword":"Testkeyword",
                    "category":"test-kategorie",
                    "article_type":"Beratung",
                    "plan_slot":slot,
                    "identity_sha256":"c"*64,
                },
                "production_plan_item":{},
            }],
            "publish_allowed":False,
        }
        binding["binding_sha256"]=k8_progress_guard.stable(binding)

        state={
            "contract":k8_progress_guard.CHECKPOINT_CONTRACT,
            "batch_sha256":binding["batch_sha256"],
            "production_binding_sha256":binding["binding_sha256"],
            "item_count":1,
            "next_item_index":1,
            "phase":"PSERC_PASS_ENDSTEMPEL_REQUIRED",
            "status":"IN_PROGRESS",
            "drafts":[{
                "item_index":0,
                "plan_slot":slot,
                "filename":"00_"+slot+".md",
                "draft_sha256":draft_sha,
                "size_bytes":len(raw),
                "content_utf8":body,
                "revision":1,
                "lt68":"PASS",
                "ppm679":"PASS",
            }],
            "completed_items":[{
                "item_index":0,
                "plan_slot":slot,
                "draft_sha256":draft_sha,
                "revision":1,
                "lt68":"PASS",
                "ppm679":"PASS",
            }],
            "current_item":None,
            "pserc_package_sha256":"d"*64,
            "publish_allowed":False,
        }
        state["allowed_action"]=k8_progress_guard.expected_action(binding,state)
        state["checkpoint_sha256"]=k8_progress_guard.stable(state)
        return binding,state,draft_sha

    def test_export_matches_proven_direct_handoff_shape(self):
        binding,state,draft_sha=self._binding_and_checkpoint()
        context={
            "fact_pack":{"contract":"canonical_fact_pack_v1"},
            "production_plan_item":{"article_type":"Beratung"},
        }
        with patch.object(k8_wordpress_export.k8_bound_fact_context,"build_item",return_value=context):
            out=k8_wordpress_export.build(binding,state)
        self.assertEqual(out["contract"],"SYSTEM4_WORDPRESS_HANDOFF_V1")
        self.assertIs(out["wordpress_review"]["direct_wordpress_upload_ready"],True)
        self.assertEqual(out["article_count"],1)
        self.assertEqual(set(out["articles"][0]),{
            "index","title","target_keyword","category","article_type","plan_slot",
            "final_draft_sha256","revision_count","body","production_context",
            "languagetool","ppm679",
        })
        self.assertEqual(out["articles"][0]["final_draft_sha256"],draft_sha)

    def test_terminal_stop_requires_wordpress_delivery(self):
        binding,state,_=self._binding_and_checkpoint()
        state.pop("checkpoint_sha256")
        state["phase"]="ENDSTEMPEL_PASS_STOP"
        state["status"]="PASS"
        state["endstempel_final_file_sha256"]="e"*64
        with self.assertRaisesRegex(k8_progress_guard.Blocked,"WORDPRESS_EXPORT_CONTRACT_MISSING"):
            k8_progress_guard.expected_action(binding,state)


if __name__ == "__main__":
    unittest.main()
