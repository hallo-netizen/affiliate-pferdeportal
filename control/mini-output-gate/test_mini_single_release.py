"""Single-file MINI distribution tests; all editorial/title results are synthetic QA data."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from mini_release_gate import init, write
from mini_single_release import run, deliver, RELEASE_DIR, RELEASE_NAME, CONTRACT


def base_source(already_category=False):
    items = [{'pool_key': f'TEST-{i}', 'raw_query': f'QA test question {i}', 'mode': 'NEW',
              'decision': 'JA', 'source_sha256': f'item{i}'} for i in range(3)]
    resume = [{'item_index': i, 'next': 'EDITORIAL' if already_category else 'CATEGORY',
               'category': {'route':'FACH', 'category_slug':'test-cat', 'article_type':'FAQ'} if already_category else None,
               'editorial':None, 'title':None} for i in range(3)]
    return {'contract': 'TEXTERSTELLUNG_SINGLE_EDITOR_BATCH_V1',
            'checkpoint_contract': 'TEXTERSTELLUNG_MINI_CHECKPOINT_V1',
            'batch_id': 'TEST-MINI-ONE-RELEASE', 'source_sha256':'TEST-SOURCE-SHA',
            'items': items, 'resume_checkpoints': resume}


def stage(source, which, fields):
    return {'contract':source['contract'],'checkpoint_contract':source['checkpoint_contract'],
            'batch_id':source['batch_id'],'source_sha256':source['source_sha256'],
            'checkpoint_stage':which,'items':[{**v,**fields[i]} for i,v in enumerate(source['items'])]}


class MiniOneFileGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ws = Path(self.tmp.name) / 'session'
        self.src = base_source()
        self._reset_source(self.src)

    def _reset_source(self, src):
        self.src = src
        with tempfile.TemporaryDirectory() as tmp:
            original = Path(tmp) / 'original.json'
            write(original, src)
            init(original, self.ws)

    def _complete(self, category=True):
        if category:
            write(self.ws/'CATEGORY.json',stage(self.src,'CATEGORY',[
                {'route':'FACH','category_slug':'test-cat','article_type':'FAQ'}]*3))
        write(self.ws/'EDITORIAL.json',stage(self.src,'EDITORIAL',[
            {'box':'FREI','intent_summary':'synthetic QA','matched_ref':'','reason':''},
            {'box':'BELEGT','intent_summary':'','matched_ref':'WP-TEST-REFERENCE','reason':''},
            {'box':'KLAERUNG','intent_summary':'','matched_ref':'','reason':'synthetic uncertainty'}]))
        write(self.ws/'TITLE.json',stage(self.src,'TITLE',[
            {'approved_title':'Synthetic question one?'},
            {'approved_title':''},
            {'approved_title':''}]))

    def test_no_early_release_and_repair(self):
        r=run(self.ws)
        self.assertEqual(r['next_worker'],'CATEGORY')
        self.assertFalse((self.ws/RELEASE_DIR).exists())
        self.assertTrue((self.ws/'REPARATUR.json').exists())

    def test_full_flow_one_public_import_file_and_no_stage_files(self):
        self._complete()
        r=run(self.ws)
        self.assertEqual(r['status'],'FREIGEGEBEN')
        self.assertEqual(r['release_count'],1)
        published = self.ws/RELEASE_DIR
        self.assertEqual(sorted(x.name for x in published.iterdir()),['MINI_EINMAL_REIMPORT.json','NACHWEIS.json'])
        p=json.loads((published/RELEASE_NAME).read_text())
        self.assertEqual(len(p['decisions']),3)
        self.assertEqual(p['decisions'][0]['category']['article_type'],'FAQ')
        self.assertEqual(p['decisions'][0]['editorial']['box'],'FREI')
        self.assertEqual(p['decisions'][0]['title']['approved_title'],'Synthetic question one?')
        self.assertEqual(p['decisions'][1]['editorial']['box'],'BELEGT')
        self.assertIsNone(p['decisions'][1]['title'])
        self.assertIsNone(p['decisions'][2]['title'])
        self.assertNotIn('categories',p)
        self.assertEqual(run(self.ws)['status'],'FREIGEGEBEN')

    def test_after_success_missing_title_revokes_release_and_repairs_only_owner(self):
        self._complete()
        self.assertEqual(run(self.ws)['status'],'FREIGEGEBEN')
        row= json.loads((self.ws/'TITLE.json').read_text())
        row['items'][0]['approved_title']=''
        write(self.ws/'TITLE.json',row)
        r=run(self.ws)
        self.assertEqual(r['status'],'REPARATUR')
        self.assertEqual(r['next_worker'],'TITLE')
        self.assertEqual(len(r['fix_only']),1)
        self.assertFalse((self.ws/RELEASE_DIR).exists())

    def test_already_stored_category_cannot_be_redone(self):
        with tempfile.TemporaryDirectory() as d:
            ws=Path(d)/'run'
            original=Path(d)/'source.json'
            src=base_source(already_category=True)
            write(original,src)
            init(original,ws)
            write(ws/'EDITORIAL.json',stage(src,'EDITORIAL',[
                {'box':'FREI','intent_summary':'QA','matched_ref':'','reason':''},
                {'box':'BELEGT','intent_summary':'','matched_ref':'WP-TEST','reason':''},
                {'box':'KLAERUNG','intent_summary':'','matched_ref':'','reason':'QA'}]))
            write(ws/'TITLE.json',stage(src,'TITLE',[
                {'approved_title':'Synthetic correct title?'},{'approved_title':''},{'approved_title':''}]))
            r=run(ws)
            self.assertEqual(r['status'],'FREIGEGEBEN')
            p=read_json(ws/RELEASE_DIR/RELEASE_NAME)
            self.assertIsNone(p['decisions'][0]['category'])
            self.assertEqual(p['decisions'][0]['editorial']['box'],'FREI')
            write(ws/'CATEGORY.json', stage(src,'CATEGORY',[
                {'route':'FACH','category_slug':'test-cat','article_type':'FAQ'}]*3))
            bad=run(ws)
            self.assertEqual(bad['status'],'REPARATUR')
            self.assertEqual(bad['next_worker'],'CATEGORY')
            self.assertFalse((ws/RELEASE_DIR).exists())

    def test_category_only_never_escapes_chat_delivery_gate(self):
        write(self.ws/'CATEGORY.json',stage(self.src,'CATEGORY',[
            {'route':'FACH','category_slug':'test-cat','article_type':'FAQ'}]*3))
        out=Path(self.tmp.name)/'CHAT_OUTPUT.json'
        out.write_text('STALE_PREVIOUS_SUCCESS')
        result=deliver(self.ws,out,self.ws/'CATEGORY.json')
        self.assertEqual(result['status'],'GESPERRT')
        self.assertEqual(result['next_worker'],'EDITORIAL')
        self.assertFalse(out.exists())
        self.assertFalse((self.ws/RELEASE_DIR).exists())

    def test_only_category_and_editorial_cannot_escape(self):
        write(self.ws/'CATEGORY.json',stage(self.src,'CATEGORY',[
            {'route':'FACH','category_slug':'test-cat','article_type':'FAQ'}]*3))
        write(self.ws/'EDITORIAL.json',stage(self.src,'EDITORIAL',[
            {'box':'FREI','intent_summary':'QA','matched_ref':'','reason':''}]*3))
        out=Path(self.tmp.name)/'CHAT_OUTPUT.json'
        result=deliver(self.ws,out)
        self.assertEqual(result['status'],'GESPERRT')
        self.assertEqual(result['next_worker'],'TITLE')
        self.assertFalse(out.exists())

    def test_forged_success_marker_is_not_enough(self):
        out=Path(self.tmp.name)/'CHAT_OUTPUT.json'
        fake=Path(self.tmp.name)/'FAKE_PASS.json'
        write(fake,{'contract':CONTRACT, 'release':{'state':'PASS','finished':True},
                    'decisions':[{'category':{'route':'FACH'}}]*3})
        result=deliver(self.ws,out,fake)
        self.assertEqual(result['status'],'GESPERRT')
        self.assertFalse(out.exists())

    def test_complete_batch_can_be_emitted_exactly_once(self):
        self._complete()
        out=Path(self.tmp.name)/'CHAT_OUTPUT.json'
        result=deliver(self.ws,out)
        self.assertEqual(result['status'],'FREIGEGEBEN')
        self.assertTrue(result['release_available'])
        self.assertTrue(out.exists())
        self.assertEqual(out.read_bytes(),(self.ws/RELEASE_DIR/RELEASE_NAME).read_bytes())
        self.assertEqual(result['import_sha256'],hashlib.sha256(out.read_bytes()).hexdigest())
        self.assertEqual(read_json(out)['release']['finished'], True)
        self.assertEqual(len(read_json(out)['decisions']),3)

    def test_complete_batch_rejects_any_different_direct_chat_file(self):
        self._complete()
        category=Path(self.tmp.name)/'CAT_ONLY.json'
        write(category,stage(self.src,'CATEGORY',[
            {'route':'FACH','category_slug':'test-cat','article_type':'FAQ'}]*3))
        output=Path(self.tmp.name)/'CHAT_OUTPUT.json'
        result=deliver(self.ws,output,category)
        self.assertEqual(result['status'],'GESPERRT')
        self.assertEqual(result['reason'],'MINI_DIRECT_FILE_NOT_APPROVED')
        self.assertFalse(output.exists())

    def test_revalidation_revokes_stale_output_when_title_is_removed(self):
        self._complete()
        output=Path(self.tmp.name)/'CHAT_OUTPUT.json'
        self.assertEqual(deliver(self.ws,output)['status'],'FREIGEGEBEN')
        title=read_json(self.ws/'TITLE.json')
        title['items'][0]['approved_title']=''
        write(self.ws/'TITLE.json',title)
        result=deliver(self.ws,output)
        self.assertEqual(result['status'],'GESPERRT')
        self.assertEqual(result['next_worker'],'TITLE')
        self.assertFalse(output.exists())

    def test_complete_batch_accepts_only_byte_identical_candidate(self):
        self._complete()
        self.assertEqual(run(self.ws)['status'],'FREIGEGEBEN')
        output=Path(self.tmp.name)/'CHAT_OUTPUT.json'
        result=deliver(self.ws,output,self.ws/RELEASE_DIR/RELEASE_NAME)
        self.assertEqual(result['status'],'FREIGEGEBEN')
        self.assertTrue(output.exists())

    def test_source_mutation_is_fail_closed(self):
        self._complete()
        self.assertEqual(run(self.ws)['status'],'FREIGEGEBEN')
        source=self.ws/'ORIGINAL_MINI.json'
        source.write_text(source.read_text()+'\n')
        r=run(self.ws)
        self.assertEqual(r['status'],'REPARATUR')
        self.assertFalse((self.ws/RELEASE_DIR).exists())


def read_json(path):
    return json.loads(path.read_text())

if __name__ == '__main__':
    unittest.main(verbosity=2)