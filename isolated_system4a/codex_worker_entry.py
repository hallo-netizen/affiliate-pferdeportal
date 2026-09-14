from __future__ import annotations

from pathlib import Path

from external_host import PersistentArticleWorkerPool


def build_codex_production_worker_pool(
    source_dir: Path,
    entrypoint: str,
    runtime_parent: Path,
    *,
    runtime_processes: int = 1,
    timeout_seconds: float = 120.0,
) -> PersistentArticleWorkerPool:
    """Canonical Codex production worker entry. Cross-UID is fixed inside the factory."""
    return PersistentArticleWorkerPool.from_python_bundle(
        source_dir,
        entrypoint,
        run_as_user='nobody',
        runtime_parent=runtime_parent,
        runtime_processes=runtime_processes,
        timeout_seconds=timeout_seconds,
    )
