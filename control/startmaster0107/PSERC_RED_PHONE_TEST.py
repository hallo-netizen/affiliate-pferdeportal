#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RED = HERE / "PSERC_RED_PHONE.py"
FIXTURE_HASH = "2a7aa7028a00c48f88d6e09ee73a23e06dd803eedccdddd36811fac514b3f6e0"
FIXTURE_SIG = "HAqffBSB3k5iPBaWSdFZmJqZS+sLe6Q6dYv+gK22vNAPpVPv8QmrIui4uES/crzxvCmNGrrVl90ITP6Zuo+gBw=="


def load_red():
    spec = importlib.util.spec_from_file_location("red_phone_test_target", RED)
    if spec is None or spec.loader is None:
        raise AssertionError("RED_PHONE_TEST_IMPORT_FAILED")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


class Proc:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def expect_blocked(fn, needle):
    try:
        fn()
    except Exception as exc:
        if needle not in str(exc):
            raise AssertionError(f"EXPECTED {needle}, GOT {exc}") from exc
        return
    raise AssertionError("EXPECTED_BLOCKED:" + needle)


def receipt(repo: Path, *, status="OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED", batch=None, publish=False):
    batch = batch or "7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a"
    p = repo / "receipt.json"
    p.write_text(
        json.dumps(
            {
                "contract": "PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2",
                "status": status,
                "batch_sha256": batch,
                "publish_allowed": publish,
                "outputs": [{"released_ref": f"x{i}", "sha256": "0" * 64} for i in range(7)],
            }
        ),
        encoding="utf-8",
    )
    return p


def main() -> int:
    red = load_red()

    red.verify_signature(FIXTURE_HASH, FIXTURE_SIG)

    calls = []

    def good_runner(args, **kwargs):
        calls.append((args, kwargs))
        request = json.loads(kwargs["input"])
        assert request == {
            "contract": "PSERC_SIGN_REQUEST_V1",
            "signature_algorithm": "ED25519",
            "signing_key_id": red.PROD_KEY_ID,
            "signing_public_key_sha256": red.PROD_KEY_SHA256,
            "payload_sha256": FIXTURE_HASH,
        }
        return Proc(
            0,
            json.dumps(
                {
                    "signature_b64": FIXTURE_SIG,
                    "signing_key_id": red.PROD_KEY_ID,
                    "signing_public_key_sha256": red.PROD_KEY_SHA256,
                }
            ),
            "",
        )

    assert red.call_red_phone(FIXTURE_HASH, runner=good_runner, command="red-phone") == FIXTURE_SIG
    assert len(calls) == 1

    def fixture_sig_runner(args, **kwargs):
        return Proc(
            0,
            json.dumps(
                {
                    "signature_b64": FIXTURE_SIG,
                    "signing_key_id": red.PROD_KEY_ID,
                    "signing_public_key_sha256": red.PROD_KEY_SHA256,
                }
            ),
            "",
        )

    expect_blocked(
        lambda: red.call_red_phone("0" * 64, runner=fixture_sig_runner, command="red-phone"),
        "RED_PHONE_SIGNATURE_INVALID",
    )

    def wrong_sig_runner(args, **kwargs):
        return Proc(0, json.dumps({"signature_b64": "A" * 88}), "")

    expect_blocked(
        lambda: red.call_red_phone(FIXTURE_HASH, runner=wrong_sig_runner, command="red-phone"),
        "RED_PHONE_SIGNATURE",
    )

    def wrong_id_runner(args, **kwargs):
        return Proc(
            0,
            json.dumps(
                {
                    "signature_b64": FIXTURE_SIG,
                    "signing_key_id": "wrong",
                    "signing_public_key_sha256": red.PROD_KEY_SHA256,
                }
            ),
            "",
        )

    expect_blocked(
        lambda: red.call_red_phone(FIXTURE_HASH, runner=wrong_id_runner, command="red-phone"),
        "RED_PHONE_KEY_ID_MISMATCH",
    )

    def timeout_runner(args, **kwargs):
        raise subprocess.TimeoutExpired(args, kwargs.get("timeout", 20))

    expect_blocked(
        lambda: red.call_red_phone(FIXTURE_HASH, runner=timeout_runner, command="red-phone"),
        "RED_PHONE_TIMEOUT",
    )

    def unreachable_runner(args, **kwargs):
        raise OSError("no route")

    expect_blocked(
        lambda: red.call_red_phone(FIXTURE_HASH, runner=unreachable_runner, command="red-phone"),
        "RED_PHONE_UNREACHABLE",
    )

    fail_calls = []

    def failing_runner(args, **kwargs):
        fail_calls.append(1)
        return Proc(7, "", "fail")

    expect_blocked(
        lambda: red.call_red_phone(FIXTURE_HASH, runner=failing_runner, command="red-phone"),
        "RED_PHONE_SIGNER_FAILED",
    )
    assert len(fail_calls) == 1

    expect_blocked(
        lambda: red.call_red_phone(FIXTURE_HASH, runner=good_runner, command=""),
        "RED_PHONE_DIRECT_LINE_NOT_CONNECTED",
    )

    with tempfile.TemporaryDirectory() as td:
        repo = Path(td)
        p = receipt(repo)
        red.validate_107008_receipt(repo, p.name)
        p = receipt(repo, status="BLOCKED")
        expect_blocked(lambda: red.validate_107008_receipt(repo, p.name), "RED_PHONE_107008_PASS_REQUIRED")
        p = receipt(repo, batch="1" * 64)
        expect_blocked(lambda: red.validate_107008_receipt(repo, p.name), "RED_PHONE_BATCH_MISMATCH")
        p = receipt(repo, publish=True)
        expect_blocked(lambda: red.validate_107008_receipt(repo, p.name), "RED_PHONE_PUBLISH_MUST_REMAIN_FALSE")

    print(
        json.dumps(
            {
                "status": "SECTION_2_SAFETY_PASS",
                "positive": True,
                "negative": True,
                "production_public_key_fixture_verified": True,
                "single_call_only": True,
                "fallback_routes": 0,
                "publish_allowed": False,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
