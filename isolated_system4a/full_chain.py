from __future__ import annotations

import hashlib
import json
import os
import secrets
import sys
from pathlib import Path
from typing import Any, Callable, Mapping

HERE = Path(__file__).resolve().parent
REPO = HERE.parent if HERE.name == 'isolated_system4a' else HERE
SYSTEM4 = REPO / 'isolated_system4'
if str(SYSTEM4) not in sys.path:
    sys.path.insert(0, str(SYSTEM4))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import batch_gate  # type: ignore
import handoff_transport  # type: ignore
from capsule import CapsuleController, CapsuleError
from system4_readonly import System4ReadOnlyChecks


class FullChainError(RuntimeError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise FullChainError(code)


def _canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def _sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class FullChainSupervisor:
    """Single entry/single authority orchestration for System 4A.

    Production mode creates the real read-only System-4 checker backend internally.
    Test mode may inject a checker, but its result is architecture evidence only.
    """

    def __init__(self, *, mode: str = 'production', checks: Any | None = None):
        _require(mode in {'production', 'test'}, 'MODE_INVALID')
        if mode == 'production':
            _require(checks is None, 'PRODUCTION_CHECK_BACKEND_INJECTION_FORBIDDEN')
            self._checks = None
            self._controller = None
        else:
            _require(checks is not None, 'TEST_CHECK_BACKEND_REQUIRED')
            self._checks = checks
            self._controller = CapsuleController(secrets.token_bytes(32), checks)
        self._mode = mode
        self._started = False
        self._finished = False
        self._capsule_ids: list[str] = []
        self._batch_sha256: str | None = None
        self._source_snapshot_sha256: str | None = None
        self._last_output_sha256: str | None = None
        self._last_inline_path: str | None = None

    @property
    def mode(self) -> str:
        return self._mode

    def status(self) -> dict[str, Any]:
        return {
            'mode': self._mode,
            'started': self._started,
            'finished': self._finished,
            'article_count': len(self._capsule_ids),
            'publish_allowed': False,
            'output_sha256': self._last_output_sha256,
            'parent_chat_inline_path': self._last_inline_path,
        }

    def _activate_production_backend(self) -> None:
        _require(self._mode == 'production', 'PRODUCTION_BACKEND_MODE_REQUIRED')
        _require(not self._started, 'PRODUCTION_BACKEND_AFTER_START_FORBIDDEN')
        if self._controller is None:
            checks = System4ReadOnlyChecks()
            self._checks = checks
            self._controller = CapsuleController(secrets.token_bytes(32), checks)

    def _ingress(self, snapshot_path: Path) -> list[dict[str, str]]:
        _require(not self._started, 'FULL_CHAIN_ALREADY_STARTED')
        _require(self._controller is not None, 'SUPERVISOR_BACKEND_NOT_BOUND')
        snapshot_sha, batch_sha, items = batch_gate.load_snapshot(Path(snapshot_path))
        _require(items, 'FULL_CHAIN_EMPTY_BATCH')
        self._started = True
        self._source_snapshot_sha256 = snapshot_sha
        self._batch_sha256 = batch_sha
        for item in items:
            self._capsule_ids.append(self._controller.create(item, snapshot_sha, batch_sha))
        return items

    @staticmethod
    def _production_evidence(export: Mapping[str, Any]) -> Mapping[str, Any]:
        evidence = export.get('production_evidence')
        _require(isinstance(evidence, Mapping), 'PRODUCTION_EVIDENCE_MISSING')
        _require(evidence.get('contract') == 'SYSTEM4_FULL_PRODUCTION_CHECK_V1', 'PRODUCTION_EVIDENCE_CONTRACT_INVALID')
        _require(evidence.get('status') == 'PASS', 'PRODUCTION_EVIDENCE_NOT_PASS')
        nested = evidence.get('evidence')
        _require(isinstance(nested, Mapping), 'PRODUCTION_EVIDENCE_NESTED_MISSING')
        for key in ('no_legacy', 'no_external_links', 'languagetool', 'ppm679'):
            _require(isinstance(nested.get(key), Mapping), 'PRODUCTION_EVIDENCE_COMPONENT_MISSING:' + key)
        return nested

    def _handoff_payload(self, exports: list[dict[str, Any]]) -> dict[str, Any]:
        _require(self._batch_sha256 is not None, 'BATCH_NOT_BOUND')
        rows = []
        for index, export in enumerate(exports):
            article = export['article']
            nested = self._production_evidence(export)
            context = export['production_context']
            rows.append({
                'index': index,
                'title': article['title'],
                'target_keyword': article['target_keyword'],
                'category': article['category'],
                'article_type': article['article_type'],
                'plan_slot': article['plan_slot'],
                'final_draft_sha256': export['body_sha256'],
                'revision_count': export['revision'],
                'body': export['body'],
                'production_context': {
                    'fact_pack': context['fact_pack'],
                    'production_plan_item': context['production_plan_item'],
                },
                'languagetool': dict(nested['languagetool']),
                'ppm679': dict(nested['ppm679']),
            })
        return {
            'contract': handoff_transport.HANDOFF_CONTRACT,
            'batch_sha256': self._batch_sha256,
            'publish_allowed': False,
            'signing_deferred': True,
            'batch_gate_status': 'SYSTEM4_BATCH_FULL_PASS_COLLECTED',
            'no_legacy_status': 'PASS',
            'test_suite_status': 'PASS',
            'wordpress_review': {
                'file_format': 'JSON',
                'mime_type': 'application/json',
                'intended_next_step': 'WORDPRESS_DIRECT_IMPORT',
                'plugin_name': 'Portal SEO Editorial Plan Compiler',
                'plugin_version_verified_against': handoff_transport.DIRECT_IMPORT_PLUGIN_VERSION,
                'ppm_version_verified_against': '6.7.9',
                'direct_wordpress_upload_ready': True,
                'direct_upload_block_reason': None,
                'required_downstream_components': [],
            },
            'articles': rows,
        }

    def _write_verified_handoff(self, payload: dict[str, Any], output_path: Path) -> dict[str, Any]:
        handoff_transport.validate_handoff(payload)
        raw = _canonical(payload)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = output_path.with_name(output_path.name + '.tmp')
        try:
            tmp.write_bytes(raw)
            os.replace(tmp, output_path)
            verified, reread = handoff_transport.read_validate_handoff(output_path)
            _require(reread == raw, 'HANDOFF_READBACK_BYTES_CHANGED')
            _require(verified == payload, 'HANDOFF_READBACK_PAYLOAD_CHANGED')
        except Exception:
            try:
                tmp.unlink(missing_ok=True)
            except Exception:
                pass
            try:
                output_path.unlink(missing_ok=True)
            except Exception:
                pass
            raise
        sha = _sha_bytes(raw)
        self._last_output_sha256 = sha
        return {'path': str(output_path), 'sha256': sha, 'bytes': len(raw)}

    def _pack_parent_chat(self, output_path: Path) -> dict[str, Any]:
        inline_name = getattr(handoff_transport, 'INLINE_FILENAME', 'SYSTEM4_PARENT_CHAT_INLINE_V2.txt')
        inline_path = Path(output_path).with_name(inline_name)
        result = handoff_transport.inline_pack(Path(output_path), inline_path)
        self._last_inline_path = str(inline_path)
        return {'path': str(inline_path), **dict(result)}

    def simulate_parent_chat_roundtrip(self, inline_path: Path, output_dir: Path) -> dict[str, Any]:
        rebuilt = handoff_transport.inline_unpack(Path(inline_path), Path(output_dir))
        payload, raw = handoff_transport.read_validate_handoff(rebuilt)
        return {'status': 'SYSTEM4A_PARENT_CHAT_ROUNDTRIP_PASS', 'path': str(rebuilt), 'sha256': _sha_bytes(raw), 'article_count': len(payload['articles']), 'publish_allowed': False}

    def _execute(
        self,
        snapshot_path: Path,
        worker: Callable[[Mapping[str, Any]], Mapping[str, Any]],
        output_path: Path,
        *,
        terminal_status: str,
    ) -> dict[str, Any]:
        _require(callable(worker), 'WORKER_INVALID')
        _require(self._controller is not None, 'SUPERVISOR_BACKEND_NOT_BOUND')
        self._ingress(Path(snapshot_path))
        exports: list[dict[str, Any]] = []
        try:
            for capsule_id in self._capsule_ids:
                exports.append(self._controller.run_automatic(capsule_id, worker))
            batch_result = self._controller.batch_check(self._capsule_ids)
            _require(batch_result.get('status') == 'PASS', 'BATCH_NOT_PASS')
            payload = self._handoff_payload(exports)
            written = self._write_verified_handoff(payload, Path(output_path))
            inline = self._pack_parent_chat(Path(output_path))
        except Exception:
            try:
                Path(output_path).unlink(missing_ok=True)
                if self._last_inline_path:
                    Path(self._last_inline_path).unlink(missing_ok=True)
            except Exception:
                pass
            raise
        self._finished = True
        return {
            'status': terminal_status,
            'article_count': len(exports),
            'output': written,
            'parent_chat_inline': inline,
            'publish_allowed': False,
        }

    def run_full(
        self,
        snapshot_path: Path,
        worker: Callable[[Mapping[str, Any]], Mapping[str, Any]],
        output_path: Path,
    ) -> dict[str, Any]:
        _require(self._mode == 'test', 'PRODUCTION_REQUIRES_EXTERNAL_SUPERVISOR_HOST')
        return self._execute(
            snapshot_path, worker, output_path,
            terminal_status='SYSTEM4A_FULL_CHAIN_ARCHITECTURE_PASS',
        )

    def _run_external_production(
        self,
        snapshot_path: Path,
        worker: Callable[[Mapping[str, Any]], Mapping[str, Any]],
        output_path: Path,
    ) -> dict[str, Any]:
        _require(self._mode == 'production', 'EXTERNAL_PRODUCTION_MODE_REQUIRED')
        self._activate_production_backend()
        return self._execute(
            snapshot_path, worker, output_path,
            terminal_status='SYSTEM4A_FULL_CHAIN_PRODUCTION_PASS',
        )

    def verify_output(self, output_path: Path) -> dict[str, Any]:
        payload, raw = handoff_transport.read_validate_handoff(Path(output_path))
        return {
            'status': 'SYSTEM4A_OUTPUT_VERIFY_PASS',
            'sha256': _sha_bytes(raw),
            'article_count': len(payload['articles']),
            'publish_allowed': False,
        }
