from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import acceptance_parity_guard as guard
import real_route_test_support

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
TEST_NONCE='unit-test-fresh-article-nonce-0001'

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

    def test_missing_run_nonce_is_hard_blocked(self):
        with tempfile.TemporaryDirectory(prefix='s4-fresh-guard-') as td:
            _,_,state=real_route_test_support.start_to_context_real(Path(td),0)
            body=real_route_test_support.valid_real_article(state,0)
            with mock.patch.dict(os.environ,{guard.TEST_RUN_NONCE_ENV:''},clear=False):
                with self.assertRaisesRegex(guard.AcceptanceParityError,'TEST_RUN_NONCE_REQUIRED'):
                    guard.build_fresh_generation_receipt(REPO,state,body)

    def test_current_run_generation_receipt_is_bound_to_evidence_body_and_run(self):
        with tempfile.TemporaryDirectory(prefix='s4-fresh-guard-') as td:
            workspace,_,state=real_route_test_support.start_to_context_real(Path(td),0)
            guard.verify_pre_author_state(state)
            body=real_route_test_support.valid_real_article(state,97)
            ledger=Path(td)/'fresh-ledger.jsonl'
            receipt=guard.build_fresh_generation_receipt(REPO,state,body,run_nonce=TEST_NONCE,ledger_path=ledger)
            guard.verify_fresh_generation_receipt(state,body,receipt,run_nonce=TEST_NONCE)
            changed=body+'\n<!-- mutation -->'
            with self.assertRaisesRegex(guard.AcceptanceParityError,'BODY_MISMATCH'):
                guard.verify_fresh_generation_receipt(state,changed,receipt,run_nonce=TEST_NONCE)
            with self.assertRaisesRegex(guard.AcceptanceParityError,'RUN_MISMATCH'):
                guard.verify_fresh_generation_receipt(state,body,receipt,run_nonce='different-fresh-run-nonce-0002')
            with self.assertRaisesRegex(guard.AcceptanceParityError,'ALREADY_USED_IN_THIS_RUN'):
                guard.build_fresh_generation_receipt(REPO,state,body,run_nonce=TEST_NONCE,ledger_path=ledger)

if __name__=='__main__':
    unittest.main(verbosity=2)
