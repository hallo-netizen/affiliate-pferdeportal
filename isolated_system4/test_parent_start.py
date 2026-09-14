from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import parent_start

ITEM={'article_type':'Beratung','category':'hindernisstangen-beratung','plan_slot':'9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56','target_keyword':'Hindernisstangen für Pferde','title':'Das Wichtigste über Hindernisstangen für Pferde'}
EVIDENCE='Authoritative parent-machine evidence snapshot with enough factual material for the System 4 bound research source.'

def source(evidence=EVIDENCE):
    return {'source_id':'parent-test-0','source_title':'Bound source','source_url':'https://example.org/source','retrieved_at':'2026-09-14T18:20:00+00:00','evidence':evidence,'snapshot_sha256':parent_start.sha256(evidence.encode('utf-8')),'http_status':200,'source_kind':'parent_machine_bound_snapshot'}

class ParentStartTests(unittest.TestCase):
    def _launch(self,sources=None,publish=False): return {'contract':parent_start.CONTRACT,'publish_allowed':publish,'items':[ITEM],'bound_sources':[sources or [source()]]}

    def test_positive_bound_capsule_entry_creates_point0_and_root_dispatch_without_network(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-bound-') as td:
            runtime=Path(td)/'runtime'; launch=self._launch()
            with mock.patch.object(parent_start,'_load_bound_capsule',return_value=launch):
                rc=parent_start.main(['parent_start.py','start-bound','isolated_system4/bound_launches/test.json','1'*64,str(runtime)])
            self.assertEqual(rc,0); workspace=runtime/'item-0'
            self.assertTrue((runtime/'point0-0.json').is_file()); self.assertTrue((runtime/'parent_start_receipt.json').is_file()); self.assertTrue((workspace/'point0.json').is_file()); self.assertTrue((workspace/'supervisor_state.json').is_file()); self.assertTrue((workspace/'root_receipt.json').is_file()); self.assertTrue((workspace/'worker_dispatch.json').is_file())
            receipt=parent_start.json.loads((runtime/'parent_start_receipt.json').read_text(encoding='utf-8')); self.assertEqual(receipt['source_transport'],'PREBOUND_PARENT_SNAPSHOTS_NO_CODEX_NETWORK')

    def test_bound_capsule_loader_requires_clean_tracked_canonical_hash(self):
        rel='isolated_system4/bound_launches/test-loader.json'; path=parent_start.REPO/rel; path.parent.mkdir(parents=True,exist_ok=True); existed=path.exists(); old=path.read_bytes() if existed else None; raw=parent_start.canon(self._launch()); path.write_bytes(raw)
        try:
            def clean_git(*args): return rel if args[0]=='ls-files' else ''
            with mock.patch.object(parent_start.root_entry,'_git',side_effect=clean_git):
                value=parent_start._load_bound_capsule(rel,parent_start.sha256(raw)); self.assertEqual(value['contract'],parent_start.CONTRACT)
                with self.assertRaises(parent_start.ParentStartError): parent_start._load_bound_capsule(rel,'0'*64)
            def dirty_git(*args): return rel if args[0]=='ls-files' else ' M '+rel
            with mock.patch.object(parent_start.root_entry,'_git',side_effect=dirty_git):
                with self.assertRaises(parent_start.ParentStartError): parent_start._load_bound_capsule(rel,parent_start.sha256(raw))
        finally:
            if existed: path.write_bytes(old)
            else: path.unlink(missing_ok=True)

    def test_negative_source_urls_network_mode_is_forbidden(self):
        launch=self._launch(); launch['source_urls']=[['https://example.org/source']]
        with self.assertRaisesRegex(parent_start.ParentStartError,'PARENT_LAUNCH_FREE_NETWORK_SOURCE_URLS_FORBIDDEN'): parent_start._validate_launch(launch)

    def test_negative_tampered_source_snapshot_is_forbidden(self):
        bad=source(); bad['evidence']+=' tampered'
        with self.assertRaisesRegex(parent_start.ParentStartError,'PARENT_BOUND_SOURCE_SHA_MISMATCH'): parent_start._validate_launch(self._launch([bad]))

    def test_negative_unverified_http_status_is_forbidden(self):
        bad=source(); bad['http_status']=403
        with self.assertRaisesRegex(parent_start.ParentStartError,'PARENT_BOUND_SOURCE_HTTP_NOT_VERIFIED'): parent_start._validate_launch(self._launch([bad]))

    def test_negative_long_token_and_old_file_entries_are_forbidden(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-old-') as td:
            runtime=Path(td)/'runtime'; self.assertEqual(parent_start.main(['parent_start.py','start-b64','abc',str(runtime)]),2); self.assertEqual(parent_start.main(['parent_start.py','start','launch.json',str(runtime)]),2); self.assertFalse(runtime.exists())

    def test_negative_bad_capsule_path_or_sha_blocks_before_runtime(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-bad-') as td:
            runtime=Path(td)/'runtime'; self.assertEqual(parent_start.main(['parent_start.py','start-bound','/tmp/free.json','0'*64,str(runtime)]),2); self.assertEqual(parent_start.main(['parent_start.py','start-bound','isolated_system4/bound_launches/x.json','bad',str(runtime)]),2); self.assertFalse(runtime.exists())

    def test_negative_publish_true_validation(self):
        with self.assertRaises(parent_start.ParentStartError): parent_start._validate_launch(self._launch(publish=True))

if __name__=='__main__': unittest.main(verbosity=2)
