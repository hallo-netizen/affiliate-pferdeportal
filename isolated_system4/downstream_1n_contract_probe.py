from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import os
import shutil
import tempfile
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

REPO = Path(__file__).resolve().parent.parent
CHAT_PATH = REPO / "control/startmaster0107/chat_delivery_payload.py"
FINAL_PATH = REPO / "control/startmaster0107/GITHUB_FINAL_RELEASE.py"
OUTPUT_GATE_PATH = REPO / "control/output-quarantine/output_release_gate.py"
STEP107008 = REPO / "control/startmaster0107/STEP_107008_FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH.json"
ENDSTEMPEL_GATE = REPO / "control/startmaster0107/ENDSTEMPEL_HANDOFF_GATE.py"
ENDSTEMPEL_WORKFLOW = REPO / ".github/workflows/pferde-atelier-endstempel.yml"
OUTPUT_DIR = Path(os.environ.get("SYSTEM4_ACCEPTANCE_OUTPUT_DIR", "/tmp/system4-acceptance-output"))


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("MODULE_LOAD_FAILED:" + str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def canon(obj: object) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def hraw(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(obj: object) -> str:
    return hraw(canon(obj))


def release_identity(batch: str, worker_receipt_sha256: str) -> str:
    return stable({
        "contract": "PFERDE_ATELIER_OUTPUT_RELEASE_IDENTITY_V1",
        "batch_sha256": batch,
        "worker_receipt_sha256": worker_receipt_sha256,
    })


def build_fixture(root: Path, count: int, run_label: str = "run-a") -> tuple[str, str, str, dict]:
    if count < 1:
        raise ValueError("count")
    batch = hraw(("batch-" + str(count)).encode())
    worker_receipt_sha = hraw(("worker-receipt-" + run_label).encode())
    release_id = release_identity(batch, worker_receipt_sha)
    release_dir = root / ".pferde-release" / release_id
    source_dir = root / "control/startmaster0107/recovery_sources" / release_id
    release_dir.mkdir(parents=True, exist_ok=True)
    source_dir.mkdir(parents=True, exist_ok=True)

    release_items = []
    plan_items = []
    outputs = []
    source_items = []
    for i in range(count):
        slot = hraw((f"slot-{count}-{i}").encode())
        cid = hraw((f"cid-{count}-{i}").encode())
        body = f"<p>System4A downstream fixture {count}/{i} {run_label}</p>"
        raw = body.encode("utf-8")
        digest = hraw(raw)
        name = f"ARTICLE_{slot}.md"
        released_ref = f".pferde-release/{release_id}/{name}"
        source_ref = f"control/startmaster0107/recovery_sources/{release_id}/{name}"
        (release_dir / name).write_bytes(raw)
        (source_dir / name).write_bytes(raw)
        release_items.append({"plan_slot": slot, "canonical_article_id": cid})
        plan_items.append({"canonical_article_id": cid, "canonical_article": {"body_html": body}})
        outputs.append({"source_ref": source_ref, "released_ref": released_ref, "sha256": digest})
        source_items.append({"ref": source_ref, "sha256": digest, "plan_slot": slot})

    fact_pack = {"contract": "TEST_FACT_PACK", "items": []}
    production_plan = {"contract": "production_plan_v4", "items": plan_items}
    workflow_release = {
        "contract": "WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED",
        "status": "PASS",
        "wordpress_write_performed": False,
        "exact_five_batch_sha256": batch,
        "items": release_items,
    }
    package = {
        "contract": "PSERC_APPROVED_PRODUCTION_PACKAGE_V1",
        "source": "DOWNSTREAM_1N_TEST",
        "fact_pack_bundle": fact_pack,
        "fact_pack_bundle_sha256": stable(fact_pack),
        "production_plan": production_plan,
        "production_plan_sha256": stable(production_plan),
        "workflow_release": workflow_release,
        "workflow_release_sha256": stable(workflow_release),
    }
    package["package_id"] = stable({
        "contract": package["contract"],
        "fact_pack_bundle_sha256": package["fact_pack_bundle_sha256"],
        "production_plan_sha256": package["production_plan_sha256"],
        "workflow_release_sha256": package["workflow_release_sha256"],
    })
    package["package_payload_sha256"] = stable(package)

    final_name = "GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json"
    final_ref = f".pferde-release/{release_id}/{final_name}"
    (release_dir / final_name).write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    receipt = {
        "contract": "PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2",
        "status": "OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED",
        "batch_sha256": batch,
        "release_identity_sha256": release_id,
        "worker_receipt_sha256": worker_receipt_sha,
        "outputs": outputs,
        "publish_allowed": False,
    }
    receipt_ref = f".pferde-release/{release_id}/RELEASE_RECEIPT.json"
    (release_dir / "RELEASE_RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    import_ref = f"control/startmaster0107/recovery_sources/{release_id}/PSERC_IMPORT_ENVELOPE.json"
    import_raw = canon(package)
    (source_dir / "PSERC_IMPORT_ENVELOPE.json").write_bytes(import_raw)
    source = {
        "contract": "PFERDE_ATELIER_EXISTING_ARTICLE_RECOVERY_SOURCE_V1",
        "batch_sha256": batch,
        "release_identity_sha256": release_id,
        "item_count": count,
        "import_envelope_ref": import_ref,
        "import_envelope_sha256": hraw(import_raw),
        "publish_allowed": False,
        "content_mutation_performed": False,
        "items": source_items,
    }
    source_ref = f"control/startmaster0107/recovery_sources/{release_id}/MANIFEST.json"
    (source_dir / "MANIFEST.json").write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return receipt_ref, final_ref, source_ref, source


def real_signed_finalize(root: Path, source_ref: str, module_name: str) -> tuple[dict, Path]:
    final = load_module(FINAL_PATH, module_name)
    final.REPO = root
    private = Ed25519PrivateKey.generate()
    public = private.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    public_b64 = base64.b64encode(public).decode("ascii")
    public_sha = hashlib.sha256(public).hexdigest()
    key_id = "simulation-" + public_sha[:16]
    identity = {
        "signing_key_id": key_id,
        "signing_public_key_sha256": public_sha,
        "public_key_b64": public_b64,
    }
    final.trusted_identity = lambda: dict(identity)

    def signer(manifest_sha256: str, batch: str, source_sha256: str, n: int):
        return {
            **identity,
            "signature_b64": base64.b64encode(private.sign(manifest_sha256.encode("ascii"))).decode("ascii"),
        }

    final.call_signer = signer
    result = final.finalize(source_ref)
    path = root / result["final_ref"]
    package = json.loads(path.read_text(encoding="utf-8"))
    manifest = package["article_manifest"]
    if package.get("release_identity_sha256") != result.get("release_identity_sha256"):
        raise AssertionError("SIGNED_RELEASE_IDENTITY_MISMATCH")
    if manifest.get("release_identity_sha256") != result.get("release_identity_sha256"):
        raise AssertionError("SIGNED_MANIFEST_RELEASE_IDENTITY_MISMATCH")
    if package.get("batch_sha256") != result.get("content_batch_sha256"):
        raise AssertionError("SIGNED_CONTENT_BATCH_MISMATCH")
    if result.get("batch_sha256") != result.get("release_identity_sha256"):
        raise AssertionError("LEGACY_WORKFLOW_TRANSPORT_IDENTITY_MISMATCH")
    return result, path


def exercise_count(count: int) -> dict:
    with tempfile.TemporaryDirectory(prefix=f"system4a-downstream-{count}-") as td:
        root = Path(td)
        receipt_ref, final_ref, source_ref, source = build_fixture(root, count, f"count-{count}")

        chat = load_module(CHAT_PATH, f"chat_delivery_{count}")
        chat.REPO = root
        envelope = chat.build(receipt_ref, final_ref)
        if envelope.get("article_count") != count:
            raise AssertionError(f"CHAT_COUNT_MISMATCH:{count}:{envelope.get('article_count')}")
        if envelope.get("release_identity_sha256") != source["release_identity_sha256"]:
            raise AssertionError("CHAT_RELEASE_IDENTITY_MISMATCH")

        result, signed_path = real_signed_finalize(root, source_ref, f"github_final_{count}")
        if result.get("article_count") != count:
            raise AssertionError(f"FINAL_COUNT_MISMATCH:{count}:{result.get('article_count')}")
        if result.get("content_batch_sha256") != source["batch_sha256"]:
            raise AssertionError("FINAL_LOGICAL_BATCH_CHANGED")
        if result.get("release_identity_sha256") != source["release_identity_sha256"]:
            raise AssertionError("FINAL_RELEASE_IDENTITY_CHANGED")

        if count in {1, 3}:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            dst = OUTPUT_DIR / f"PRECODEX_SIGNED_ENDSTEMPEL_SIMULATION_{count}_ARTICLE.json"
            shutil.copyfile(signed_path, dst)
            if hraw(dst.read_bytes()) != result["final_sha256"]:
                raise AssertionError("PARENT_CHAT_COPY_HASH_MISMATCH")
        return {
            "batch_sha256": source["batch_sha256"],
            "release_identity_sha256": source["release_identity_sha256"],
            "signed_sha256": result["final_sha256"],
        }


def positive_same_batch_two_fresh_releases() -> None:
    with tempfile.TemporaryDirectory(prefix="system4a-release-identity-") as td:
        root = Path(td)
        _, _, source_a, data_a = build_fixture(root, 3, "fresh-a")
        _, _, source_b, data_b = build_fixture(root, 3, "fresh-b")
        if data_a["batch_sha256"] != data_b["batch_sha256"]:
            raise AssertionError("LOGICAL_BATCH_DRIFT")
        if data_a["release_identity_sha256"] == data_b["release_identity_sha256"]:
            raise AssertionError("RELEASE_IDENTITY_COLLISION")
        a, path_a = real_signed_finalize(root, source_a, "github_final_release_a")
        b, path_b = real_signed_finalize(root, source_b, "github_final_release_b")
        if path_a == path_b or not path_a.is_file() or not path_b.is_file():
            raise AssertionError("SIGNED_FINAL_RELEASE_COLLISION")
        if a["content_batch_sha256"] != b["content_batch_sha256"]:
            raise AssertionError("SAME_BATCH_NOT_PRESERVED")
        if a["release_identity_sha256"] == b["release_identity_sha256"]:
            raise AssertionError("FRESH_RELEASE_IDENTITY_NOT_UNIQUE")


def negative_release_identity_tamper() -> None:
    with tempfile.TemporaryDirectory(prefix="system4a-release-negative-") as td:
        root = Path(td)
        _, _, source_ref, source = build_fixture(root, 1, "tamper")
        source["release_identity_sha256"] = "0" * 64
        p = root / source_ref
        p.write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        final = load_module(FINAL_PATH, "github_final_release_negative")
        final.REPO = root
        try:
            final.load_source(source_ref)
        except Exception:
            return
        raise AssertionError("NEGATIVE_RELEASE_IDENTITY_TAMPER_NOT_BLOCKED")


def negative_source_count_mismatch() -> None:
    with tempfile.TemporaryDirectory(prefix="system4a-downstream-negative-") as td:
        root = Path(td)
        _, _, source_ref, source = build_fixture(root, 3, "count-negative")
        source["item_count"] = 2
        p = root / source_ref
        p.write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        final = load_module(FINAL_PATH, "github_final_negative")
        final.REPO = root
        try:
            final.snapshot(*final.load_source(source_ref))
        except Exception:
            return
        raise AssertionError("NEGATIVE_SOURCE_COUNT_MISMATCH_NOT_BLOCKED")


def negative_zero_count() -> None:
    with tempfile.TemporaryDirectory(prefix="system4a-downstream-zero-") as td:
        root = Path(td)
        _, _, source_ref, source = build_fixture(root, 1, "zero-negative")
        source["item_count"] = 0
        p = root / source_ref
        p.write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        final = load_module(FINAL_PATH, "github_final_zero")
        final.REPO = root
        try:
            final.load_source(source_ref)
        except Exception:
            return
        raise AssertionError("NEGATIVE_ZERO_COUNT_NOT_BLOCKED")


def contract_source_guards() -> None:
    step_text = STEP107008.read_text(encoding="utf-8")
    if "article_count=7" in step_text or "sieben finalen Artikel" in step_text or "sieben Artikel" in step_text:
        raise AssertionError("STEP107008_FIXED_SEVEN_STILL_ACTIVE")

    gate_text = ENDSTEMPEL_GATE.read_text(encoding="utf-8")
    workflow_text = ENDSTEMPEL_WORKFLOW.read_text(encoding="utf-8")
    forbidden = (
        "len(articles) != 7",
        '"article_count": 7',
        "req.get('article_count')!=7",
        "m.get('article_count')!=7",
        "len(m.get('articles') or [])!=7",
    )
    for token in forbidden:
        if token in gate_text or token in workflow_text:
            raise AssertionError("DOWNSTREAM_FIXED_SEVEN_STILL_ACTIVE:" + token)

    final_text = FINAL_PATH.read_text(encoding="utf-8")
    if "IMPORT_ENVELOPE_NAME" in final_text and "IMPORT_ENVELOPE_NAME =" not in final_text:
        raise AssertionError("GITHUB_FINAL_IMPORT_ENVELOPE_NAME_UNDEFINED")
    if "IMPORT_ENVELOPE_KEYS" in final_text and "IMPORT_ENVELOPE_KEYS =" not in final_text:
        raise AssertionError("GITHUB_FINAL_IMPORT_ENVELOPE_KEYS_UNDEFINED")
    if '"release_identity_sha256"' not in final_text:
        raise AssertionError("GITHUB_FINAL_RELEASE_IDENTITY_MISSING")

    output_gate = load_module(OUTPUT_GATE_PATH, "output_gate_release_identity_contract")
    batch = "a" * 64
    a = output_gate.release_identity(batch, "b" * 64)
    b = output_gate.release_identity(batch, "c" * 64)
    if a == b or a != output_gate.release_identity(batch, "b" * 64):
        raise AssertionError("OUTPUT_RELEASE_IDENTITY_NOT_DETERMINISTIC_UNIQUE")


def main() -> int:
    contract_source_guards()
    one = exercise_count(1)
    three = exercise_count(3)
    exercise_count(25)
    exercise_count(1000)
    positive_same_batch_two_fresh_releases()
    negative_release_identity_tamper()
    negative_source_count_mismatch()
    negative_zero_count()
    print("SYSTEM4A_DOWNSTREAM_1N_CONTRACT_PROBE_OK")
    print("POSITIVE_COUNTS=1,3,25,1000")
    print("SAME_LOGICAL_BATCH_TWO_FRESH_RELEASES=PASS")
    print("NEGATIVE_RELEASE_IDENTITY_TAMPER=BLOCKED")
    print("NEGATIVE_COUNT_MISMATCH=BLOCKED")
    print("NEGATIVE_ZERO_COUNT=BLOCKED")
    print("PARENT_CHAT_SIGNED_FILE_1_SHA256=" + one["signed_sha256"])
    print("PARENT_CHAT_SIGNED_FILE_3_SHA256=" + three["signed_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
