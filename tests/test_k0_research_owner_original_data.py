"""Original 2026-11-15/16 K0 data: one research decision, same-owner repair."""
import copy
import hashlib
import json
import os
import unittest
from unittest import mock
from pathlib import Path

from engine.k0_writer_station import research_owner_decision, prepare

ROOT=Path(__file__).resolve().parents[1]
POS=ROOT/'real_runs/k0/k0-20261115-horseware-neu-quellenregel-9221a640'
NEG=ROOT/'real_runs/k0/k0-20261116-wassertrog-anleitung-7e55abd7'
RUN='run:'+'1'*24

def read(base,name):
    return json.loads((base/name).read_text(encoding='utf-8'))

def original_context(base):
    ctx=read(base,'AUTHORING_CONTEXT.json')
    ctx['run_instance_id']=RUN
    return ctx

def portal_for(ident):
    return {'contract':'K0_PORTAL_ASSIGNMENT_V1','status':'PASS',
            'items':[{'portal_id':'pferdeatelier','status':'AUTO_DETECTED','job_identity':ident}]}

class SourceOwnerOriginalDataTests(unittest.TestCase):
    def test_positive_original_horseware_sources_kept(self):
        ctx=original_context(POS)
        self.assertEqual(len(ctx['rule_context']['research_claims']),8)
        self.assertIsNone(research_owner_decision(ctx,ctx['identity'],RUN))
        job=prepare(read(POS,'WORDPRESS_INTAKE.json'),portal_for(ctx['identity']),ctx)
        self.assertEqual(job['status'],'OPEN')
        self.assertEqual(job['contract'],'K0_WRITER_JOB_V1')

    def test_negative_original_wassertrog_returns_same_owner(self):
        ctx=original_context(NEG)
        self.assertEqual(len(ctx['rule_context']['research_claims']),7)
        decision=research_owner_decision(ctx,ctx['identity'],RUN)
        self.assertEqual(decision['status'],'REPAIR_REQUIRED')
        self.assertEqual(decision['owner'],'SAME_RESEARCH_OWNER')
        self.assertEqual(len(decision['issues']),7)
        job=prepare(read(NEG,'WORDPRESS_INTAKE.json'),portal_for(ctx['identity']),ctx)
        self.assertEqual(job['contract'],'K0_RESEARCH_RETURN_V1')
        self.assertNotIn('job_id',job)
        self.assertEqual(job['identity'],ctx['identity'])

    def test_repair_restores_original_horseware_context_and_resumes_same_run(self):
        good=original_context(POS)
        changed=copy.deepcopy(good)
        changed['rule_context']['research_claims']['F1']['evidence_text']=changed['rule_context']['research_claims']['F1']['statement']
        same_intake=read(POS,'WORDPRESS_INTAKE.json')
        same_portal=portal_for(good['identity'])
        ticket=prepare(same_intake,same_portal,changed)
        self.assertEqual(ticket['status'],'REPAIR_REQUIRED')
        self.assertEqual(ticket['identity'],good['identity'])
        # Repair at original researcher restores the ORIGINAL source excerpt.
        restored=prepare(same_intake,same_portal,good)
        self.assertEqual(restored['status'],'OPEN')
        self.assertEqual(restored['contract'],'K0_WRITER_JOB_V1')
        self.assertEqual(restored['run_instance_id'],ticket['run_instance_id'])

    def test_negative_excerpt_hash_mismatch_returns_same_owner(self):
        good=original_context(POS)
        good['rule_context']['research_claims']['F1']['evidence_text_sha256']='1'*64
        ticket=research_owner_decision(good,good['identity'],RUN)
        self.assertEqual(ticket['status'],'REPAIR_REQUIRED')
        self.assertEqual(ticket['issues'][0]['reason'],'SOURCE_EXCERPT_DIGEST_MISMATCH')

    def _real_source_texts(self, ctx):
        originals={}
        for claim in ctx['rule_context']['research_claims'].values():
            originals.setdefault(claim['source_url'], []).append(claim['evidence_text'])
        return {url:'\n'.join(excerpts) for url,excerpts in originals.items()}

    def test_original_source_proof_uses_same_research_owner(self):
        ctx=original_context(POS)
        originals=self._real_source_texts(ctx)
        with mock.patch.dict(os.environ, {'K0_REQUIRE_ORIGINAL_SOURCE_PROOF':'1'}):
            with mock.patch('engine.k0_writer_station._k0_fetch_original_source_text',
                            side_effect=lambda url:originals[url]) as fetch:
                result=prepare(read(POS,'WORDPRESS_INTAKE.json'),portal_for(ctx['identity']),ctx)
        self.assertEqual(result['status'],'OPEN')
        self.assertEqual(fetch.call_count,len(originals))

    def test_forged_sha_consistent_but_unverified_excerpt_returns_to_same_researcher(self):
        ctx=original_context(POS)
        originals=self._real_source_texts(ctx)
        claim=ctx['rule_context']['research_claims']['F1']
        claim['evidence_text']='An invented fragment that does not appear in the actual original.'
        claim['evidence_text_sha256']=hashlib.sha256(claim['evidence_text'].encode()).hexdigest()
        with mock.patch.dict(os.environ, {'K0_REQUIRE_ORIGINAL_SOURCE_PROOF':'1'}):
            with mock.patch('engine.k0_writer_station._k0_fetch_original_source_text',
                            side_effect=lambda url:originals[url]):
                ticket=prepare(read(POS,'WORDPRESS_INTAKE.json'),portal_for(ctx['identity']),ctx)
        self.assertEqual(ticket['status'],'REPAIR_REQUIRED')
        self.assertEqual(ticket['owner'],'SAME_RESEARCH_OWNER')
        self.assertNotIn('job_id',ticket)
        self.assertTrue(any(x['reason']=='ORIGINAL_SOURCE_EXCERPT_NOT_PROVEN' for x in ticket['issues']))

    def test_original_source_unavailable_is_repairable_not_writer_entry(self):
        ctx=original_context(POS)
        with mock.patch.dict(os.environ, {'K0_REQUIRE_ORIGINAL_SOURCE_PROOF':'1'}):
            with mock.patch('engine.k0_writer_station._k0_fetch_original_source_text',
                            side_effect=OSError('source offline')):
                ticket=prepare(read(POS,'WORDPRESS_INTAKE.json'),portal_for(ctx['identity']),ctx)
        self.assertEqual(ticket['status'],'REPAIR_REQUIRED')
        self.assertEqual(ticket['owner'],'SAME_RESEARCH_OWNER')
        self.assertNotIn('job_id',ticket)
        self.assertEqual(len(ticket['issues']),8)
        self.assertTrue(all(x['reason']=='ORIGINAL_SOURCE_NOT_RETRIEVABLE' for x in ticket['issues']))

    def test_live_source_proof_is_mandatory_in_canonical_authoring_workflow(self):
        workflow=(ROOT/'.github/workflows/k0-authoring-context.yml').read_text(encoding='utf-8')
        self.assertIn("K0_REQUIRE_ORIGINAL_SOURCE_PROOF: '1'",workflow)
        self.assertIn('python3 -m engine.k0_writer_station prepare',workflow)
        self.assertIn("j['status']=='REPAIR_REQUIRED'",workflow)
        self.assertIn("j['owner']=='SAME_RESEARCH_OWNER'",workflow)

if __name__=='__main__':
    unittest.main()
