from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping


class ReleaseError(RuntimeError):
    pass


def build_unsigned(state: Mapping[str, Any], out_dir: Path) -> dict[str, Any]:
    """FULL_PRODUCTION may only leave System 4 through the complete batch gate.

    The former single-article adapter bound one article to the SHA of the complete
    WordPress batch. That is unsafe because WordPress consumes the batch identity
    atomically. Keep this function only as a fail-closed compatibility surface for
    callers that still know the old command name.
    """
    raise ReleaseError("PER_ARTICLE_FULL_PRODUCTION_RELEASE_FORBIDDEN_USE_BATCH_GATE")


def finalize_signed(unsigned: Mapping[str, Any], signature: Mapping[str, str], final_path: Path) -> dict[str, Any]:
    """A single article may never be finalized as the signed WordPress batch."""
    raise ReleaseError("PER_ARTICLE_SIGNED_FINALIZE_FORBIDDEN_USE_BATCH_GATE")
