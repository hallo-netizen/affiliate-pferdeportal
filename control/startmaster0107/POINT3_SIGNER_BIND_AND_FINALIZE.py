#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BATCH = "7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a"
DUAL = REPO / "control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py"
RECEIPTS = (
    REPO / ".pferde-release" / BATCH / "RELEASE_RECEIPT.json",
    REPO / "control/startmaster0107/durable_release_archive" / BATCH / "RELEASE_RECEIPT.json",
)


def load_dual():
    spec = importlib.util.spec_from_file_location("point3_dual", DUAL)
    if spec is None or spec.loader is None:
        raise RuntimeError("POINT3_DUAL_LOAD_FAILED")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def bind_existing_signer() -> str:
    direct = os.environ.get("PSERC_SIGNER_CMD", "").strip()
    if direct:
        return direct

    env_candidates = []
    for key, value in os.environ.items():
        value = str(value or "").strip()
        if key.endswith("_SIGNER_CMD") and value:
            env_candidates.append(value)
    env_candidates = list(dict.fromkeys(env_candidates))
    if len(env_candidates) == 1:
        os.environ["PSERC_SIGNER_CMD"] = env_candidates[0]
        return env_candidates[0]
    if len(env_candidates) > 1:
        raise RuntimeError("POINT3_SIGNER_CMD_AMBIGUOUS")

    path_candidates = []
    pattern = re.compile(r"(?:pserc|workflow|supervisor).*signer|signer.*(?:pserc|workflow|supervisor)", re.I)
    for folder in os.environ.get("PATH", "").split(os.pathsep):
        p = Path(folder)
        if not p.is_dir():
            continue
        try:
            names = list(p.iterdir())
        except OSError:
            continue
        for candidate in names:
            if pattern.fullmatch(candidate.name) and candidate.is_file() and os.access(candidate, os.X_OK):
                resolved = str(candidate.resolve())
                if resolved not in path_candidates:
                    path_candidates.append(resolved)
    if len(path_candidates) == 1:
        os.environ["PSERC_SIGNER_CMD"] = path_candidates[0]
        return path_candidates[0]
    if len(path_candidates) > 1:
        raise RuntimeError("POINT3_HOST_SIGNER_AMBIGUOUS")
    raise RuntimeError("POINT3_EXISTING_HOST_SIGNER_NOT_EXPOSED")


def receipt_ref() -> str:
    existing = [p for p in RECEIPTS if p.is_file()]
    if not existing:
        raise RuntimeError("POINT3_RELEASE_RECEIPT_NOT_AVAILABLE")
    p = existing[0]
    return str(p.relative_to(REPO))


def main() -> int:
    bind_existing_signer()
    dual = load_dual()
    result = dual.finalize_after_107008(REPO, receipt_ref())
    if result.get("status") != "PSERC_FINAL_PACKAGE_PASS":
        raise RuntimeError("POINT3_FINALIZER_BLOCKED:" + str(result.get("reason") or "UNKNOWN"))
    print("POINT3_SIGNER_FINALIZE_PASS")
    print("package_ref=" + result["package_ref"])
    print("package_sha256=" + result["package_sha256"])
    print("package_id=" + result["package_id"])
    print("publish_allowed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
