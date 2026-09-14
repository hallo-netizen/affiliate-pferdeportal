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

    def _write_launch(self, root: Path, urls, *, publish=False):
        path = root / 'launch.json'
        value = {
            'contract': parent_start.CONTRACT,
            'publish_allowed': publish,
            'items': [ITEM],
            'source_urls': [urls],
        }
        path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
        return path

    def test_positive_external_launch_creates_point0_and_root_dispatch(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-launch-') as td:
            root = Path(td)
            launch = self._write_launch(root, [self.base + '/ok'])
            runtime = root / 'runtime'
            workspaces = parent_start.run(launch, runtime)
            self.assertEqual(len(workspaces), 1)
            self.assertTrue((runtime / 'point0-0.json').is_file())
            self.assertTrue((runtime / 'parent_start_receipt.json').is_file())
            self.assertTrue((workspaces[0] / 'point0.json').is_file())
            self.assertTrue((workspaces[0] / 'supervisor.json').is_file())
            self.assertTrue((workspaces[0] / 'worker_dispatch.json').is_file())
            point0 = json.loads((runtime / 'point0-0.json').read_text(encoding='utf-8'))
            self.assertEqual(point0['contract'], 'SYSTEM4_POINT0_SNAPSHOT_V1')
            self.assertEqual(point0['research_runtime']['status'], 'PASS')
            self.assertEqual(point0['research_runtime']['source_count'], 1)
            self.assertEqual(point0['research_runtime']['sources'][0]['http_status'], 200)

    def test_negative_missing_source_urls_blocks_before_runtime_creation(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-missing-') as td:
            root = Path(td)
            launch = self._write_launch(root, [])
            runtime = root / 'runtime'
            with self.assertRaisesRegex(parent_start.ParentStartError, 'PARENT_LAUNCH_SOURCE_URLS_EMPTY'):
                parent_start.run(launch, runtime)
            self.assertFalse(runtime.exists())

    def test_negative_http_403_blocks_before_root_workspace(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-403-') as td:
            root = Path(td)
            launch = self._write_launch(root, [self.base + '/forbidden'])
            runtime = root / 'runtime'
            with self.assertRaisesRegex(parent_start.ParentStartError, 'PARENT_SOURCE_FETCH_FAILED'):
                parent_start.run(launch, runtime)
            self.assertTrue(runtime.exists())
            self.assertFalse((runtime / 'item-0').exists())

    def test_negative_publish_true_blocks_before_runtime_creation(self):
        with tempfile.TemporaryDirectory(prefix='s4-parent-publish-') as td:
            root = Path(td)
            launch = self._write_launch(root, [self.base + '/ok'], publish=True)
            runtime = root / 'runtime'
            with self.assertRaisesRegex(parent_start.ParentStartError, 'PARENT_LAUNCH_PUBLISH_MUST_BE_FALSE'):
                parent_start.run(launch, runtime)
            self.assertFalse(runtime.exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
