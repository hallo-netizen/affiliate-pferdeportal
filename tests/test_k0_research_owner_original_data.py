"""Original 2026-11-15/16 K0 data: one research decision, same-owner repair."""
import copy
import json
import unittest
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

if __name__=='__main__':
    unittest.main()
