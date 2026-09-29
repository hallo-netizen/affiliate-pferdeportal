#!/usr/bin/env python3
import argparse, hashlib, json, subprocess, sys, tempfile, zipfile
from pathlib import Path

PPM_VERSION = "6.7.9"
PPM_SHA256 = "acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"

class PPMError(RuntimeError):
    pass

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path: Path):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise PPMError("PPM679_INPUT_JSON_INVALID") from exc
    if not isinstance(value, dict):
        raise PPMError("PPM679_INPUT_OBJECT_REQUIRED")
    return value

def validate_input(payload):
    if payload.get("contract") != "K9_PPM679_INPUT_V1":
        raise PPMError("PPM679_INPUT_CONTRACT_INVALID")
    generated = payload.get("generated")
    item = payload.get("item")
    fact_pack = payload.get("fact_pack")
    if not isinstance(generated, dict) or not isinstance(item, dict) or not isinstance(fact_pack, dict):
        raise PPMError("PPM679_INPUT_PARTS_MISSING")
    for key in ("article_type", "title", "content_html", "content_hash"):
        if key not in generated:
            raise PPMError("PPM679_GENERATED_FIELD_MISSING:" + key)
    if not str(generated.get("content_html") or "").strip():
        raise PPMError("PPM679_CONTENT_EMPTY")
    expected = hashlib.sha256(str(generated["content_html"]).encode("utf-8")).hexdigest()
    if generated.get("content_hash") != expected:
        raise PPMError("PPM679_DECLARED_CONTENT_HASH_MISMATCH")
    if not str(item.get("article_type") or ""):
        raise PPMError("PPM679_ITEM_ARTICLE_TYPE_MISSING")
    if not str(item.get("source_snapshot_id") or ""):
        raise PPMError("PPM679_ITEM_SOURCE_SNAPSHOT_MISSING")
    if not isinstance(fact_pack.get("claims"), list):
        raise PPMError("PPM679_FACT_PACK_CLAIMS_MISSING")
    return generated, item, fact_pack

PHP = r'''<?php
$root=$argv[1];
$payload=json_decode((string)file_get_contents($argv[2]),true);
if(!is_array($payload)){fwrite(STDERR,"PAYLOAD_INVALID\n");exit(2);}
require $root.'/tests/bootstrap-test.php';
PPM679_WP::reset_test_state();
PPM679_Storage::reset_test_state();
PPM679_Handoff_Permit::reset_test_state();
PPM679_Storage::ensure_schema();
$pack=(array)($payload['fact_pack']??[]);
$item=(array)($payload['item']??[]);
$generated=(array)($payload['generated']??[]);
$import=PPM679_Admin::import_fact_pack_bundle([
  'contract'=>'canonical_fact_pack_import_v1',
  'fact_packs'=>[$pack]
]);
if(empty($import['ok'])){
  echo json_encode(['ok'=>false,'phase'=>'FACT_PACK_IMPORT','import_result'=>$import],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
  exit(0);
}
$result=PPM679_Content_Validator::check($generated,$item,'k9_native_article_control','k9-native');
echo json_encode(['ok'=>!empty($result['ok']),'phase'=>'CONTENT_VALIDATION','result'=>$result],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
?>'''

def run(package: Path, input_path: Path):
    if not package.is_file():
        raise PPMError("PPM679_PACKAGE_MISSING")
    actual_package_sha = file_sha256(package)
    if actual_package_sha != PPM_SHA256:
        raise PPMError("PPM679_PACKAGE_HASH_MISMATCH")

    payload = load_json(input_path)
    generated, item, fact_pack = validate_input(payload)

    with tempfile.TemporaryDirectory(prefix="k9-ppm679-") as td:
        root = Path(td)
        extracted = root / "ppm"
        extracted.mkdir()
        with zipfile.ZipFile(package) as archive:
            archive.extractall(extracted)
        ppm_root = extracted / "portal-production-machine"
        if not (ppm_root / "tests" / "bootstrap-test.php").is_file():
            raise PPMError("PPM679_BOOTSTRAP_MISSING")

        normalized = {
            "generated": generated,
            "item": item,
            "fact_pack": fact_pack,
        }
        payload_path = root / "payload.json"
        payload_path.write_text(json.dumps(normalized, ensure_ascii=False), encoding="utf-8")
        php_path = root / "check.php"
        php_path.write_text(PHP, encoding="utf-8")
        try:
            proc = subprocess.run(
                ["php", str(php_path), str(ppm_root), str(payload_path)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise PPMError("PPM679_EXECUTION_TIMEOUT") from exc

    if proc.returncode != 0:
        raise PPMError("PPM679_EXECUTION_FAILED:" + (proc.stderr or proc.stdout).strip()[:260])

    try:
        wrapper = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise PPMError("PPM679_RESULT_INVALID") from exc
    if not isinstance(wrapper, dict):
        raise PPMError("PPM679_RESULT_OBJECT_REQUIRED")

    if wrapper.get("phase") == "FACT_PACK_IMPORT":
        return {
            "contract": "K9_PPM679_RESULT_V1",
            "status": "BLOCKED",
            "ppm_version": PPM_VERSION,
            "ppm_package_sha256": actual_package_sha,
            "phase": "FACT_PACK_IMPORT",
            "details": wrapper.get("import_result"),
            "publish_allowed": False,
        }

    result = wrapper.get("result")
    if not isinstance(result, dict):
        raise PPMError("PPM679_VALIDATOR_RESULT_MISSING")

    errors = result.get("errors") if isinstance(result.get("errors"), list) else []
    checks = result.get("checks") if isinstance(result.get("checks"), dict) else {}
    content_sha = hashlib.sha256(str(generated["content_html"]).encode("utf-8")).hexdigest()

    status = "PASS" if wrapper.get("ok") is True else "REPAIR_REQUIRED"
    return {
        "contract": "K9_PPM679_RESULT_V1",
        "status": status,
        "ppm_version": PPM_VERSION,
        "ppm_package_sha256": actual_package_sha,
        "content_sha256": content_sha,
        "technical_status": result.get("technical_status"),
        "content_quality_status": result.get("content_quality_status"),
        "fail_closed_aggregate_status": checks.get("fail_closed_aggregate_status"),
        "errors": errors,
        "checks": checks,
        "publish_allowed": False,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("package")
    ap.add_argument("input")
    ap.add_argument("--output")
    args = ap.parse_args()
    try:
        result = run(Path(args.package), Path(args.input))
    except (PPMError, OSError, zipfile.BadZipFile) as exc:
        result = {
            "contract": "K9_PPM679_RESULT_V1",
            "status": "BLOCKED",
            "reason": str(exc),
            "publish_allowed": False,
        }
        payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if args.output:
            Path(args.output).write_text(payload, encoding="utf-8")
        print(payload, end="")
        raise SystemExit(2)

    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    print(payload, end="")
    if result["status"] == "PASS":
        raise SystemExit(0)
    if result["status"] == "REPAIR_REQUIRED":
        raise SystemExit(3)
    raise SystemExit(2)

if __name__ == "__main__":
    main()
