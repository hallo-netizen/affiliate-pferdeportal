"""Original 2026-11-15/16 K0 data: one research decision, same-owner repair."""
import copy
import hashlib
import json
import os
import unittest
from unittest import mock
from pathlib import Path

from engine.k0_writer_station import (
    research_owner_decision, prepare, _k0_research_source_quality_reason,
)
from tests.k0_rule_context_fixture import adapt_historical_table_context_for_current_k0

ROOT=Path(__file__).resolve().parents[1]
POS=ROOT/'real_runs/k0/k0-20261115-horseware-neu-quellenregel-9221a640'
NEG=ROOT/'real_runs/k0/k0-20261116-wassertrog-anleitung-7e55abd7'
RUN='run:'+'1'*24

def read(base,name):
    return json.loads((base/name).read_text(encoding='utf-8'))

def original_context(base):
    ctx=read(base,'AUTHORING_CONTEXT.json')
    ctx['run_instance_id']=RUN
    return adapt_historical_table_context_for_current_k0(ctx)

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

    def test_only_verified_official_hosts_and_real_wikipedia_articles_pass(self):
        allowed=(
            'https://www.horseware.com/de-de/faqs',
            'https://www.tierschutzbund.de/ueber-uns/',
            'https://www.dlg.org/mediacenter/',
            'https://www.umweltbundesamt.de/themen/',
            'https://www.msdvetmanual.com/integumentary-system/dermatophytosis/dermatophytosis-in-horses',
            'https://wcvm.usask.ca/learnaboutparasites/parasites/oxyuris-equi.php',
            'https://storage.googleapis.com/worldhorsewelfare-cloud/2024/12/horse.pdf',
            'https://de.wikipedia.org/wiki/Pferd',
            'https://en.wikipedia.org/wiki/Horse',
            'https://www.bund.de/verwaltung',
            'https://www.cdc.gov/disease',
            'https://commission.europa.eu/index_en',
        )
        for url in allowed:
            with self.subTest(url=url):
                self.assertIsNone(_k0_research_source_quality_reason(url))
        rejected={
            'https://pferde-atelier.de/reiten/':'RESEARCH_OWN_PORTAL_SOURCE_FORBIDDEN',
            'https://www.pferde-atelier.de/thema/':'RESEARCH_OWN_PORTAL_SOURCE_FORBIDDEN',
            'https://cdn.pferde-atelier.de/seite/':'RESEARCH_OWN_PORTAL_SOURCE_FORBIDDEN',
            'https://hobbydepot.de/thema/':'RESEARCH_OWN_PORTAL_SOURCE_FORBIDDEN',
            'https://privateblog.de/pferde/':'RESEARCH_SOURCE_NOT_APPROVED_OFFICIAL',
            'https://www.pferdeforum.de/fragen/':'RESEARCH_SOURCE_NOT_APPROVED_OFFICIAL',
            'https://www.horseware.com.privateblog.de/':'RESEARCH_SOURCE_NOT_APPROVED_OFFICIAL',
            'https://de.wikipedia.org.privateblog.de/wiki/Pferd':'RESEARCH_SOURCE_NOT_APPROVED_OFFICIAL',
            'https://de.wikipedia.org/':'RESEARCH_WIKIPEDIA_ARTICLE_REQUIRED',
            'https://de.wikipedia.org/wiki/Benutzer:Privat':'RESEARCH_WIKIPEDIA_ARTICLE_REQUIRED',
            'https://en.wikipedia.org/wiki/User:Someone':'RESEARCH_WIKIPEDIA_ARTICLE_REQUIRED',
            'https://de.wikipedia.org/wiki/Diskussion:Pferd':'RESEARCH_WIKIPEDIA_ARTICLE_REQUIRED',
            'https://de.wikipedia.org/wiki/Spezial:Suche':'RESEARCH_WIKIPEDIA_ARTICLE_REQUIRED',
            'https://storage.googleapis.com/private-person/brochure.pdf':'RESEARCH_SOURCE_NOT_APPROVED_OFFICIAL',
            'http://de.wikipedia.org/wiki/Pferd':'RESEARCH_SOURCE_HTTPS_REQUIRED',
            'https://pferde-atelier.de@www.horseware.com/faqs':'RESEARCH_SOURCE_HTTPS_REQUIRED',
        }
        for url,reason in rejected.items():
            with self.subTest(url=url):
                self.assertEqual(_k0_research_source_quality_reason(url),reason)

    def test_real_two_article_batch_official_veterinary_sources_pass(self):
        for suffix in ('01','02'):
            directory=ROOT/('real_runs/k0/k0-20261118-txe-01a689f8-'+suffix)
            ctx=read(directory,'AUTHORING_CONTEXT.json')
            urls={row['source_url'] for row in ctx['rule_context']['research_claims'].values()}
            urls.update(row['source_url'] for row in ctx['production_context']['fact_pack']['sources'])
            self.assertTrue(urls)
            for url in urls:
                with self.subTest(article=suffix,url=url):
                    self.assertIsNone(_k0_research_source_quality_reason(url))

    def test_approved_wikipedia_original_excerpt_flows_through_existing_owner(self):
        ctx=original_context(POS)
        article_url='https://de.wikipedia.org/wiki/Pferd'
        ctx['rule_context']['research_claims']['F1']['source_url']=article_url
        originals=self._real_source_texts(ctx)
        with mock.patch.dict(os.environ, {'K0_REQUIRE_ORIGINAL_SOURCE_PROOF':'1'}):
            with mock.patch('engine.k0_writer_station._k0_fetch_original_source_text',
                            side_effect=lambda url: originals[url]) as fetch:
                result=research_owner_decision(ctx,ctx['identity'],RUN)
        self.assertIsNone(result)
        self.assertIn(article_url,[c.args[0] for c in fetch.call_args_list])

    def test_private_source_and_own_portal_return_to_same_research_owner(self):
        for bad_url in ('https://privateblog.de/pferde/',
                        'https://pferde-atelier.de/ausruestung/'):
            with self.subTest(url=bad_url):
                ctx=original_context(POS)
                ctx['rule_context']['research_claims']['F1']['source_url']=bad_url
                originals=self._real_source_texts(original_context(POS))
                with mock.patch.dict(os.environ, {'K0_REQUIRE_ORIGINAL_SOURCE_PROOF':'1'}):
                    with mock.patch('engine.k0_writer_station._k0_fetch_original_source_text',
                                    side_effect=lambda url: originals[url]) as fetch:
                        ticket=research_owner_decision(ctx,ctx['identity'],RUN)
                self.assertEqual(ticket['owner'],'SAME_RESEARCH_OWNER')
                self.assertEqual(ticket['status'],'REPAIR_REQUIRED')
                self.assertNotIn(bad_url,[c.args[0] for c in fetch.call_args_list])
                self.assertEqual(len(ticket['issues']),1)
                self.assertIn(ticket['issues'][0]['reason'],
                              ('RESEARCH_SOURCE_NOT_APPROVED_OFFICIAL',
                               'RESEARCH_OWN_PORTAL_SOURCE_FORBIDDEN'))

    def test_private_fact_pack_or_comparison_source_cannot_hide_beyond_claims(self):
        for target in ('fact_pack','comparison'):
            with self.subTest(target=target):
                ctx=original_context(POS)
                if target=='fact_pack':
                    ctx['production_context']['fact_pack']['sources'][0]['source_url']='https://privateblog.de/blog/'
                else:
                    ctx['rule_context']['comparison_source_bindings'][0]['source_url']='https://privateblog.de/blog/'
                originals=self._real_source_texts(original_context(POS))
                with mock.patch.dict(os.environ, {'K0_REQUIRE_ORIGINAL_SOURCE_PROOF':'1'}):
                    with mock.patch('engine.k0_writer_station._k0_fetch_original_source_text',
                                    side_effect=lambda url: originals[url]):
                        ticket=research_owner_decision(ctx,ctx['identity'],RUN)
                self.assertEqual(ticket['status'],'REPAIR_REQUIRED')
                self.assertEqual(len(ticket['issues']),1)
                self.assertEqual(ticket['issues'][0]['reason'],
                                 'RESEARCH_SOURCE_NOT_APPROVED_OFFICIAL')

    def test_private_product_candidate_is_rejected_in_same_owner_decision(self):
        ctx=original_context(POS)
        ctx['production_context']['property_research']={
            'candidates':[{'source_url':'https://privateblog.de/ranking'}],
            'winner':{'source_url':'https://privateblog.de/ranking'},
        }
        originals=self._real_source_texts(original_context(POS))
        with mock.patch.dict(os.environ, {'K0_REQUIRE_ORIGINAL_SOURCE_PROOF':'1'}):
            with mock.patch('engine.k0_writer_station._k0_fetch_original_source_text',
                            side_effect=lambda url: originals[url]):
                ticket=research_owner_decision(ctx,ctx['identity'],RUN)
        self.assertEqual(ticket['status'],'REPAIR_REQUIRED')
        self.assertEqual(len(ticket['issues']),1)
        self.assertEqual(ticket['issues'][0]['reason'],'RESEARCH_SOURCE_NOT_APPROVED_OFFICIAL')

    def test_live_source_proof_is_mandatory_in_canonical_authoring_workflow(self):
        workflow=(ROOT/'.github/workflows/k0-authoring-context.yml').read_text(encoding='utf-8')
        self.assertIn("K0_REQUIRE_ORIGINAL_SOURCE_PROOF: '1'",workflow)
        self.assertIn('python3 -m engine.k0_writer_station prepare',workflow)
        self.assertIn("j['status']=='REPAIR_REQUIRED'",workflow)
        self.assertIn("j['owner']=='SAME_RESEARCH_OWNER'",workflow)

if __name__=='__main__':
    unittest.main()
