import hashlib, json, unittest
from engine.writer_contract_guard import WriterContractBlocked, verify_package, inspect_html
from engine.k0_writer_station import prepare, seal, verify, conclusion_heading_repair_request, list_bridge_repair_request, Blocked as StationBlocked
from tests.k0_rule_context_fixture import rule_context

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
    return {
      'contract':'K0_AUTHORING_CONTEXT_V1',
      'run_instance_id':'run:1234567890abcdef12345678',
      'identity':ident,
      'content_profile':{'search_intent':'DECISION_SUPPORT'},
      'production_context':{'fact_pack':{'contract':'canonical_fact_pack_v1'},'production_plan_item':{'article_type':'Beratung'}},
      'rule_context':rule_context(ident),
      'publish_allowed':False
    }

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

def list_before_fazit_html(bridge=None):
    """Valid legacy writer fixture, with a list at the very end before Fazit."""
    body=good_html()
    table=f'<section data-block="table"><h2>Übersicht</h2><p>{words(30,"Tabelle")}</p></section>'
    # Keep the table and all existing type rules, but it is not directly before Fazit.
    assert table in body
    body=body.replace(table,'')
    old=f'<section data-block="practical"><h2>Praxis verständlich zusammenführen</h2><p>{words(135,"Praxis")}</p></section>'
    bullets='<ul data-list="key_answers"><li>Erster Punkt der praktischen Prüfung</li><li>Zweiter Punkt der sachlichen Planung</li><li>Dritter Punkt zur weiteren Auswahl</li><li>Vierter Punkt zur abschließenden Kontrolle</li></ul>'
    replacement=(f'<section data-block="practical"><h2>Praxis verständlich zusammenführen</h2>'
                 f'<p>{words(112,"Praxis")}</p>{bullets}{bridge or ""}</section>')
    assert old in body
    return body.replace(old,table+replacement)


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

    def test_fazit_heading_is_exact_hard_writer_requirement(self):
        # Negative: each still contains a valid conclusion SECTION, but no exact visible Fazit H2.
        for replacement in ('<h2>Zusammenfassung</h2>', '<h2>Fazit:</h2>', ''):
            with self.subTest(heading=replacement):
                body=good_html().replace('<h2>Fazit</h2>',replacement)
                with self.assertRaisesRegex(WriterContractBlocked,'WRITER_CONCLUSION_HEADING_INVALID'):
                    seal(self.job,draft(self.job,body))

    def test_same_writer_fazit_repair_and_resubmit_positive(self):
        original=draft(self.job,good_html().replace('<h2>Fazit</h2>','<h2>Schlussgedanken</h2>'))
        with self.assertRaisesRegex(WriterContractBlocked,'WRITER_CONCLUSION_HEADING_INVALID'):
            seal(self.job,original)
        receipt=conclusion_heading_repair_request(self.job,original)
        self.assertEqual(receipt['status'],'RETURN_TO_SAME_WRITER')
        self.assertEqual(receipt['job_id'],self.job['job_id'])
        self.assertEqual(receipt['writer_job_sha256'],self.job['job_sha256'])
        self.assertEqual(receipt['rule_id'],'writer.conclusion_heading_exact')
        self.assertEqual(receipt['required_heading'],'Fazit')
        self.assertFalse(receipt['publish_allowed'])
        corrected=draft(self.job,original['content_html'].replace('<h2>Schlussgedanken</h2>','<h2>Fazit</h2>'))
        corrected['revision_count']=2
        self.assertNotEqual(receipt['draft_sha256'],conclusion_heading_repair_request(self.job,corrected)['draft_sha256'])
        product=seal(self.job,corrected)
        self.assertEqual(verify(self.job,product)['status'],'PASS')
        self.assertEqual(verify_package(product)['status'],'PASS')

    def test_last_list_without_paragraph_before_fazit_fails_original_writer(self):
        original=draft(self.job,list_before_fazit_html())
        with self.assertRaisesRegex(WriterContractBlocked,'WRITER_LIST_BEFORE_FAZIT_BRIDGE_REQUIRED'):
            seal(self.job,original)

    def test_short_or_incomplete_bridge_fails(self):
        for bridge in ('<p>Kurzer Übergang.</p>',
                       '<p>Diese wichtigen Schritte müssen nun im Gesamtzusammenhang betrachtet und für den tatsächlichen Einsatzzweck sinnvoll eingeordnet werden</p>',
                       '<div>Ein langer Übergangstext außerhalb eines normalen Absatzes sollte für diese Regel nicht ausreichen, auch wenn er mehrere Wörter enthält.</div>'):
            with self.subTest(bridge=bridge[:30]):
                with self.assertRaisesRegex(WriterContractBlocked,'WRITER_LIST_BEFORE_FAZIT_BRIDGE_REQUIRED'):
                    inspect_html(list_before_fazit_html(bridge))

    def test_same_original_writer_repairs_and_resubmits_list_before_fazit(self):
        original=draft(self.job,list_before_fazit_html())
        with self.assertRaisesRegex(WriterContractBlocked,'WRITER_LIST_BEFORE_FAZIT_BRIDGE_REQUIRED'):
            seal(self.job,original)
        receipt=list_bridge_repair_request(self.job,original)
        self.assertEqual(receipt['status'],'RETURN_TO_SAME_WRITER')
        self.assertEqual(receipt['job_id'],self.job['job_id'])
        self.assertEqual(receipt['writer_job_sha256'],self.job['job_sha256'])
        self.assertEqual(receipt['rule_id'],'writer.list_before_fazit_bridge')
        self.assertEqual(receipt['minimum_bridge_words'],18)
        self.assertFalse(receipt['publish_allowed'])
        bridge='<p>Die genannten Prüfschritte helfen, die passende Variante anhand der bereits erklärten Kriterien einzuordnen. Entscheidend bleibt, wie sie unter den tatsächlichen Bedingungen zusammenspielen.</p>'
        corrected=draft(self.job,list_before_fazit_html(bridge))
        corrected['revision_count']=2
        self.assertNotEqual(receipt['draft_sha256'],list_bridge_repair_request(self.job,corrected)['draft_sha256'])
        product=seal(self.job,corrected)
        self.assertEqual(verify(self.job,product)['status'],'PASS')
        self.assertEqual(verify_package(product)['status'],'PASS')

    def test_table_directly_before_fazit_retains_original_behavior(self):
        # A table with its own summary has separate K0 rules, not this list rule.
        body=good_html().replace(
            f'<section data-block="practical"><h2>Praxis verständlich zusammenführen</h2><p>{words(135,"Praxis")}</p></section>',
            f'<section data-block="practical"><h2>Praxis verständlich zusammenführen</h2><p>{words(112,"Praxis")}</p><ul><li>Erster Punkt</li><li>Zweiter Punkt</li><li>Dritter Punkt</li><li>Vierter Punkt</li></ul></section>'
        )
        self.assertEqual(inspect_html(body)['status'],'PASS')

    def test_no_final_list_passes_without_extra_paragraph(self):
        self.assertEqual(inspect_html(good_html())['status'],'PASS')

    def test_missing_further_information_is_blocked(self):
        body=good_html()
        start=body.index('<section data-block="further_information">')
        end=body.index('</section>',start)+len('</section>')
        body=body[:start]+body[end:]
        with self.assertRaisesRegex(WriterContractBlocked,'WRITER_REQUIRED_SECTION_COUNT:further_information'):
            seal(self.job,draft(self.job,body))

if __name__=='__main__':
    unittest.main()
