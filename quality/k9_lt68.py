#!/usr/bin/env python3
import argparse, hashlib, html, json, re, subprocess, sys, tempfile
from pathlib import Path

LT_JAR_SHA256 = "2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8"
ENGINE = "LanguageTool 6.8"

class LTError(RuntimeError):
    pass

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def plain_text(article_html: str) -> str:
    value = re.sub(r"(?is)<!--.*?-->", "\n", article_html)
    value = re.sub(r"(?is)<(script|style)\\b[^>]*>.*?</\\1>", "\n", value)
    value = re.sub(r"(?is)</?(?:article|section|p|div|li|h[1-6]|br|tr|td|th|ul|ol|table|blockquote)\\b[^>]*>", "\n", value)
    value = re.sub(r"(?s)<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r"\n[ \t]*\n+", "\n\n", value)
    return value.strip() + "\n"

def run(jar: Path, article_path: Path) -> dict:
    if not jar.is_file():
        raise LTError("LT68_JAR_MISSING")
    actual = file_sha256(jar)
    if actual != LT_JAR_SHA256:
        raise LTError("LT68_JAR_HASH_MISMATCH")

    raw_html = article_path.read_text(encoding="utf-8")
    checked = plain_text(raw_html)
    if not checked.strip():
        raise LTError("LT68_TEXT_EMPTY")

    with tempfile.TemporaryDirectory(prefix="k9-lt68-") as td:
        src = Path(td) / "article.txt"
        src.write_text(checked, encoding="utf-8")
        proc = subprocess.run(
            ["java", "-Xmx1024m", "-jar", str(jar), "--json", "-l", "de-DE", str(src)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
            check=False,
        )
    if proc.returncode != 0:
        raise LTError("LT68_EXECUTION_FAILED:" + (proc.stderr or proc.stdout).strip()[:220])

    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise LTError("LT68_REPORT_INVALID") from exc

    matches = report.get("matches") if isinstance(report, dict) else None
    if not isinstance(matches, list):
        raise LTError("LT68_MATCHES_INVALID")

    findings = []
    for raw in matches:
        match = raw if isinstance(raw, dict) else {}
        rule = match.get("rule") if isinstance(match.get("rule"), dict) else {}
        context = match.get("context") if isinstance(match.get("context"), dict) else {}
        findings.append({
            "rule_id": str(rule.get("id") or ""),
            "message": str(match.get("message") or ""),
            "offset": match.get("offset"),
            "length": match.get("length"),
            "context": str(context.get("text") or ""),
        })

    return {
        "contract": "K9_LT68_RESULT_V1",
        "engine": ENGINE,
        "jar_sha256": actual,
        "article_sha256": sha256_bytes(raw_html.encode("utf-8")),
        "checked_text_sha256": sha256_bytes(checked.encode("utf-8")),
        "finding_count": len(findings),
        "findings": findings,
        "status": "PASS" if not findings else "REPAIR_REQUIRED",
        "publish_allowed": False,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jar")
    ap.add_argument("article")
    ap.add_argument("--output")
    args = ap.parse_args()

    try:
        result = run(Path(args.jar), Path(args.article))
    except (LTError, subprocess.TimeoutExpired, OSError) as exc:
        print(json.dumps({"contract":"K9_LT68_RESULT_V1","status":"BLOCKED","reason":str(exc),"publish_allowed":False}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["status"] == "PASS" else 3)

if __name__ == "__main__":
    main()
