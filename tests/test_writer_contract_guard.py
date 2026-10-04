import hashlib, json, unittest
from engine.writer_contract_guard import WriterContractBlocked, verify_package
from engine.k0_writer_station import prepare, seal, verify, Blocked as StationBlocked
from tests.k0_rule_context_fixture import rule_context
from tests.k0_freshness_fixture import bind_freshness

def stable_json(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))

def words(n, seed):
    return " ".join([seed] * n)

def intake():
    x={
      'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2',
      'status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
      'content_or_format_payload_present':False,
      'item_count':1,
      'items':[{
        'article_type':'Beratung',
        'category':'discgolf-beratung',
        'plan_slot':'5d3d43eebb1f755c178415b811fb1241a0ef022739ca7f7896a491792ca126e9',
        'target_keyword':'Discgolf Ausrüstung',
        'title':'Was braucht man für Discgolf?'
      }],
      'publish_allowed':False,
    }
    x['batch_sha256']=hashlib.sha256(stable_json(x).encode()).hexdigest()
    return x

def portal(i):
    ident=i['items'][0]
    return {
      'contract':'K0_PORTAL_ASSIGNMENT_V1','status':'PASS','source_batch_sha256':i['batch_sha256'],
      'item_count':1,'items':[{'portal_id':'hobby','portal_name':'Hobby','status':'AUTO_DETECTED','basis':'category:'+ident['category'],'job_identity':ident}],
      'publish_allowed':False
    }

def context(i):
    ident=i['items'][0]
    return bind_freshness({
      'contract':'K0_AUTHORING_CONTEXT_V1',
      'run_instance_id':'run:1234567890abcdef12345678',
      'identity':ident,
      'content_profile':{'search_intent':'DECISION_SUPPORT'},
      'production_context':{'fact_pack':{'contract':'canonical_fact_pack_v1'},'production_plan_item':{'article_type':'Beratung'}},
      'rule_context':rule_context(ident),
      'publish_allowed':False
    })

def good_html():
    return f"""<article>
<section data-block="intro"><p>{words(75,'Einleitung')}</p></section>
<section data-block="criteria"><h2>Kriterien sinnvoll einordnen</h2><p>{words(135,'Kriterium')}</p></section>
<section data-block="decision"><h2>Unterschiede im Zusammenhang betrachten</h2><p>{words(135,'Zusammenhang')}</p></section>
<section data-block="types"><h2>Passende Varianten unterscheiden</h2><p>{words(135,'Variante')}</p></section>
<section data-block="practical"><h2>Praxis verständlich zusammenführen</h2><p>{words(135,'Praxis')}</p></section>
<section data-block="table"><h2>Übersicht</h2><p>{words(30,'Tabelle')}</p></section>
<section data-block="conclusion"><h2>Fazit</h2><p>{words(88,'Fazitwort')}</p></section>
<section data-block="further_information"><h2>Weiterführende Informationen</h2><p>{words(38,'Hinweis')}</p></section>
</article>"""

def draft(job, body=None):
    return {
      'contract':'K0_WRITER_DRAFT_V1',
      'job_id':job['job_id'],
      'title':job['identity']['title'],
      'content_html':body or good_html(),
      'table_decision':job['rule_context']['table_decision'],
      'lt_authoritative_terms':[],
      'revision_count':1,
      'publish_allowed':False
    }

class WriterContractGuardTests(unittest.TestCase):
    def setUp(self):
        self.i=intake()
        self.job=prepare(self.i,portal(self.i),context(self.i))

    def test_only_writer_draft_route_can_create_verified_package(self):
        pkg=seal(self.job,draft(self.job))
        self.assertEqual(verify(self.job,pkg)['status'],'PASS')
        self.assertEqual(verify_package(pkg)['status'],'PASS')
        self.assertEqual(pkg['writer_provenance']['route'],'K0_WRITER_DRAFT_ONLY')

    def test_direct_article_without_writer_seal_is_blocked(self):
        pkg={'contract':'K0_ARTICLE_PACKAGE_V1','identity':self.i['items'][0],'html':good_html(),'final_draft_sha256':'x','publish_allowed':False}
        with self.assertRaisesRegex(WriterContractBlocked,'WRITER_PROVENANCE_MISSING'):
            verify_package(pkg)

    def test_ready_article_cannot_be_submitted_as_writer_draft(self):
        bad=draft(self.job)
        bad['html']=bad.pop('content_html')
        with self.assertRaisesRegex(StationBlocked,'K0_WRITER_DRAFT_FIELDS_INVALID'):
            seal(self.job,bad)

    def test_authoring_context_cannot_contain_article_text(self):
        ctx=context(self.i); ctx['html']=good_html()
        with self.assertRaisesRegex(StationBlocked,'K0_AUTHORING_CONTEXT_TEXT_PAYLOAD_FORBIDDEN'):
            prepare(self.i,portal(self.i),ctx)

    def test_short_h2_sections_are_blocked(self):
        body=good_html().replace(words(135,'Kriterium'),words(35,'Kriterium')).replace(words(75,'Einleitung'),words(180,'Einleitung'))
        with self.assertRaisesRegex(WriterContractBlocked,'WRITER_H2_WORD_RANGE'):
            seal(self.job,draft(self.job,body))

    def test_short_conclusion_is_blocked(self):
        body=good_html().replace(words(88,'Fazitwort'),words(20,'Fazitwort')).replace(words(75,'Einleitung'),words(150,'Einleitung'))
        with self.assertRaisesRegex(WriterContractBlocked,'WRITER_CONCLUSION_TOO_SHORT'):
            seal(self.job,draft(self.job,body))

    def test_missing_further_information_is_blocked(self):
        body=good_html()
        start=body.index('<section data-block="further_information">')
        end=body.index('</section>',start)+len('</section>')
        body=body[:start]+body[end:]
        with self.assertRaisesRegex(WriterContractBlocked,'WRITER_REQUIRED_SECTION_COUNT:further_information'):
            seal(self.job,draft(self.job,body))

if __name__=='__main__':
    unittest.main()
