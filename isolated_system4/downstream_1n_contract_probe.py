from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAT_PATH = REPO / "control/startmaster0107/chat_delivery_payload.py"
FINAL_PATH = REPO / "control/startmaster0107/GITHUB_FINAL_RELEASE.py"
STEP107008 = REPO / "control/startmaster0107/STEP_107008_FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH.json"
ENDSTEMPEL_GATE = REPO / "control/startmaster0107/ENDSTEMPEL_HANDOFF_GATE.py"
ENDSTEMPEL_WORKFLOW = REPO / ".github/workflows/pferde-atelier-endstempel.yml"


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


def build_fixture(root: Path, count: int) -> tuple[str, str, str, dict]:
    if count < 1:
        raise ValueError("count")
    batch = hraw(("batch-" + str(count)).encode())
    release_dir = root / ".pferde-release" / batch
    source_dir = root / "control/startmaster0107/recovery_sources" / batch
    release_dir.mkdir(parents=True, exist_ok=True)
    source_dir.mkdir(parents=True, exist_ok=True)

    release_items = []
    plan_items = []
    outputs = []
    source_items = []
    for i in range(count):
        slot = hraw((f"slot-{count}-{i}").encode())
        cid = hraw((f"cid-{count}-{i}").encode())
        body = f"<p>System4A downstream fixture {count}/{i}</p>"
        raw = body.encode("utf-8")
        digest = hraw(raw)
        name = f"ARTICLE_{slot}.md"
        released_ref = f".pferde-release/{batch}/{name}"
        source_ref = f"control/startmaster0107/recovery_sources/{batch}/{name}"
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
    final_ref = f".pferde-release/{batch}/{final_name}"
    (release_dir / final_name).write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    receipt = {
        "contract": "PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2",
        "status": "OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED",
        "batch_sha256": batch,
        "outputs": outputs,
        "publish_allowed": False,
    }
    receipt_ref = f".pferde-release/{batch}/RELEASE_RECEIPT.json"
    (release_dir / "RELEASE_RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    import_ref = f"control/startmaster0107/recovery_sources/{batch}/PSERC_IMPORT_ENVELOPE.json"
    import_raw = canon(package)
    (source_dir / "PSERC_IMPORT_ENVELOPE.json").write_bytes(import_raw)
    source = {
        "contract": "PFERDE_ATELIER_EXISTING_ARTICLE_RECOVERY_SOURCE_V1",
        "batch_sha256": batch,
        "item_count": count,
        "import_envelope_ref": import_ref,
        "import_envelope_sha256": hraw(import_raw),
        "publish_allowed": False,
        "content_mutation_performed": False,
        "items": source_items,
    }
    source_ref = f"control/startmaster0107/recovery_sources/{batch}/MANIFEST.json"
    (source_dir / "MANIFEST.json").write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return receipt_ref, final_ref, source_ref, source


def exercise_count(count: int) -> None:
    with tempfile.TemporaryDirectory(prefix=f"system4a-downstream-{count}-") as td:
        root = Path(td)
        receipt_ref, final_ref, source_ref, _ = build_fixture(root, count)

        chat = load_module(CHAT_PATH, f"chat_delivery_{count}")
        chat.REPO = root
        envelope = chat.build(receipt_ref, final_ref)
        if envelope.get("article_count") != count:
            raise AssertionError(f"CHAT_COUNT_MISMATCH:{count}:{envelope.get('article_count')}")

        final = load_module(FINAL_PATH, f"github_final_{count}")
        final.REPO = root
        final.trusted_identity = lambda: {"signing_key_id": "test-key", "signing_public_key_sha256": "0" * 64, "public_key_b64": "AA=="}
        final.call_signer = lambda manifest_sha256, batch, source_sha256, n: {"signing_key_id": "test-key", "signing_public_key_sha256": "0" * 64, "public_key_b64": "AA==", "signature_b64": "AA=="}
        final.verify_sig = lambda *args, **kwargs: None
        result = final.finalize(source_ref)
        if result.get("article_count") != count:
            raise AssertionError(f"FINAL_COUNT_MISMATCH:{count}:{result.get('article_count')}")


def negative_source_count_mismatch() -> None:
    with tempfile.TemporaryDirectory(prefix="system4a-downstream-negative-") as td:
        root = Path(td)
        _, _, source_ref, source = build_fixture(root, 3)
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
        _, _, source_ref, source = build_fixture(root, 1)
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


def main() -> int:
    contract_source_guards()
    exercise_count(1)
    exercise_count(3)
    exercise_count(25)
    exercise_count(1000)
    negative_source_count_mismatch()
    negative_zero_count()
    print("SYSTEM4A_DOWNSTREAM_1N_CONTRACT_PROBE_OK")
    print("POSITIVE_COUNTS=1,3,25,1000")
    print("NEGATIVE_COUNT_MISMATCH=BLOCKED")
    print("NEGATIVE_ZERO_COUNT=BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
