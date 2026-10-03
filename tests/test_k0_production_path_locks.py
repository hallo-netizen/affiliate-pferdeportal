import hashlib
import json
import unittest

from engine.k0_production_gate import verify as verify_gate, Blocked as GateBlocked
from engine.k0_writer_station import prepare, seal, Blocked as WriterBlocked
from engine.writer_contract_guard import verify_package, WriterContractBlocked
from tests.k0_rule_context_fixture import rule_context

def stable(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))

def words(n,seed):
    return ' '.join([seed]*n)

def intake():
    x={
        'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2',
        'status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
        'content_or_format_payload_present':False,
        'item_count':1,
        'items':[{
            'article_type':'Beratung',
            'category':'schermaschinen-beratung',
            'plan_slot':'2'*64,
            'target_keyword':'Schermaschinen für Pferde',
            'title':'Schermaschinen für Pferde auswählen'
        }],
        'publish_allowed':False,
    }
    x['batch_sha256']=hashlib.sha256(stable(x).encode()).hexdigest()
    return x

def portal(i):
    ident=i['items'][0]
    return {
        'contract':'K0_PORTAL_ASSIGNMENT_V1','status':'PASS','item_count':1,
        'items':[{'portal_id':'pferdeatelier','portal_name':'Pferdeatelier','status':'AUTO_DETECTED','basis':'category:'+ident['category'],'job_identity':ident}],
        'publish_allowed':False
    }

def context(i):
    return {
        'contract':'K0_AUTHORING_CONTEXT_V1',
        'run_instance_id':'run:aaaaaaaaaaaaaaaaaaaaaaaa',
        'identity':i['items'][0],
        'content_profile':{'search_intent':'DECISION_SUPPORT'},
        'production_context':{'fact_pack':{'contract':'canonical_fact_pack_v1'},'production_plan_item':{'article_type':'Beratung'}},
        'rule_context':rule_context(i['items'][0]),
        'publish_allowed':False
    }

def body():
    return f"""<article>
<section data-block="intro"><p>{words(75,'Intro')}</p></section>
<section data-block="one"><h2>Erster Abschnitt</h2><p>{words(135,'Eins')}</p></section>
<section data-block="two"><h2>Zweiter Abschnitt</h2><p>{words(135,'Zwei')}</p></section>
<section data-block="three"><h2>Dritter Abschnitt</h2><p>{words(135,'Drei')}</p></section>
<section data-block="four"><h2>Vierter Abschnitt</h2><p>{words(135,'Vier')}</p></section>
<section data-block="table"><h2>Übersicht</h2><p>{words(30,'Tabelle')}</p></section>
<section data-block="conclusion"><h2>Fazit</h2><p>{words(88,'Fazit')}</p></section>
<section data-block="further_information"><h2>Weiterführende Informationen</h2><p>{words(38,'Info')}</p></section>
</article>"""

class ProductionPathLocks(unittest.TestCase):
    def test_midstream_article_package_without_writer_seal_is_blocked(self):
        i=intake()
        package={
            'contract':'K0_ARTICLE_PACKAGE_V1',
            'identity':i['items'][0],
            'html':body(),
            'final_draft_sha256':hashlib.sha256(body().encode()).hexdigest(),
            'content_profile':{'search_intent':'DECISION_SUPPORT'},
            'table_decision':{'exception_code':'NUANCE_LOSS'},
            'production_context':{'fact_pack':{},'production_plan_item':{}},
            'publish_allowed':False,
        }
        with self.assertRaisesRegex(GateBlocked,'WRITER_CONTRACT_BLOCKED'):
            verify_gate(package,portal(i),[{'id':1,'slug':i['items'][0]['category']}])

    def test_forged_ready_article_cannot_pass_writer_contract(self):
        i=intake()
        package={'contract':'K0_ARTICLE_PACKAGE_V1','identity':i['items'][0],'html':body(),'final_draft_sha256':hashlib.sha256(body().encode()).hexdigest(),'publish_allowed':False}
        with self.assertRaisesRegex(WriterContractBlocked,'WRITER_PROVENANCE_MISSING'):
            verify_package(package)

    def test_article_text_in_authoring_context_is_blocked(self):
        i=intake(); ctx=context(i); ctx['article_text']='fertiger Text'
        with self.assertRaisesRegex(WriterBlocked,'TEXT_PAYLOAD_FORBIDDEN'):
            prepare(i,portal(i),ctx)

    def test_writer_job_cannot_be_changed_after_prepare(self):
        i=intake(); job=prepare(i,portal(i),context(i))
        job['identity']['title']='Manipulierter Titel'
        draft={
            'contract':'K0_WRITER_DRAFT_V1','job_id':job['job_id'],'title':'Manipulierter Titel',
            'content_html':body(),'table_decision':job['rule_context']['table_decision'],
            'lt_authoritative_terms':[],'revision_count':1,'publish_allowed':False
        }
        with self.assertRaisesRegex(WriterBlocked,'JOB_HASH_INVALID'):
            seal(job,draft)

if __name__=='__main__':
    unittest.main()
