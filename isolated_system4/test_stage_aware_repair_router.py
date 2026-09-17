from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import point0_snapshot
import repair_router


def state_for(finding:dict)->dict:
    return {'phase':'REPAIR_REQUIRED','checks':{'status':'FAIL','findings':[finding]},'last_error':str(finding.get('error_code') or 'FAIL'),'machine_repair_cycle':0,'article':{'title':'Testartikel','target_keyword':'Test'}}


class StageAwareRepairRouterTests(unittest.TestCase):
    def test_title_category_slot_link_source_and_body_route_to_owners(self):
        cases=[
            ({'error_code':'BLOCKED_CONTENT_TITLE_COLON','field':'content.title','failed_rule':'ARTICLE_TITLE_MUST_NOT_CONTAIN_COLON'},('PARENT_METADATA','TITLE_BINDING')),
            ({'error_code':'CATEGORY_INVALID','field':'content.category'},('PARENT_METADATA','CATEGORY_BINDING')),
            ({'error_code':'PLAN_SLOT_INVALID','field':'plan_slot'},('PARENT_METADATA','PLAN_SLOT_BINDING')),
            ({'error_code':'LINK_BINDING_INVALID','field':'links[0].href'},('CONTEXT_BINDING','LINK_BINDING')),
            ({'error_code':'FACT_NOT_SUPPORTED','field':'fact_pack.claims'},('RESEARCH_BINDING','RESEARCH_OR_FACT_BINDING')),
            ({'error_code':'LANGUAGETOOL_FINDING','field':'content.body'},('DRAFT_BODY','SAME_ARTICLE_BODY')),
        ]
        for finding,expected in cases:
            with self.subTest(finding=finding):
                route=repair_router.classify(state_for(finding))
                self.assertEqual((route['owner'],route['target']),expected)

    def test_every_repairable_owner_emits_nonterminal_verified_continuation(self):
        cases=[
            ({'error_code':'CATEGORY_INVALID','field':'content.category'},'PARENT_METADATA','CATEGORY_BINDING','RETURN_TO_OWNER'),
            ({'error_code':'PLAN_SLOT_INVALID','field':'plan_slot'},'PARENT_METADATA','PLAN_SLOT_BINDING','RETURN_TO_OWNER'),
            ({'error_code':'LINK_BINDING_INVALID','field':'links[0].href'},'CONTEXT_BINDING','LINK_BINDING','RETURN_TO_OWNER'),
            ({'error_code':'FACT_NOT_SUPPORTED','field':'fact_pack.claims'},'RESEARCH_BINDING','RESEARCH_OR_FACT_BINDING','RETURN_TO_OWNER'),
            ({'error_code':'LANGUAGETOOL_FINDING','field':'content.body'},'DRAFT_BODY','SAME_ARTICLE_BODY','SAME_ARTICLE_BODY_REPAIR'),
            ({'error_code':'NEW_FUTURE_CHECKER_FINDING'},'DRAFT_BODY','SAME_ARTICLE_BODY','SAME_ARTICLE_BODY_REPAIR'),
        ]
        for finding,owner,target,status in cases:
            with self.subTest(owner=owner,target=target), tempfile.TemporaryDirectory() as td:
                workspace=Path(td)/'item-0'; workspace.mkdir()
                (workspace/'state.json').write_text(json.dumps(state_for(finding)),encoding='utf-8')
                result=repair_router.route(workspace)
                verified=repair_router.verify_continuation_result(workspace,result)
                self.assertEqual(verified['contract'],repair_router.RETURN_CONTRACT)
                self.assertEqual(verified['status'],status)
                self.assertEqual(verified['owner'],owner)
                self.assertEqual(verified['target'],target)
                self.assertTrue(verified['repairable'])
                self.assertFalse(verified['terminal'])
                self.assertTrue(verified['continuation_required'])
                self.assertEqual(verified['cycle'],1)
                request=json.loads((workspace/'machine_repair_request.json').read_text(encoding='utf-8'))
                self.assertEqual(request,verified)

    def test_mixed_owner_findings_are_grouped_before_routing(self):
        body={'error_code':'LANGUAGETOOL_FINDING','field':'content.body','rule_id':'GERMAN_SPELLER_RULE'}
        link={'error_code':'LINK_BINDING_INVALID','field':'links[0].href'}
        state=state_for(body); state['checks']['findings']=[body,link]
        route=repair_router.classify(state)
        self.assertEqual((route['owner'],route['target']),('CONTEXT_BINDING','LINK_BINDING'))
        self.assertEqual(route['findings'],[link])
        self.assertEqual(route['all_findings'],[body,link])
        self.assertEqual(route['finding_count'],1)
        self.assertEqual(route['all_finding_count'],2)
        self.assertEqual(route['pending_owner_target_groups'][0]['owner'],'DRAFT_BODY')
        with tempfile.TemporaryDirectory() as td:
            workspace=Path(td)/'item-0'; workspace.mkdir(); (workspace/'state.json').write_text(json.dumps(state),encoding='utf-8')
            result=repair_router.route(workspace)
            verified=repair_router.verify_continuation_result(workspace,result)
            self.assertEqual(verified['status'],'RETURN_TO_OWNER')
            self.assertEqual(verified['owner'],'CONTEXT_BINDING')
            self.assertEqual(verified['target'],'LINK_BINDING')
            self.assertEqual(verified['findings'],[link])
            self.assertEqual(verified['all_findings'],[body,link])
            self.assertEqual(verified['pending_owner_target_groups'][0]['owner'],'DRAFT_BODY')

    def test_tampered_or_missing_continuation_contract_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            workspace=Path(td)/'item-0'; workspace.mkdir()
            finding={'error_code':'FACT_NOT_SUPPORTED','field':'fact_pack.claims'}
            (workspace/'state.json').write_text(json.dumps(state_for(finding)),encoding='utf-8')
            result=repair_router.route(workspace)
            bad=copy.deepcopy(result); bad['terminal']=True
            with self.assertRaisesRegex(repair_router.RepairRouteError,'MUST_BE_NONTERMINAL'):
                repair_router.verify_continuation_result(workspace,bad)
            bad=copy.deepcopy(result); bad['finding']['field']='tampered'
            with self.assertRaisesRegex(repair_router.RepairRouteError,'FINDING_HASH_INVALID'):
                repair_router.verify_continuation_result(workspace,bad)
            bad=copy.deepcopy(result); bad.pop('contract')
            with self.assertRaisesRegex(repair_router.RepairRouteError,'CONTRACT_INVALID'):
                repair_router.verify_continuation_result(workspace,bad)

    def test_unknown_repairable_finding_defaults_to_same_article_body_not_terminal(self):
        route=repair_router.classify(state_for({'error_code':'NEW_FUTURE_CHECKER_FINDING'}))
        self.assertEqual(route['owner'],'DRAFT_BODY')
        self.assertEqual(route['target'],'SAME_ARTICLE_BODY')

    def test_title_rule_is_repaired_by_parent_and_restarted_from_point0(self):
        with tempfile.TemporaryDirectory() as td:
            runtime=Path(td); workspace=runtime/'item-0'; workspace.mkdir()
            finding={'error_code':'BLOCKED_CONTENT_TITLE_COLON','field':'content.title','failed_rule':'ARTICLE_TITLE_MUST_NOT_CONTAIN_COLON','actual':'Pferde prüfen: Checkliste','expected':'no colon'}
            state=state_for(finding); state['machine_repair_cycle']=0
            (workspace/'state.json').write_text(json.dumps(state),encoding='utf-8')
            item={'title':'Pferde prüfen: Checkliste','target_keyword':'Pferde prüfen','category':'test-beratung','article_type':'Beratung','plan_slot':'a'*64}
            material={'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','content_or_format_payload_present':False,'item_count':1,'items':[item],'maximum_articles':0,'maximum_articles_per_type':0,'publish_allowed':False,'status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE'}
            material['batch_sha256']=repair_router.sha256(repair_router.canon(material))
            prod={'contract':'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1','next_textmachine_metadata_batch':material,'source_snapshot_original_sha256':repair_router.sha256(repair_router.canon([item])),'system4_root_manifest_sha256':'b'*64}
            evidence='Gebundene Quelle mit ausreichend langem, überprüfbarem Evidenztext für den Test.'
            source={'source_id':'s1','source_title':'Testquelle','source_url':'https://example.org/source','retrieved_at':'2026-09-14T00:00:00Z','evidence':evidence,'snapshot_sha256':repair_router.sha256(evidence.encode()),'http_status':200,'source_kind':'parent_machine_bound_snapshot'}
            p0=point0_snapshot.build(production_snapshot_bytes=repair_router.canon(prod),root_manifest_sha256='b'*64,head_sha='c'*40,research_provider='TEST',sources=[source])
            (runtime/'point0-0.json').write_bytes(point0_snapshot.canon(p0))
            def fake_root(argv):
                new_workspace=Path(argv[3]); new_workspace.mkdir(); (new_workspace/'state.json').write_text(json.dumps({'phase':'RESEARCH_REQUIRED'}),encoding='utf-8'); return 0
            with mock.patch.object(repair_router.root_entry,'_critical_manifest_sha256',return_value='b'*64), mock.patch.object(repair_router.root_entry,'_git',return_value='c'*40), mock.patch.object(repair_router.root_entry,'main',side_effect=fake_root):
                result=repair_router.route(workspace)
            self.assertEqual(result['status'],'RESTARTED')
            self.assertEqual(result['owner'],'PARENT_METADATA')
            self.assertFalse(result['terminal'])
            self.assertTrue(result['continuation_required'])
            repair_router.verify_continuation_result(workspace,result)
            self.assertNotIn(':',result['to_article']['title'])
            self.assertTrue(Path(result['workspace']).name.startswith('item-0-repair-1'))
            new_point=json.loads(Path(result['point0']).read_text(encoding='utf-8'))
            new_raw=point0_snapshot.verify(new_point)
            new_prod=json.loads(new_raw.decode('utf-8'))
            self.assertNotIn(':',new_prod['next_textmachine_metadata_batch']['items'][0]['title'])

    def test_wrong_phase_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            workspace=Path(td)/'item-0'; workspace.mkdir(); (workspace/'state.json').write_text(json.dumps({'phase':'CHECK_REQUIRED'}),encoding='utf-8')
            with self.assertRaisesRegex(repair_router.RepairRouteError,'REPAIR_PHASE_REQUIRED'):
                repair_router.route(workspace)

if __name__=='__main__': unittest.main(verbosity=2)
