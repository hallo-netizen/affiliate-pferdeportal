import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from authority_store import SupervisorAuthorityStore
from capsule import CapsuleError
from persistent_capsule import PersistentCapsuleController
from test_full_chain_local import Checks

ARTICLE = {
    'title': 'Artikel Persistenz',
    'target_keyword': 'Persistenz',
    'category': 'beratung',
    'article_type': 'Beratung',
    'plan_slot': '1' * 64,
}


class AuthorityStoreTests(unittest.TestCase):
    def test_positive_capsule_resumes_after_controller_restart(self):
        with tempfile.TemporaryDirectory() as td:
            store = SupervisorAuthorityStore(Path(td) / 'authority')
            c1 = PersistentCapsuleController(store.authority_key(), Checks(), store)
            cid = c1.create(ARTICLE, '2' * 64, '3' * 64)
            research = json.dumps({
                'contract': 'SYSTEM4_RESEARCH_EVIDENCE_V1',
                'sources': [{
                    'source_id': 's',
                    'source_title': 'Quelle',
                    'source_url': 'https://example.org',
                    'retrieved_at': '2026-09-13T08:00:00Z',
                    'snapshot_sha256': '4' * 64,
                    'evidence': 'Beleg A. Beleg B. Mehr Kontext.',
                }],
            })
            c1.submit_research(cid, research)
            self.assertEqual(c1.status(cid)['phase'], 'FACTS_REQUIRED')
            c2 = PersistentCapsuleController(store.authority_key(), Checks(), store)
            self.assertEqual(c2.status(cid)['phase'], 'FACTS_REQUIRED')
            self.assertEqual(c2.status(cid)['article']['plan_slot'], '1' * 64)

    def test_negative_tampered_persistent_state_fails_hmac(self):
        with tempfile.TemporaryDirectory() as td:
            store = SupervisorAuthorityStore(Path(td) / 'authority')
            c1 = PersistentCapsuleController(store.authority_key(), Checks(), store)
            cid = c1.create(ARTICLE, '2' * 64, '3' * 64)
            con = sqlite3.connect(store.db_path)
            try:
                with con:
                    raw = con.execute(
                        'SELECT state_json FROM capsules WHERE capsule_id=?', (cid,)
                    ).fetchone()[0]
                    value = json.loads(raw)
                    value['phase'] = 'ARTICLE_PASS'
                    con.execute(
                        'UPDATE capsules SET state_json=? WHERE capsule_id=?',
                        (json.dumps(value), cid),
                    )
            finally:
                con.close()
            c2 = PersistentCapsuleController(store.authority_key(), Checks(), store)
            with self.assertRaisesRegex(CapsuleError, 'STATE_INTEGRITY_FAIL'):
                c2.status(cid)

    def test_authority_files_are_supervisor_private(self):
        with tempfile.TemporaryDirectory() as td:
            store = SupervisorAuthorityStore(Path(td) / 'authority')
            self.assertEqual(store.root.stat().st_mode & 0o777, 0o700)
            self.assertEqual(store.key_path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(store.db_path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(len(store.authority_key()), 32)

    def test_key_is_stable_across_store_restart(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / 'authority'
            s1 = SupervisorAuthorityStore(root)
            key = s1.authority_key()
            s2 = SupervisorAuthorityStore(root)
            self.assertEqual(s2.authority_key(), key)


if __name__ == '__main__':
    unittest.main(verbosity=2)
