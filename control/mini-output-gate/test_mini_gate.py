#!/usr/bin/env python3
"""Local regression tests: use actual 10-item MINI and CATEGORY files; do not publish TEST decisions."""
import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from mini_release_gate import gate, init, write, REPAIR, RELEASE, STATUS, ORIGINAL, new_title_rule_error

ROOT = Path(__file__).resolve().parent
SRC = Path(os.getenv('MINI_TEST_ORIGINAL', str(ROOT/'fixtures'/'MINI_TEST_ORIGINAL.json')))
CAT = Path(os.getenv('MINI_TEST_CATEGORY', str(ROOT/'fixtures'/'MINI_TEST_CATEGORY.json')))


def mock_stage(original, stage, example):
    return {
        'contract': original['contract'],
        'checkpoint_contract': original['checkpoint_contract'],
        'batch_id': original['batch_id'],
        'source_sha256': original['source_sha256'],
        'checkpoint_stage': stage,
        'items': [{**v, **example(i, v)} for i, v in enumerate(original['items'])],
    }


class TestMiniGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ws = Path(self.tmp.name)
        self.origin = json.loads(SRC.read_text())
        self.cat = json.loads(CAT.read_text())
        self.assertEqual(init(SRC, self.ws)['status'], 'REPARATUR')
        write(self.ws/'CATEGORY.json', self.cat)
        self.assertEqual(gate(self.ws)['next_worker'], 'EDITORIAL')

    def insert_mock_editorial(self):
        def decide(i, item):
            if i == 8:
                return {'box':'BELEGT', 'intent_summary':'', 'matched_ref':'WORDPRESS:123456', 'reason':''}
            if i == 9:
                return {'box':'KLAERUNG', 'intent_summary':'', 'matched_ref':'', 'reason':'TEST_UNCLEAR'}
            return {'box':'FREI', 'intent_summary':'TEST-Ziel der Nutzerfrage', 'matched_ref':'', 'reason':''}
        write(self.ws/'EDITORIAL.json', mock_stage(self.origin,'EDITORIAL',decide))

    def insert_mock_title(self):
        # Existing MINI article types: Vergleich, FAQ, Beratung, then FAQ.
        natural = [
            'Minerallecksteine und Salzlecksteine für Pferde',
            'Sind Salzlecksteine für Pferde sinnvoll?',
            'Minerallecksteine für Pferde',
            'Wie zeigen Pferde Traurigkeit?',
            'Dürfen Pferde im Regen stehen?',
            'Ab wann sind Pferde alt?',
            'Wie lange erinnern sich Pferde an ihre Besitzer?',
            'In welchem Alter sind Pferde besonders schwierig?',
        ]
        write(self.ws/'TITLE.json', mock_stage(self.origin,'TITLE',
             lambda i, item: {'approved_title': natural[i] if i < 8 else ''}))

    def test_invalid_existing_wordpress_reference_repairs_editorial_only(self):
        self.insert_mock_editorial()
        self.insert_mock_title()
        editorial = json.loads((self.ws/'EDITORIAL.json').read_text())
        editorial['items'][8]['matched_ref'] = 'WORDPRESS:post:123456'
        write(self.ws/'EDITORIAL.json', editorial)
        bad = gate(self.ws)
        self.assertEqual(bad['next_worker'], 'EDITORIAL')
        self.assertEqual([(x['item_index'], x['code']) for x in bad['fix_only']],
                         [(8, 'BESTANDSREFERENZ_FORMAT_UNGUELTIG')])
        self.assertFalse((self.ws/RELEASE).exists())
        editorial['items'][8]['matched_ref'] = 'WORDPRESS:123456'
        write(self.ws/'EDITORIAL.json', editorial)
        self.assertEqual(gate(self.ws)['status'], 'FREIGEGEBEN_FUER_WP_IMPORTE')

    def test_existing_wordpress_reference_must_be_in_original_snapshot(self):
        self.insert_mock_editorial()
        self.insert_mock_title()
        source = json.loads((self.ws/ORIGINAL).read_text())
        source['existing_wordpress_and_plan_inventory'] = [
            {'source': 'WORDPRESS', 'id': 123456, 'type': 'post', 'title': 'QA existing article'}
        ]
        write(self.ws/ORIGINAL, source)
        from mini_release_gate import sha
        (self.ws/'ORIGINAL_SHA256.txt').write_text(sha(self.ws/ORIGINAL)+'\\n')
        editorial = json.loads((self.ws/'EDITORIAL.json').read_text())
        editorial['items'][8]['matched_ref'] = 'WORDPRESS:999999'
        write(self.ws/'EDITORIAL.json', editorial)
        bad = gate(self.ws)
        self.assertEqual(bad['next_worker'], 'EDITORIAL')
        self.assertIn('BESTANDSREFERENZ_NICHT_IM_ORIGINALEXPORT',
                      [x['code'] for x in bad['fix_only']])
        editorial['items'][8]['matched_ref'] = 'WORDPRESS:123456'
        write(self.ws/'EDITORIAL.json', editorial)
        self.assertEqual(gate(self.ws)['status'], 'FREIGEGEBEN_FUER_WP_IMPORTE')

    def test_title_language_rules_user_examples_and_natural_alternatives(self):
        bad = [
            'Mineralfutter richtig einordnen',
            'Mineralfutter sachlich einordnen',
            'Mineralfutter korrekt auswählen',
            'Mineralfutter passend auswählen',
            'Mineralfutter gezielt auswählen',
            'Mineralfutter bedarfsgerecht auswählen',
            'Mineralfutter sorgfältig auswählen',
            'Mineralfutter passend dosiert auswählen',
        ]
        for title in bad:
            with self.subTest(title=title):
                self.assertEqual(new_title_rule_error(title,'Beratung'),
                                 'TITEL_GENERISCHE_ENDFORMEL')
        for title in [
            'Mineralfutter für Pferde mit Sommerekzem',
            'Mineralfutter mit Selen für Pferde',
            'Welches Mineralfutter braucht mein Pferd?',
        ]:
            with self.subTest(title=title):
                self.assertIsNone(new_title_rule_error(title,'Beratung'))
        for title in [
            'Mineralfutter: Das gilt',
            'Mineralfutter - Das gilt',
            'Mineralfutter – Das gilt',
        ]:
            with self.subTest(title=title):
                self.assertEqual(new_title_rule_error(title,'Beratung'),
                                 'TITEL_SONDERZEICHEN_UNZULAESSIG')
        self.assertIsNone(new_title_rule_error('Was brauchen Pferde im Winter?','FAQ'))
        self.assertEqual(new_title_rule_error('Was brauchen Pferde im Winter','FAQ'),
                         'FAQ_TITEL_FRAGEZEICHEN_FEHLT')

    def test_category_only_fails_without_release(self):
        result=gate(self.ws)
        self.assertEqual(result['next_worker'],'EDITORIAL')
        self.assertEqual(len(result['fix_only']), 10)
        self.assertFalse((self.ws/RELEASE).exists())
        self.assertTrue((self.ws/REPAIR).is_file())

    def test_same_batch_repair_then_success_and_no_extra_decision(self):
        self.insert_mock_editorial()
        step=gate(self.ws)
        self.assertEqual(step['next_worker'],'TITLE')
        self.assertEqual(len(step['fix_only']),8)
        self.assertFalse((self.ws/RELEASE).exists())
        self.insert_mock_title()
        passed=gate(self.ws)
        self.assertEqual(passed['status'], 'FREIGEGEBEN_FUER_WP_IMPORTE')
        self.assertEqual(passed['topic_count'],10)
        self.assertEqual(len(passed['files']),3)
        self.assertFalse((self.ws/REPAIR).exists())
        self.assertTrue((self.ws/RELEASE/'NACHWEIS.json').is_file())
        report=json.loads((self.ws/RELEASE/'NACHWEIS.json').read_text())
        self.assertFalse(report['wordpress_import_confirmed'])
        self.assertFalse(report['domain_redecision_performed'])
        self.assertEqual([x['stage'] for x in report['files_in_import_order']],['CATEGORY','EDITORIAL','TITLE'])

    def test_tamper_source_is_rejected(self):
        self.insert_mock_editorial()
        self.insert_mock_title()
        corrupted=json.loads((self.ws/'TITLE.json').read_text())
        corrupted['items'][4]['raw_query']='changed'
        write(self.ws/'TITLE.json',corrupted)
        res=gate(self.ws)
        self.assertTrue(any(x['code']=='AUSGANGSDATEN_ODER_REIHENFOLGE_VERAENDERT' for x in res['fix_only']))
        self.assertFalse((self.ws/RELEASE).exists())
        self.insert_mock_title()
        self.assertEqual(gate(self.ws)['status'],'FREIGEGEBEN_FUER_WP_IMPORTE')

    def test_missing_title_repair_without_retry_others(self):
        self.insert_mock_editorial()
        self.insert_mock_title()
        titles=json.loads((self.ws/'TITLE.json').read_text())
        titles['items'][3]['approved_title']=''
        write(self.ws/'TITLE.json',titles)
        res=gate(self.ws)
        self.assertEqual(res['next_worker'],'TITLE')
        self.assertEqual(len(res['fix_only']),1)
        self.assertEqual(res['fix_only'][0]['item_index'],3)
        self.assertFalse((self.ws/RELEASE).exists())
        titles['items'][3]['approved_title']='Wie zeigen Pferde ihre Gefühle?'
        write(self.ws/'TITLE.json',titles)
        self.assertEqual(gate(self.ws)['status'],'FREIGEGEBEN_FUER_WP_IMPORTE')

    def test_title_rule_rejects_empty_standard_endings_and_returns_to_title(self):
        self.insert_mock_editorial()
        self.insert_mock_title()
        titles=json.loads((self.ws/'TITLE.json').read_text())
        titles['items'][2]['approved_title']='Minerallecksteine für Pferde passend auswählen'
        write(self.ws/'TITLE.json',titles)
        failed=gate(self.ws)
        self.assertEqual(failed['next_worker'],'TITLE')
        self.assertEqual(len(failed['fix_only']),1)
        self.assertEqual(failed['fix_only'][0]['item_index'],2)
        self.assertEqual(failed['fix_only'][0]['code'],'TITEL_GENERISCHE_ENDFORMEL')
        self.assertFalse((self.ws/RELEASE).exists())
        titles['items'][2]['approved_title']='Minerallecksteine für Pferde'
        write(self.ws/'TITLE.json',titles)
        self.assertEqual(gate(self.ws)['status'],'FREIGEGEBEN_FUER_WP_IMPORTE')

    def test_title_rule_rejects_colon_dash_and_hyphen_but_accepts_question(self):
        self.insert_mock_editorial()
        self.insert_mock_title()
        titles=json.loads((self.ws/'TITLE.json').read_text())
        titles['items'][0]['approved_title']='Minerallecksteine: Vergleich'
        titles['items'][1]['approved_title']='Sind Salzlecksteine - für Pferde sinnvoll?'
        titles['items'][3]['approved_title']='Wie zeigen Pferde Traurigkeit?'
        write(self.ws/'TITLE.json',titles)
        result=gate(self.ws)
        self.assertEqual(result['next_worker'],'TITLE')
        bad=[p for p in result['fix_only'] if p['stage']=='TITLE']
        self.assertEqual([(x['item_index'],x['code']) for x in bad],[
            (0,'TITEL_SONDERZEICHEN_UNZULAESSIG'),
            (1,'TITEL_SONDERZEICHEN_UNZULAESSIG'),
        ])
        self.insert_mock_title()
        self.assertEqual(gate(self.ws)['status'],'FREIGEGEBEN_FUER_WP_IMPORTE')

    def test_new_title_format_error_does_not_redecide_locked_title(self):
        self.insert_mock_editorial()
        self.insert_mock_title()
        source=json.loads((self.ws/ORIGINAL).read_text())
        source['resume_checkpoints'][0]['title']={'approved_title':'Alttitel: Bestand bleibt'}
        source['resume_checkpoints'][0]['next']='DONE'
        import hashlib
        write(self.ws/ORIGINAL,source)
        (self.ws/'ORIGINAL_SHA256.txt').write_text(
            hashlib.sha256((self.ws/ORIGINAL).read_bytes()).hexdigest()+'\n')
        titles=json.loads((self.ws/'TITLE.json').read_text())
        titles['items'][0]['approved_title']=''
        write(self.ws/'TITLE.json',titles)
        # A locked title is never reassessed; category/editorial must remain locked too.
        categories=json.loads((self.ws/'CATEGORY.json').read_text())
        categories['items'][0]['route']=''
        categories['items'][0]['category_slug']=''
        categories['items'][0]['article_type']=''
        write(self.ws/'CATEGORY.json',categories)
        editorial=json.loads((self.ws/'EDITORIAL.json').read_text())
        for k in ('box','intent_summary','matched_ref','reason'):
            editorial['items'][0][k]=''
        write(self.ws/'EDITORIAL.json',editorial)
        result=gate(self.ws)
        self.assertFalse(any(x['item_index']==0 and x['stage']=='TITLE'
                             for x in result.get('fix_only',[])))
        self.assertEqual(result['status'],'FREIGEGEBEN_FUER_WP_IMPORTE')

    def test_title_series_repair_only_repeated_generic_endings(self):
        self.insert_mock_editorial()
        self.insert_mock_title()
        titles=json.loads((self.ws/'TITLE.json').read_text())
        titles['items'][0]['approved_title']='Minerallecksteine für die Pferdepflege'
        titles['items'][2]['approved_title']='Nadelstriegel bei der Pferdepflege'
        titles['items'][4]['approved_title']='Welche Bürsten eignen sich für die Pferdepflege?'
        write(self.ws/'TITLE.json', titles)
        failed=gate(self.ws)
        self.assertEqual(failed['next_worker'], 'TITLE')
        self.assertEqual([(p['item_index'],p['code']) for p in failed['fix_only']],
                         [(2,'TITEL_SERIENFORMEL_WIEDERHOLT'),
                          (4,'TITEL_SERIENFORMEL_WIEDERHOLT')])
        self.assertFalse((self.ws/RELEASE).exists())
        titles['items'][2]['approved_title']='Nadelstriegel für Pferde'
        titles['items'][4]['approved_title']='Dürfen Pferde im Regen stehen?'
        write(self.ws/'TITLE.json', titles)
        self.assertEqual(gate(self.ws)['status'],'FREIGEGEBEN_FUER_WP_IMPORTE')

    def test_title_series_one_generic_ending_allowed(self):
        self.insert_mock_editorial()
        self.insert_mock_title()
        titles=json.loads((self.ws/'TITLE.json').read_text())
        titles['items'][2]['approved_title']='Nadelstriegel für die Pferdepflege'
        write(self.ws/'TITLE.json',titles)
        self.assertEqual(gate(self.ws)['status'],'FREIGEGEBEN_FUER_WP_IMPORTE')

    def test_single_hollow_and_their_usage_ending_repair(self):
        self.insert_mock_editorial()
        self.insert_mock_title()
        titles=json.loads((self.ws/'TITLE.json').read_text())
        titles['items'][2]['approved_title']='Metallstriegel für Pferde und ihre Verwendung'
        write(self.ws/'TITLE.json',titles)
        result=gate(self.ws)
        self.assertEqual(result['next_worker'],'TITLE')
        self.assertEqual([(x['item_index'],x['code']) for x in result['fix_only']],
                         [(2,'TITEL_GENERISCHE_ENDFORMEL')])
        titles['items'][2]['approved_title']='Metallstriegel beim Pferd sicher verwenden'
        write(self.ws/'TITLE.json',titles)
        self.assertEqual(gate(self.ws)['status'],'FREIGEGEBEN_FUER_WP_IMPORTE')

    def test_wrong_batch_and_stale_release_removed(self):
        self.insert_mock_editorial()
        self.insert_mock_title()
        self.assertEqual(gate(self.ws)['status'],'FREIGEGEBEN_FUER_WP_IMPORTE')
        e=json.loads((self.ws/'EDITORIAL.json').read_text())
        e['batch_id']='OTHER'
        write(self.ws/'EDITORIAL.json',e)
        res=gate(self.ws)
        self.assertEqual(res['status'],'REPARATUR')
        self.assertFalse((self.ws/RELEASE).exists())

    def test_original_immutable(self):
        f=self.ws/ORIGINAL
        txt=f.read_text()
        f.write_text(txt+'\n')
        with self.assertRaisesRegex(ValueError,'Original ist nicht unverändert'):
            gate(self.ws)

    def test_locked_category_cannot_be_decided_twice(self):
        resume = json.loads((self.ws / ORIGINAL).read_text())
        resume['resume_checkpoints'][0]['next'] = 'EDITORIAL'
        resume['resume_checkpoints'][0]['category'] = {
            k: self.cat['items'][0][k] for k in ('route', 'category_slug', 'article_type')}
        write(self.ws / ORIGINAL, resume)
        import hashlib
        (self.ws/'ORIGINAL_SHA256.txt').write_text(hashlib.sha256((self.ws/ORIGINAL).read_bytes()).hexdigest()+'\n')
        result = gate(self.ws)
        self.assertEqual(result['status'], 'REPARATUR')
        self.assertTrue(any(x['code'] == 'ABGESCHLOSSENE_KATEGORIE_ERNEUT_ENTSCHIEDEN'
                            and x['item_index'] == 0 for x in result['fix_only']))

    def test_done_topic_cannot_be_redecided(self):
        resume = json.loads((self.ws / ORIGINAL).read_text())
        resume['resume_checkpoints'][0]['next'] = 'DONE'
        write(self.ws / ORIGINAL, resume)
        import hashlib
        (self.ws/'ORIGINAL_SHA256.txt').write_text(hashlib.sha256((self.ws/ORIGINAL).read_bytes()).hexdigest()+'\n')
        result = gate(self.ws)
        self.assertTrue(any(x['code'] == 'BEREITS_ABGESCHLOSSENE_ENTSCHEIDUNG_WIEDERHOLT'
                            and x['item_index'] == 0 for x in result['fix_only']))
        self.assertFalse((self.ws/RELEASE).exists())

    def test_no_second_domain_review_and_legacy_only_category(self):
        with tempfile.TemporaryDirectory() as p:
            w=Path(p)
            older=copy.deepcopy(self.origin)
            for item in older['items']:
                item.update({'mode':'LEGACY_CATEGORY_ONLY','locked_box':'FREI','locked_title':'Bereits feststehender Titel','locked_intent':'Altbestand','locked_article_id':'','locked_plan_slot':''})
            older['batch_id']='TEST-LEGACY'
            orig=w/'src.json'
            write(orig,older)
            # CAT must preserve ALL original fields, including historical locked items.
            cp=mock_stage(older,'CATEGORY',lambda i,x: {k:self.cat['items'][i][k] for k in ('route','category_slug','article_type')})
            init(orig,w/'run')
            write(w/'run'/'CATEGORY.json',cp)
            r=gate(w/'run')
            self.assertEqual(r['status'],'FREIGEGEBEN_FUER_WP_IMPORTE')
            self.assertEqual([x['stage'] for x in r['files']],['CATEGORY'])

if __name__=='__main__':
    unittest.main(verbosity=2)