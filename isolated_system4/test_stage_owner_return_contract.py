from __future__ import annotations

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import content_guard
import controller
import controller_engine


def _sha_text(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def _base_state(phase: str) -> dict:
    article = {
        'title': 'Testtitel Pferde',
        'target_keyword': 'Pferde Test',
        'category': 'test-beratung',
        'article_type': 'Beratung',
        'plan_slot': 'a' * 64,
    }
    state = {
        'contract': controller_engine.CONTRACT,
        'source_snapshot_sha256': 'b' * 64,
        'batch_sha256': 'c' * 64,
        'article': article,
        'immutable_core_sha256': '',
        'publish_allowed': False,
        'phase': phase,
        'revision': 0,
        'research': None,
        'facts': None,
        'production_context': None,
        'authoring_contract': None,
        'draft_markdown': None,
        'draft_sha256': None,
        'checks': {},
        'last_error': None,
        'release_prepared': None,
        'released': False,
    }
    state['immutable_core_sha256'] = controller_engine.sha(controller_engine.immutable_core(state))
    return state


def _write_workspace(root: Path, state: dict) -> Path:
    root.mkdir()
    (root / 'state.json').write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True), encoding='utf-8')
    return root


class StageOwnerReturnContractTests(unittest.TestCase):
    def _run_stage_and_freeze(self, workspace: Path, command: str, fn, args: list[str], expected_owner: str, expected_route: str) -> None:
        before = (workspace / 'state.json').read_bytes()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = controller._stage_owner_call(command, fn, str(workspace), *args)
        self.assertEqual(rc, 4, out.getvalue())
        self.assertEqual((workspace / 'state.json').read_bytes(), before)
        self.assertIn('SYSTEM4_STAGE_OWNER_RETURN:' + expected_owner + ':' + expected_route, out.getvalue())

    def test_research_content_failure_returns_research_worker_same_stage(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ws = _write_workspace(root / 'ws', _base_state('RESEARCH_REQUIRED'))
            inp = root / 'research.json'; inp.write_text('{}', encoding='utf-8')
            with mock.patch.object(controller_engine.content_guard, 'validate_research_document', side_effect=content_guard.ContentGuardError('RESEARCH_SOURCE_EVIDENCE_INVALID:0')):
                self._run_stage_and_freeze(ws, 'research', controller_engine.cmd_research, [str(inp)], 'RESEARCH_WORKER', 'RESEARCH_STAGE')

    def test_facts_content_failure_returns_facts_worker_same_stage(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            state = _base_state('FACT_CHECK_REQUIRED')
            research = '{"contract":"SYSTEM4_RESEARCH_EVIDENCE_V1","sources":[]}'
            state['research'] = {'text': research, 'sha256': _sha_text(research)}
            ws = _write_workspace(root / 'ws', state)
            inp = root / 'facts.json'; inp.write_text('{}', encoding='utf-8')
            with mock.patch.object(controller_engine.content_guard, 'validate_facts_document', side_effect=content_guard.ContentGuardError('FACT_EVIDENCE_NOT_IN_SOURCE:0')):
                self._run_stage_and_freeze(ws, 'facts', controller_engine.cmd_facts, [str(inp)], 'FACTS_WORKER', 'FACTS_STAGE')

    def test_context_fact_pack_failure_returns_context_worker_same_stage(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            state = _base_state('CONTEXT_REQUIRED')
            research = '{"contract":"SYSTEM4_RESEARCH_EVIDENCE_V1","sources":[]}'
            facts = '{"contract":"SYSTEM4_FACTS_EVIDENCE_V1","claims":[]}'
            state['research'] = {'text': research, 'sha256': _sha_text(research)}
            state['facts'] = {'text': facts, 'sha256': _sha_text(facts)}
            ws = _write_workspace(root / 'ws', state)
            fact = root / 'fact.json'; fact.write_text('{}', encoding='utf-8')
            plan = root / 'plan.json'; plan.write_text('{}', encoding='utf-8')
            with mock.patch.object(controller_engine.content_guard, 'validate_fact_pack', side_effect=content_guard.ContentGuardError('FACT_PACK_CLAIMS_TOO_LOW')):
                self._run_stage_and_freeze(ws, 'context', controller_engine.cmd_context, [str(fact), str(plan)], 'CONTEXT_WORKER', 'CONTEXT_STAGE')

    def test_draft_missing_bound_link_returns_draft_worker_same_stage(self):
        self.assertEqual(
            controller._stage_owner_route('draft', 'ARTICLE_AUTHORING_CONTRACT_FAIL:PREWRITE_BOUND_LINK_MISSING:parent_category'),
            ('DRAFT_WORKER', 'DRAFT_STAGE'),
        )

    def test_draft_external_link_violation_returns_draft_worker_same_stage(self):
        self.assertEqual(
            controller._stage_owner_route('draft', 'ARTICLE_AUTHORING_CONTRACT_FAIL:PREWRITE_EXTERNAL_LINK_FORBIDDEN'),
            ('DRAFT_WORKER', 'DRAFT_STAGE'),
        )

    def test_draft_binding_or_integrity_failure_remains_hard_block(self):
        self.assertIsNone(controller._stage_owner_route('draft', 'ARTICLE_AUTHORING_CONTRACT_FAIL:QUALITY_BINDING_HASH_INVALID'))
        self.assertIsNone(controller._stage_owner_route('draft', 'DRAFT_INTEGRITY_FAIL'))

    def test_supervisor_research_binding_failure_remains_hard_block(self):
        self.assertIsNone(controller._stage_owner_route('research', 'SUPERVISOR_RESEARCH_BINDING_FAIL:UNBOUND_RESEARCH_SUBMISSION_BLOCKED'))

    def test_context_machine_prewrite_binding_failure_remains_hard_block(self):
        self.assertIsNone(controller._stage_owner_route('context', 'PRODUCTION_CONTEXT_FAIL:MACHINE_PREWRITE_RAIL_MISMATCH:quality_binding'))

    def test_integrity_failure_remains_hard_block(self):
        self.assertIsNone(controller._stage_owner_route('facts', 'FACTS_INTEGRITY_FAIL'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
