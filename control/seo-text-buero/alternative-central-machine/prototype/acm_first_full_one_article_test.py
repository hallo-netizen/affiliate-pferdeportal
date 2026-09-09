#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

from p7_release_boundary import Blocked, build_release, canon, verify_for_import, write_release
from p22_signed_normal_draft_integration import WRITE_PHP
from p40_handoff_controller import _load_exact_handoff
from p47_existing_handoff_public_prewrite import BUILD_HANDOFF_PHP, PUBLIC_PREWRITE_PHP, run_json

REPO = Path(__file__).resolve().parents[4]
PPM = REPO / "control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        ppm_out = root / "ppm"
        ppm_out.mkdir()
        with zipfile.ZipFile(PPM) as z:
            z.extractall(ppm_out)
        ppm = ppm_out / "portal-production-machine"

        handoff = root / "FACHWORKFLOW_HANDOFF_REQUEST.json"
        build_php = ppm / "acm-full-build-handoff.php"
        prewrite_php = ppm / "acm-full-public-prewrite.php"
        write_php = ppm / "acm-full-write.php"
        build_php.write_text(BUILD_HANDOFF_PHP, encoding="utf-8")
        prewrite_php.write_text(PUBLIC_PREWRITE_PHP, encoding="utf-8")
        write_php.write_text(WRITE_PHP, encoding="utf-8")

        # 1. Existing single handoff is the only production input.
        ready = run_json(["php", str(build_php), str(handoff)], ppm)
        if ready.get("status") != "P47_HANDOFF_FIXTURE_READY":
            raise RuntimeError("FULL_TEST_HANDOFF_NOT_READY")
        request = _load_exact_handoff(handoff)
        handoff_before = handoff.read_bytes()

        # 2. Existing public PPM path to prepare(), no WordPress write.
        prewrite = run_json(["php", str(prewrite_php), str(handoff)], ppm)
        if prewrite.get("status") != "P47_EXISTING_HANDOFF_PUBLIC_PREWRITE_PASS":
            raise RuntimeError("FULL_TEST_PREWRITE_FAILED")
        if prewrite.get("prepare_no_write") is not True or prewrite.get("identity_bound") is not True:
            raise RuntimeError("FULL_TEST_PREWRITE_INVARIANT_FAILED")
        if handoff.read_bytes() != handoff_before:
            raise RuntimeError("FULL_TEST_HANDOFF_MUTATED")

        prepared = prewrite.get("prepared")
        if not isinstance(prepared, dict) or not prepared.get("ok"):
            raise RuntimeError("FULL_TEST_PREPARED_MISSING")
        item_id = str(prepared.get("plan_item_key") or "")
        canonical_id = str(prepared.get("canonical_article_id") or "")
        if item_id != str(request["production_plan_item"].get("plan_item_key") or ""):
            raise RuntimeError("FULL_TEST_ITEM_ID_DRIFT")
        if canonical_id != str(request["canonical_article_id"]):
            raise RuntimeError("FULL_TEST_CANONICAL_ID_DRIFT")

        # 3. Existing external signature boundary.
        private = root / "private.pem"
        public = root / "public.pem"
        release_path = root / "release.json"
        signature = root / "release.sig"
        subprocess.run(
            ["openssl", "genpkey", "-algorithm", "Ed25519", "-out", str(private)],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        subprocess.run(
            ["openssl", "pkey", "-in", str(private), "-pubout", "-out", str(public)],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        release = build_release("ACM-FIRST-FULL-ONE-ARTICLE", item_id, prepared)
        write_release(release_path, release)
        subprocess.run(
            ["openssl", "pkeyutl", "-sign", "-inkey", str(private), "-rawin",
             "-in", str(release_path), "-out", str(signature)],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        verified = verify_for_import(release_path, signature, public)
        if verified.get("status") != "IMPORT_VERIFIED_NO_PUBLISH":
            raise RuntimeError("FULL_TEST_SIGNATURE_VERIFY_FAILED")

        signed_release = json.loads(release_path.read_text(encoding="utf-8"))
        signed_prepared = signed_release["payload"]
        if str(signed_prepared.get("canonical_article_id") or "") != canonical_id:
            raise RuntimeError("FULL_TEST_SIGNED_CANONICAL_DRIFT")
        prepared_path = root / "verified-signed-prepared.json"
        prepared_path.write_bytes(canon(signed_prepared))

        # 4. Existing draft writer + readback: exactly one draft, zero publish change.
        positive = run_json(["php", str(write_php), str(prepared_path)], ppm)
        if positive.get("status") != "P22_SIGNED_PREPARED_DRAFT_WRITTEN":
            raise RuntimeError("FULL_TEST_DRAFT_WRITE_FAILED")
        if positive.get("after_publish") != positive.get("before_publish"):
            raise RuntimeError("FULL_TEST_PUBLISH_CHANGED")
        if positive.get("after_draft") != positive.get("before_draft") + 1:
            raise RuntimeError("FULL_TEST_NOT_EXACTLY_ONE_DRAFT")
        if positive.get("snapshot_status") != "draft":
            raise RuntimeError("FULL_TEST_STATUS_NOT_DRAFT")
        if positive.get("readback_ok") is not True:
            raise RuntimeError("FULL_TEST_READBACK_FAILED")

        # 5. Negative: same signed release modified after signature must fail before any second write.
        tampered = copy.deepcopy(signed_release)
        tampered["payload"]["payload"]["content"] += " MANIPULIERT"
        release_path.write_bytes(canon(tampered))
        tamper_blocked = False
        try:
            verify_for_import(release_path, signature, public)
        except Blocked:
            tamper_blocked = True
        if not tamper_blocked:
            raise RuntimeError("FULL_TEST_TAMPER_NOT_BLOCKED")

        print(json.dumps({
            "status": "ACM_FIRST_FULL_ONE_ARTICLE_TEST_PASS",
            "input_truth": "FACHWORKFLOW_HANDOFF_REQUEST.json",
            "canonical_article_id": canonical_id,
            "plan_item_key": item_id,
            "prewrite_no_write": True,
            "external_signature_verified": True,
            "exactly_one_draft_written": True,
            "draft_readback_pass": True,
            "publish_count_unchanged": True,
            "post_signature_tamper_blocked": True,
            "second_write_after_tamper": False,
            "article_html": str(((prepared.get("payload") or {}).get("content")) or ""),
            "new_controller_used": False,
            "new_ppm_api_used": False,
            "publish_allowed": False
        }, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
