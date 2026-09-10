#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import urllib.request
from pathlib import Path
from typing import Callable

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2] if len(HERE.parents) > 2 else HERE
PROOF_DIR = REPO / ".pferde-environment"
PROOF_PATH = PROOF_DIR / "CODEX_PRODUCTION_PREFLIGHT.json"
CONTRACT = "PFERDE_ATELIER_CODEX_PRODUCTION_ENVIRONMENT_PREFLIGHT_V2"
REPO_FULL_NAME = "hallo-netizen/affiliate-pferdeportal"
MAIN_API = f"https://api.github.com/repos/{REPO_FULL_NAME}/branches/main"
MAIN_TRACKING_REF = "refs/remotes/origin/main"
TOOLBOX_MANIFEST_REL = "control/startmaster0107/codex-production-runtime/RUNTIME_TOOLBOX_MANIFEST.json"
LT_PROOF_REL = ".pferde-environment/LANGUAGETOOL_RUNTIME.json"
ALLOWED_STEPS = {
    ("RUN_NEW_ARTICLE_BATCH_NO_STOP", 107007),
    ("FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH", 107008),
}


class PreflightBlocked(RuntimeError):
    pass


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            block = fh.read(1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def rel(repo: Path, value: str) -> Path:
    p = Path(str(value or ""))
    if not value or p.is_absolute() or ".." in p.parts:
        raise PreflightBlocked("INVALID_RELATIVE_PATH")
    full = (repo / p).resolve()
    root = repo.resolve()
    if full != root and root not in full.parents:
        raise PreflightBlocked("RELATIVE_PATH_ESCAPE")
    return full


def _hex64(value: object) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{64}", str(value or "")))


def validate_toolbox_manifest(repo: Path) -> tuple[dict, str]:
    path = repo / TOOLBOX_MANIFEST_REL
    if not path.is_file():
        raise PreflightBlocked("RUNTIME_TOOLBOX_MANIFEST_MISSING")
    try:
        m = load(path)
    except Exception as exc:
        raise PreflightBlocked("RUNTIME_TOOLBOX_MANIFEST_JSON_INVALID") from exc
    if m.get("contract") != "PFERDE_ATELIER_RUNTIME_TOOLBOX_MANIFEST_V1":
        raise PreflightBlocked("RUNTIME_TOOLBOX_MANIFEST_CONTRACT_INVALID")
    if m.get("schema_version") != 1:
        raise PreflightBlocked("RUNTIME_TOOLBOX_MANIFEST_SCHEMA_INVALID")
    if m.get("scope") != "TECHNICAL_RUNTIME_IDENTITY_ONLY":
        raise PreflightBlocked("RUNTIME_TOOLBOX_MANIFEST_SCOPE_INVALID")

    authority = m.get("authority") or {}
    for key in (
        "chat_execution_authority",
        "chat_tool_selection_authority",
        "worker_tool_selection_authority",
        "workflow_navigation_authority",
        "repair_choice_authority",
        "content_semantics_authority",
        "quality_authority",
        "design_authority",
        "seo_authority",
    ):
        if authority.get(key) != "NONE":
            raise PreflightBlocked("RUNTIME_TOOLBOX_MANIFEST_AUTHORITY_INVALID:" + key)
    if authority.get("publish_allowed") is not False:
        raise PreflightBlocked("RUNTIME_TOOLBOX_MANIFEST_PUBLISH_AUTHORITY_INVALID")

    update = m.get("update_policy") or {}
    if update.get("mode") != "EXACT_MANIFEST_ONLY_FAIL_CLOSED":
        raise PreflightBlocked("RUNTIME_TOOLBOX_UPDATE_POLICY_INVALID")
    if set(update.get("allowed_triggers") or []) != {
        "CACHE_MISSING",
        "CACHE_HASH_MISMATCH",
        "MANIFEST_CHANGED",
    }:
        raise PreflightBlocked("RUNTIME_TOOLBOX_UPDATE_TRIGGER_INVALID")
    for key in (
        "alternative_tool_allowed",
        "fallback_version_allowed",
        "worker_choice_allowed",
        "chat_choice_allowed",
    ):
        if update.get(key) is not False:
            raise PreflightBlocked("RUNTIME_TOOLBOX_UPDATE_CHOICE_INVALID:" + key)

    agent = m.get("agent_phase") or {}
    for key in ("network_required", "tool_install_allowed", "tool_update_allowed", "tool_selection_allowed"):
        if agent.get(key) is not False:
            raise PreflightBlocked("RUNTIME_TOOLBOX_AGENT_POLICY_INVALID:" + key)

    runtimes = m.get("system_runtimes") or {}
    java = runtimes.get("java") or {}
    php = runtimes.get("php") or {}
    if java.get("provider") != "CODEX_UNIVERSAL" or not re.fullmatch(r"\d+", str(java.get("selector") or "")):
        raise PreflightBlocked("JAVA_MANIFEST_BINDING_INVALID")
    if java.get("probe") != "JAVA_FEATURE_VERSION" or java.get("real_execution_required") is not True:
        raise PreflightBlocked("JAVA_MANIFEST_PROBE_INVALID")
    if php.get("provider") != "CODEX_UNIVERSAL" or not re.fullmatch(r"\d+\.\d+", str(php.get("selector") or "")):
        raise PreflightBlocked("PHP_MANIFEST_BINDING_INVALID")
    if php.get("probe") != "PHP_MAJOR_MINOR" or php.get("real_execution_required") is not True:
        raise PreflightBlocked("PHP_MANIFEST_PROBE_INVALID")

    crypto = ((m.get("python_packages") or {}).get("cryptography") or {})
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(crypto.get("version") or "")):
        raise PreflightBlocked("CRYPTOGRAPHY_MANIFEST_VERSION_INVALID")
    if crypto.get("real_import_required") is not True:
        raise PreflightBlocked("CRYPTOGRAPHY_MANIFEST_PROBE_INVALID")

    lt = m.get("languagetool") or {}
    if lt.get("engine") != "LanguageTool 6.8 / Bestand 43" or lt.get("component_version") != "6.8":
        raise PreflightBlocked("LANGUAGETOOL_MANIFEST_IDENTITY_INVALID")
    if not str(lt.get("source_url") or "").startswith("https://github.com/"):
        raise PreflightBlocked("LANGUAGETOOL_MANIFEST_SOURCE_INVALID")
    for key in (
        "inner_zip_sha256",
        "historical_outer_sha256",
        "commandline_jar_sha256",
        "commandline_jar_manifest_sha256",
    ):
        if not _hex64(lt.get(key)):
            raise PreflightBlocked("LANGUAGETOOL_MANIFEST_HASH_INVALID:" + key)
    if int(lt.get("inner_zip_size") or 0) <= 0 or lt.get("real_execution_required") is not True:
        raise PreflightBlocked("LANGUAGETOOL_MANIFEST_RUNTIME_INVALID")
    cache_rel = Path(str(lt.get("persistent_cache_root") or ""))
    if not str(cache_rel) or cache_rel.is_absolute() or ".." in cache_rel.parts:
        raise PreflightBlocked("LANGUAGETOOL_MANIFEST_CACHE_ROOT_INVALID")

    packages = m.get("repository_packages") or {}
    for name in ("ppm679", "pserc"):
        row = packages.get(name) or {}
        rel(repo, str(row.get("ref") or ""))
        if not _hex64(row.get("sha256")):
            raise PreflightBlocked("RUNTIME_PACKAGE_MANIFEST_HASH_INVALID:" + name)

    return m, sha256(path)


def git(repo: Path, *args: str) -> str:
    try:
        cp = subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception as exc:
        raise PreflightBlocked("GIT_CHECK_FAILED:" + " ".join(args)) from exc
    return cp.stdout.strip()


def authoritative_main_sha(repo: Path = REPO) -> tuple[str, str]:
    try:
        value = git(repo, "rev-parse", "--verify", MAIN_TRACKING_REF)
        if len(value) == 40:
            return value, "CODEX_CHECKOUT_REMOTE_TRACKING_MAIN"
    except Exception:
        pass
    try:
        req = urllib.request.Request(
            MAIN_API,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "pferde-atelier-codex-preflight",
            },
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
        value = str(((raw.get("commit") or {}).get("sha")) or "")
        if len(value) == 40:
            return value, "GITHUB_PUBLIC_BRANCH_API"
    except Exception:
        pass
    raise PreflightBlocked("AUTHORITATIVE_MAIN_SHA_UNAVAILABLE")


def ed25519_available(expected_version: str | None = None) -> bool:
    try:
        import cryptography
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey  # noqa: F401
    except Exception as exc:
        raise PreflightBlocked("ED25519_RUNTIME_UNAVAILABLE") from exc
    if expected_version is not None and cryptography.__version__ != expected_version:
        raise PreflightBlocked(
            "CRYPTOGRAPHY_VERSION_MISMATCH:"
            + cryptography.__version__
            + ":EXPECTED:"
            + expected_version
        )
    return True


def _run_local_tool(
    argv: list[str],
    repo: Path,
    token: str,
    timeout: int = 60,
) -> subprocess.CompletedProcess:
    try:
        cp = subprocess.run(
            argv,
            cwd=repo,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
    except Exception as exc:
        raise PreflightBlocked(token) from exc
    if cp.returncode != 0:
        raise PreflightBlocked(token)
    return cp


def _expected_lt_jar(manifest: dict) -> Path:
    lt = manifest["languagetool"]
    cache_rel = Path(str(lt["persistent_cache_root"]))
    root = (Path.home() / cache_rel).resolve()
    runtime = root / ("runtime-" + str(lt["inner_zip_sha256"]))
    return (
        runtime
        / f"LanguageTool-{lt['component_version']}"
        / "languagetool-commandline.jar"
    ).resolve()


def validate_runtime_tools(repo: Path, manifest: dict, manifest_sha: str) -> dict:
    repo = Path(repo).resolve()
    packages = manifest["repository_packages"]

    ppm_row = packages["ppm679"]
    ppm = rel(repo, ppm_row["ref"])
    if not ppm.is_file():
        raise PreflightBlocked("PPM679_PACKAGE_ZIP_MISSING")
    if sha256(ppm) != ppm_row["sha256"]:
        raise PreflightBlocked("PPM679_PACKAGE_HASH_MISMATCH")

    pserc_row = packages["pserc"]
    pserc = rel(repo, pserc_row["ref"])
    if not pserc.is_file():
        raise PreflightBlocked("PSERC_FIX_ZIP_MISSING")
    if sha256(pserc) != pserc_row["sha256"]:
        raise PreflightBlocked("PSERC_FIX_PACKAGE_HASH_MISMATCH")

    php_selector = str(manifest["system_runtimes"]["php"]["selector"])
    php = shutil.which("php")
    if not php:
        raise PreflightBlocked("PHP_RUNTIME_UNAVAILABLE")
    php_selector_cp = _run_local_tool(
        [php, "-r", 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;'],
        repo,
        "PHP_RUNTIME_NOT_EXECUTABLE",
    )
    if php_selector_cp.stdout.strip() != php_selector:
        raise PreflightBlocked(
            "PHP_RUNTIME_VERSION_MISMATCH:"
            + php_selector_cp.stdout.strip()
            + ":EXPECTED:"
            + php_selector
        )
    php_full_cp = _run_local_tool(
        [php, "-r", "echo PHP_VERSION;"],
        repo,
        "PHP_RUNTIME_VERSION_UNAVAILABLE",
    )
    php_version = php_full_cp.stdout.strip()
    if not php_version:
        raise PreflightBlocked("PHP_RUNTIME_VERSION_UNAVAILABLE")

    java_selector = str(manifest["system_runtimes"]["java"]["selector"])
    java = shutil.which("java")
    if not java:
        raise PreflightBlocked("JAVA_RUNTIME_UNAVAILABLE")
    java_cp = _run_local_tool([java, "-version"], repo, "JAVA_RUNTIME_NOT_EXECUTABLE")
    java_output = java_cp.stderr or java_cp.stdout
    first_line = java_output.splitlines()[0].strip() if java_output else ""
    match = re.search(r'version\s+"(\d+)(?:[.\"]|$)', java_output)
    if not match:
        raise PreflightBlocked("JAVA_RUNTIME_VERSION_UNAVAILABLE")
    if match.group(1) != java_selector:
        raise PreflightBlocked(
            "JAVA_RUNTIME_VERSION_MISMATCH:"
            + match.group(1)
            + ":EXPECTED:"
            + java_selector
        )

    crypto_version = str(manifest["python_packages"]["cryptography"]["version"])
    ed25519_available(crypto_version)

    lt_manifest = manifest["languagetool"]
    lt_proof_path = repo / LT_PROOF_REL
    if not lt_proof_path.is_file():
        raise PreflightBlocked("LANGUAGETOOL_RUNTIME_PROOF_MISSING")
    lt = load(lt_proof_path)
    required_lt = {
        "contract": "PFERDE_ATELIER_LANGUAGETOOL_RUNTIME_BINDING_V2",
        "status": "LANGUAGETOOL_RUNTIME_READY",
        "toolbox_manifest_ref": TOOLBOX_MANIFEST_REL,
        "toolbox_manifest_sha256": manifest_sha,
        "engine": lt_manifest["engine"],
        "source_url": lt_manifest["source_url"],
        "outer_dependency_ref": lt_manifest["historical_outer_ref"],
        "outer_dependency_sha256": lt_manifest["historical_outer_sha256"],
        "inner_dependency_sha256": lt_manifest["inner_zip_sha256"],
        "inner_dependency_size": int(lt_manifest["inner_zip_size"]),
        "executed_commandline_jar_sha256": lt_manifest["commandline_jar_sha256"],
        "executed_commandline_jar_manifest_sha256": lt_manifest[
            "commandline_jar_manifest_sha256"
        ],
        "executed_component_version": lt_manifest["component_version"],
        "agent_network_required_for_execution": False,
        "content_semantics_inspected": False,
        "quality_authority": "NONE",
        "content_or_quality_rules_changed": False,
        "publish_allowed": False,
    }
    for key, expected in required_lt.items():
        if lt.get(key) != expected:
            raise PreflightBlocked("LANGUAGETOOL_RUNTIME_PROOF_INVALID:" + key)

    expected_jar = _expected_lt_jar(manifest)
    jar_ref = Path(str(lt.get("executed_commandline_jar_ref") or "")).resolve()
    if jar_ref != expected_jar:
        raise PreflightBlocked("LANGUAGETOOL_COMMANDLINE_JAR_PATH_MISMATCH")
    if not expected_jar.is_file():
        raise PreflightBlocked("LANGUAGETOOL_COMMANDLINE_JAR_MISSING")
    if sha256(expected_jar) != lt_manifest["commandline_jar_sha256"]:
        raise PreflightBlocked("LANGUAGETOOL_COMMANDLINE_JAR_HASH_MISMATCH")

    proof_dir = repo / ".pferde-environment"
    proof_dir.mkdir(parents=True, exist_ok=True)
    smoke_path = proof_dir / "LANGUAGETOOL_PREFLIGHT_SMOKE.txt"
    smoke_path.write_text("Das ist ein einfacher Testsatz.\n", encoding="utf-8")
    try:
        lt_cp = _run_local_tool(
            [
                java,
                "-Xmx1024m",
                "-jar",
                str(expected_jar),
                "--json",
                "-l",
                "de-DE",
                str(smoke_path),
            ],
            repo,
            "LANGUAGETOOL_RUNTIME_NOT_EXECUTABLE",
            timeout=120,
        )
        try:
            parsed = json.loads(lt_cp.stdout)
        except Exception as exc:
            raise PreflightBlocked("LANGUAGETOOL_RUNTIME_OUTPUT_INVALID") from exc
        if not isinstance(parsed, dict):
            raise PreflightBlocked("LANGUAGETOOL_RUNTIME_OUTPUT_INVALID")
    finally:
        try:
            smoke_path.unlink()
        except FileNotFoundError:
            pass

    return {
        "status": "RUNTIME_TOOLBOX_PASS",
        "toolbox_manifest_sha256": manifest_sha,
        "php_executable": True,
        "php_selector": php_selector,
        "php_version": php_version,
        "java_executable": True,
        "java_selector": java_selector,
        "java_version": first_line,
        "cryptography_version": crypto_version,
        "ed25519_runtime": True,
        "languagetool_real_execution": True,
        "languagetool_engine": lt_manifest["engine"],
        "languagetool_outer_sha256": lt_manifest["historical_outer_sha256"],
        "languagetool_inner_sha256": lt_manifest["inner_zip_sha256"],
        "languagetool_jar_sha256": lt_manifest["commandline_jar_sha256"],
        "ppm679_package_sha256": ppm_row["sha256"],
        "pserc_fix_package_sha256": pserc_row["sha256"],
        "agent_network_required": False,
        "content_semantics_inspected": False,
        "quality_authority": "NONE",
        "workflow_navigation_authority": "NONE",
        "repair_choice_authority": "NONE",
        "publish_allowed": False,
    }


def require_runtime_tools(value: dict, manifest: dict, manifest_sha: str) -> dict:
    lt = manifest["languagetool"]
    required = {
        "status": "RUNTIME_TOOLBOX_PASS",
        "toolbox_manifest_sha256": manifest_sha,
        "php_executable": True,
        "php_selector": str(manifest["system_runtimes"]["php"]["selector"]),
        "java_executable": True,
        "java_selector": str(manifest["system_runtimes"]["java"]["selector"]),
        "cryptography_version": str(manifest["python_packages"]["cryptography"]["version"]),
        "ed25519_runtime": True,
        "languagetool_real_execution": True,
        "languagetool_engine": lt["engine"],
        "languagetool_outer_sha256": lt["historical_outer_sha256"],
        "languagetool_inner_sha256": lt["inner_zip_sha256"],
        "languagetool_jar_sha256": lt["commandline_jar_sha256"],
        "ppm679_package_sha256": manifest["repository_packages"]["ppm679"]["sha256"],
        "pserc_fix_package_sha256": manifest["repository_packages"]["pserc"]["sha256"],
        "agent_network_required": False,
        "content_semantics_inspected": False,
        "quality_authority": "NONE",
        "workflow_navigation_authority": "NONE",
        "repair_choice_authority": "NONE",
        "publish_allowed": False,
    }
    if not isinstance(value, dict):
        raise PreflightBlocked("RUNTIME_TOOLBOX_PROOF_INVALID")
    for key, expected in required.items():
        if value.get(key) != expected:
            raise PreflightBlocked("RUNTIME_TOOLBOX_PROOF_INVALID:" + key)
    if not str(value.get("php_version") or "").strip():
        raise PreflightBlocked("RUNTIME_TOOLBOX_PROOF_INVALID:php_version")
    if not str(value.get("java_version") or "").strip():
        raise PreflightBlocked("RUNTIME_TOOLBOX_PROOF_INVALID:java_version")
    return value


def validate(
    repo: Path = REPO,
    *,
    main_sha_provider: Callable[[], tuple[str, str]] | None = None,
    ed25519_provider: Callable[[], bool] | None = None,
    runtime_tools_provider: Callable[..., dict] | None = None,
) -> dict:
    repo = Path(repo).resolve()
    manifest, manifest_sha = validate_toolbox_manifest(repo)

    head = git(repo, "rev-parse", "HEAD")
    expected_main, authority_source = (
        main_sha_provider() if main_sha_provider is not None else authoritative_main_sha(repo)
    )
    if head != expected_main:
        raise PreflightBlocked(
            "CODEX_CHECKOUT_NOT_CURRENT_MAIN:" + head + ":EXPECTED:" + expected_main
        )

    pointer_path = repo / "control/CURRENT_STARTMASTER.json"
    if not pointer_path.is_file():
        raise PreflightBlocked("STARTMASTER_POINTER_MISSING")
    ptr = load(pointer_path)
    if ptr.get("contract") != "PFERDE_ATELIER_CURRENT_STARTMASTER_POINTER_V2":
        raise PreflightBlocked("STARTMASTER_POINTER_CONTRACT_INVALID")
    if ptr.get("startmaster") != "STARTMASTER0107":
        raise PreflightBlocked("STARTMASTER_NOT_0107")
    if ptr.get("free_chat_execution_authority") is not False:
        raise PreflightBlocked("FREE_CHAT_EXECUTION_MUST_BE_FALSE")
    if ptr.get("chat_project_result_authority") != "NONE":
        raise PreflightBlocked("CHAT_PROJECT_RESULT_AUTHORITY_MUST_BE_NONE")
    if ptr.get("hard_worker") != "CODEX_CLOUD":
        raise PreflightBlocked("HARD_WORKER_MUST_BE_CODEX_CLOUD")
    if ptr.get("visible_output_authority") != "RELEASE_RECEIPT_ONLY":
        raise PreflightBlocked("VISIBLE_OUTPUT_AUTHORITY_INVALID")

    rootp = rel(repo, ptr.get("root_ref"))
    statep = rel(repo, ptr.get("state_ref"))
    policyp = rel(repo, ptr.get("visible_output_policy_ref"))
    runtime_entryp = rel(repo, ptr.get("execution_entrance_gate_ref"))
    for path in (rootp, statep, policyp, runtime_entryp):
        if not path.is_file():
            raise PreflightBlocked(
                "AUTHORITY_FILE_MISSING:" + str(path.relative_to(repo))
            )

    root = load(rootp)
    state = load(statep)
    policy = load(policyp)
    if (
        root.get("startmaster") != "STARTMASTER0107"
        or state.get("startmaster") != "STARTMASTER0107"
    ):
        raise PreflightBlocked("STARTMASTER_IDENTITY_MISMATCH")
    if sha256(statep) != root.get("current_state_sha256"):
        raise PreflightBlocked("STATE_HASH_MISMATCH")
    if root.get("next_allowed_step") != state.get("next_allowed_step"):
        raise PreflightBlocked("ROOT_STATE_STEP_MISMATCH")
    if sha256(policyp) != ptr.get("visible_output_policy_sha256"):
        raise PreflightBlocked("OUTPUT_POLICY_HASH_MISMATCH")
    if sha256(runtime_entryp) != ptr.get("execution_entrance_gate_sha256"):
        raise PreflightBlocked("RUNTIME_ENTRY_HASH_MISMATCH")

    if (
        policy.get("chat_execution_authority") != "NONE"
        or policy.get("chat_output_authority") != "NONE"
    ):
        raise PreflightBlocked("CHAT_AUTHORITY_MUST_BE_NONE")
    for key in (
        "domain_logic_authority",
        "content_semantics_authority",
        "quality_authority",
        "design_authority",
        "seo_authority",
    ):
        if policy.get(key) != "NONE":
            raise PreflightBlocked("POLICY_MUST_BE_DOMAIN_BLIND:" + key)
    if policy.get("publish_allowed") is not False:
        raise PreflightBlocked("PUBLISH_MUST_BE_FALSE")

    gate = state.get("execution_gate") or {}
    step_id = str(state.get("next_allowed_step") or "")
    sequence = int(gate.get("sequence", -1))
    if gate.get("step_id") != step_id:
        raise PreflightBlocked("STEP_GATE_MISMATCH")
    if (step_id, sequence) not in ALLOWED_STEPS:
        raise PreflightBlocked("CODEX_PRODUCTION_STEP_NOT_ALLOWED")
    if gate.get("domain_logic_authority") != "NONE":
        raise PreflightBlocked("DOMAIN_LOGIC_AUTHORITY_MUST_BE_NONE")
    if gate.get("content_quality_design_authority") != "NONE":
        raise PreflightBlocked("CONTENT_QUALITY_DESIGN_AUTHORITY_MUST_BE_NONE")
    if gate.get("hard_worker_target") != "CODEX_CLOUD":
        raise PreflightBlocked("HARD_WORKER_TARGET_INVALID")

    bundlep = rel(repo, gate.get("bundle_ref"))
    if not bundlep.is_file() or sha256(bundlep) != gate.get("bundle_sha256"):
        raise PreflightBlocked("BUNDLE_HASH_MISMATCH")

    runtimep = repo / "control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json"
    if not runtimep.is_file():
        raise PreflightBlocked("RUNTIME_INBOX_STATE_MISSING")
    runtime = load(runtimep)
    if runtime.get("contract") != "PFERDE_ATELIER_RUNTIME_BATCH_SLOT_STATE_V1":
        raise PreflightBlocked("RUNTIME_CONTRACT_INVALID")
    if runtime.get("status") != "EXECUTION_READY":
        raise PreflightBlocked("RUNTIME_NOT_EXECUTION_READY")
    if runtime.get("publish_allowed") is not False:
        raise PreflightBlocked("RUNTIME_PUBLISH_MUST_BE_FALSE")
    package_ref = str(runtime.get("production_package_ref") or "")
    package_sha = str(runtime.get("production_package_sha256") or "")
    packagep = rel(repo, package_ref)
    if not packagep.is_file():
        raise PreflightBlocked("PRODUCTION_PACKAGE_MISSING")
    if len(package_sha) != 64 or sha256(packagep) != package_sha:
        raise PreflightBlocked("PRODUCTION_PACKAGE_HASH_MISMATCH")

    expected_crypto = str(manifest["python_packages"]["cryptography"]["version"])
    if ed25519_provider is None:
        ed25519_available(expected_crypto)
    elif ed25519_provider() is not True:
        raise PreflightBlocked("ED25519_RUNTIME_UNAVAILABLE")

    if runtime_tools_provider is None:
        raw_tools = validate_runtime_tools(repo, manifest, manifest_sha)
    else:
        try:
            raw_tools = runtime_tools_provider(repo, manifest, manifest_sha)
        except TypeError:
            raw_tools = runtime_tools_provider(repo)
    runtime_tools = require_runtime_tools(raw_tools, manifest, manifest_sha)

    return {
        "contract": CONTRACT,
        "status": "CODEX_PRODUCTION_PREFLIGHT_PASS",
        "repository": REPO_FULL_NAME,
        "main_authority_source": authority_source,
        "expected_main_sha": expected_main,
        "local_head_sha": head,
        "startmaster": "STARTMASTER0107",
        "step_id": step_id,
        "sequence": sequence,
        "runtime_status": "EXECUTION_READY",
        "generation": int(runtime.get("generation") or 0),
        "batch_sha256": str(runtime.get("batch_sha256") or ""),
        "production_package_ref": package_ref,
        "production_package_sha256": package_sha,
        "state_sha256": sha256(statep),
        "bundle_sha256": sha256(bundlep),
        "toolbox_manifest_ref": TOOLBOX_MANIFEST_REL,
        "toolbox_manifest_sha256": manifest_sha,
        "ed25519_runtime": True,
        "runtime_tools": runtime_tools,
        "chat_execution_authority": "NONE",
        "chat_output_authority": "NONE",
        "domain_logic_authority": "NONE",
        "quality_authority": "NONE",
        "content_semantics_inspected": False,
        "workflow_navigation_decision": False,
        "repair_choice_authority": "NONE",
        "publish_allowed": False,
    }


def write_proof(repo: Path, proof: dict) -> Path:
    target = Path(repo).resolve() / ".pferde-environment/CODEX_PRODUCTION_PREFLIGHT.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(".json.tmp")
    tmp.write_text(
        json.dumps(proof, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    tmp.replace(target)
    return target


def main() -> int:
    try:
        proof = validate(REPO)
        path = write_proof(REPO, proof)
        print(
            json.dumps(
                {
                    "ok": True,
                    "status": proof["status"],
                    "proof": str(path.relative_to(REPO)),
                    "expected_main_sha": proof["expected_main_sha"],
                    "local_head_sha": proof["local_head_sha"],
                    "runtime_status": proof["runtime_status"],
                    "toolbox_manifest_sha256": proof["toolbox_manifest_sha256"],
                    "content_semantics_inspected": False,
                    "quality_authority": "NONE",
                    "workflow_navigation_decision": False,
                    "repair_choice_authority": "NONE",
                    "publish_allowed": False,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    except Exception as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "status": "CODEX_PRODUCTION_PREFLIGHT_BLOCKED",
                    "reason": str(exc),
                    "content_semantics_inspected": False,
                    "quality_authority": "NONE",
                    "workflow_navigation_decision": False,
                    "repair_choice_authority": "NONE",
                    "publish_allowed": False,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
