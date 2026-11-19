#!/usr/bin/env python3
"""Local regression tests: use actual 10-item MINI and CATEGORY files; do not publish TEST decisions."""
import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from mini_release_gate import gate, init, write, REPAIR, RELEASE, STATUS, ORIGINAL

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
        write(self.ws/'TITLE.json', mock_stage(self.origin,'TITLE',
             lambda i, item: {'approved_title':f'TEST-Titel {i} zur Bearbeitung' if i < 8 else ''}))

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
        titles['items'][3]['approved_title']='TEST-Korrigierter Titel'
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