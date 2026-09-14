#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SYSTEM4 = REPO / "isolated_system4"
SYSTEM4A = REPO / "isolated_system4a"

CONTRACT = "SYSTEM4A_CHAT_TO_FILE_FULL_ACCEPTANCE_V1"
POINT0_CONTRACT = "SYSTEM4_POINT0_SNAPSHOT_V1"
HANDOFF_CONTRACT = "SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2"

# This is the exact locally proven Point-0/Supervisor System-4 candidate.
# A remote/documentation head is NOT accepted as a substitute for these proven runtime bytes.
REQUIRED_PROVEN_RUNTIME = {
    "proof_head": "cd6c134a3ee27f4535ea91bfe6cc223a34c9eb25",
    "point0_snapshot.py": "4dab3cc58da04cf2d5d53f22bc7e837b3cca7c88",
    "supervisor.py": "0afb25204fe8cac1dc24912f638451842a68399b",
    "root_supervisor_bridge.py": "2c9e0ce6e22efee20ceedfef5e3ba37c044eeb2f",
    "worker_dispatch.py": "608627f4d9d1b09758e42fd7ece4690fe9761575",
    "codex_entry.py": "c74044a85e9da6de3e9af6472555306e8f6fb28c",
    "root_entry.py": "b533e8223351ef291be6b624bb803b9f888d5268",
}

KNOWN_LIVE_ESCAPE_CLASSES = [
    "wrong_or_missing_chat_trigger_binding",
    "wrong_runtime_bytes_or_partial_remote_transfer",
    "point0_missing_or_mutated",
    "legacy_root_entry_used_instead_of_start_point0",
    "root_snapshot_or_manifest_binding_missing",
    "supervisor_not_external_authority",
    "worker_private_path_inaccessible_cross_uid",
    "private_python_interpreter_leak",
    "worker_factory_signature_drift",
    "worker_exits_without_response",
    "worker_can_return_authority_fields",
    "research_not_bound_to_point0_sources",
    "facts_not_bound_to_accepted_research",
    "unknown_or_foreign_fact_id",
    "context_snapshot_mismatch",
    "prebound_quality_binding",
    "quality_binding_missing_at_ppm_rebind",
    "noncanonical_category",
    "wrong_or_missing_plan_slot",
    "wrong_internal_link_binding",
    "prebound_runtime_links",
    "missing_textmachine_authoring_binding",
    "repair_restarts_article_or_mutates_context",
    "languagetool_dependency_missing_or_wrong_hash",
    "languagetool_not_executed_through_fullcheck",
    "ppm_dependency_missing_or_wrong_hash",
    "ppm_not_actually_executed",
    "synthetic_or_pregenerated_checker_pass",
    "ppm_content_hash_not_final_article_hash",
    "required_table_or_design_contract_missing",
    "batch_drops_duplicates_or_reorders_articles",
    "batch_context_mismatch",
    "handoff_schema_or_canonical_bytes_mismatch",
    "inline_part_missing_duplicate_reordered_or_tampered",
    "parent_chat_reconstruction_not_byte_identical",
    "publish_allowed_not_false",
]

class AcceptanceBlocked(RuntimeError):
    pass


def require(ok: bool, code: str) -> None:
    if not ok:
        raise AcceptanceBlocked(code)


def git_blob(path: Path) -> str:
    cp = subprocess.run(
        ["git", "hash-object", str(path)], cwd=REPO,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
    )
    require(cp.returncode == 0, "RUNTIME_GIT_BLOB_UNAVAILABLE:" + path.name)
    return cp.stdout.strip()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_runtime_identity() -> dict[str, str]:
    actual: dict[str, str] = {}
    for name, expected in REQUIRED_PROVEN_RUNTIME.items():
        if name == "proof_head":
            continue
        path = SYSTEM4 / name
        require(path.is_file(), "CURRENT_RUNTIME_FILE_MISSING:" + name)
        blob = git_blob(path)
        actual[name] = blob
        require(blob == expected, "CURRENT_RUNTIME_IDENTITY_MISMATCH:" + name + ":" + blob + ":EXPECTED:" + expected)

    # controller.py changed in the proven candidate but its exact tested blob was never
    # atomically bound to the current remote branch. Until that transfer is completed and
    # a bound manifest is present, this gate MUST stop. This prevents another false green.
    manifest = SYSTEM4 / "CURRENT_PROVEN_RUNTIME_MANIFEST.json"
    require(manifest.is_file(), "CURRENT_PROVEN_RUNTIME_MANIFEST_MISSING")
    value = json.loads(manifest.read_text(encoding="utf-8"))
    require(value.get("contract") == "SYSTEM4_PROVEN_RUNTIME_MANIFEST_V1", "CURRENT_PROVEN_RUNTIME_MANIFEST_INVALID")
    require(value.get("proof_head") == REQUIRED_PROVEN_RUNTIME["proof_head"], "CURRENT_PROVEN_RUNTIME_PROOF_HEAD_MISMATCH")
    files = value.get("git_blobs")
    require(isinstance(files, dict) and files.get("controller.py"), "CURRENT_PROVEN_CONTROLLER_BINDING_MISSING")
    for name, expected in files.items():
        path = SYSTEM4 / name
        require(path.is_file(), "BOUND_RUNTIME_FILE_MISSING:" + name)
        require(git_blob(path) == expected, "BOUND_RUNTIME_FILE_MISMATCH:" + name)
    actual["controller.py"] = str(files["controller.py"])
    return actual


def load_trigger(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(value.get("contract") == CONTRACT, "CHAT_TRIGGER_CONTRACT_INVALID")
    count = value.get("article_count")
    require(isinstance(count, int) and 1 <= count <= 3, "CHAT_TRIGGER_ARTICLE_COUNT_MUST_BE_1_TO_3")
    require(value.get("publish_allowed") is False, "PUBLISH_ALLOWED_MUST_BE_FALSE")
    articles = value.get("articles")
    require(isinstance(articles, list) and len(articles) == count, "CHAT_TRIGGER_ARTICLE_COUNT_MISMATCH")
    for i, article in enumerate(articles):
        require(isinstance(article, dict), f"CHAT_TRIGGER_ARTICLE_INVALID:{i}")
        for field in ("article_type", "category", "plan_slot", "target_keyword", "title"):
            require(isinstance(article.get(field), str) and article[field].strip(), f"CHAT_TRIGGER_FIELD_MISSING:{i}:{field}")
        require(len(article["plan_slot"]) == 64, f"CHAT_TRIGGER_PLAN_SLOT_INVALID:{i}")
    return value


def run_simulation(trigger: Path, work_root: Path, worker_source: Path, worker_entrypoint: str, lt_jar: Path) -> dict[str, Any]:
    # Runtime identity is checked BEFORE any article/research work.
    identity = verify_runtime_identity()
    request = load_trigger(trigger)

    ppm = REPO / "control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
    require(lt_jar.is_file(), "LANGUAGETOOL_JAR_MISSING")
    require(sha256_file(lt_jar) == "2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8", "LANGUAGETOOL_JAR_SHA_MISMATCH")
    require(ppm.is_file(), "PPM679_PACKAGE_MISSING")
    require(sha256_file(ppm) == "acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1", "PPM679_PACKAGE_SHA_MISMATCH")

    # The machine must construct Point 0 from the chat trigger. The worker does not.
    sys.path.insert(0, str(SYSTEM4))
    from point0_snapshot import build_point0_from_chat_trigger  # type: ignore
    from root_supervisor_bridge import run_point0_supervised_batch  # type: ignore

    point0_path = work_root / "point0.json"
    work_root.mkdir(parents=True, exist_ok=True)
    point0 = build_point0_from_chat_trigger(request, output_path=point0_path)
    require(point0.get("contract") == POINT0_CONTRACT, "POINT0_CONTRACT_INVALID")

    result = run_point0_supervised_batch(
        point0_path=point0_path,
        workspace=work_root / "runtime",
        worker_source=worker_source,
        worker_entrypoint=worker_entrypoint,
        lt_jar=lt_jar,
        output_path=work_root / "SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json",
        parent_chat_dir=work_root / "parent-chat",
        codex_enabled=False,
    )
    require(result.get("status") == "SYSTEM4_CHAT_TO_FILE_PASS", "FULL_ROUTE_NOT_PASS:" + str(result.get("status")))
    require(result.get("article_count") == request["article_count"], "FINAL_ARTICLE_COUNT_MISMATCH")
    require(result.get("publish_allowed") is False, "FINAL_PUBLISH_ALLOWED_INVALID")
    require(result.get("languagetool", {}).get("executed") is True, "LANGUAGETOOL_NOT_ACTUALLY_EXECUTED")
    require(result.get("ppm679", {}).get("executed") is True, "PPM679_NOT_ACTUALLY_EXECUTED")
    require(result.get("handoff_contract") == HANDOFF_CONTRACT, "HANDOFF_CONTRACT_INVALID")
    require(result.get("parent_chat_byte_equal") is True, "PARENT_CHAT_NOT_BYTE_IDENTICAL")
    return {
        "status": "SYSTEM4A_CHAT_TO_FILE_FULL_ACCEPTANCE_PASS",
        "article_count": request["article_count"],
        "codex_used": False,
        "runtime_identity": identity,
        "historical_escape_classes_bound": len(KNOWN_LIVE_ESCAPE_CLASSES),
        "publish_allowed": False,
        "result": result,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--trigger", required=True)
    p.add_argument("--work-root", required=True)
    p.add_argument("--worker-source", required=True)
    p.add_argument("--worker-entrypoint", required=True)
    p.add_argument("--lt-jar", required=True)
    args = p.parse_args(argv)
    try:
        result = run_simulation(Path(args.trigger), Path(args.work_root), Path(args.worker_source), args.worker_entrypoint, Path(args.lt_jar))
    except Exception as exc:
        print(json.dumps({
            "status": "SYSTEM4A_CHAT_TO_FILE_FULL_ACCEPTANCE_BLOCKED",
            "first_blocker": str(exc),
            "codex_used": False,
            "publish_allowed": False,
            "historical_escape_classes_bound": len(KNOWN_LIVE_ESCAPE_CLASSES),
        }, ensure_ascii=False, sort_keys=True))
        return 4
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
