from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import batch_gate
import controller
import live_parity_v2 as live_parity
import repair_proof_contract as repair_proof
import real7_article0_quality_authority_probe
import test_route_input_factory
import verify_real7_multifinding_repair
import workspace_recovery_capsule as recovery

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
        'Befund wird vorab sorgfältig geprüft',
        'Abweichung wird vorher eindeutig geklärt',
        'Zustand wird aktuell erneut bestätigt',
        'Funktion wird gezielt vollständig kontrolliert',
        'Ergebnis wird neu eindeutig festgestellt',
        'Prüfpunkt bleibt weiterhin klar nachvollziehbar',
        'Kontrolle erfolgt direkt vor Fahrtbeginn',
        'Beobachtung wird anschließend eindeutig bewertet',
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

    def test_repair_required_survives_process_death_and_restores_same_article(self):
        with tempfile.TemporaryDirectory(prefix='system4-restart-repair-') as td:
            root = Path(td)
            _, rows = _prepare_batch(root, 1)
            workspace, generated, _ = rows[0]
            state_before = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
            repair = controller.production_checks.RepairRequired(
                'languagetool',
                [{'error_code': 'LANGUAGETOOL_FINDING', 'rule_id': 'GERMAN_SPELLER_RULE'}],
            )
            with mock.patch.object(controller.production_checks, 'run_all', side_effect=repair):
                self.assertEqual(controller.cmd_fullcheck(workspace), 3)

            stopped = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
            self.assertEqual(stopped['phase'], 'REPAIR_REQUIRED')
            self.assertEqual(stopped['revision'], 1)
            self.assertEqual(stopped['checks']['repair_owner'], 'DRAFT_WORKER')
            original_article = dict(stopped['article'])
            original_findings = list(stopped['checks']['findings'])
            original_draft = stopped['draft_markdown']
            original_draft_sha = stopped['draft_sha256']

            capsule = root / 'article0-repair-required.recovery.json'
            created = recovery.create_capsule(workspace, capsule)
            self.assertEqual(created['workspace_identity']['phase'], 'REPAIR_REQUIRED')
            self.assertEqual(created['workspace_identity']['revision'], 1)
            self.assertEqual(created['workspace_identity']['draft_sha256'], original_draft_sha)

            # Simulate the historical failure exactly: the original task/workspace is gone.
            shutil.rmtree(workspace)
            self.assertFalse(workspace.exists())

            restarted_generated = root / 'restarted-generated'
            cp = subprocess.run(
                [
                    sys.executable,
                    str(HERE / 'restart_repair_probe.py'),
                    str(capsule),
                    str(workspace),
                    str(restarted_generated),
                ],
                cwd=HERE.parent,
                env=_env(),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(cp.returncode, 0, cp.stdout + '\n' + cp.stderr)
            probe = json.loads(cp.stdout.strip().splitlines()[-1])
            self.assertEqual(probe['status'], 'PASS')
            self.assertTrue(probe['new_process_restore_and_repair'])
            self.assertTrue(probe['same_article'])

            restored = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
            self.assertEqual(restored['article'], original_article)
            self.assertEqual(restored['phase'], 'CHECK_REQUIRED')
            self.assertEqual(restored['revision'], 2)
            self.assertNotEqual(restored['draft_sha256'], original_draft_sha)
            self.assertNotEqual(restored['draft_markdown'], original_draft)

            # The recovery capsule itself must preserve the exact pre-restart findings.
            verified = recovery.verify_capsule(capsule)
            self.assertEqual(
                verified['workspace_identity']['checks_sha256'],
                recovery._sha_bytes(recovery._canon({'status': 'FAIL', 'mode': 'FULL_PRODUCTION', 'errors': stopped['checks']['errors'], 'findings': original_findings, 'checker': stopped['checks']['checker'], 'checked_draft_sha256': stopped['checks']['checked_draft_sha256'], 'repair_owner': stopped['checks']['repair_owner'], 'repair_owners': stopped['checks']['repair_owners']})),
            )

            passed = _pass_result(restored)
            with mock.patch.object(controller.production_checks, 'run_all', return_value=passed):
                self.assertEqual(controller.cmd_fullcheck(workspace), 0)
            final = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
            self.assertEqual(final['phase'], 'OUTPUT_GATE_REQUIRED')
            self.assertEqual(final['checks']['status'], 'PASS')
            self.assertEqual(final['revision'], 2)
            self.assertEqual(final['article'], original_article)

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
            changed = _minor_repair(changed)
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


    def test_real7_four_finding_returns_to_same_article_until_real_checks_pass(self):
        with tempfile.TemporaryDirectory(prefix='system4-real7-multifinding-') as td:
            root = Path(td)
            fixture = root / 'fixture'
            runroot = root / 'run'
            output = root / 'output'
            evidence = root / 'evidence'
            token = 'real7-multifinding-' + root.name

            with mock.patch.dict(os.environ, {
                'SYSTEM4_FRESH_RUN_TOKEN': token,
                'SYSTEM4_REPAIR_EVIDENCE_OUTPUT_DIR': str(evidence),
                'SYSTEM4_TEST_REAL7_PPM_MULTIFINDING': '1',
            }, clear=False):
                # Bind this technical repair proof to the actual article-0 authority:
                # Beratung, duplicate <=2%, conclusion >=10%, table new-token >=18%.
                self.assertEqual(real7_article0_quality_authority_probe.main(), 0)

                test_route_input_factory.create(fixture, 1)
                live_parity.FIX = fixture.resolve()
                live_parity.prepare(runroot)
                result = live_parity.item(runroot, 0)
                self.assertEqual(result['status'], 'PASS')
                self.assertGreaterEqual(len(result.get('repair_artifacts') or []), 2)
                self.assertEqual(result['revision'], 3)

                previous_after = None
                first_codes = None
                for artifact in result['repair_artifacts']:
                    self.assertEqual(artifact['worker'], 'DETERMINISTIC_TEST_WORKER')
                    self.assertFalse(artifact['codex_used'])
                    self.assertFalse(artifact['prepared_final_fixture_used'])
                    self.assertTrue(artifact['repair_routing_proven'])
                    self.assertTrue(artifact['same_article_repair'])
                    self.assertTrue(artifact['recheck_executed'])
                    self.assertFalse(artifact['live_codex_repair_proven'])
                    if previous_after is not None:
                        self.assertEqual(previous_after, artifact['before_sha256'])
                    previous_after = artifact['after_sha256']
                    if first_codes is None:
                        first_codes = {
                            str(row.get('error_code') or '')
                            for row in artifact.get('findings') or []
                        }

                self.assertTrue({
                    'BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO',
                    'BLOCKED_KNOWN_SHORT_CONCLUSION',
                    'BLOCKED_WAVE2_CONCLUSION_BALANCE',
                    'BLOCKED_WAVE2_TABLE_VALUE',
                }.issubset(first_codes or set()))

                with mock.patch.dict(os.environ, {
                    'SYSTEM4_LIVE_PARITY_OUTPUT_DIR': str(output),
                }, clear=False):
                    final = live_parity.finalize(runroot)
                self.assertEqual(final['lt'], ['PASS'])
                self.assertEqual(final['ppm'], ['PASS'])
                self.assertEqual(final['repair_proof_level'], 'REPAIR_ROUTING_PROVEN')
                self.assertFalse(final['real_codex_repair_proven'])

                self.assertEqual(
                    verify_real7_multifinding_repair.main([
                        'verify_real7_multifinding_repair.py',
                        str(evidence),
                        str(output),
                    ]),
                    0,
                )

    def test_user_approved_codex_reference_separates_content_quality_from_structure(self):
        body = (HERE / 'testdata' / 'article_quality_reference_putzplatzmatten_20260918.txt').read_text(encoding='utf-8')
        metadata = json.loads(
            (HERE / 'testdata' / 'article_quality_reference_putzplatzmatten_20260918.json').read_text(encoding='utf-8')
        )
        result = repair_proof.validate_quality_reference(body, metadata)
        self.assertEqual(result['content_quality_reference'], 'USER_APPROVED_POSITIVE_REFERENCE')
        self.assertEqual(result['structural_compliance'], 'NOT_ASSERTED')
        self.assertEqual(result['fullcheck_status'], 'NOT_ASSERTED')
        self.assertFalse(result['production_pass'])

    def test_green_mock_prebuilt_or_testworker_repair_never_counts_as_real_codex_repair(self):
        base = {
            'repair_routing_proven': True,
            'same_article_repair': True,
            'recheck_executed': True,
            'pre_repair_sha256': '1' * 64,
            'post_repair_sha256': '2' * 64,
            'findings_sha256': '3' * 64,
            'pre_revision': 1,
            'post_revision': 2,
            'durable_before_ref': 'proof/pre.html',
            'durable_after_ref': 'proof/post.html',
            'durable_findings_ref': 'proof/findings.json',
            'fullcheck_status': 'PASS',
            'languagetool_status': 'PASS',
            'ppm_status': 'PASS',
            'ppm_content_quality_status': 'CONTENT_QUALITY_CHECK_OK',
        }
        cases = (
            dict(base, worker='CODEX_CLOUD', codex_used=True, mocks_used=True, prepared_final_fixture_used=False),
            dict(base, worker='CODEX_CLOUD', codex_used=True, mocks_used=False, prepared_final_fixture_used=True),
            dict(base, worker='DETERMINISTIC_TEST_WORKER', codex_used=False, mocks_used=False, prepared_final_fixture_used=False),
        )
        for evidence in cases:
            with self.subTest(worker=evidence['worker'], mocks=evidence['mocks_used'], fixture=evidence['prepared_final_fixture_used']):
                proof = repair_proof.classify_repair_proof(evidence)
                self.assertEqual(proof['repair_proof_level'], repair_proof.ROUTING_PROVEN)
                self.assertTrue(proof['repair_routing_proven'])
                self.assertFalse(proof['real_codex_repair_proven'])

    def test_real_codex_repair_proof_requires_durable_before_after_and_quality_evidence(self):
        evidence = {
            'repair_routing_proven': True,
            'same_article_repair': True,
            'recheck_executed': True,
            'worker': 'CODEX_CLOUD',
            'codex_used': True,
            'mocks_used': False,
            'prepared_final_fixture_used': False,
            'pre_repair_sha256': '1' * 64,
            'post_repair_sha256': '2' * 64,
            'findings_sha256': '3' * 64,
            'pre_revision': 1,
            'post_revision': 2,
            'durable_before_ref': 'proof/pre.html',
            'durable_after_ref': 'proof/post.html',
            'durable_findings_ref': 'proof/findings.json',
            'fullcheck_status': 'PASS',
            'languagetool_status': 'PASS',
            'ppm_status': 'PASS',
            'ppm_content_quality_status': 'CONTENT_QUALITY_CHECK_OK',
        }
        complete = repair_proof.classify_repair_proof(evidence)
        self.assertEqual(complete['repair_proof_level'], repair_proof.REAL_CODEX_PROVEN)
        self.assertTrue(complete['real_codex_repair_proven'])

        missing_bytes = dict(evidence, durable_before_ref='')
        blocked = repair_proof.classify_repair_proof(missing_bytes)
        self.assertEqual(blocked['repair_proof_level'], repair_proof.ROUTING_PROVEN)
        self.assertFalse(blocked['real_codex_repair_proven'])
        self.assertIn('durable_before_ref', blocked['missing_real_codex_evidence'])

        missing_quality = dict(evidence, ppm_content_quality_status='CONTENT_QUALITY_CHECK_FAILED')
        blocked_quality = repair_proof.classify_repair_proof(missing_quality)
        self.assertEqual(blocked_quality['repair_proof_level'], repair_proof.ROUTING_PROVEN)
        self.assertFalse(blocked_quality['real_codex_repair_proven'])
        self.assertIn('ppm_content_quality_status', blocked_quality['missing_real_codex_evidence'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
