import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import batch_gate
import controller


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def stage_payloads(index: int):
    source_id = f'src-test-{index}'
    ev1 = f'Erster konkreter Beleg für Artikel {index} mit ausreichender Länge und klarer Quellenbindung.'
    ev2 = f'Zweiter konkreter Beleg für Artikel {index} mit ausreichender Länge und anderer Aussage.'
    evidence = ev1 + '\n' + ev2 + '\n' + f'Zusätzlicher gesicherter Quellenkontext für Artikel {index}.'
    source = {
        'source_id': source_id,
        'source_title': f'Fachquelle Reparaturtest {index}',
        'source_url': f'https://example.org/repair-{index}',
        'retrieved_at': '2026-09-12T20:00:00Z',
        'snapshot_sha256': sha_text(evidence),
        'evidence': evidence,
    }
    research = {'contract': 'SYSTEM4_RESEARCH_EVIDENCE_V1', 'sources': [dict(source)]}
    claims = [
        {'fact_id': f'fact-{index}-a', 'source_id': source_id, 'statement': f'Erste konkrete Aussage für Artikel {index}.', 'evidence_text': ev1, 'evidence_text_sha256': sha_text(ev1)},
        {'fact_id': f'fact-{index}-b', 'source_id': source_id, 'statement': f'Zweite konkrete Aussage für Artikel {index}.', 'evidence_text': ev2, 'evidence_text_sha256': sha_text(ev2)},
    ]
    facts = {'contract': 'SYSTEM4_FACTS_EVIDENCE_V1', 'claims': claims}
    fact_pack = {'contract': 'canonical_fact_pack_v1', 'status': 'SOURCE_VERIFIED_PRODUCTION_READY', 'sources': [dict(source)], 'claims': claims}
    return research, facts, fact_pack


def write_json(root: Path, name: str, value: dict) -> Path:
    path = root / name
    path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
    return path


def write_stage_file(root: Path, name: str, text: str) -> Path:
    path = root / name
    path.write_text(text, encoding='utf-8')
    return path


def prepare_workspace(root: Path, workspace: Path, index: int) -> dict:
    snapshot = Path(__file__).resolve().parent / 'live_fixture' / 'wordpress_snapshot.json'
    controller.cmd_ingress(snapshot, workspace, index)
    research, facts, fact_pack = stage_payloads(index)
    controller.cmd_research(workspace, write_json(root, f'research-{index}.json', research))
    controller.cmd_facts(workspace, write_json(root, f'facts-{index}.json', facts))
    state_path = workspace / 'state.json'
    state = json.loads(state_path.read_text(encoding='utf-8'))
    context = {'fact_pack': fact_pack, 'production_plan_item': {'test_index': index}}
    state['production_context'] = {**context, 'sha256': controller.sha(context)}
    controller.save(state, state_path)
    return fact_pack


def draft_for(index: int, suffix: str = 'Erster Entwurf') -> str:
    return f'<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung"><h2>Prüfung</h2><p data-fact-ids="fact-{index}-a fact-{index}-b">{suffix} für Artikel {index}.</p><table class="system-129-table comparison-table"><tr><th>A</th><th>B</th></tr><tr><td>X</td><td>Y</td></tr></table></article>'


class RepairContinuityTests(unittest.TestCase):
    def test_repairable_languagetool_finding_stays_same_draft_flow(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); workspace = root / 'item0'
            prepare_workspace(root, workspace, 0)
            draft = write_stage_file(root, 'draft.html', draft_for(0))
            controller.cmd_draft(workspace, draft)
            repair = controller.production_checks.RepairRequired('languagetool',[{'error_code': 'LANGUAGETOOL_FINDING', 'rule_id': 'GERMAN_SPELLER_RULE'}])
            passed = {'contract': 'SYSTEM4_FULL_PRODUCTION_CHECK_V1', 'status': 'PASS'}
            with mock.patch.object(controller.production_checks, 'run_all', side_effect=[repair, passed]) as run_all:
                self.assertEqual(controller.cmd_fullcheck(workspace), 3)
                state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
                self.assertEqual(state['phase'], 'REPAIR_REQUIRED'); self.assertEqual(state['last_error'], 'FULL:languagetool:LANGUAGETOOL_FINDING'); self.assertEqual(state['revision'], 1)
                draft.write_text(draft_for(0, 'Korrigierter Entwurf'), encoding='utf-8')
                controller.cmd_repair(workspace, draft); self.assertEqual(controller.cmd_fullcheck(workspace), 0)
                state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
                self.assertEqual(state['phase'], 'OUTPUT_GATE_REQUIRED'); self.assertEqual(state['checks']['status'], 'PASS'); self.assertEqual(state['checks']['mode'], 'FULL_PRODUCTION'); self.assertEqual(state['revision'], 2); self.assertEqual(run_all.call_count, 2)

    def test_broad_repair_is_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); workspace = root / 'item0'; prepare_workspace(root, workspace, 0)
            original = '<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung"><h2>Prüfung</h2><p data-fact-ids="fact-0-a fact-0-b">' + ('Konkreter Ausgangstext für denselben Artikel. ' * 25) + '</p><table class="system-129-table comparison-table"><tr><th>A</th><th>B</th></tr><tr><td>X</td><td>Y</td></tr></table></article>'
            draft = write_stage_file(root, 'draft.html', original); controller.cmd_draft(workspace, draft)
            state, path = controller.load(workspace); state['checks']={'status':'FAIL','mode':'FULL_PRODUCTION','checked_draft_sha256':state['draft_sha256']}; state['last_error']='FULL:languagetool:LANGUAGETOOL_FINDING'; state['phase']='REPAIR_REQUIRED'; controller.save(state,path)
            draft.write_text('<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung"><h2>Prüfung</h2><p data-fact-ids="fact-0-a fact-0-b">' + ('Völlig neuer Ersatztext ohne Kontinuität. ' * 8) + '</p><table class="system-129-table comparison-table"><tr><th>A</th><th>B</th></tr><tr><td>X</td><td>Y</td></tr></table></article>', encoding='utf-8')
            with self.assertRaisesRegex(controller.Fail, 'REPAIR_SCOPE_FAIL:REPAIR_SCOPE_TOO_LARGE'): controller.cmd_repair(workspace, draft)

    def test_design_change_in_repair_is_blocked_not_normalized(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); workspace=root/'item0'; prepare_workspace(root,workspace,0); draft=write_stage_file(root,'draft.html',draft_for(0)); controller.cmd_draft(workspace,draft)
            state,path=controller.load(workspace); state['checks']={'status':'FAIL','mode':'FULL_PRODUCTION','checked_draft_sha256':state['draft_sha256']}; state['last_error']='FULL:languagetool:LANGUAGETOOL_FINDING'; state['phase']='REPAIR_REQUIRED'; controller.save(state,path)
            changed=draft_for(0,'Korrigierter Entwurf').replace('system-129-table comparison-table','comparison-table'); draft.write_text(changed,encoding='utf-8')
            with self.assertRaisesRegex(controller.Fail,'ARTICLE_DESIGN_GUARD_FAIL:DESIGN_TABLE_SYSTEM129_CLASS_MISSING'): controller.cmd_repair(workspace,draft)
            self.assertIn('class="comparison-table"',draft.read_text(encoding='utf-8'))

    def test_real_tool_failure_remains_hard_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); workspace = root / 'item0'; prepare_workspace(root, workspace, 0); controller.cmd_draft(workspace, write_stage_file(root, 'draft.html', draft_for(0)))
            hard = controller.production_checks.ProductionCheckError('LANGUAGETOOL_REAL_EXECUTION_FAILED')
            with mock.patch.object(controller.production_checks, 'run_all', side_effect=hard):
                with self.assertRaisesRegex(controller.Fail, 'FULL_CHECK_HARD_BLOCK:LANGUAGETOOL_REAL_EXECUTION_FAILED'): controller.cmd_fullcheck(workspace)
            state = json.loads((workspace / 'state.json').read_text(encoding='utf-8')); self.assertEqual(state['phase'], 'CHECK_REQUIRED'); self.assertNotEqual(state.get('checks', {}).get('status'), 'PASS')

    def test_seven_item_batch_repairs_only_failed_item_and_collects_once(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); snapshot = Path(__file__).resolve().parent / 'live_fixture' / 'wordpress_snapshot.json'; state_paths = []; per_slot_calls = {}
            def fake_run_all(repo, state, fact_pack, production_plan_item):
                slot = state['article']['plan_slot']; count = per_slot_calls.get(slot, 0) + 1; per_slot_calls[slot] = count
                if state['article']['title'] == 'Mistcontainer mit Deckel wählen' and count == 1: raise controller.production_checks.RepairRequired('languagetool',[{'error_code':'LANGUAGETOOL_FINDING','rule_id':'GERMAN_SPELLER_RULE'}])
                draft_sha = state['draft_sha256']
                return {'contract':'SYSTEM4_FULL_PRODUCTION_CHECK_V1','status':'PASS','checked_draft_sha256':draft_sha,'publish_allowed':False,'evidence':{'no_legacy':{'status':'PASS','legacy_import_count':0},'no_external_links':{'status':'PASS','external_link_count':0},'languagetool':{'status':'PASS','engine':'LanguageTool 6.8 / Bestand 43','finding_count':0},'ppm679':{'status':'PASS','ppm_version':'6.7.9','technical_status':'TECHNICAL_CHECK_OK','content_quality_status':'CONTENT_QUALITY_CHECK_OK','fail_closed_aggregate_status':'PASS','content_sha256':draft_sha,'language_evidence_source':'REAL_LT68_FULLCHECK_REUSED'}}}
            with mock.patch.object(controller.production_checks, 'run_all', side_effect=fake_run_all) as run_all:
                for index in range(7):
                    workspace = root / f'item{index}'; prepare_workspace(root, workspace, index); unique=' '.join(f'eigen{index}_{n}' for n in range(60))
                    draft = write_stage_file(root, f'draft-{index}.html', f'<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung"><h2>Prüfung {index}</h2><p data-fact-ids="fact-{index}-a fact-{index}-b">Artikel {index} {unique}</p><table class="system-129-table comparison-table"><tr><th>A</th><th>B</th></tr><tr><td>{index}</td><td>Y</td></tr></table></article>'); controller.cmd_draft(workspace, draft); result = controller.cmd_fullcheck(workspace)
                    if result == 3:
                        draft.write_text(f'<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung"><h2>Prüfung {index}</h2><p data-fact-ids="fact-{index}-a fact-{index}-b">Artikel {index} korrigiert {unique}</p><table class="system-129-table comparison-table"><tr><th>A</th><th>B</th></tr><tr><td>{index}</td><td>Y</td></tr></table></article>', encoding='utf-8'); controller.cmd_repair(workspace, draft); self.assertEqual(controller.cmd_fullcheck(workspace), 0)
                    else: self.assertEqual(result, 0)
                    state_paths.append(workspace / 'state.json')
                self.assertEqual(run_all.call_count, 8)
            revisions = [json.loads(path.read_text(encoding='utf-8'))['revision'] for path in state_paths]; self.assertEqual(revisions, [1,1,2,1,1,1,1]); self.assertEqual(sum(per_slot_calls.values()), 8)
            out = root / 'batch'; result = batch_gate.collect_batch(snapshot, state_paths, out); self.assertEqual(result['status'], 'SYSTEM4_BATCH_FULL_PASS_COLLECTED'); self.assertEqual(result['article_count'], 7); self.assertEqual(result['batch_sha256'], '7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a'); self.assertFalse(result['publish_allowed'])


if __name__ == '__main__': unittest.main(verbosity=2)
