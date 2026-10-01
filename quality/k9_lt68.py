#!/usr/bin/env python3
import argparse, hashlib, html, json, re, subprocess, sys, tempfile
from pathlib import Path

LT_JAR_SHA256 = "2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8"
LT_OUTER_DEPENDENCY_SHA256 = "187f7c2efe7762049e9f00553dafe686e269bbf62220abe2f2715fe55df8605a"
LT_INNER_DEPENDENCY_SHA256 = "6a7f6b67b779ae9505f7579f0c41453ea8d1bd72ae750bdc2c55ba974281467d"
ENGINE = "LanguageTool 6.8 / Bestand 43"
DOMAIN_DICTIONARY_PATH = Path(__file__).resolve().parents[1] / "contracts" / "K9_LT68_DOMAIN_DICTIONARY.json"

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

def load_domain_dictionary() -> tuple[set[str], str]:
    if not DOMAIN_DICTIONARY_PATH.is_file():
        raise LTError("LT68_DOMAIN_DICTIONARY_MISSING")
    raw = DOMAIN_DICTIONARY_PATH.read_bytes()
    try:
        data = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise LTError("LT68_DOMAIN_DICTIONARY_INVALID_JSON") from exc
    required={"contract","status","purpose","applies_to_rule_id","matching_mode","words","safeguards","publish_allowed"}
    if set(data)!=required:
        raise LTError("LT68_DOMAIN_DICTIONARY_SCHEMA_DRIFT")
    if data.get("contract")!="K9_LT68_DOMAIN_DICTIONARY_V1" or data.get("status")!="ACTIVE":
        raise LTError("LT68_DOMAIN_DICTIONARY_CONTRACT_INVALID")
    if data.get("applies_to_rule_id")!="GERMAN_SPELLER_RULE" or data.get("matching_mode")!="EXACT_VISIBLE_TOKEN_CASEFOLD":
        raise LTError("LT68_DOMAIN_DICTIONARY_SCOPE_INVALID")
    if data.get("publish_allowed") is not False:
        raise LTError("LT68_DOMAIN_DICTIONARY_PUBLISH_INVALID")
    safeguards=data.get("safeguards")
    if not isinstance(safeguards,dict) or safeguards.get("other_rule_ids_remain_blocking") is not True or safeguards.get("partial_matches_forbidden") is not True or safeguards.get("unknown_spelling_findings_remain_blocking") is not True or safeguards.get("engine_version_unchanged")!=ENGINE:
        raise LTError("LT68_DOMAIN_DICTIONARY_SAFEGUARDS_INVALID")
    words=data.get("words")
    if not isinstance(words,list) or not words or any(not isinstance(x,str) or not x.strip() for x in words):
        raise LTError("LT68_DOMAIN_DICTIONARY_WORDS_INVALID")
    normalized=[x.strip().casefold() for x in words]
    if len(normalized)!=len(set(normalized)):
        raise LTError("LT68_DOMAIN_DICTIONARY_DUPLICATE_WORD")
    return set(normalized), sha256_bytes(raw)

def apply_domain_dictionary(checked: str, report: dict, authoritative_words=None) -> tuple[dict, list[dict], str, str]:
    words, dictionary_sha = load_domain_dictionary()
    authoritative=set()
    for raw in authoritative_words or []:
        if not isinstance(raw,str) or not raw.strip():
            raise LTError("LT68_AUTHORITATIVE_DOMAIN_WORD_INVALID")
        token=raw.strip()
        if not re.fullmatch(r"[A-Za-zÄÖÜäöüß-]+",token):
            raise LTError("LT68_AUTHORITATIVE_DOMAIN_WORD_NOT_EXACT_TOKEN:"+token[:40])
        authoritative.add(token.casefold())
    words=set(words)|authoritative
    authoritative_sha=sha256_bytes(json.dumps(sorted(authoritative),ensure_ascii=False,separators=(",",":")).encode("utf-8"))
    matches=report.get("matches")
    if not isinstance(matches,list):
        raise LTError("LT68_MATCHES_INVALID")
    kept=[]
    ignored=[]
    for raw in matches:
        match=raw if isinstance(raw,dict) else {}
        rule=match.get("rule") if isinstance(match.get("rule"),dict) else {}
        rid=str(rule.get("id") or "")
        offset=match.get("offset")
        length=match.get("length")
        token=""
        if isinstance(offset,int) and isinstance(length,int) and 0 <= offset <= len(checked) and 0 <= length and offset+length <= len(checked):
            token=checked[offset:offset+length]
        exact_token=bool(re.fullmatch(r"[A-Za-zÄÖÜäöüß-]+",token or ""))
        if rid=="GERMAN_SPELLER_RULE" and exact_token and token.casefold() in words:
            context=match.get("context") if isinstance(match.get("context"),dict) else {}
            ignored.append({
                "rule_id":rid,
                "token":token,
                "offset":offset,
                "length":length,
                "context":str(context.get("text") or ""),
                "source":"AUTHORITATIVE_ARTICLE_METADATA" if token.casefold() in authoritative else "STATIC_DOMAIN_DICTIONARY"
            })
        else:
            kept.append(raw)
    filtered=dict(report)
    filtered["matches"]=kept
    return filtered, ignored, dictionary_sha, authoritative_sha

def ppm_visible_language_text(article_html: str) -> str:
    """Exact Python copy of PPM 6.7.9 Wave-2 visible_language_text()."""
    lines = []
    for match in re.finditer(r"<(h2|p|li|th|td|small)\b[^>]*>(.*?)</\1>", article_html, re.I | re.S):
        value = html.unescape(match.group(2))
        value = re.sub(r"<[^>]+>", " ", value)
        value = re.sub(r"\s+", " ", value).strip()
        value = re.sub(r"\s+([.,;:!?])", r"\1", value)
        if value:
            lines.append(value)
    return "\n\n".join(lines)

def run(jar: Path, article_path: Path, authoritative_words=None) -> dict:
    if not jar.is_file():
        raise LTError("LT68_JAR_MISSING")
    actual = file_sha256(jar)
    if actual != LT_JAR_SHA256:
        raise LTError("LT68_JAR_HASH_MISMATCH")

    raw_html = article_path.read_text(encoding="utf-8")
    checked = ppm_visible_language_text(raw_html)
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

    raw_report_unfiltered = proc.stdout
    try:
        report_unfiltered = json.loads(raw_report_unfiltered)
    except json.JSONDecodeError as exc:
        raise LTError("LT68_REPORT_INVALID") from exc

    report, domain_ignored, domain_dictionary_sha, authoritative_domain_terms_sha = apply_domain_dictionary(checked, report_unfiltered, authoritative_words)
    matches = report.get("matches") if isinstance(report, dict) else None
    if not isinstance(matches, list):
        raise LTError("LT68_MATCHES_INVALID")
    raw_report = json.dumps(report, ensure_ascii=False, separators=(",",":"))

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

    article_sha = sha256_bytes(raw_html.encode("utf-8"))
    checked_sha = sha256_bytes(checked.encode("utf-8"))
    raw_sha = sha256_bytes(raw_report.encode("utf-8"))
    raw_unfiltered_sha = sha256_bytes(raw_report_unfiltered.encode("utf-8"))
    evidence = {
        "engine": ENGINE,
        "outer_dependency_sha256": LT_OUTER_DEPENDENCY_SHA256,
        "inner_dependency_sha256": LT_INNER_DEPENDENCY_SHA256,
        "content_hash": article_sha,
        "checked_text": checked,
        "checked_text_sha256": checked_sha,
        "raw_report_json": raw_report,
        "raw_report_sha256": raw_sha,
        "raw_report_unfiltered_json": raw_report_unfiltered,
        "raw_report_unfiltered_sha256": raw_unfiltered_sha,
        "domain_dictionary_sha256": domain_dictionary_sha,
        "authoritative_domain_terms_sha256": authoritative_domain_terms_sha,
        "domain_dictionary_ignored_findings": domain_ignored,
        "raw_finding_count": len(matches),
        "unresolved_finding_count": len(matches),
        "return_code": proc.returncode,
        "approved_exceptions": [],
        "execution_record": {
            "input_sha256": checked_sha,
            "raw_stdout_sha256": raw_sha,
            "return_code": proc.returncode,
        },
    }

    return {
        "contract": "K9_LT68_RESULT_V1",
        "engine": ENGINE,
        "jar_sha256": actual,
        "outer_dependency_sha256": LT_OUTER_DEPENDENCY_SHA256,
        "inner_dependency_sha256": LT_INNER_DEPENDENCY_SHA256,
        "article_sha256": article_sha,
        "checked_text_sha256": checked_sha,
        "raw_report_sha256": raw_sha,
        "return_code": proc.returncode,
        "finding_count": len(findings),
        "findings": findings,
        "domain_dictionary_sha256": domain_dictionary_sha,
        "authoritative_domain_terms_sha256": authoritative_domain_terms_sha,
        "domain_dictionary_ignored_count": len(domain_ignored),
        "language_evidence": evidence,
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
