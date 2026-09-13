from __future__ import annotations

import base64
import hashlib
import json
import lzma
import os
import tempfile
import unittest
import zipfile
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
SYSTEM4=HERE.parent/'isolated_system4'
for _p in (str(HERE),str(SYSTEM4)):
    if _p not in sys.path: sys.path.insert(0,_p)

import batch_gate
import content_guard
import handoff_transport
import production_checks
import root_entry
import external_host
from codex_worker_entry import build_codex_production_worker_pool
from external_host import ExternalHostError, PersistentArticleWorkerPool
from production_ingress import _validate_external_business_contract, ProductionIngressError, REPO
from production_plan_binding import bind_production_plan, validate_link_bindings_against_wp_snapshot, ProductionPlanBindingError, stable_hash


def canonical_article(**overrides):
    package=REPO/'control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip'
    with zipfile.ZipFile(package) as z:
        plan=json.loads(z.read('portal-production-machine/contracts/canonical-complete-editorial-plan-v1.json'))
    slot=[s for s in plan['slots'] if s.get('canonical_article_id')=='article:fe39320b47c1ba40194c8d69'][0]
    value={
        'title':slot['working_title'],
        'target_keyword':'Checklisten für Pferdeanhänger',
        'category':slot['category_slug'],
        'article_type':slot['article_type'],
        'plan_slot':stable_hash(slot),
    }
    value.update(overrides)
    return value


def external(a=None):
    a=a or canonical_article()
    return {'contract':'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1','next_textmachine_metadata_batch':{
        'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE','batch_sha256':'b'*64,
        'item_count':1,'items':[a],'publish_allowed':False}}


def canonical_fact_pack(source='s'):
    return {'contract':'canonical_fact_pack_v1','source_snapshot_id':source,'fact_pack_id':source,'status':'SOURCE_VERIFIED_PRODUCTION_READY','claims':[]}


def bare_plan(a=None):
    a=a or canonical_article()
    return {'article_type':a['article_type'],'target_keyword':a['target_keyword'],'topic':a['title'],'runtime_order':{}}


class ErrorHistoryRemainingTests(unittest.TestCase):
    def test_unknown_fact_id(self):
        with self.assertRaisesRegex(content_guard.ContentGuardError,'^ARTICLE_UNKNOWN_FACT_ID:X$'):
            content_guard.validate_article_fact_ids('<p data-fact-id="X">x</p>',{'claims':[{'fact_id':'F1'}]})

    def test_fact_id_not_in_canonical_fact_pack(self):
        with self.assertRaisesRegex(content_guard.ContentGuardError,'^ARTICLE_UNKNOWN_FACT_ID:F2$'):
            content_guard.validate_article_fact_ids('<p data-fact-ids="F1 F2">x</p>',{'claims':[{'fact_id':'F1'}]})

    def test_wrong_or_missing_plan_slot(self):
        bad=canonical_article(plan_slot='f'*64)
        expected=canonical_article()['plan_slot']
        with self.assertRaisesRegex(ProductionIngressError,'^PPM679_PLAN_SLOT_HASH_MISMATCH:'+expected+':'+('f'*64)+'$'):
            _validate_external_business_contract(external(bad))

    def test_context_runtime_mismatch(self):
        a=canonical_article(); state={'article':a,'source_snapshot_sha256':'s'}
        fp=canonical_fact_pack()
        plan=bind_production_plan(a,bare_plan(a),fp); plan['topic']='WRONG'
        with self.assertRaisesRegex(production_checks.ProductionCheckError,'^PRODUCTION_PLAN_IDENTITY_MISMATCH:topic$'):
            production_checks.validate_bound_context(state,fp,plan)

    def test_hash_manifest_mismatch(self):
        with self.assertRaisesRegex(root_entry.EntryFail,'^ROOT_ENTRY_MANIFEST_MISMATCH$'):
            root_entry._verify_snapshot_binding({'system4_root_manifest_sha256':'0'*64},'1'*64)

    def test_wrong_link_binding(self):
        a=canonical_article(); q=bind_production_plan(a,bare_plan(a),canonical_fact_pack())['quality_binding']
        q=json.loads(json.dumps(q)); q['link_bindings'][0]['href']='/wrong/'
        with self.assertRaisesRegex(ProductionPlanBindingError,'^PORTAL_LINK_BINDING_SOURCE_MISMATCH:parent_category$'):
            validate_link_bindings_against_wp_snapshot(q)

    def test_missing_required_fields(self):
        a=canonical_article(); a.pop('title')
        with self.assertRaisesRegex(ProductionIngressError,'^EXTERNAL_ITEM_SCHEMA_INVALID$'):
            _validate_external_business_contract(external(a))

    def test_wrong_article_identity(self):
        expected=canonical_article(); state={'contract':batch_gate.STATE_CONTRACT,'source_snapshot_sha256':'s','batch_sha256':'b'*64,'article':canonical_article(title='WRONG')}
        state['immutable_core_sha256']=batch_gate.stable_hash(batch_gate.immutable_core(state))
        with self.assertRaisesRegex(batch_gate.BatchGateError,'^STATE_ARTICLE_BINDING_MISMATCH$'):
            batch_gate.validate_state(state,expected,'s','b'*64)

    def test_batch_article_context_mismatch(self):
        state={'contract':batch_gate.STATE_CONTRACT,'source_snapshot_sha256':'s','batch_sha256':'c'*64,'article':canonical_article()}
        state['immutable_core_sha256']=batch_gate.stable_hash(batch_gate.immutable_core(state))
        with self.assertRaisesRegex(batch_gate.BatchGateError,'^STATE_BATCH_MISMATCH$'):
            batch_gate.validate_state(state,canonical_article(),'s','b'*64)

    def test_handoff_manipulation(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'inline.txt'; raw=b'abc'; comp=lzma.compress(raw)
            env={'contract':handoff_transport.INLINE_CONTRACT,'filename':handoff_transport.HANDOFF_FILENAME,'mime_type':'application/json','compression':'xz-lzma2-preset9e','encoding':'base64','part_index':0,'part_count':1,'byte_length':3,'plaintext_sha256':hashlib.sha256(raw).hexdigest(),'compressed_sha256':'0'*64,'payload_base64':base64.b64encode(comp).decode(),'publish_allowed':False}
            p.write_text(handoff_transport.INLINE_BEGIN+'\n'+json.dumps(env,separators=(',',':'))+'\n'+handoff_transport.INLINE_END+'\n')
            with self.assertRaisesRegex(handoff_transport.HandoffError,'^INLINE_COMPRESSED_SHA_MISMATCH$'):
                handoff_transport.inline_unpack(p,Path(td)/'out')

    def test_synthetic_pass_authority(self):
        with tempfile.TemporaryDirectory(prefix='s4a-pass-inject-') as td:
            root=Path(td); root.chmod(0o755)
            worker=root/'worker.py'
            worker.write_text("""import json,sys
for line in sys.stdin:
 e=json.loads(line); print(json.dumps({'contract':e['contract'],'session_id':e['session_id'],'result':{'content':'x','phase':'ARTICLE_PASS'}}),flush=True)
""",encoding='utf-8')
            worker.chmod(0o644)
            py=external_host._resolve_worker_python('nobody')
            pool=PersistentArticleWorkerPool([py,str(worker)],root/'workers',run_as_user='nobody',require_cross_uid=True,runtime_processes=1)
            try:
                with self.assertRaisesRegex(ExternalHostError,'^WORKER_RESULT_SCHEMA_INVALID$'):
                    pool.request({'task':'research','article':{'plan_slot':canonical_article()['plan_slot']}})
            finally:
                pool.close()

    def test_ppm_quality_binding_missing(self):
        with self.assertRaisesRegex(production_checks.ProductionCheckError,'^PPM679_QUALITY_BINDING_MISSING$'):
            production_checks._runtime_rebound_plan(REPO,'<p>x</p>',{})

    def test_root_bound_snapshot_missing(self):
        with self.assertRaisesRegex(root_entry.EntryFail,'^ROOT_ENTRY_MANIFEST_BINDING_MISSING$'):
            root_entry._verify_snapshot_binding({},'1'*64)

    def test_languagetool_dependency_missing(self):
        old=os.environ.get('SYSTEM4_LANGUAGETOOL_JAR')
        try:
            os.environ['SYSTEM4_LANGUAGETOOL_JAR']='/definitely/missing/languagetool.jar'
            with self.assertRaisesRegex(production_checks.ProductionCheckError,'^LANGUAGETOOL_6_8_EXPLICIT_JAR_INVALID$'):
                production_checks._find_languagetool_jar(REPO)
        finally:
            if old is None: os.environ.pop('SYSTEM4_LANGUAGETOOL_JAR',None)
            else: os.environ['SYSTEM4_LANGUAGETOOL_JAR']=old

    def test_worker_factory_signature_drift(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/'worker.py').write_text('print(1)')
            with self.assertRaises(TypeError):
                build_codex_production_worker_pool(root,'worker.py',root,require_cross_uid=True)

if __name__=='__main__': unittest.main(verbosity=2)
