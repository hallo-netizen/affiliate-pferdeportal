import json
import tempfile
import unittest
from pathlib import Path

from engine.k0_historical_content_guard import verify, Blocked

def package(text):
    return {
        'contract': 'K0_ARTICLE_PACKAGE_V1',
        'html': '<article><p>' + text + '</p></article>',
    }

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
