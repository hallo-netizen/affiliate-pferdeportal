from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import tempfile
import unittest
from pathlib import Path

import batch_gate
import chat_delivery_gate
import codex_entry
import controller
import full_route_start
import handoff_transport
import parent_start
import supervisor
from real_route_test_support import valid_real_article

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
BOUND_REL='isolated_system4/bound_launches/real_article_pferdeanhaenger_beladen_20260914.json'
BOUND_SHA256='d081ee92694fd9f5dfed9b74f8bf05966250f20b53768b92a10fa78915aa5a01'

def canon(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')

def write_json(path:Path,value):
    path.write_bytes(canon(value)); return path

def _evidence_claims(research:dict)->list[dict]:
    claims=[]
    for index,source in enumerate(research['sources']):
        evidence=str(source['evidence']).strip()
        match=re.match(r'^(.{20,}?[.!?])(?:\s|$)',evidence,re.S)
        excerpt=(match.group(1) if match else evidence[:180]).strip()
        if len(excerpt)<20:
            continue
        claims.append({
            'fact_id':f'bound-chat-fact-{index+1}',
            'source_id':source['source_id'],
            'statement':excerpt,
            'evidence_text':excerpt,
            'evidence_text_sha256':hashlib.sha256(excerpt.encode('utf-8')).hexdigest(),
        })
    if len(claims)<2:
        raise AssertionError('CHAT_TEST_NEEDS_AT_LEAST_TWO_BOUND_CLAIMS')
    return claims

def _run_parent_bound_without_codex(runtime:Path)->Path:
    capsule=REPO/BOUND_REL
    if hashlib.sha256(capsule.read_bytes()).hexdigest()!=BOUND_SHA256:
        raise AssertionError('CHAT_START_BOUND_CAPSULE_SHA_MISMATCH')
    rc=parent_start.main(['parent_start.py','start-bound',BOUND_REL,BOUND_SHA256,str(runtime)])
    if rc!=0:
        raise AssertionError('CHAT_START_PARENT_START_FAILED:'+str(rc))
    receipt=json.loads((runtime/'parent_start_receipt.json').read_text(encoding='utf-8'))
    if receipt['article_count']!=1 or receipt['publish_allowed'] is not False:
        raise AssertionError('CHAT_START_PARENT_RECEIPT_INVALID')
    workspace=Path(receipt['workspaces'][0])

    # This invokes only the machine worker-dispatch gate. No Codex model/network call is made.
    if codex_entry.main(['codex_entry.py','worker-start',str(workspace)])!=0:
        raise AssertionError('CHAT_START_WORKER_GATE_FAILED')

    research=supervisor.expected_research_document(workspace)
    research_path=write_json(runtime/'deterministic-research.json',research)
    if controller.main(['controller.py','research',str(workspace),str(research_path)])!=0:
        raise AssertionError('CHAT_START_RESEARCH_FAILED')

    facts={'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':_evidence_claims(research)}
    facts_path=write_json(runtime/'deterministic-facts.json',facts)
    if controller.main(['controller.py','facts',str(workspace),str(facts_path)])!=0:
        raise AssertionError('CHAT_START_FACTS_FAILED')

    full_route_start._machine_context(workspace,runtime,0)
    if codex_entry.main(['codex_entry.py','next',str(workspace)])!=0:
        raise AssertionError('CHAT_START_DRAFT_GATE_FAILED')
    state=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
    draft=valid_real_article(state,0)
    draft_path=runtime/'deterministic-draft.html'
    draft_path.write_text(draft,encoding='utf-8')
    if controller.main(['controller.py','draft',str(workspace),str(draft_path)])!=0:
        raise AssertionError('CHAT_START_DRAFT_FAILED')
    full_rc=controller.main(['controller.py','fullcheck',str(workspace)])
    if full_rc!=0:
        raise AssertionError('CHAT_START_REAL_FULLCHECK_NOT_PASS:'+str(full_rc))

    state_path=workspace/'state.json'
    state=json.loads(state_path.read_text(encoding='utf-8'))
    if state.get('phase')!='OUTPUT_GATE_REQUIRED':
        raise AssertionError('CHAT_START_OUTPUT_GATE_NOT_REACHED')
    if state['checks']['production_evidence']['evidence']['languagetool']['engine']!='LanguageTool 6.8 / Bestand 43':
        raise AssertionError('CHAT_START_REAL_LT_BINDING_MISSING')
    if state['checks']['production_evidence']['evidence']['ppm679']['ppm_version']!='6.7.9':
        raise AssertionError('CHAT_START_REAL_PPM_BINDING_MISSING')

    batch_dir=runtime/'batch'
    collected=batch_gate.collect_batch(workspace/'bound_snapshot.json',[state_path],batch_dir)
    if collected.get('status')!='SYSTEM4_BATCH_FULL_PASS_COLLECTED' or collected.get('article_count')!=1:
        raise AssertionError('CHAT_START_BATCH_NOT_PASS')

    source=write_json(runtime/'handoff-source.json',full_route_start._handoff([state]))
    canonical=runtime/handoff_transport.HANDOFF_FILENAME
    canonical_bytes=handoff_transport.canonicalize_handoff(source,canonical)
    inline=runtime/handoff_transport.INLINE_FILENAME
    envelope=handoff_transport.inline_pack(canonical,inline)
    reconstructed=handoff_transport.inline_unpack(inline,runtime/'parent-chat')
    if reconstructed.read_bytes()!=canonical_bytes:
        raise AssertionError('CHAT_START_INLINE_RECONSTRUCTION_MISMATCH')
    if envelope['plaintext_sha256']!=hashlib.sha256(canonical_bytes).hexdigest():
        raise AssertionError('CHAT_START_INLINE_SHA_MISMATCH')
    return reconstructed

def _write_mutation(base:Path,payload:dict,name:str)->Path:
    path=base/name
    path.write_bytes(canon(payload))
    return path

@unittest.skipUnless(os.environ.get('SYSTEM4_REAL_TOOL_CORRIDOR')=='1','exact LT/PPM corridor is an explicit isolated test stage')
class LocalEndToEndChatHandoffRealTests(unittest.TestCase):
    def test_chat_start_to_real_wordpress_artifact_positive_and_negative(self):
        output_env=os.environ.get('SYSTEM4_CHAT_ARTIFACT_DIR')
        self.assertTrue(output_env,'SYSTEM4_CHAT_ARTIFACT_DIR_REQUIRED')
        output_dir=Path(output_env)
        with tempfile.TemporaryDirectory(prefix='system4-chat-e2e-') as td:
            runtime=Path(td)/'runtime'
            final=_run_parent_bound_without_codex(runtime)
            payload,raw=handoff_transport.read_validate_handoff(final)

            self.assertEqual(payload['contract'],'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2')
            self.assertFalse(payload['publish_allowed'])
            self.assertEqual(len(payload['articles']),1)
            wr=payload['wordpress_review']
            self.assertEqual(wr['file_format'],'JSON')
            self.assertEqual(wr['mime_type'],'application/json')
            self.assertEqual(wr['intended_next_step'],'WORDPRESS_DIRECT_IMPORT')
            self.assertEqual(wr['plugin_name'],'Portal SEO Editorial Plan Compiler')
            self.assertEqual(wr['plugin_version_verified_against'],'0.28.23')
            self.assertEqual(wr['ppm_version_verified_against'],'6.7.9')
            self.assertTrue(wr['direct_wordpress_upload_ready'])
            self.assertIsNone(wr['direct_upload_block_reason'])
            self.assertEqual(wr['required_downstream_components'],[])
            row=payload['articles'][0]
            for field in ('title','target_keyword','category','article_type','plan_slot','body','production_context','languagetool','ppm679'):
                self.assertIn(field,row)
            self.assertEqual(row['final_draft_sha256'],hashlib.sha256(row['body'].encode('utf-8')).hexdigest())
            self.assertEqual(row['languagetool']['status'],'PASS')
            self.assertEqual(row['languagetool']['finding_count'],0)
            self.assertEqual(row['ppm679']['status'],'PASS')
            self.assertEqual(row['ppm679']['content_sha256'],row['final_draft_sha256'])

            # NEGATIVE: production authorization may never arrive as true.
            bad=copy.deepcopy(payload); bad['publish_allowed']=True
            with self.assertRaisesRegex(handoff_transport.HandoffError,'HANDOFF_PUBLISH_MUST_BE_FALSE'):
                handoff_transport.read_validate_handoff(_write_mutation(Path(td),bad,'bad-publish.json'))

            # NEGATIVE: WordPress import contract/version must be exact.
            bad=copy.deepcopy(payload); bad['wordpress_review']['plugin_version_verified_against']='0.28.22'
            with self.assertRaisesRegex(handoff_transport.HandoffError,'HANDOFF_WORDPRESS_PLUGIN_VERSION_INVALID'):
                handoff_transport.read_validate_handoff(_write_mutation(Path(td),bad,'bad-plugin-version.json'))
            bad=copy.deepcopy(payload); del bad['wordpress_review']['ppm_version_verified_against']
            with self.assertRaisesRegex(handoff_transport.HandoffError,'HANDOFF_WORDPRESS_REVIEW_SCHEMA_INVALID'):
                handoff_transport.read_validate_handoff(_write_mutation(Path(td),bad,'bad-wp-schema.json'))

            # NEGATIVE: article identity and exact bytes are mandatory.
            bad=copy.deepcopy(payload); bad['articles'][0]['title']=''
            with self.assertRaisesRegex(handoff_transport.HandoffError,'HANDOFF_ARTICLE_FIELD_INVALID:0:title'):
                handoff_transport.read_validate_handoff(_write_mutation(Path(td),bad,'bad-title.json'))
            bad=copy.deepcopy(payload); bad['articles'][0]['body']+='tamper'
            with self.assertRaisesRegex(handoff_transport.HandoffError,'HANDOFF_BODY_SHA_MISMATCH:0'):
                handoff_transport.read_validate_handoff(_write_mutation(Path(td),bad,'bad-body.json'))

            artifact,receipt=chat_delivery_gate.stage(final,output_dir)
            staged=chat_delivery_gate.verify(artifact,receipt)
            self.assertEqual(artifact.read_bytes(),raw)
            self.assertEqual(staged['overall_acceptance_status'],'PENDING_CHAT_ATTACHMENT')
            self.assertEqual(staged['chat_surface_requirement'],'MUST_BE_ATTACHED_IN_REQUESTING_CHAT_BEFORE_OVERALL_PASS')

            # NEGATIVE: an internal PASS/file path is insufficient if the actual artifact is absent or changed.
            with self.assertRaisesRegex(chat_delivery_gate.ChatDeliveryError,'CHAT_ARTIFACT_MISSING'):
                chat_delivery_gate.verify(output_dir/'does-not-exist.json',receipt)
            original=artifact.read_bytes()
            artifact.write_bytes(original+b'X')
            with self.assertRaisesRegex(chat_delivery_gate.ChatDeliveryError,'CHAT_ARTIFACT_SHA_MISMATCH'):
                chat_delivery_gate.verify(artifact,receipt)
            artifact.write_bytes(original)
            chat_delivery_gate.verify(artifact,receipt)

            self.assertEqual(hashlib.sha256(artifact.read_bytes()).hexdigest(),staged['sha256'])
            self.assertEqual(artifact.stat().st_size,staged['byte_length'])

if __name__=='__main__':
    unittest.main(verbosity=2)
