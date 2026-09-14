from __future__ import annotations

import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

import parent_start

ITEM={'article_type':'Beratung','category':'hindernisstangen-beratung','plan_slot':'9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56','target_keyword':'Hindernisstangen für Pferde','title':'Das Wichtigste über Hindernisstangen für Pferde'}

class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/ok':
            body=b'<html><head><title>Real parent source</title></head><body><main>This is a real HTTP source response with enough bound evidence for the System 4 parent start path.</main></body></html>'
            self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body); return
        self.send_response(403); self.end_headers()
    def log_message(self,fmt,*args): pass

class ParentStartTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),_Handler); cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True); cls.thread.start(); cls.base=f'http://127.0.0.1:{cls.server.server_address[1]}'
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join(timeout=2)
    def _launch(self,urls,publish=False): return {'contract':parent_start.CONTRACT,'publish_allowed':publish,'items':[ITEM],'source_urls':[urls]}

    def test_positive_bound_capsule_entry_creates_point0_and_root_dispatch(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-bound-') as td:
            runtime=Path(td)/'runtime'; launch=self._launch([self.base+'/ok'])
            with mock.patch.object(parent_start,'_load_bound_capsule',return_value=launch):
                rc=parent_start.main(['parent_start.py','start-bound','isolated_system4/bound_launches/test.json','1'*64,str(runtime)])
            self.assertEqual(rc,0); workspace=runtime/'item-0'
            self.assertTrue((runtime/'point0-0.json').is_file()); self.assertTrue((runtime/'parent_start_receipt.json').is_file()); self.assertTrue((workspace/'point0.json').is_file()); self.assertTrue((workspace/'supervisor_state.json').is_file()); self.assertTrue((workspace/'root_receipt.json').is_file()); self.assertTrue((workspace/'worker_dispatch.json').is_file())

    def test_bound_capsule_loader_requires_clean_tracked_canonical_hash(self):
        rel='isolated_system4/bound_launches/test-loader.json'; path=parent_start.REPO/rel; path.parent.mkdir(parents=True,exist_ok=True); existed=path.exists(); old=path.read_bytes() if existed else None; raw=parent_start.canon(self._launch([self.base+'/ok'])); path.write_bytes(raw)
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

    def test_negative_long_token_and_old_file_entries_are_forbidden(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-old-') as td:
            runtime=Path(td)/'runtime'; self.assertEqual(parent_start.main(['parent_start.py','start-b64','abc',str(runtime)]),2); self.assertEqual(parent_start.main(['parent_start.py','start','launch.json',str(runtime)]),2); self.assertFalse(runtime.exists())

    def test_negative_bad_capsule_path_or_sha_blocks_before_runtime(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-bad-') as td:
            runtime=Path(td)/'runtime'; self.assertEqual(parent_start.main(['parent_start.py','start-bound','/tmp/free.json','0'*64,str(runtime)]),2); self.assertEqual(parent_start.main(['parent_start.py','start-bound','isolated_system4/bound_launches/x.json','bad',str(runtime)]),2); self.assertFalse(runtime.exists())

    def test_negative_publish_true_validation(self):
        with self.assertRaises(parent_start.ParentStartError): parent_start._validate_launch(self._launch([self.base+'/ok'],publish=True))

if __name__=='__main__': unittest.main(verbosity=2)
