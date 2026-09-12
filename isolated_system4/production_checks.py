from __future__ import annotations

import ast
import hashlib
import html
import json
import os
import re
import subprocess
import tempfile
import time
import zipfile
import socket
import fcntl
import struct
import signal
from pathlib import Path
from typing import Any, Mapping

PPM_VERSION = "6.7.9"
PPM_PACKAGE_REL = "control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PPM_PACKAGE_SHA256 = "acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
LT_ENGINE = "LanguageTool 6.8 / Bestand 43"
LT_JAR_SHA256 = "2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8"
LT_WORKER_SOURCE_REL = "isolated_system4/LT68Worker.java"
LT_WORKER_SOURCE_SHA256 = "f2487a84b9fc4424e6207a26d8278d31207a7746e7cd504800faa22652876503"
LT_WORKER_META = Path("/tmp/system4-lt68-worker-v1.json")
LT_WORKER_LOCK = Path("/tmp/system4-lt68-worker-v1.lock")
LT_WORKER_MAX_USES = 32
LT_WORKER_REQUEST_TIMEOUT = 30.0
LT_OUTER_DEPENDENCY_SHA256 = "187f7c2efe7762049e9f00553dafe686e269bbf62220abe2f2715fe55df8605a"
LT_INNER_DEPENDENCY_SHA256 = "6a7f6b67b779ae9505f7579f0c41453ea8d1bd72ae750bdc2c55ba974281467d"
SYSTEM4_DIRNAME = "isolated_system4"


class ProductionCheckError(RuntimeError):
    pass


class RepairRequired(ProductionCheckError):
    def __init__(self, checker: str, findings: list[dict[str, Any]]):
        self.checker = checker
        self.findings = findings
        super().__init__(checker)


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def stable_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        raise ProductionCheckError("JSON_INVALID:" + str(path)) from exc
    if not isinstance(value, dict):
        raise ProductionCheckError("JSON_OBJECT_REQUIRED:" + str(path))
    return value


def _repo_root(system4_file: Path | None = None) -> Path:
    source = Path(system4_file or __file__).resolve()
    root = source.parent.parent
    if root.name == SYSTEM4_DIRNAME:
        root = root.parent
    if not (root / SYSTEM4_DIRNAME).is_dir():
        raise ProductionCheckError("SYSTEM4_REPO_ROOT_NOT_FOUND")
    return root


def _safe_repo_path(repo: Path, rel: str) -> Path:
    p = Path(str(rel or ""))
    if not rel or p.is_absolute() or ".." in p.parts:
        raise ProductionCheckError("INVALID_REPOSITORY_REFERENCE")
    out = (repo / p).resolve()
    root = repo.resolve()
    if out != root and root not in out.parents:
        raise ProductionCheckError("REPOSITORY_REFERENCE_ESCAPE")
    return out


def no_external_links(article: str) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for match in re.finditer(r"(?i)\bhref\s*=\s*([\"'])(.*?)\1", article):
        target = html.unescape(match.group(2)).strip()
        if re.match(r"(?i)^(?:https?:)?//", target) or re.match(r"(?i)^[a-z][a-z0-9+.-]*:", target):
            findings.append({"error_code": "EXTERNAL_LINK_FORBIDDEN", "target": target})
    for match in re.finditer(r"(?i)(?<![=\"'])\bhttps?://[^\s<>'\"]+", article):
        findings.append({"error_code": "EXTERNAL_URL_FORBIDDEN", "target": match.group(0)})
    if findings:
        raise RepairRequired("no_external_links", findings)
    return {"status": "PASS", "external_link_count": 0}


def _plain_text(article_html: str) -> str:
    value = re.sub(r"(?is)<!--.*?-->", "\n", article_html)
    value = re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1>", "\n", value)
    value = re.sub(r"(?is)</?(?:article|section|p|div|li|h[1-6]|br|tr|td|th|ul|ol|table|blockquote)\b[^>]*>", "\n", value)
    value = re.sub(r"(?s)<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r"\n[ \t]*\n+", "\n\n", value)
    return value.strip() + "\n"


def _ppm_visible_language_text(article_html: str) -> str:
    lines: list[str] = []
    for match in re.finditer(r"<(h2|p|li|th|td|small)\b[^>]*>(.*?)</\1>", article_html, re.I | re.S):
        value = html.unescape(match.group(2))
        value = re.sub(r"<[^>]+>", " ", value)
        value = re.sub(r"\s+", " ", value).strip()
        value = re.sub(r"\s+([.,;:!?])", r"\1", value)
        if value:
            lines.append(value)
    return "\n\n".join(lines)


def _canonical_body_text(article_html: str) -> str:
    value = html.unescape(article_html)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def _find_languagetool_jar(repo: Path) -> Path:
    explicit = os.environ.get("SYSTEM4_LANGUAGETOOL_JAR", "").strip()
    if explicit:
        candidate = Path(explicit)
        if candidate.is_file() and file_sha256(candidate) == LT_JAR_SHA256:
            return candidate.resolve()
        raise ProductionCheckError("LANGUAGETOOL_6_8_EXPLICIT_JAR_INVALID")

    candidates: list[Path] = []
    roots = [
        repo / ".pferde-environment",
        Path.home() / ".cache" / "pferde-atelier-languagetool",
        Path.home() / ".cache" / "language_tool_python",
        Path("/tmp"),
    ]
    names = {"languagetool-commandline.jar", "LanguageTool.jar"}
    for root in roots:
        if root.exists():
            for name in names:
                candidates.extend(root.rglob(name))
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate.resolve()) if candidate.exists() else str(candidate)
        if key in seen:
            continue
        seen.add(key)
        if candidate.is_file() and file_sha256(candidate) == LT_JAR_SHA256:
            return candidate.resolve()
    raise ProductionCheckError("LANGUAGETOOL_6_8_HASH_BOUND_JAR_MISSING")


def _worker_source(repo: Path) -> Path:
    source = _safe_repo_path(repo, LT_WORKER_SOURCE_REL)
    if not source.is_file():
        raise ProductionCheckError("LANGUAGETOOL_6_8_WORKER_SOURCE_MISSING")
    if file_sha256(source) != LT_WORKER_SOURCE_SHA256:
        raise ProductionCheckError("LANGUAGETOOL_6_8_WORKER_SOURCE_HASH_MISMATCH")
    return source


def _free_local_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])
    finally:
        sock.close()


def _read_exact(sock: socket.socket, size: int) -> bytes:
    chunks: list[bytes] = []
    left = size
    while left:
        chunk = sock.recv(left)
        if not chunk:
            raise ProductionCheckError("LANGUAGETOOL_REAL_EXECUTION_FAILED:WORKER_SHORT_RESPONSE")
        chunks.append(chunk)
        left -= len(chunk)
    return b"".join(chunks)


def _worker_request(port: int, checked_text: str, timeout: float = 120.0) -> tuple[dict[str, Any], str, int]:
    payload = checked_text.encode("utf-8")
    if len(payload) > 5_000_000:
        raise ProductionCheckError("LANGUAGETOOL_TEXT_TOO_LARGE")
    try:
        with socket.create_connection(("127.0.0.1", int(port)), timeout=min(timeout, 10.0)) as sock:
            sock.settimeout(timeout)
            sock.sendall(struct.pack("!I", len(payload)) + payload)
            response_size = struct.unpack("!I", _read_exact(sock, 4))[0]
            if response_size > 20_000_000:
                raise ProductionCheckError("LANGUAGETOOL_REPORT_TOO_LARGE")
            raw = _read_exact(sock, response_size).decode("utf-8")
    except ProductionCheckError:
        raise
    except Exception as exc:
        raise ProductionCheckError("LANGUAGETOOL_REAL_EXECUTION_FAILED:WORKER_REQUEST:" + str(exc)[:220]) from exc
    try:
        report = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ProductionCheckError("LANGUAGETOOL_REPORT_INVALID") from exc
    matches = report.get("matches") if isinstance(report, dict) else None
    if not isinstance(matches, list):
        raise ProductionCheckError("LANGUAGETOOL_MATCHES_INVALID")
    return report, raw, 0


def _worker_meta_valid(meta: Any, jar: Path, source: Path) -> bool:
    if not isinstance(meta, dict):
        return False
    try:
        pid = int(meta.get("pid") or 0)
        port = int(meta.get("port") or 0)
    except (TypeError, ValueError):
        return False
    if pid <= 1 or not (1024 <= port <= 65535):
        return False
    if meta.get("jar") != str(jar) or meta.get("jar_sha256") != LT_JAR_SHA256:
        return False
    if meta.get("source") != str(source) or meta.get("source_sha256") != LT_WORKER_SOURCE_SHA256:
        return False
    proc = Path(f"/proc/{pid}/cmdline")
    if not proc.is_file():
        return False
    try:
        cmdline = proc.read_bytes().replace(b"\x00", b" ").decode("utf-8", "replace")
    except OSError:
        return False
    return str(source) in cmdline and str(port) in cmdline and "java" in cmdline


def _terminate_worker(meta: Any) -> None:
    if not isinstance(meta, dict):
        return
    try:
        pid = int(meta.get("pid") or 0)
    except (TypeError, ValueError):
        return
    if pid > 1:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            return
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline and Path(f"/proc/{pid}").exists():
            time.sleep(0.05)
        if Path(f"/proc/{pid}").exists():
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                pass


def _ensure_lt_worker(repo: Path, jar: Path) -> int:
    source = _worker_source(repo)
    LT_WORKER_LOCK.touch(exist_ok=True)
    with LT_WORKER_LOCK.open("r+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        meta: Any = None
        if LT_WORKER_META.is_file():
            try:
                meta = json.loads(LT_WORKER_META.read_text(encoding="utf-8"))
            except Exception:
                meta = None
        if _worker_meta_valid(meta, jar, source):
            try:
                uses = int(meta.get("uses") or 0)
            except (TypeError, ValueError):
                uses = LT_WORKER_MAX_USES
            if uses < LT_WORKER_MAX_USES:
                return int(meta["port"])
            _terminate_worker(meta)
        try:
            LT_WORKER_META.unlink(missing_ok=True)
        except OSError:
            pass
        port = _free_local_port()
        proc = subprocess.Popen(
            ["java", "-Xmx1536m", "--class-path", str(jar), str(source), str(port)],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True, close_fds=True,
        )
        meta = {
            "pid": proc.pid, "port": port, "jar": str(jar), "jar_sha256": LT_JAR_SHA256,
            "source": str(source), "source_sha256": LT_WORKER_SOURCE_SHA256, "uses": 0,
        }
        LT_WORKER_META.write_text(json.dumps(meta, sort_keys=True), encoding="utf-8")
        deadline = time.monotonic() + 35.0
        while time.monotonic() < deadline:
            if proc.poll() is not None:
                LT_WORKER_META.unlink(missing_ok=True)
                raise ProductionCheckError("LANGUAGETOOL_REAL_EXECUTION_FAILED:WORKER_START")
            try:
                _worker_request(port, "Systemprüfung.", timeout=5.0)
                return port
            except ProductionCheckError:
                time.sleep(0.2)
        _terminate_worker(meta)
        LT_WORKER_META.unlink(missing_ok=True)
        raise ProductionCheckError("LANGUAGETOOL_REAL_EXECUTION_FAILED:WORKER_START_TIMEOUT")


def _invalidate_lt_worker() -> None:
    LT_WORKER_LOCK.touch(exist_ok=True)
    with LT_WORKER_LOCK.open("r+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        meta: Any = None
        if LT_WORKER_META.is_file():
            try:
                meta = json.loads(LT_WORKER_META.read_text(encoding="utf-8"))
            except Exception:
                pass
        _terminate_worker(meta)
        try:
            LT_WORKER_META.unlink(missing_ok=True)
        except OSError:
            pass


def _run_languagetool_cli(jar: Path, checked_text: str) -> tuple[dict[str, Any], str, int]:
    with tempfile.TemporaryDirectory(prefix="system4-lt-") as td:
        source = Path(td) / "article.txt"
        source.write_text(checked_text, encoding="utf-8")
        try:
            proc = subprocess.run(
                ["java", "-Xmx1024m", "-jar", str(jar), "--json", "-l", "de-DE", str(source)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise ProductionCheckError("LANGUAGETOOL_REAL_EXECUTION_FAILED:TIMEOUT") from exc
    if proc.returncode != 0:
        raise ProductionCheckError("LANGUAGETOOL_REAL_EXECUTION_FAILED:" + (proc.stderr or proc.stdout).strip()[:300])
    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise ProductionCheckError("LANGUAGETOOL_REPORT_INVALID") from exc
    matches = report.get("matches") if isinstance(report, dict) else None
    if not isinstance(matches, list):
        raise ProductionCheckError("LANGUAGETOOL_MATCHES_INVALID")
    return report, proc.stdout, proc.returncode


def _run_languagetool_text(repo: Path, checked_text: str) -> tuple[dict[str, Any], str, int]:
    if not checked_text.strip():
        raise ProductionCheckError("LANGUAGETOOL_PLAINTEXT_EMPTY")
    jar = _find_languagetool_jar(repo)
    if os.environ.get("SYSTEM4_LANGUAGETOOL_DISABLE_WORKER", "").strip() == "1":
        return _run_languagetool_cli(jar, checked_text)
    first_error: ProductionCheckError | None = None
    for attempt in range(2):
        try:
            port = _ensure_lt_worker(repo, jar)
            result = _worker_request(port, checked_text, timeout=LT_WORKER_REQUEST_TIMEOUT)
            LT_WORKER_LOCK.touch(exist_ok=True)
            with LT_WORKER_LOCK.open("r+") as lock:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
                if LT_WORKER_META.is_file():
                    try:
                        meta = json.loads(LT_WORKER_META.read_text(encoding="utf-8"))
                    except Exception:
                        meta = None
                    if isinstance(meta, dict) and int(meta.get("port") or 0) == int(port):
                        meta["uses"] = int(meta.get("uses") or 0) + 1
                        LT_WORKER_META.write_text(json.dumps(meta, sort_keys=True), encoding="utf-8")
            return result
        except ProductionCheckError as exc:
            first_error = first_error or exc
            _invalidate_lt_worker()
    try:
        return _run_languagetool_cli(jar, checked_text)
    except ProductionCheckError as cli_exc:
        raise ProductionCheckError("LANGUAGETOOL_REAL_EXECUTION_FAILED:WORKER_AND_CLI:" + str(first_error or cli_exc)[:220]) from cli_exc


def _repair_findings_from_lt(report: Mapping[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for raw in report.get("matches", []):
        match = raw if isinstance(raw, dict) else {}
        rule = match.get("rule") if isinstance(match.get("rule"), dict) else {}
        context = match.get("context") if isinstance(match.get("context"), dict) else {}
        findings.append({
            "error_code": "LANGUAGETOOL_FINDING",
            "rule_id": str(rule.get("id") or ""),
            "message": str(match.get("message") or ""),
            "offset": match.get("offset"),
            "length": match.get("length"),
            "context": str(context.get("text") or ""),
        })
    return findings


def run_languagetool(repo: Path, article_html: str) -> dict[str, Any]:
    plain = _plain_text(article_html)
    report, raw, return_code = _run_languagetool_text(repo, plain)
    if report["matches"]:
        raise RepairRequired("languagetool", _repair_findings_from_lt(report))
    return {
        "status": "PASS",
        "engine": LT_ENGINE,
        "commandline_jar_sha256": LT_JAR_SHA256,
        "finding_count": 0,
        "_checked_text": plain.rstrip("\n"),
        "_raw_report_json": raw,
        "_return_code": return_code,
    }


def _language_evidence_valid_for(article_html: str, evidence: Any) -> bool:
    if not isinstance(evidence, dict):
        return False
    checked = _ppm_visible_language_text(article_html)
    raw = evidence.get("raw_report_json")
    if not isinstance(raw, str):
        return False
    try:
        decoded = json.loads(raw)
    except json.JSONDecodeError:
        return False
    matches = decoded.get("matches") if isinstance(decoded, dict) else None
    execution = evidence.get("execution_record") if isinstance(evidence.get("execution_record"), dict) else {}
    checked_hash = text_sha256(checked)
    raw_hash = text_sha256(raw)
    return (
        evidence.get("engine") == LT_ENGINE
        and evidence.get("outer_dependency_sha256") == LT_OUTER_DEPENDENCY_SHA256
        and evidence.get("inner_dependency_sha256") == LT_INNER_DEPENDENCY_SHA256
        and evidence.get("content_hash") == text_sha256(article_html)
        and evidence.get("checked_text") == checked
        and evidence.get("checked_text_sha256") == checked_hash
        and evidence.get("raw_report_sha256") == raw_hash
        and isinstance(matches, list) and len(matches) == 0
        and evidence.get("raw_finding_count") == 0
        and evidence.get("unresolved_finding_count") == 0
        and evidence.get("return_code") == 0
        and isinstance(evidence.get("approved_exceptions"), list)
        and execution.get("input_sha256") == checked_hash
        and execution.get("raw_stdout_sha256") == raw_hash
        and execution.get("return_code") == 0
    )


def _fresh_ppm_language_evidence(repo: Path, article_html: str, lt_pass: Mapping[str, Any] | None = None) -> tuple[dict[str, Any], str]:
    checked = _ppm_visible_language_text(article_html)
    if isinstance(lt_pass, Mapping) and lt_pass.get("_checked_text") == checked:
        raw = str(lt_pass.get("_raw_report_json") or "")
        return_code = int(lt_pass.get("_return_code", -1))
        try:
            report = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ProductionCheckError("LANGUAGETOOL_REPORT_INVALID") from exc
        matches = report.get("matches") if isinstance(report, dict) else None
        if not isinstance(matches, list) or matches:
            raise ProductionCheckError("LANGUAGETOOL_REUSE_EVIDENCE_INVALID")
        source = "REAL_LT68_FULLCHECK_REUSED"
    else:
        report, raw, return_code = _run_languagetool_text(repo, checked)
        if report["matches"]:
            raise RepairRequired("languagetool", _repair_findings_from_lt(report))
        source = "REAL_LT68_CURRENT_DRAFT_REFRESHED"
    checked_hash = text_sha256(checked)
    raw_hash = text_sha256(raw)
    evidence = {
        "engine": LT_ENGINE,
        "outer_dependency_sha256": LT_OUTER_DEPENDENCY_SHA256,
        "inner_dependency_sha256": LT_INNER_DEPENDENCY_SHA256,
        "content_hash": text_sha256(article_html),
        "checked_text": checked,
        "checked_text_sha256": checked_hash,
        "raw_report_json": raw,
        "raw_report_sha256": raw_hash,
        "raw_finding_count": 0,
        "unresolved_finding_count": 0,
        "return_code": return_code,
        "approved_exceptions": [],
        "execution_record": {
            "input_sha256": checked_hash,
            "raw_stdout_sha256": raw_hash,
            "return_code": return_code,
        },
    }
    return evidence, source


def _runtime_rebound_plan(repo: Path, article_html: str, production_plan_item: Mapping[str, Any], lt_pass: Mapping[str, Any] | None = None) -> tuple[dict[str, Any], str]:
    item = json.loads(json.dumps(dict(production_plan_item), ensure_ascii=False))
    quality = item.get("quality_binding")
    if not isinstance(quality, dict) or quality.get("contract") != "content_structure_language_binding_v2":
        raise ProductionCheckError("PPM679_QUALITY_BINDING_MISSING")
    declared = str(item.get("quality_binding_hash") or "").lower().strip()
    actual = stable_hash(quality)
    if not re.fullmatch(r"[0-9a-f]{64}", declared) or declared != actual:
        raise ProductionCheckError("PPM679_BOUND_QUALITY_BINDING_HASH_INVALID")

    canonical = dict(item.get("canonical_article") or {})
    canonical["body_html"] = article_html
    canonical["body_html_sha256"] = text_sha256(article_html)
    canonical["body_text"] = _canonical_body_text(article_html)
    if "body_text_sha256" in canonical:
        canonical["body_text_sha256"] = text_sha256(canonical["body_text"])
    canonical.setdefault("title", str(item.get("topic") or ""))
    item["canonical_article"] = canonical

    bound_evidence = quality.get("language_evidence")
    if _language_evidence_valid_for(article_html, bound_evidence):
        evidence_source = "BOUND_CURRENT_REUSED"
    else:
        fresh_evidence, evidence_source = _fresh_ppm_language_evidence(repo, article_html, lt_pass)
        quality["language_evidence"] = fresh_evidence
    item["quality_binding"] = quality
    item["quality_binding_hash"] = stable_hash(quality)
    return item, evidence_source


def _ppm_repair_findings(value: Any) -> list[dict[str, Any]]:
    allowed_prefixes = ("BLOCKED_CONTENT_", "BLOCKED_WAVE2_", "BLOCKED_CANONICAL_RUNTIME_LINK_")
    findings: list[dict[str, Any]] = []

    def add(code: Any, node: Mapping[str, Any]) -> None:
        code = str(code or "")
        if not code.startswith(allowed_prefixes):
            return
        findings.append({
            "error_code": code,
            "failed_rule": node.get("failed_rule"),
            "field_path": node.get("field_path"),
            "expected": node.get("expected"),
            "actual": node.get("actual"),
            "reason": node.get("reason"),
            "validator_id": node.get("validator_id"),
        })

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            add(node.get("error_code"), node)
            for key in ("reason_codes", "errors"):
                values = node.get(key)
                if isinstance(values, list):
                    for code in values:
                        if isinstance(code, str):
                            add(code, node)
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in findings:
        key = json.dumps(item, ensure_ascii=False, sort_keys=True, default=str)
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def run_ppm_content_validator(
    repo: Path,
    article_html: str,
    fact_pack: Mapping[str, Any],
    production_plan_item: Mapping[str, Any],
    lt_pass: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    package = _safe_repo_path(repo, PPM_PACKAGE_REL)
    if not package.is_file():
        raise ProductionCheckError("PPM679_PACKAGE_MISSING")
    if file_sha256(package) != PPM_PACKAGE_SHA256:
        raise ProductionCheckError("PPM679_PACKAGE_HASH_MISMATCH")

    item, language_evidence_source = _runtime_rebound_plan(repo, article_html, production_plan_item, lt_pass)
    payload = {"fact_pack": dict(fact_pack), "production_plan_item": item}

    php = r'''<?php
$root=$argv[1];
$payload=json_decode((string)file_get_contents($argv[2]),true);
if(!is_array($payload)){fwrite(STDERR,"PAYLOAD_INVALID\n");exit(2);}
require $root.'/tests/bootstrap-test.php';
PPM679_WP::reset_test_state();
PPM679_Storage::reset_test_state();
PPM679_Handoff_Permit::reset_test_state();
PPM679_Storage::ensure_schema();
$pack=(array)($payload['fact_pack']??[]);
$item=(array)($payload['production_plan_item']??[]);
$ca=(array)($item['canonical_article']??[]);
$import=PPM679_Admin::import_fact_pack_bundle(['contract'=>'canonical_fact_pack_import_v1','fact_packs'=>[$pack]]);
if(empty($import['ok'])){
 echo json_encode(['ok'=>false,'phase'=>'FACT_PACK_IMPORT','result'=>$import],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);exit(0);
}
$html=(string)($ca['body_html']??'');
$generated=[
 'article_type'=>(string)($item['article_type']??''),
 'title'=>(string)($ca['title']??''),
 'content_html'=>$html,
 'content_hash'=>hash('sha256',$html),
];
$result=PPM679_Content_Validator::check($generated,$item,'system4_direct_article_control','bound-system4');
echo json_encode(['ok'=>!empty($result['ok']),'result'=>$result],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
?>'''

    with tempfile.TemporaryDirectory(prefix="system4-ppm-") as td:
        td_path = Path(td)
        root = td_path / "ppm"
        root.mkdir()
        with zipfile.ZipFile(package) as archive:
            archive.extractall(root)
        ppm_root = root / "portal-production-machine"
        if not (ppm_root / "tests" / "bootstrap-test.php").is_file():
            raise ProductionCheckError("PPM679_PURE_VALIDATOR_RUNTIME_MISSING")
        payload_path = td_path / "payload.json"
        payload_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        script = td_path / "check.php"
        script.write_text(php, encoding="utf-8")
        proc = subprocess.run(
            ["php", str(script), str(ppm_root), str(payload_path)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
            check=False,
        )
    if proc.returncode != 0:
        raise ProductionCheckError("PPM679_VALIDATOR_EXECUTION_FAILED:" + (proc.stderr or proc.stdout).strip()[:300])
    try:
        wrapper = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise ProductionCheckError("PPM679_VALIDATOR_RESULT_INVALID") from exc
    result = wrapper.get("result") if isinstance(wrapper, dict) else None
    if not isinstance(result, dict):
        raise ProductionCheckError("PPM679_VALIDATOR_RESULT_MISSING")
    if wrapper.get("ok") is not True:
        repair = _ppm_repair_findings(result)
        if repair:
            raise RepairRequired("ppm679", repair)
        errors = result.get("errors") if isinstance(result.get("errors"), list) else []
        codes = [str(row.get("error_code") or "") for row in errors if isinstance(row, dict) and row.get("error_code")]
        phase = str(wrapper.get("phase") or "PPM679_BLOCKED")
        raise ProductionCheckError("PPM679_VALIDATOR_BLOCKED:" + (codes[0] if codes else phase))
    checks = result.get("checks")
    if result.get("technical_status") != "TECHNICAL_CHECK_OK":
        raise ProductionCheckError("PPM679_TECHNICAL_NOT_PASS")
    if result.get("content_quality_status") != "CONTENT_QUALITY_CHECK_OK":
        repair = _ppm_repair_findings(result)
        if repair:
            raise RepairRequired("ppm679", repair)
        raise ProductionCheckError("PPM679_CONTENT_QUALITY_NOT_PASS")
    if result.get("content_hash") != text_sha256(article_html):
        raise ProductionCheckError("PPM679_CONTENT_HASH_MISMATCH")
    if not isinstance(checks, dict) or checks.get("fail_closed_aggregate_status") != "PASS":
        raise ProductionCheckError("PPM679_FAIL_CLOSED_NOT_PASS")
    return {
        "status": "PASS",
        "ppm_version": PPM_VERSION,
        "ppm_package_sha256": PPM_PACKAGE_SHA256,
        "technical_status": result["technical_status"],
        "content_quality_status": result["content_quality_status"],
        "fail_closed_aggregate_status": checks["fail_closed_aggregate_status"],
        "content_sha256": text_sha256(article_html),
        "language_evidence_source": language_evidence_source,
    }


def validate_bound_context(
    state: Mapping[str, Any], fact_pack: Mapping[str, Any], production_plan_item: Mapping[str, Any]
) -> None:
    article = state.get("article")
    if not isinstance(article, dict):
        raise ProductionCheckError("SYSTEM4_ARTICLE_BINDING_MISSING")
    source = str(state.get("source_snapshot_sha256") or "")
    if fact_pack.get("contract") != "canonical_fact_pack_v1":
        raise ProductionCheckError("FACT_PACK_CONTRACT_INVALID")
    if fact_pack.get("source_snapshot_id") != source or fact_pack.get("fact_pack_id") != source:
        raise ProductionCheckError("FACT_PACK_SOURCE_BINDING_INVALID")
    if fact_pack.get("status") != "SOURCE_VERIFIED_PRODUCTION_READY":
        raise ProductionCheckError("FACT_PACK_NOT_PRODUCTION_READY")
    if not isinstance(fact_pack.get("claims"), list):
        raise ProductionCheckError("FACT_PACK_CLAIMS_ARRAY_REQUIRED")
    expected = {
        "article_type": article.get("article_type"),
        "target_keyword": article.get("target_keyword"),
        "topic": article.get("title"),
    }
    for key, value in expected.items():
        if production_plan_item.get(key) != value:
            raise ProductionCheckError("PRODUCTION_PLAN_IDENTITY_MISMATCH:" + key)
    if "plan_slot" in production_plan_item:
        raise ProductionCheckError("PRODUCTION_PLAN_SYNTHETIC_SLOT_FORBIDDEN")
    quality = production_plan_item.get("quality_binding")
    category = quality.get("wordpress_category") if isinstance(quality, dict) else None
    category_binding = production_plan_item.get("category_binding")
    slug = None
    if isinstance(category_binding, dict):
        slug = category_binding.get("slug")
    if not slug and isinstance(category, dict):
        slug = category.get("slug")
    if slug != article.get("category"):
        raise ProductionCheckError("WORDPRESS_CATEGORY_BINDING_MISMATCH")


def no_legacy_runtime_dependencies(repo: Path) -> dict[str, Any]:
    root = repo / SYSTEM4_DIRNAME
    if not root.is_dir():
        raise ProductionCheckError("SYSTEM4_ROOT_MISSING")
    forbidden_modules = {
        "control", "startmaster", "single_door_boundary", "fachworkflow_proof_handoff",
        "runtime_entry_gate", "cloud_entry", "production_continuity_guard",
    }
    violations: list[str] = []
    for path in sorted(root.glob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            raise ProductionCheckError("SYSTEM4_PYTHON_SYNTAX_INVALID:" + path.name) from exc
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in forbidden_modules:
                        violations.append(path.name + ":import:" + alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = str(node.module or "")
                if module.split(".")[0] in forbidden_modules:
                    violations.append(path.name + ":from:" + module)
    if violations:
        raise ProductionCheckError("LEGACY_RUNTIME_DEPENDENCY_BLOCKED:" + violations[0])
    return {
        "status": "PASS",
        "legacy_import_count": 0,
        "pure_tool_allowlist": [
            PPM_PACKAGE_REL,
            "LanguageTool 6.8 commandline.jar by exact SHA256",
        ],
    }


def run_all(
    repo: Path,
    state: Mapping[str, Any],
    fact_pack: Mapping[str, Any],
    production_plan_item: Mapping[str, Any],
) -> dict[str, Any]:
    article_html = str(state.get("draft_markdown") or "")
    draft_sha = str(state.get("draft_sha256") or "")
    if not article_html or text_sha256(article_html) != draft_sha:
        raise ProductionCheckError("SYSTEM4_DRAFT_BINDING_INVALID")
    validate_bound_context(state, fact_pack, production_plan_item)
    lt_runtime = run_languagetool(repo, article_html)
    lt_public = {k: v for k, v in lt_runtime.items() if not k.startswith("_")}
    evidence = {
        "no_legacy": no_legacy_runtime_dependencies(repo),
        "no_external_links": no_external_links(article_html),
        "languagetool": lt_public,
        "ppm679": run_ppm_content_validator(repo, article_html, fact_pack, production_plan_item, lt_runtime),
    }
    return {
        "contract": "SYSTEM4_FULL_PRODUCTION_CHECK_V1",
        "status": "PASS",
        "checked_draft_sha256": draft_sha,
        "publish_allowed": False,
        "evidence": evidence,
    }
