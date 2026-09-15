from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import chat_start_gate
import point0_snapshot
import root_entry
import supervisor

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CONTROLLER = HERE / 'controller.py'
ROOT_ENTRY = HERE / 'root_entry.py'


def h(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def stable(value) -> str:
    raw=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def build_point0(path: Path) -> dict:
    manifest=root_entry._critical_manifest_sha256()
    head=subprocess.check_output(['git','rev-parse','--verify','HEAD'],cwd=REPO,text=True).strip()
    article={
        'title':'Kontext muss vor Draft gebunden sein',
        'target_keyword':'Kontextbindung',
        'category':'test-beratung',
        'article_type':'Beratung',
        'plan_slot':h('context-required-slot-'+head),
    }
    link={
        'active':True,'anchor':'Test Beratung','hierarchy_path':['Test'],
        'href':'/test-beratung/','reason':'Context-Regressionsprüfung',
        'role':'parent_category','section_id':'criteria',
        'snapshot_contract':'WORDPRESS_LINK_TARGET_SNAPSHOT_V1',
        'target_status':'publish','target_type':'page',
    }
    registry={'contract':'portal_link_registry_snapshot_v2','entries':[dict(link)]}
    quality={
        'contract':'content_structure_language_binding_v2',
        'link_bindings':[dict(link)],
        'portal_link_registry':registry,
        'portal_link_registry_hash':stable(registry),
        'wordpress_category':{'slug':'test-beratung'},
    }
    plan={
        'article_type':'Beratung','target_keyword':'Kontextbindung',
        'topic':'Kontext muss vor Draft gebunden sein',
        'search_intent':'DECISION_SUPPORT','gold_core_binding':'TEST',
        'category_binding':{'slug':'test-beratung'},
        'quality_binding':quality,'quality_binding_hash':stable(quality),
    }
    pre=point0_snapshot.prewrite_from_plan(article,0,plan)
    evidence=(
        'Diese reale Testquelle enthält genügend gebundenen Belegtext für den System-4-Test. '
        'Der Kontext muss vor dem Schreiben verbindlich gebunden sein. '
        'Eine bekannte Pflicht darf nicht erst im Fullcheck auftauchen. '
        'Der Draft darf erst nach erfolgreicher Context-Bindung beginnen.'
    )
    source={
        'source_id':'context-source-'+head[:12],
        'source_title':'Reale Testquelle Kontextbindung',
        'source_url':'https://example.org/system4/contextbindung',
        'retrieved_at':'2026-09-15T00:00:00Z',
        'snapshot_sha256':h(evidence),'evidence':evidence,
        'http_status':200,'source_kind':'WEB',
    }
    batch_sha=h('context-required-batch-'+head)
    snapshot={
        'contract':'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1',
        'next_textmachine_metadata_batch':{
            'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2',
            'status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
            'publish_allowed':False,'batch_sha256':batch_sha,
            'item_count':1,'items':[article],
        },
        'system4_root_manifest_sha256':manifest,
    }
    event={
        'contract':chat_start_gate.START_EVENT_CONTRACT,
        'button_id':chat_start_gate.START_BUTTON_ID,
        'action':chat_start_gate.START_ACTION,
        'route':chat_start_gate.START_ROUTE,
        'article_count':1,'batch_sha256':batch_sha,'publish_allowed':False,
    }
    bound=chat_start_gate.bind(snapshot,event)
    raw=(json.dumps(bound,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')
    p0=point0_snapshot.build(
        production_snapshot_bytes=raw,
        root_manifest_sha256=manifest,
        head_sha=head,
        research_provider='SYSTEM4_CONTEXT_REGRESSION_TEST',
        source_pools=[[source]],
        prewrite_bindings=[pre],
    )
    path.write_bytes(point0_snapshot.canon(p0))
    return {'source':source,'article':article}


def run_controller(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable,str(CONTROLLER),*map(str,args)],
        cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False,
    )


class ContextRequiredRegressionTests(unittest.TestCase):
    def test_facts_cannot_open_draft_directly(self):
        with tempfile.TemporaryDirectory(prefix='system4-context-required-') as td_raw:
            td=Path(td_raw)
            point0=td/'point0.json'
            workspace=td/'workspace'
            bound=build_point0(point0)

            root=subprocess.run(
                [sys.executable,str(ROOT_ENTRY),'start-point0',str(point0),str(workspace),'0'],
                cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False,
            )
            self.assertEqual(root.returncode,0,root.stdout.decode()+root.stderr.decode())
            self.assertIn('SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY',root.stdout.decode())

            research_obj=supervisor.expected_research_document(workspace)
            research=td/'research.json'
            research.write_text(json.dumps(research_obj,ensure_ascii=False),encoding='utf-8')
            cp=run_controller('research',workspace,research)
            self.assertEqual(cp.returncode,0,cp.stdout.decode()+cp.stderr.decode())

            evidence=bound['source']['evidence']
            ev1='Der Kontext muss vor dem Schreiben verbindlich gebunden sein.'
            ev2='Eine bekannte Pflicht darf nicht erst im Fullcheck auftauchen.'
            self.assertIn(ev1,evidence); self.assertIn(ev2,evidence)
            facts_obj={
                'contract':'SYSTEM4_FACTS_EVIDENCE_V1',
                'claims':[
                    {'fact_id':'fact-context-1','source_id':bound['source']['source_id'],'statement':'Der Kontext muss vor dem Schreiben verbindlich gebunden sein.','evidence_text':ev1,'evidence_text_sha256':h(ev1)},
                    {'fact_id':'fact-context-2','source_id':bound['source']['source_id'],'statement':'Eine bekannte Pflicht darf nicht erst im Fullcheck auftauchen.','evidence_text':ev2,'evidence_text_sha256':h(ev2)},
                ],
            }
            facts=td/'facts.json'
            facts.write_text(json.dumps(facts_obj,ensure_ascii=False),encoding='utf-8')
            cp=run_controller('facts',workspace,facts)
            self.assertEqual(cp.returncode,0,cp.stdout.decode()+cp.stderr.decode())

            state=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
            self.assertEqual(state['phase'],'CONTEXT_REQUIRED')
            self.assertIsNone(state['production_context'])
            self.assertIsNone(state['authoring_contract'])

            draft=td/'draft.html'
            draft.write_text('<article>nicht zulässig vor Context</article>',encoding='utf-8')
            blocked=run_controller('draft',workspace,draft)
            self.assertEqual(blocked.returncode,2)
            self.assertIn('PHASE_FAIL:DRAFT',blocked.stdout.decode())

            state_after=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
            self.assertEqual(state_after['phase'],'CONTEXT_REQUIRED')
            self.assertEqual(state_after['revision'],0)
            self.assertIsNone(state_after['production_context'])
            self.assertIsNone(state_after['authoring_contract'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
