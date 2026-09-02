#!/usr/bin/env python3
from __future__ import annotations

import base64
import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FINALIZER = HERE / "ENDSTEMPEL_FINALIZER.py"
PHP_VERIFY = HERE / "ENDSTEMPEL_WORDPRESS_VERIFY.php"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("MODULE_LOAD_FAILED")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fsha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_fixture(root: Path):
    batch = "c" * 64
    rel = root / ".pferde-release" / batch
    rel.mkdir(parents=True)
    outputs = []
    originals = {}
    for i, body in enumerate(["Artikel eins\nOriginal.\n", "Artikel zwei\nOriginal.\n"]):
        slot = format(i + 1, "064x")
        name = f"ARTICLE_{slot}.md"
        p = rel / name
        p.write_bytes(body.encode("utf-8"))
        originals[name] = p.read_bytes()
        outputs.append({"source_ref": f"source/{name}", "released_ref": str(p.relative_to(root)), "sha256": fsha(p)})
    receipt = {
        "contract": "PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2",
        "status": "OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED",
        "startmaster": "STARTMASTER0107",
        "source_step_id": "RUN_NEW_ARTICLE_BATCH_NO_STOP",
        "source_sequence": 107007,
        "source_ticket_id": "ticket",
        "source_state_sha256": "a" * 64,
        "source_bundle_sha256": "b" * 64,
        "batch_sha256": batch,
        "worker_receipt_sha256": "d" * 64,
        "final_review_step_id": "FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH",
        "final_review_sequence": 107008,
        "final_review_ticket_id": "ticket-final",
        "final_review_receipt_sha256": "e" * 64,
        "main_head": "f" * 40,
        "outputs": outputs,
        "chat_execution_authority": "NONE",
        "chat_output_authority": "NONE",
        "domain_logic_authority": "NONE",
        "quality_authority": "NONE",
        "publish_allowed": False,
    }
    rp = rel / "RELEASE_RECEIPT.json"
    dump(rp, receipt)
    return batch, rel, rp, originals


def php_check(final_path: Path, trusted: dict, used: bool = False) -> tuple[int, str]:
    harness = final_path.parent / "_verify_harness.php"
    verifier = str(PHP_VERIFY).replace("\\", "\\\\").replace("'", "\\'")
    trusted_json = json.dumps(trusted, separators=(",", ":")).replace("\\", "\\\\").replace("'", "\\'")
    harness.write_text(
        "<?php\n"
        f"require '{verifier}';\n"
        f"$trusted=json_decode('{trusted_json}', true);\n"
        f"$used={'true' if used else 'false'};\n"
        "try { $r=pferde_endstempel_verify_before_write($argv[1],$trusted,function($b) use ($used){return $used;}); echo json_encode($r); exit(0); }"
        " catch(Throwable $e){ echo $e->getMessage(); exit(2);}\n",
        encoding="utf-8",
    )
    cp = subprocess.run(["php", str(harness), str(final_path)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    harness.unlink(missing_ok=True)
    return cp.returncode, cp.stdout + cp.stderr


def php_atomic_failure(final_path: Path, trusted: dict) -> tuple[int, str]:
    harness = final_path.parent / "_atomic_harness.php"
    verifier = str(PHP_VERIFY).replace("\\", "\\\\").replace("'", "\\'")
    trusted_json = json.dumps(trusted, separators=(",", ":")).replace("\\", "\\\\").replace("'", "\\'")
    harness.write_text(
        "<?php\n"
        f"require '{verifier}';\n"
        f"$trusted=json_decode('{trusted_json}', true);\n"
        "$pending=[];$committed=[];$rolled=false;\n"
        "try { pferde_endstempel_atomic_import($argv[1],$trusted,function($b){return false;},"
        "function(){},"
        "function($v) use (&$pending){$pending[]='first'; throw new RuntimeException('SIMULATED_IMPORT_FAIL');},"
        "function($b){},"
        "function() use (&$pending,&$committed){$committed=$pending;},"
        "function() use (&$pending,&$rolled){$pending=[];$rolled=true;}); } catch(Throwable $e) {}\n"
        "if(count($pending)===0 && count($committed)===0 && $rolled){echo 'ZERO_COMMITTED_WRITES';exit(0);} echo 'PARTIAL_IMPORT';exit(2);\n",
        encoding="utf-8",
    )
    cp = subprocess.run(["php", str(harness), str(final_path)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    harness.unlink(missing_ok=True)
    return cp.returncode, cp.stdout + cp.stderr


def main() -> int:
    if shutil.which("php") is None:
        print(json.dumps({"ok": False, "status": "HARD_BLOCK", "reason": "PHP_RUNTIME_MISSING"}))
        return 2
    end = load_module(FINALIZER, "endstempel_finalizer_test")
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        batch, release_dir, receipt_path, originals = make_fixture(root)
        priv = Ed25519PrivateKey.generate()
        pub = priv.public_key().public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
        pub_b64 = base64.b64encode(pub).decode("ascii")
        pub_sha = hashlib.sha256(pub).hexdigest()
        key_id = "endstamp-test-" + pub_sha[:16]

        def signer(h: str, b: str, r: str, n: int):
            assert b == batch and n == 2 and len(r) == 64
            return {
                "signing_key_id": key_id,
                "signing_public_key_sha256": pub_sha,
                "public_key_b64": pub_b64,
                "signature_b64": base64.b64encode(priv.sign(h.encode("ascii"))).decode("ascii"),
            }

        result = end.finalize(root, str(receipt_path.relative_to(root)), signer)
        assert result["status"] == "ENDSTEMPEL_FINAL_PASS"
        final_path = root / result["final_ref"]
        for name, raw in originals.items():
            assert (release_dir / name).read_bytes() == raw
        trusted = {key_id: {"sha256": pub_sha, "public_key_b64": pub_b64}}
        rc, out = php_check(final_path, trusted)
        assert rc == 0, out

        first = release_dir / sorted(originals)[0]
        original = first.read_bytes()
        first.write_bytes(original + b"X")
        rc, _ = php_check(final_path, trusted)
        assert rc != 0
        first.write_bytes(original)

        pkg = json.loads(final_path.read_text(encoding="utf-8"))
        bad = copy.deepcopy(pkg)
        bad["batch_sha256"] = "d" * 64
        bad_copy = dict(bad); bad_copy.pop("package_payload_sha256", None)
        bad["package_payload_sha256"] = end.stable_hash(bad_copy)
        bad_path = release_dir / "BAD_BATCH.json"; dump(bad_path, bad)
        rc, _ = php_check(bad_path, trusted)
        assert rc != 0

        second = release_dir / sorted(originals)[1]
        saved = second.read_bytes(); second.unlink()
        rc, _ = php_check(final_path, trusted)
        assert rc != 0
        second.write_bytes(saved)

        extra = release_dir / ("ARTICLE_" + "f" * 64 + ".md")
        extra.write_text("extra", encoding="utf-8")
        rc, _ = php_check(final_path, trusted)
        assert rc != 0
        extra.unlink()

        bad = copy.deepcopy(pkg)
        bad["signature_b64"] = base64.b64encode(b"0" * 64).decode("ascii")
        bad_copy = dict(bad); bad_copy.pop("package_payload_sha256", None)
        bad["package_payload_sha256"] = end.stable_hash(bad_copy)
        bad_path = release_dir / "BAD_SIG.json"; dump(bad_path, bad)
        rc, _ = php_check(bad_path, trusted)
        assert rc != 0

        rc, _ = php_check(final_path, trusted, used=True)
        assert rc != 0

        rc, out = php_atomic_failure(final_path, trusted)
        assert rc == 0 and "ZERO_COMMITTED_WRITES" in out, out

        bad_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        bad_receipt["final_review_sequence"] = 107007
        bad_rp = release_dir / "BAD_RECEIPT.json"; dump(bad_rp, bad_receipt)
        try:
            end.build_manifest(root, str(bad_rp.relative_to(root)))
            raise AssertionError("BAD_RECEIPT_ACCEPTED")
        except end.Blocked:
            pass

    print(json.dumps({
        "ok": True,
        "status": "ENDSTEMPEL_FIXED_TESTS_PASS",
        "positive": True,
        "negative": True,
        "article_mutation_performed": False,
        "publish_allowed": False,
        "tests": [
            "original_pass",
            "one_character_changed_block",
            "wrong_batch_block",
            "missing_file_block",
            "additional_file_block",
            "wrong_signature_block",
            "replay_block",
            "import_failure_zero_committed_writes"
        ]
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
