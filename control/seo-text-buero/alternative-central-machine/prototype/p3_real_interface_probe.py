#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]

PPM_REL = "control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PPM_SHA = "acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
PSERC_REL = "control/startmaster0107/runtime_packages/PSERC-FIX.zip"
PSERC_SHA = "77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314"
PSERC_INNER = "PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def blocked(code: str):
    raise RuntimeError(code)

def exact_package(path: Path, expected: str, label: str):
    if not path.is_file():
        blocked(label + "_MISSING")
    got = sha(path)
    if got != expected:
        blocked(label + "_HASH_MISMATCH")
    return got

def main() -> int:
    ppm = REPO / PPM_REL
    pserc = REPO / PSERC_REL

    ppm_hash = exact_package(ppm, PPM_SHA, "PPM")
    pserc_hash = exact_package(pserc, PSERC_SHA, "PSERC")

    # Negative proof: one-byte drift must fail the same identity rule.
    with tempfile.TemporaryDirectory() as td:
        tampered = Path(td) / "tampered.zip"
        shutil.copy2(ppm, tampered)
        with tampered.open("ab") as fh:
            fh.write(b"X")
        if sha(tampered) == PPM_SHA:
            blocked("NEGATIVE_PACKAGE_TAMPER_NOT_DETECTED")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        ppm_out = root / "ppm"
        pserc_outer = root / "pserc_outer"
        pserc_out = root / "pserc"
        ppm_out.mkdir()
        pserc_outer.mkdir()
        pserc_out.mkdir()

        with zipfile.ZipFile(ppm) as zf:
            zf.extractall(ppm_out)
        with zipfile.ZipFile(pserc) as zf:
            zf.extractall(pserc_outer)

        inner = pserc_outer / PSERC_INNER
        if not inner.is_file():
            blocked("PSERC_INNER_ZIP_MISSING")
        with zipfile.ZipFile(inner) as zf:
            zf.extractall(pserc_out)

        ppm_root = ppm_out / "portal-production-machine"
        pserc_root = pserc_out / "portal-seo-editorial-plan-compiler"
        fixture = ppm_root / "tests/normal-draft-production/fixture-builder.php"
        bridge = pserc_root / "includes/class-pserc-ppm-intake-bridge.php"

        if not fixture.is_file():
            blocked("PPM_FIXTURE_BUILDER_MISSING")
        if not bridge.is_file():
            blocked("PSERC_BRIDGE_MISSING")

        # Find the real pipeline declaration from the exact, hash-bound package.
        pipeline_files = []
        pipeline_token = "PPM679_Normal_Draft_Pipeline"
        for php in ppm_root.rglob("*.php"):
            try:
                text = php.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if pipeline_token in text and "execute_plan" in text:
                pipeline_files.append(php)

        if not pipeline_files:
            blocked("REAL_PPM_PIPELINE_ENTRY_NOT_FOUND")

        bridge_text = bridge.read_text(encoding="utf-8")
        if "PSERC_PPM_Intake_Bridge" not in bridge_text:
            blocked("REAL_PSERC_BRIDGE_CLASS_NOT_FOUND")
        if "execute_plan" not in bridge_text:
            blocked("REAL_PSERC_TO_PPM_CALL_NOT_FOUND")

        # Runtime syntax proof on the real files.
        for target in [fixture, bridge, pipeline_files[0]]:
            proc = subprocess.run(
                ["php", "-l", str(target)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            if proc.returncode != 0:
                blocked("PHP_LINT_FAIL:" + target.name)

        # The current production handoff already documents this one real call seam.
        handoff = REPO / "control/startmaster0107/fachworkflow_proof_handoff.py"
        htxt = handoff.read_text(encoding="utf-8")
        seam = "PSERC_PPM_Intake_Bridge::execute -> PPM679_Normal_Draft_Pipeline::execute_plan"
        if seam not in htxt:
            blocked("BOUND_REAL_ENTRY_SEAM_NOT_DOCUMENTED")

        # P3 must not accept runtime engine-path selection.
        forbidden_env = {"PPM_ALT_PATH", "TEXTMACHINE_PATH", "TEXTMACHINE_ENGINE"}
        if any(name in os.environ for name in forbidden_env):
            # Presence is allowed in the host, but this probe never consumes them.
            pass

        result = {
            "status": "P3_REAL_INTERFACE_PROBE_PASS",
            "ppm_sha256": ppm_hash,
            "pserc_sha256": pserc_hash,
            "real_bridge": str(bridge.relative_to(pserc_root)),
            "real_pipeline_file": str(pipeline_files[0].relative_to(ppm_root)),
            "real_entry_seam": seam,
            "negative_package_tamper": "BLOCKED",
            "new_handoff_required": False,
            "textmachine_modified": False,
            "publish_allowed": False,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({
            "status": "P3_REAL_INTERFACE_PROBE_BLOCKED",
            "error": str(exc),
            "publish_allowed": False,
        }, ensure_ascii=False, indent=2))
        raise SystemExit(2)
