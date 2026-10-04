import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from engine.k0_historical_content_guard import verify, Blocked

def stable(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    ).hexdigest()

def package(text, draft=None):
    out = {
        'contract': 'K0_ARTICLE_PACKAGE_V1',
        'html': '<article><p>' + text + '</p></article>',
    }
    if draft is not None:
        out['writer_provenance'] = {
            'job_id': draft['job_id'],
            'draft_sha256': stable(draft),
        }
    return out

class TestK0HistoricalContentGuard(unittest.TestCase):
    def test_unique_new_text_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root/'real_runs/k0/old').mkdir(parents=True)
            (root/'real_runs/k0/new').mkdir(parents=True)
            old = ' '.join('altwort' + str(i) for i in range(40))
            (root/'real_runs/k0/old/WORDPRESS_SINGLE.json').write_text(
                json.dumps({'body': old}), encoding='utf-8'
            )
            new = ' '.join('neuwort' + str(i) for i in range(50))
            r = verify(package(new), 'real_runs/k0/new', root)
            self.assertEqual(r['status'], 'PASS')

    def test_exact_old_article_sequence_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root/'real_runs/k0/old').mkdir(parents=True)
            (root/'real_runs/k0/new').mkdir(parents=True)
            copied = ' '.join('kopiert' + str(i) for i in range(24))
            (root/'real_runs/k0/old/WORDPRESS_SINGLE.json').write_text(
                json.dumps({'articles': [{'body': copied}]}), encoding='utf-8'
            )
            new = 'start neue worte ' + copied + ' weitere neue worte am ende'
            with self.assertRaisesRegex(Blocked, 'K0_HISTORICAL_TEXT_REUSE_BLOCKED'):
                verify(package(new), 'real_runs/k0/new', root)

    def test_exact_current_source_draft_is_not_history(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root/'real_runs/k0/new').mkdir(parents=True)
            (root/'writer_drafts').mkdir(parents=True)
            text = ' '.join('aktuell' + str(i) for i in range(30))
            draft = {
                'contract':'K0_WRITER_DRAFT_V1',
                'job_id':'k0w-' + 'a'*24,
                'content_html':'<article><p>' + text + '</p></article>',
                'publish_allowed':False,
            }
            (root/'writer_drafts/current.json').write_text(json.dumps(draft),encoding='utf-8')
            r = verify(package(text, draft), 'real_runs/k0/new', root)
            self.assertEqual(r['status'], 'PASS')

    def test_other_historical_writer_draft_with_same_text_still_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root/'real_runs/k0/new').mkdir(parents=True)
            (root/'writer_drafts').mkdir(parents=True)
            text = ' '.join('kopiert' + str(i) for i in range(30))
            current = {
                'contract':'K0_WRITER_DRAFT_V1',
                'job_id':'k0w-' + 'b'*24,
                'content_html':'<article><p>' + text + '</p></article>',
                'publish_allowed':False,
            }
            old = dict(current)
            old['job_id']='k0w-' + 'c'*24
            (root/'writer_drafts/current.json').write_text(json.dumps(current),encoding='utf-8')
            (root/'writer_drafts/old.json').write_text(json.dumps(old),encoding='utf-8')
            with self.assertRaisesRegex(Blocked, 'K0_HISTORICAL_TEXT_REUSE_BLOCKED:writer_drafts/old.json'):
                verify(package(text, current), 'real_runs/k0/new', root)

    def test_same_job_but_mutated_draft_is_not_exempt(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root/'real_runs/k0/new').mkdir(parents=True)
            (root/'writer_drafts').mkdir(parents=True)
            text = ' '.join('gleich' + str(i) for i in range(30))
            current = {
                'contract':'K0_WRITER_DRAFT_V1',
                'job_id':'k0w-' + 'd'*24,
                'content_html':'<article><p>' + text + '</p></article>',
                'publish_allowed':False,
            }
            mutated = dict(current)
            mutated['revision_count']=99
            (root/'writer_drafts/mutated.json').write_text(json.dumps(mutated),encoding='utf-8')
            with self.assertRaisesRegex(Blocked, 'K0_HISTORICAL_TEXT_REUSE_BLOCKED:writer_drafts/mutated.json'):
                verify(package(text, current), 'real_runs/k0/new', root)

    def test_current_run_is_excluded_from_history_scan(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root/'real_runs/k0/new').mkdir(parents=True)
            text = ' '.join('eigen' + str(i) for i in range(30))
            (root/'real_runs/k0/new/WORDPRESS_SINGLE.json').write_text(
                json.dumps({'body': text}), encoding='utf-8'
            )
            r = verify(package(text), 'real_runs/k0/new', root)
            self.assertEqual(r['status'], 'PASS')

if __name__ == '__main__':
    unittest.main()
