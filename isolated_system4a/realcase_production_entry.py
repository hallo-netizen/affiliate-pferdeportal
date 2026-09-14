from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from codex_worker_entry import build_codex_production_worker_pool
from external_host import ExternalSupervisorHost


def run_realcase(
    *,
    external_input: Path,
    worker_source: Path,
    worker_entrypoint: str,
    runtime_parent: Path,
    authority_root: Path,
    output: Path,
    parent_chat_dir: Path,
    timeout_seconds: float = 180.0,
) -> dict[str, Any]:
    pool = build_codex_production_worker_pool(
        Path(worker_source),
        worker_entrypoint,
        Path(runtime_parent),
        runtime_processes=1,
        timeout_seconds=timeout_seconds,
    )
    host = ExternalSupervisorHost(mode='production', authority_root=Path(authority_root))
    return host.run_production(
        Path(external_input),
        pool,
        Path(output),
        Path(parent_chat_dir),
    )


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='system4a-realcase-production')
    p.add_argument('--external-input', required=True)
    p.add_argument('--worker-source', required=True)
    p.add_argument('--worker-entrypoint', required=True)
    p.add_argument('--runtime-parent', required=True)
    p.add_argument('--authority-root', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--parent-chat-dir', required=True)
    p.add_argument('--timeout-seconds', type=float, default=180.0)
    return p


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    result = run_realcase(
        external_input=Path(args.external_input),
        worker_source=Path(args.worker_source),
        worker_entrypoint=args.worker_entrypoint,
        runtime_parent=Path(args.runtime_parent),
        authority_root=Path(args.authority_root),
        output=Path(args.output),
        parent_chat_dir=Path(args.parent_chat_dir),
        timeout_seconds=args.timeout_seconds,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(',', ':')))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
