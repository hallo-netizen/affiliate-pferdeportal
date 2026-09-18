from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import machine_point0
import source_acquisition


class SourceAcquisitionOwnerContractTests(unittest.TestCase):
    def _files(self, root: Path) -> tuple[Path, Path, Path, Path]:
        snapshot = root / 'snapshot.json'
        sources = root / 'sources.json'
        plans = root / 'plans.json'
        out = root / 'point0.json'
        snapshot.write_text('{}', encoding='utf-8')
        sources.write_text(json.dumps({'contract': source_acquisition.CONTRACT, 'item_count': 1, 'items': []}), encoding='utf-8')
        plans.write_text('{}', encoding='utf-8')
        return snapshot, sources, plans, out

    def _run_fetch_error(self, error: str, expected_rc: int, expected_marker: str) -> None:
        with tempfile.TemporaryDirectory(prefix='s4-source-owner-') as td:
            root = Path(td)
            snapshot, sources, plans, out = self._files(root)
            buf = io.StringIO()
            with mock.patch.object(source_acquisition, 'acquire_batch', side_effect=source_acquisition.SourceAcquisitionError(error)):
                with contextlib.redirect_stdout(buf):
                    rc = machine_point0.main(['machine_point0.py', 'build-fetch', str(snapshot), str(sources), str(plans), str(out), 'TEST_PROVIDER'])
            self.assertEqual(rc, expected_rc, buf.getvalue())
            self.assertIn(expected_marker, buf.getvalue())
            self.assertFalse(out.exists(), 'Point-0 must not exist after source-stage failure')

    def test_http_403_returns_source_acquisition_machine(self):
        self._run_fetch_error(
            'SOURCE_HTTP_FAIL:0:0:403',
            4,
            'SYSTEM4_SOURCE_OWNER_RETURN:SOURCE_ACQUISITION_MACHINE:SOURCE_ACQUISITION_STAGE:SOURCE_HTTP_FAIL:0:0:403',
        )

    def test_fetch_runtime_failure_returns_source_acquisition_machine(self):
        self._run_fetch_error(
            'SOURCE_FETCH_RUNTIME_FAIL:https://example.invalid:TimeoutError',
            4,
            'SYSTEM4_SOURCE_OWNER_RETURN:SOURCE_ACQUISITION_MACHINE:SOURCE_ACQUISITION_STAGE:SOURCE_FETCH_RUNTIME_FAIL:',
        )

    def test_empty_evidence_returns_source_acquisition_machine(self):
        self._run_fetch_error(
            'SOURCE_EVIDENCE_EMPTY:0:0',
            4,
            'SYSTEM4_SOURCE_OWNER_RETURN:SOURCE_ACQUISITION_MACHINE:SOURCE_ACQUISITION_STAGE:SOURCE_EVIDENCE_EMPTY:0:0',
        )

    def test_malformed_source_request_is_not_softened(self):
        self.assertIsNone(machine_point0._source_owner_route('SOURCE_REQUEST_CONTRACT_INVALID'))
        self.assertIsNone(machine_point0._source_owner_route('SOURCE_REQUEST_URL_INVALID:0:0'))
        self.assertIsNone(machine_point0._source_owner_route('SOURCE_REQUEST_ITEM_BINDING_INVALID:0'))

    def test_source_owner_route_does_not_accept_unknown(self):
        self.assertIsNone(machine_point0._source_owner_route('SOMETHING_UNKNOWN'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
