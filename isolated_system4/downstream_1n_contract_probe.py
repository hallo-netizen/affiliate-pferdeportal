from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAT_PATH = REPO / "control/startmaster0107/chat_delivery_payload.py"
FINAL_PATH = REPO / "control/startmaster0107/GITHUB_FINAL_RELEASE.py"
OUTPUT_RELEASE_GATE = REPO / "control/output-quarantine/output_release_gate.py"
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


def build_fixture(root: Path, count: int, generation: int = 1) -> tuple[str, str, str, dict]:
    if count < 1:
        raise ValueError("count")
    if isinstance(generation, bool) or not isinstance(generation, int) or generation < 1:
        raise ValueError("generation")
    batch = hraw(("batch-" + str(count)).encode())
    run_dir = f"generation-{generation:06d}"
    release_dir = root / ".pferde-release" / batch / run_dir
    source_dir = root / "control/startmaster0107/recovery_sources" / batch / run_dir
    release_dir.mkdir(parents=True, exist_ok=True)
    source_dir.mkdir(parents=True, exist_ok=True)

    release_items = []
    plan_items = []
    outputs = []
    source_items = []
    for i in range(count):
        slot = hraw((f"slot-{count}-{i}").encode())
        cid = hraw((f"cid-{count}-{i}").encode())
        body = f"<p>System4A downstream fixture {count}/{i}/generation-{generation:06d}</p>"
        raw = body.encode("utf-8")
        digest = hraw(raw)
        name = f"ARTICLE_{slot}.md"
        released_ref = f".pferde-release/{batch}/{run_dir}/{name}"
        source_ref = f"control/startmaster0107/recovery_sources/{batch}/{run_dir}/{name}"
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
    final_ref = f".pferde-release/{batch}/{run_dir}/{final_name}"
    (release_dir / final_name).write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    receipt = {
        "contract": "PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2",
        "status": "OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED",
        "batch_sha256": batch,
        "runtime_generation": generation,
        "outputs": outputs,
        "publish_allowed": False,
    }
    receipt_ref = f".pferde-release/{batch}/{run_dir}/RELEASE_RECEIPT.json"
    (release_dir / "RELEASE_RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    import_ref = f"control/startmaster0107/recovery_sources/{batch}/{run_dir}/PSERC_IMPORT_ENVELOPE.json"
    import_raw = canon(package)
    (source_dir / "PSERC_IMPORT_ENVELOPE.json").write_bytes(import_raw)
    source = {
        "contract": "PFERDE_ATELIER_EXISTING_ARTICLE_RECOVERY_SOURCE_V1",
        "batch_sha256": batch,
        "runtime_generation": generation,
        "item_count": count,
        "import_envelope_ref": import_ref,
        "import_envelope_sha256": hraw(import_raw),
        "publish_allowed": False,
        "content_mutation_performed": False,
        "items": source_items,
    }
    source_ref = f"control/startmaster0107/recovery_sources/{batch}/{run_dir}/MANIFEST.json"
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
        if envelope.get("runtime_generation") != 1:
            raise AssertionError(f"CHAT_GENERATION_MISMATCH:{count}:{envelope.get('runtime_generation')}")

        final = load_module(FINAL_PATH, f"github_final_{count}")
        final.REPO = root
        final.trusted_identity = lambda: {"signing_key_id": "test-key", "signing_public_key_sha256": "0" * 64, "public_key_b64": "AA=="}
        final.call_signer = lambda manifest_sha256, batch, source_sha256, n: {"signing_key_id": "test-key", "signing_public_key_sha256": "0" * 64, "public_key_b64": "AA==", "signature_b64": "AA=="}
        final.verify_sig = lambda *args, **kwargs: None
        result = final.finalize(source_ref)
        if result.get("article_count") != count:
            raise AssertionError(f"FINAL_COUNT_MISMATCH:{count}:{result.get('article_count')}")
        if result.get("runtime_generation") != 1:
            raise AssertionError(f"FINAL_GENERATION_MISMATCH:{count}:{result.get('runtime_generation')}")


def generation_identity_probe() -> None:
    with tempfile.TemporaryDirectory(prefix="system4a-generation-identity-") as td:
        root = Path(td)
        first_refs = build_fixture(root, 3, 1)
        second_refs = build_fixture(root, 3, 2)
        if first_refs[0] == second_refs[0] or first_refs[2] == second_refs[2]:
            raise AssertionError("GENERATION_IDENTITY_COLLISION")
        chat = load_module(CHAT_PATH, "chat_delivery_generation_identity")
        chat.REPO = root
        first = chat.build(first_refs[0], first_refs[1])
        second = chat.build(second_refs[0], second_refs[1])
        if first.get("batch_sha256") != second.get("batch_sha256"):
            raise AssertionError("GENERATION_PROBE_BATCH_CHANGED")
        if (first.get("runtime_generation"), second.get("runtime_generation")) != (1, 2):
            raise AssertionError("GENERATION_PROBE_NOT_DISTINCT")

        final = load_module(FINAL_PATH, "github_final_generation_identity")
        final.REPO = root
        final.trusted_identity = lambda: {"signing_key_id": "test-key", "signing_public_key_sha256": "0" * 64, "public_key_b64": "AA=="}
        final.call_signer = lambda manifest_sha256, batch, source_sha256, n: {"signing_key_id": "test-key", "signing_public_key_sha256": "0" * 64, "public_key_b64": "AA==", "signature_b64": "AA=="}
        final.verify_sig = lambda *args, **kwargs: None
        first_final = final.finalize(first_refs[2])
        second_final = final.finalize(second_refs[2])
        if first_final.get("batch_sha256") != second_final.get("batch_sha256"):
            raise AssertionError("FINAL_GENERATION_PROBE_BATCH_CHANGED")
        if (first_final.get("runtime_generation"), second_final.get("runtime_generation")) != (1, 2):
            raise AssertionError("FINAL_GENERATION_PROBE_NOT_DISTINCT")
        if first_final.get("final_ref") == second_final.get("final_ref"):
            raise AssertionError("FINAL_GENERATION_OUTPUT_COLLISION")
        try:
            final.finalize(first_refs[2])
        except Exception as exc:
            if "REPLAY_BLOCKED" not in str(exc):
                raise
        else:
            raise AssertionError("SAME_GENERATION_REPLAY_NOT_BLOCKED")


def negative_generation_path_mismatch() -> None:
    with tempfile.TemporaryDirectory(prefix="system4a-generation-negative-") as td:
        root = Path(td)
        _, _, source_ref, source = build_fixture(root, 3, 1)
        source["runtime_generation"] = 2
        p = root / source_ref
        p.write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        final = load_module(FINAL_PATH, "github_final_generation_negative")
        final.REPO = root
        try:
            final.load_source(source_ref)
        except Exception:
            return
        raise AssertionError("GENERATION_PATH_MISMATCH_NOT_BLOCKED")


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

    output_gate_text = OUTPUT_RELEASE_GATE.read_text(encoding="utf-8")
    for marker in (
        '"runtime_generation": generation',
        'destination = release_root / prepared["batch_sha256"] / generation_name(generation)',
        'durable_release_archive" / prepared["batch_sha256"] / generation_name(generation)',
        'VISIBLE_RELEASE_RUNTIME_GENERATION_DRIFT',
    ):
        if marker not in output_gate_text:
            raise AssertionError("OUTPUT_RELEASE_GENERATION_BINDING_MISSING:" + marker)

    chat_text = CHAT_PATH.read_text(encoding="utf-8")
    if 'recovery_sources/{batch}/{run_dir}' not in chat_text or '"runtime_generation": generation' not in chat_text:
        raise AssertionError("CHAT_DELIVERY_GENERATION_BINDING_MISSING")

    if 'generation-[0-9]{6}/MANIFEST' not in workflow_text:
        raise AssertionError("ENDSTEMPEL_WORKFLOW_GENERATION_SOURCE_MISSING")
    if 'tag="endstempel-$BATCH_SHA256-g$generation_padded"' not in workflow_text:
        raise AssertionError("ENDSTEMPEL_WORKFLOW_GENERATION_TAG_MISSING")

    final_text = FINAL_PATH.read_text(encoding="utf-8")
    if "IMPORT_ENVELOPE_NAME" in final_text and "IMPORT_ENVELOPE_NAME =" not in final_text:
        raise AssertionError("GITHUB_FINAL_IMPORT_ENVELOPE_NAME_UNDEFINED")
    if "IMPORT_ENVELOPE_KEYS" in final_text and "IMPORT_ENVELOPE_KEYS =" not in final_text:
        raise AssertionError("GITHUB_FINAL_IMPORT_ENVELOPE_KEYS_UNDEFINED")
    for marker in (
        'generation_name(generation) / "MANIFEST.json"',
        '"runtime_generation": generation',
        '".pferde-final" / batch / generation_name(generation)',
    ):
        if marker not in final_text:
            raise AssertionError("GITHUB_FINAL_GENERATION_BINDING_MISSING:" + marker)


def main() -> int:
    contract_source_guards()
    exercise_count(1)
    exercise_count(3)
    exercise_count(25)
    exercise_count(1000)
    generation_identity_probe()
    negative_generation_path_mismatch()
    negative_source_count_mismatch()
    negative_zero_count()
    print("SYSTEM4A_DOWNSTREAM_1N_CONTRACT_PROBE_OK")
    print("POSITIVE_COUNTS=1,3,25,1000")
    print("NEGATIVE_COUNT_MISMATCH=BLOCKED")
    print("GENERATION_IDENTITY=SAME_BATCH_DISTINCT_RUNS_PASS")
    print("SAME_GENERATION_REPLAY=BLOCKED")
    print("NEGATIVE_GENERATION_PATH_MISMATCH=BLOCKED")
    print("NEGATIVE_ZERO_COUNT=BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
