#!/usr/bin/env python3
"""One fail-closed SOURCE gate for the existing eBay 6.72.310 test-only patch.

Does not deploy, change live WordPress, or claim eBay/WordPress end-to-end PASS.
Requires the exact 6.72.308 original ZIP; never reconstructs it.
"""
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

ORIGINAL_SHA256 = "b4d8547fd2aa134f7f82f568db3a81df54bb7d2131fd0752e76e3f0ca2251fe0"
ORIGINAL_FILES = 66
ORIGINAL_PHP = 23
ORIGINAL_JSON = 3
ROOT = "affiliate-portal-router/"
CHANGED = {
    ROOT + "includes/class-ppar-admin-kiss.php",
    ROOT + "includes/trait-ppar-ebay-run.php",
    ROOT + "includes/trait-ppar-ebay.php",
    ROOT + "pferdeportal-affiliate-router.php",
    ROOT + "readme.txt",
}

def stop(code, message):
    print(json.dumps({"gate": "SOURCE_REPLAY", "status": "FAIL",
                      "code": code, "reason": message, "release_allowed": False},
                     ensure_ascii=False))
    raise SystemExit(2)

def run(*args, cwd=None):
    cp = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if cp.returncode:
        stop("COMMAND_FAILED", f"{args[0]} failed: {cp.stderr[-1200:]} {cp.stdout[-500:]}")
    return cp.stdout

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("original_zip", type=Path)
    ap.add_argument("test_only_patch", type=Path)
    args = ap.parse_args()
    if not args.original_zip.is_file():
        stop("ORIGINAL_MISSING", "Exakte originale 6.72.308-ZIP fehlt. Keine Ersatzquelle.")
    if not args.test_only_patch.is_file():
        stop("PATCH_MISSING", "Bestehende 6.72.310-Testkorrektur fehlt.")
    content = args.original_zip.read_bytes()
    if sha(content) != ORIGINAL_SHA256:
        stop("ORIGINAL_HASH_MISMATCH", "Original-ZIP stimmt nicht bytegenau mit der geprüften 6.72.308 überein.")
    with zipfile.ZipFile(args.original_zip) as z:
        entries = [x for x in z.infolist() if not x.is_dir()]
        names = [x.filename for x in entries]
        if len(names) != ORIGINAL_FILES or len(set(names)) != len(names):
            stop("ORIGINAL_FILE_COUNT", "Erwartet genau 66 eindeutige Originaldateien.")
        if len([x for x in names if x.endswith(".php")]) != ORIGINAL_PHP:
            stop("ORIGINAL_PHP_COUNT", "Erwartet genau 23 PHP-Dateien.")
        if len([x for x in names if x.endswith(".json")]) != ORIGINAL_JSON:
            stop("ORIGINAL_JSON_COUNT", "Erwartet genau 3 JSON-Dateien.")
        if any(not x.startswith(ROOT) or ".." in Path(x).parts or Path(x).is_absolute() for x in names):
            stop("ORIGINAL_PATH_INVALID", "Unerwartete ZIP-Pfade.")
        if z.testzip() is not None:
            stop("ORIGINAL_CRC_INVALID", "ZIP-Integrität fehlgeschlagen.")
        with tempfile.TemporaryDirectory(prefix="ebay-672310-gate-") as temp:
            work = Path(temp)
            z.extractall(work)
            original = {name: sha((work / name).read_bytes()) for name in names}
            header = (work / ROOT / "pferdeportal-affiliate-router.php").read_text()
            if not re.search(r"^\s*\*\s*Version:\s*6\.72\.308\s*$", header, re.M):
                stop("ORIGINAL_VERSION_INVALID", "Pluginheader ist nicht 6.72.308.")
            patch = args.test_only_patch.read_text(encoding="utf-8")
            touched = set()
            for line in patch.splitlines():
                if line.startswith("+++ b/"):
                    touched.add(line[6:])
            if touched != CHANGED:
                stop("PATCH_SCOPE_INVALID", "Korrektur verändert andere als die fünf freigegebenen Dateien.")
            local_patch = work / "_ebay_310.patch"
            local_patch.write_text(patch, encoding="utf-8")
            run("git", "apply", "--check", str(local_patch), cwd=work)
            run("git", "apply", str(local_patch), cwd=work)
            if set(x for x in names if sha((work / x).read_bytes()) != original[x]) != CHANGED:
                stop("PATCH_IDENTITY_INVALID", "Änderungsumfang stimmt nach Anwendung nicht.")
            for name in names:
                if name.endswith(".php"):
                    run("php", "-l", str(work / name))
                elif name.endswith(".json"):
                    try:
                        json.loads((work / name).read_text(encoding="utf-8"))
                    except Exception:
                        stop("JSON_INVALID", name)
            updated = (work / ROOT / "pferdeportal-affiliate-router.php").read_text()
            if "Version: 6.72.310" not in updated or "const VERSION = '6.72.310'" not in updated:
                stop("NEW_VERSION_INVALID", "Versionsangaben in Testquelle uneinheitlich.")
    print(json.dumps({
        "gate": "SOURCE_REPLAY",
        "status": "PASS",
        "original_sha256": ORIGINAL_SHA256,
        "patch_sha256": sha(args.test_only_patch.read_bytes()),
        "plugin_files_checked": ORIGINAL_FILES,
        "php_lint_pass": ORIGINAL_PHP,
        "json_pass": ORIGINAL_JSON,
        "modified_files": len(CHANGED),
        "wordpress_mariadb_e2e": "NOT_RUN",
        "ebay_live_e2e": "NOT_RUN",
        "frontend_product_cards": "NOT_VERIFIED",
        "release_allowed": False
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
