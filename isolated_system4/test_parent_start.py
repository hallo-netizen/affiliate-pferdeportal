from __future__ import annotations

import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import parent_start


ITEM = {
    'article_type': 'Beratung',
    'category': 'hindernisstangen-beratung',
    'plan_slot': '9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56',
    'target_keyword': 'Hindernisstangen für Pferde',
    'title': 'Das Wichtigste über Hindernisstangen für Pferde',
}


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/ok':
            body = b'<html><head><title>Real parent source</title></head><body><main>This is a real HTTP source response with enough bound evidence for the System 4 parent start path.</main></body></html>'
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(403)
        self.end_headers()

    def log_message(self, fmt, *args):
        pass


class ParentStartTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), _Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_address[1]}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def _launch_value(self, urls, *, publish=False):
        return {
            'contract': parent_start.CONTRACT,
            'publish_allowed': publish,
            'items': [ITEM],
            'source_urls': [urls],
        }

    def test_positive_exact_external_command_token_creates_point0_and_root_dispatch(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-token-') as td:
            root = Path(td)
            runtime = root / 'runtime'
            token = parent_start.encode_launch(self._launch_value([self.base + '/ok']))
            rc = parent_start.main(['parent_start.py', 'start-b64', token, str(runtime)])
            self.assertEqual(rc, 0)
            workspace = runtime / 'item-0'
            self.assertTrue((runtime / 'point0-0.json').is_file())
            self.assertTrue((runtime / 'parent_start_receipt.json').is_file())
            self.assertTrue((workspace / 'point0.json').is_file())
            self.assertTrue((workspace / 'supervisor_state.json').is_file())
            self.assertTrue((workspace / 'root_receipt.json').is_file())
            self.assertTrue((workspace / 'worker_dispatch.json').is_file())
            point0 = json.loads((runtime / 'point0-0.json').read_text(encoding='utf-8'))
            self.assertEqual(point0['contract'], 'SYSTEM4_POINT0_SNAPSHOT_V1')
            self.assertEqual(point0['research_runtime']['status'], 'PASS')
            self.assertEqual(point0['research_runtime']['source_count'], 1)
            self.assertEqual(point0['research_runtime']['sources'][0]['http_status'], 200)

    def test_negative_noncanonical_or_malformed_token_blocks_before_runtime(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-bad-token-') as td:
            runtime = Path(td) / 'runtime'
            rc = parent_start.main(['parent_start.py', 'start-b64', 'not_valid!*', str(runtime)])
            self.assertEqual(rc, 2)
            self.assertFalse(runtime.exists())

    def test_negative_old_file_cli_is_not_an_external_entry(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-old-entry-') as td:
            root = Path(td)
            launch = root / 'launch.json'
            launch.write_text(json.dumps(self._launch_value([self.base + '/ok']), ensure_ascii=False), encoding='utf-8')
            runtime = root / 'runtime'
            rc = parent_start.main(['parent_start.py', 'start', str(launch), str(runtime)])
            self.assertEqual(rc, 2)
            self.assertFalse(runtime.exists())

    def test_negative_missing_source_urls_blocks_before_runtime_creation(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-missing-') as td:
            runtime = Path(td) / 'runtime'
            token = parent_start.encode_launch(self._launch_value([]))
            rc = parent_start.main(['parent_start.py', 'start-b64', token, str(runtime)])
            self.assertEqual(rc, 2)
            self.assertFalse(runtime.exists())

    def test_negative_http_403_blocks_before_root_workspace(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-403-') as td:
            runtime = Path(td) / 'runtime'
            token = parent_start.encode_launch(self._launch_value([self.base + '/forbidden']))
            rc = parent_start.main(['parent_start.py', 'start-b64', token, str(runtime)])
            self.assertEqual(rc, 2)
            self.assertTrue(runtime.exists())
            self.assertFalse((runtime / 'item-0').exists())

    def test_negative_publish_true_blocks_before_runtime_creation(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-publish-') as td:
            runtime = Path(td) / 'runtime'
            token = parent_start.encode_launch(self._launch_value([self.base + '/ok'], publish=True))
            rc = parent_start.main(['parent_start.py', 'start-b64', token, str(runtime)])
            self.assertEqual(rc, 2)
            self.assertFalse(runtime.exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
