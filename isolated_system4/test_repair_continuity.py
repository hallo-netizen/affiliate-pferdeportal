from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import batch_gate
import controller
import live_parity
import test_route_input_factory

HERE = Path(__file__).resolve().parent


def _env() -> dict[str, str]:
    value = os.environ.copy()
    value['PYTHONDONTWRITEBYTECODE'] = '1'
    return value


def _prepare_batch(root: Path, count: int):
    fixture = root / 'fixture'
    if len(str(os.environ.get('SYSTEM4_FRESH_RUN_TOKEN') or '').strip()) < 16:
        os.environ['SYSTEM4_FRESH_RUN_TOKEN'] = 'repair-continuity-' + root.name + '-' + str(count)
    test_route_input_factory.create(fixture, count)
    live_parity.FIX = fixture.resolve()
    runroot = root / 'run'
    live_parity.prepare(runroot)
    e = _env()
    rows = []
    for index in range(count):
        workspace = runroot / f'item-{index}'
        generated = runroot / f'generated-{index}'
        live_parity.run([
            sys.executable, HERE / 'root_entry.py', 'start-point0',
            runroot / 'point0.json', workspace, str(index),
        ], e)
        live_parity._worker_generate(e, workspace, generated, 'gate')

        research = generated / 'research.json'
        self_returns = live_parity._stage_with_return(
            e, workspace, generated, 'research', ['research', workspace, research], research,
        )
        if self_returns:
            raise AssertionError('unexpected research return in positive continuity baseline')

        facts = generated / 'facts.json'
        self_returns = live_parity._stage_with_return(
            e, workspace, generated, 'facts', ['facts', workspace, facts], facts,
        )
        if self_returns:
            raise AssertionError('unexpected facts return in positive continuity baseline')

        fact_pack = generated / 'fact_pack.json'
        plan = generated / 'plan.json'
        self_returns = live_parity._stage_with_return(
            e, workspace, generated, 'context', ['context', workspace, fact_pack, plan], fact_pack, plan,
        )
        if self_returns:
            raise AssertionError('unexpected context return in positive continuity baseline')

        draft = generated / 'draft.html'
        self_returns = live_parity._stage_with_return(
            e, workspace, generated, 'draft', ['draft', workspace, draft], draft,
        )
        if self_returns:
            raise AssertionError('unexpected draft return in positive continuity baseline')

        state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
        if state.get('phase') != 'CHECK_REQUIRED':
            raise AssertionError('continuity baseline did not reach CHECK_REQUIRED')
        rows.append((workspace, generated, draft))
    return runroot, rows


def _minor_repair(body: str) -> str:
    candidates = (
        'Befund wird vorab geprüft',
        'Abweichung wird vorher geklärt',
        'Zustand wird aktuell bestätigt',
        'Funktion wird gezielt kontrolliert',
        'Ergebnis wird neu festgestellt',
        'Prüfpunkt bleibt nachvollziehbar',
        'Kontrolle erfolgt vor Fahrtbeginn',
        'Beobachtung wird eindeutig bewertet',
    )
    for phrase in candidates:
        if phrase in body:
            return body.replace(phrase, phrase + ' und erneut bestätigt', 1)
    raise AssertionError('no deterministic repair sentence found')


def _pass_result(state: dict) -> dict:
    draft_sha = state['draft_sha256']
    return {
        'contract': 'SYSTEM4_FULL_PRODUCTION_CHECK_V1',
        'status': 'PASS',
        'checked_draft_sha256': draft_sha,
        'publish_allowed': False,
        'evidence': {
            'no_legacy': {'status': 'PASS', 'legacy_import_count': 0},
            'no_external_links': {'status': 'PASS', 'external_link_count': 0},
            'languagetool': {
                'status': 'PASS',
                'engine': 'LanguageTool 6.8 / Bestand 43',
                'finding_count': 0,
            },
            'ppm679': {
                'status': 'PASS',
                'ppm_version': '6.7.9',
                'technical_status': 'TECHNICAL_CHECK_OK',
                'content_quality_status': 'CONTENT_QUALITY_CHECK_OK',
                'fail_closed_aggregate_status': 'PASS',
                'content_sha256': draft_sha,
                'language_evidence_source': 'REAL_LT68_FULLCHECK_REUSED',
            },
        },
    }


class RepairContinuityTests(unittest.TestCase):
    def test_repairable_languagetool_finding_stays_same_draft_flow_and_rechecks(self):
        with tempfile.TemporaryDirectory(prefix='system4-continuity-') as td:
            root = Path(td)
            _, rows = _prepare_batch(root, 1)
            workspace, _, draft = rows[0]
            repair = controller.production_checks.RepairRequired(
                'languagetool',
                [{'error_code': 'LANGUAGETOOL_FINDING', 'rule_id': 'GERMAN_SPELLER_RULE'}],
            )
            state_before = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
            passed = _pass_result(state_before)
            with mock.patch.object(controller.production_checks, 'run_all', side_effect=[repair, passed]) as run_all:
                self.assertEqual(controller.cmd_fullcheck(workspace), 3)
                state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
                self.assertEqual(state['phase'], 'REPAIR_REQUIRED')
                self.assertEqual(state['checks']['repair_owner'], 'DRAFT_WORKER')
                self.assertEqual(state['last_error'], 'FULL:languagetool:LANGUAGETOOL_FINDING')
                self.assertEqual(state['revision'], 1)

                old = draft.read_text(encoding='utf-8')
                draft.write_text(_minor_repair(old), encoding='utf-8')
                controller.cmd_repair(workspace, draft)
                self.assertEqual(controller.cmd_fullcheck(workspace), 0)
                state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
                self.assertEqual(state['phase'], 'OUTPUT_GATE_REQUIRED')
                self.assertEqual(state['checks']['status'], 'PASS')
                self.assertEqual(state['checks']['mode'], 'FULL_PRODUCTION')
                self.assertEqual(state['revision'], 2)
                self.assertEqual(run_all.call_count, 2, 'same real checker must run again after repair')

    def test_broad_repair_is_blocked(self):
        with tempfile.TemporaryDirectory(prefix='system4-continuity-') as td:
            root = Path(td)
            _, rows = _prepare_batch(root, 1)
            workspace, _, draft = rows[0]
            state, path = controller.load(workspace)
            state['checks'] = {
                'status': 'FAIL', 'mode': 'FULL_PRODUCTION',
                'checked_draft_sha256': state['draft_sha256'],
            }
            state['last_error'] = 'FULL:languagetool:LANGUAGETOOL_FINDING'
            state['phase'] = 'REPAIR_REQUIRED'
            controller.save(state, path)
            original = draft.read_text(encoding='utf-8')
            changed = original.replace(
                '</article>',
                '<p>' + ('Völlig neuer Ersatztext ohne Kontinuität. ' * 500) + '</p></article>',
            )
            draft.write_text(changed, encoding='utf-8')
            with self.assertRaisesRegex(controller.Fail, 'REPAIR_SCOPE_FAIL:REPAIR_SCOPE_TOO_LARGE'):
                controller.cmd_repair(workspace, draft)

    def test_design_change_in_repair_is_blocked_not_normalized(self):
        with tempfile.TemporaryDirectory(prefix='system4-continuity-') as td:
            root = Path(td)
            _, rows = _prepare_batch(root, 1)
            workspace, _, draft = rows[0]
            state, path = controller.load(workspace)
            state['checks'] = {
                'status': 'FAIL', 'mode': 'FULL_PRODUCTION',
                'checked_draft_sha256': state['draft_sha256'],
            }
            state['last_error'] = 'FULL:languagetool:LANGUAGETOOL_FINDING'
            state['phase'] = 'REPAIR_REQUIRED'
            controller.save(state, path)
            changed = draft.read_text(encoding='utf-8').replace(
                'system-129-table comparison-table', 'comparison-table', 1,
            )
            self.assertNotIn('system-129-table comparison-table', changed)
            draft.write_text(changed, encoding='utf-8')
            with self.assertRaisesRegex(
                controller.Fail,
                'ARTICLE_DESIGN_GUARD_FAIL:DESIGN_TABLE_SYSTEM129_CLASS_MISSING',
            ):
                controller.cmd_repair(workspace, draft)
            self.assertIn('class="comparison-table"', draft.read_text(encoding='utf-8'))

    def test_real_tool_failure_remains_hard_fail_closed(self):
        with tempfile.TemporaryDirectory(prefix='system4-continuity-') as td:
            root = Path(td)
            _, rows = _prepare_batch(root, 1)
            workspace, _, _ = rows[0]
            hard = controller.production_checks.ProductionCheckError('LANGUAGETOOL_REAL_EXECUTION_FAILED')
            with mock.patch.object(controller.production_checks, 'run_all', side_effect=hard):
                with self.assertRaisesRegex(
                    controller.Fail,
                    'FULL_CHECK_HARD_BLOCK:LANGUAGETOOL_REAL_EXECUTION_FAILED',
                ):
                    controller.cmd_fullcheck(workspace)
            state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
            self.assertEqual(state['phase'], 'CHECK_REQUIRED')
            self.assertNotEqual(state.get('checks', {}).get('status'), 'PASS')

    def test_three_item_batch_repairs_only_failed_item_and_collects_once(self):
        with tempfile.TemporaryDirectory(prefix='system4-continuity-') as td:
            root = Path(td)
            runroot, rows = _prepare_batch(root, 3)
            states = [json.loads((workspace / 'state.json').read_text(encoding='utf-8')) for workspace, _, _ in rows]
            middle_slot = states[1]['article']['plan_slot']
            per_slot_calls: dict[str, int] = {}

            def fake_run_all(repo, state, fact_pack, production_plan_item):
                slot = state['article']['plan_slot']
                count = per_slot_calls.get(slot, 0) + 1
                per_slot_calls[slot] = count
                if slot == middle_slot and count == 1:
                    raise controller.production_checks.RepairRequired(
                        'languagetool',
                        [{'error_code': 'LANGUAGETOOL_FINDING', 'rule_id': 'GERMAN_SPELLER_RULE'}],
                    )
                return _pass_result(state)

            state_paths = []
            with mock.patch.object(controller.production_checks, 'run_all', side_effect=fake_run_all) as run_all:
                for index, (workspace, _, draft) in enumerate(rows):
                    result = controller.cmd_fullcheck(workspace)
                    if index == 1:
                        self.assertEqual(result, 3)
                        old = draft.read_text(encoding='utf-8')
                        draft.write_text(_minor_repair(old), encoding='utf-8')
                        controller.cmd_repair(workspace, draft)
                        self.assertEqual(controller.cmd_fullcheck(workspace), 0)
                    else:
                        self.assertEqual(result, 0)
                    state_paths.append(workspace / 'state.json')
                self.assertEqual(run_all.call_count, 4)

            revisions = [json.loads(path.read_text(encoding='utf-8'))['revision'] for path in state_paths]
            self.assertEqual(revisions, [1, 2, 1])
            self.assertEqual(sum(per_slot_calls.values()), 4)

            out = root / 'batch'
            result = batch_gate.collect_batch(runroot / 'snapshot.json', state_paths, out)
            self.assertEqual(result['status'], 'SYSTEM4_BATCH_FULL_PASS_COLLECTED')
            self.assertEqual(result['article_count'], 3)
            self.assertFalse(result['publish_allowed'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
