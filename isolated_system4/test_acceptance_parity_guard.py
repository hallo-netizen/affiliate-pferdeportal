from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

import acceptance_parity_guard as guard
import real_route_test_support

HERE=Path(__file__).resolve().parent
REPO=HERE.parent

class AcceptanceParityGuardTests(unittest.TestCase):
    def test_forbidden_prebuilt_paths_are_rejected(self):
        for source in (
            'legacy.build_fixture(runtime)',
            'full_local_acceptance.build_fixture(x)',
            'g9-single-faq-approved-candidate-v1.json',
            'control/startmaster0107/recovery_sources/ARTICLE_x.md',
        ):
            with self.assertRaises(guard.AcceptanceParityError):
                guard.reject_forbidden_acceptance_source(source)

    def test_current_acceptance_sources_have_no_prebuilt_article_path(self):
        guard.verify_acceptance_sources(REPO)

    def test_prebuilt_draft_before_author_stage_is_rejected(self):
        state={
            'phase':'DRAFT_REQUIRED','draft_markdown':'old article','draft_sha256':'x','revision':0,
            'research':{'sha256':'a'},'facts':{'sha256':'b'},'production_context':{},'authoring_contract':{},
        }
        with self.assertRaisesRegex(guard.AcceptanceParityError,'PREBUILT_DRAFT'):
            guard.verify_pre_author_state(state)

    def test_current_run_generation_receipt_is_bound_to_evidence_and_body(self):
        with tempfile.TemporaryDirectory(prefix='s4-fresh-guard-') as td:
            workspace,_,state=real_route_test_support.start_to_context_real(Path(td),0)
            guard.verify_pre_author_state(state)
            body=real_route_test_support.valid_real_article(state,0)
            receipt=guard.build_fresh_generation_receipt(REPO,state,body)
            guard.verify_fresh_generation_receipt(state,body,receipt)
            changed=body+'\n<!-- mutation -->'
            with self.assertRaisesRegex(guard.AcceptanceParityError,'BODY_MISMATCH'):
                guard.verify_fresh_generation_receipt(state,changed,receipt)

if __name__=='__main__':
    unittest.main(verbosity=2)
