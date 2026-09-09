#!/usr/bin/env bash
set -euo pipefail

REPO_FULL_NAME="hallo-netizen/affiliate-pferdeportal"
REPO_URL="https://github.com/${REPO_FULL_NAME}.git"
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

# Never allow proof data from a previous cached Codex chat to survive.
rm -rf .pferde-environment
mkdir -p .pferde-environment

# Resolve current GitHub main independently of the local Codex branch name.
# Codex Cloud may expose the selected UI branch as a synthetic local branch
# (for example "work"), so production proof must not depend on the literal
# output of `git branch --show-current`.
CURRENT_BRANCH="$(git branch --show-current || true)"
MAIN_SHA="$(git ls-remote "$REPO_URL" refs/heads/main | awk 'NR==1 {print $1}')"
if [[ ! "$MAIN_SHA" =~ ^[0-9a-f]{40}$ ]]; then
  echo "CODEX_MAIN_AUTHORITY_UNAVAILABLE"
  exit 2
fi

# Materialize the verified current main identity for the offline agent phase.
git fetch --no-tags "$REPO_URL" "+${MAIN_SHA}:refs/pferde-authority/current-main"
git update-ref refs/remotes/origin/main "$MAIN_SHA"

LOCAL_SHA="$(git rev-parse HEAD)"
SYNC_MODE="IDENTITY_ONLY_CURRENT_MAIN"

# Only a literal local main branch may be rewritten. This preserves the
# existing non-main no-rewrite contract. Synthetic/detached Codex checkouts
# are never rewritten merely because of their local branch name.
if [[ "$CURRENT_BRANCH" == "main" && "$LOCAL_SHA" != "$MAIN_SHA" ]]; then
  git reset --hard "$MAIN_SHA"
  LOCAL_SHA="$(git rev-parse HEAD)"
  SYNC_MODE="HARD_SYNC_CURRENT_MAIN"
fi

# Production proof is identity-based, not local-branch-name-based. This covers
# Codex Cloud's synthetic `work`/detached checkout when it points exactly at
# the selected current main, while leaving real non-main commits untouched.
if [[ "$LOCAL_SHA" == "$MAIN_SHA" ]]; then
  cat > .pferde-environment/MAIN_SYNC.json <<JSON
{
  "contract": "PFERDE_ATELIER_CODEX_MAIN_SYNC_V1",
  "status": "PASS",
  "repository": "${REPO_FULL_NAME}",
  "sync_mode": "${SYNC_MODE}",
  "main_sha": "${MAIN_SHA}",
  "local_head_sha": "${LOCAL_SHA}",
  "origin_remote_required": false,
  "agent_network_required": false,
  "content_semantics_inspected": false,
  "quality_authority": "NONE",
  "publish_allowed": false
}
JSON
fi

# Fixed technical runtime dependency for ED25519 verification.
if ! python3 - <<'PY' >/dev/null 2>&1
import cryptography
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
assert cryptography.__version__ == "50.0.1"
PY
then
  python3 -m pip install --disable-pip-version-check --no-input "cryptography==50.0.1"
fi

# Restore the exact historic LanguageTool 6.8 dependency before the agent phase.
# The large immutable transport and extracted runtime live in the persistent
# LanguageTool cache. Every reuse is still hash-validated; corrupt cache data
# is rebuilt from the exact bound inner archive. Production authority remains
# strictly current-main-only below. No content/quality rule is implemented here.
python3 - <<'PY'
from pathlib import Path
import hashlib
import json
import shutil
import urllib.request
import zipfile

ENV = Path(".pferde-environment")
CACHE = Path.home() / ".cache" / "pferde-atelier-languagetool"
RUNTIME = CACHE / "languagetool-runtime"
CACHE.mkdir(parents=True, exist_ok=True)

ASSET_URL = "https://github.com/jxmorris12/language_tool_python/releases/download/LanguageTool-6.8/LanguageTool-6.8.zip"
INNER_SHA = "6a7f6b67b779ae9505f7579f0c41453ea8d1bd72ae750bdc2c55ba974281467d"
INNER_SIZE = 258510816
OUTER_SHA = "187f7c2efe7762049e9f00553dafe686e269bbf62220abe2f2715fe55df8605a"
JAR_SHA = "2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8"
JAR_MANIFEST_SHA = "eb6fbf76ab6747b7a5a156390149c103f0e31e2ae14eddb28317cac0201ebe5c"
ENGINE = "LanguageTool 6.8 / Bestand 43"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            block = fh.read(1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()

def validate_runtime(root: Path) -> Path | None:
    jar = root / "LanguageTool-6.8" / "languagetool-commandline.jar"
    if not jar.is_file() or sha256(jar) != JAR_SHA:
        return None
    try:
        with zipfile.ZipFile(jar) as zf:
            manifest = zf.read("META-INF/MANIFEST.MF")
    except Exception:
        return None
    if hashlib.sha256(manifest).hexdigest() != JAR_MANIFEST_SHA:
        return None
    if b"ComponentVersion: 6.8" not in manifest:
        return None
    return jar

inner = CACHE / "LanguageTool-6.8.zip"
if not inner.is_file() or inner.stat().st_size != INNER_SIZE or sha256(inner) != INNER_SHA:
    tmp = CACHE / "LanguageTool-6.8.zip.tmp"
    if tmp.exists():
        tmp.unlink()
    req = urllib.request.Request(
        ASSET_URL,
        headers={"User-Agent": "pferde-atelier-codex-languagetool-runtime"},
    )
    total = 0
    h = hashlib.sha256()
    with urllib.request.urlopen(req, timeout=120) as resp, tmp.open("wb") as out:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > INNER_SIZE:
                raise SystemExit("LANGUAGETOOL_DOWNLOAD_SIZE_OVERFLOW")
            h.update(chunk)
            out.write(chunk)
    if total != INNER_SIZE:
        raise SystemExit("LANGUAGETOOL_DOWNLOAD_SIZE_MISMATCH")
    if h.hexdigest() != INNER_SHA:
        raise SystemExit("LANGUAGETOOL_INNER_ZIP_HASH_MISMATCH")
    tmp.replace(inner)

# Preserve the historic Bestand-43 transport proof exactly, but cache the
# verified outer archive instead of rebuilding 258 MB on every maintenance run.
outer = CACHE / "ARBEITSMASTER_0043_NEU_TEIL_2_LANGUAGETOOL_ABHAENGIGKEIT.zip"
if not outer.is_file() or sha256(outer) != OUTER_SHA:
    outer_tmp = CACHE / "ARBEITSMASTER_0043_NEU_TEIL_2_LANGUAGETOOL_ABHAENGIGKEIT.zip.tmp"
    if outer_tmp.exists():
        outer_tmp.unlink()
    base = "ARBEITSMASTER_0043_NEU_PRODUKTIONSMASCHINE_PFERDEPORTAL_REVISION_8_REC_03E_COMPLETE_TYPE_DIAGNOSIS_CHALLENGE_NEXT_FULL_CURRENT_STATE_2026-07-22/"
    readme = "LanguageTool 6.8 – unveränderte Offline-Abhängigkeit. Nicht als Plugin installieren.\n".encode("utf-8")
    manifest = (
        '{\n'
        '  "contract": "MASTER_0043_PART2_MANIFEST_V1",\n'
        '  "language_tool_sha256": "' + INNER_SHA + '",\n'
        '  "language_tool_size": 258510816,\n'
        '  "status": "UNCHANGED_DEPENDENCY"\n'
        '}\n'
    ).encode("utf-8")
    entries = [
        (base, True, None),
        (base + "90_DEPENDENCIES/", True, None),
        (base + "90_DEPENDENCIES/LANGUAGETOOL_6_8/", True, None),
        (base + "90_DEPENDENCIES/LANGUAGETOOL_6_8/LanguageTool-6.8.zip", False, inner),
        (base + "90_DEPENDENCIES/LANGUAGETOOL_6_8/README.txt", False, readme),
        (base + "MASTER_0043_TEIL_2_MANIFEST_SHA256.json", False, manifest),
    ]
    with zipfile.ZipFile(outer_tmp, "w") as zf:
        for name, is_dir, payload in entries:
            zi = zipfile.ZipInfo(name, (2026, 7, 22, 19, 0, 14))
            zi.create_system = 3
            zi.create_version = 20
            zi.extract_version = 20
            zi.flag_bits = 0
            zi.internal_attr = 0
            zi.external_attr = 1106051088 if is_dir else 2175008768
            zi.compress_type = zipfile.ZIP_STORED if is_dir else zipfile.ZIP_DEFLATED
            if is_dir:
                zf.writestr(zi, b"")
            elif isinstance(payload, bytes):
                zf.writestr(zi, payload)
            else:
                with zf.open(zi, "w") as dst, Path(payload).open("rb") as src:
                    shutil.copyfileobj(src, dst, 1024 * 1024)
    if sha256(outer_tmp) != OUTER_SHA:
        raise SystemExit("LANGUAGETOOL_OUTER_PROVENANCE_HASH_MISMATCH")
    outer_tmp.replace(outer)

jar = validate_runtime(RUNTIME)
if jar is None:
    tmp_runtime = CACHE / "languagetool-runtime.tmp"
    if tmp_runtime.exists():
        shutil.rmtree(tmp_runtime)
    tmp_runtime.mkdir(parents=True)
    with zipfile.ZipFile(inner) as zf:
        root = tmp_runtime.resolve()
        for info in zf.infolist():
            target = (tmp_runtime / info.filename).resolve()
            if target != root and root not in target.parents:
                raise SystemExit("LANGUAGETOOL_ZIP_PATH_ESCAPE")
        zf.extractall(tmp_runtime)
    tmp_jar = validate_runtime(tmp_runtime)
    if tmp_jar is None:
        raise SystemExit("LANGUAGETOOL_RUNTIME_CACHE_VALIDATION_FAILED")
    if RUNTIME.exists():
        shutil.rmtree(RUNTIME)
    tmp_runtime.replace(RUNTIME)
    jar = validate_runtime(RUNTIME)

if jar is None:
    raise SystemExit("LANGUAGETOOL_RUNTIME_CACHE_VALIDATION_FAILED")

proof = {
    "contract": "PFERDE_ATELIER_LANGUAGETOOL_RUNTIME_BINDING_V1",
    "status": "LANGUAGETOOL_RUNTIME_READY",
    "engine": ENGINE,
    "source_url": ASSET_URL,
    "outer_dependency_ref": str(outer),
    "outer_dependency_sha256": OUTER_SHA,
    "inner_dependency_cache_ref": str(inner),
    "inner_dependency_sha256": INNER_SHA,
    "inner_dependency_size": INNER_SIZE,
    "executed_component_version": "6.8",
    "executed_commandline_jar_ref": str(jar),
    "executed_commandline_jar_sha256": JAR_SHA,
    "executed_commandline_jar_manifest_sha256": JAR_MANIFEST_SHA,
    "command_argv_template": [
        "java", "-Xmx1024m", "-jar", str(jar),
        "--json", "-l", "de-DE", "{checked_text_file}"
    ],
    "agent_network_required_for_execution": False,
    "content_semantics_inspected": False,
    "quality_authority": "NONE",
    "content_or_quality_rules_changed": False,
    "publish_allowed": False,
}
(ENV / "LANGUAGETOOL_RUNTIME.json").write_text(
    json.dumps(proof, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY

# Real setup-phase runtime smoke tests. These prove actual usability before the
# Codex agent starts; they grant no production or quality authority.
python3 - <<'PY'
from pathlib import Path
import hashlib
import json
import shutil
import subprocess

ROOT = Path.cwd()
ENV = ROOT / ".pferde-environment"
PPM = ROOT / "control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PSERC = ROOT / "control/startmaster0107/runtime_packages/PSERC-FIX.zip"
PPM_SHA = "acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
PSERC_SHA = "77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314"
LT_JAR = Path.home() / ".cache/pferde-atelier-languagetool/languagetool-runtime/LanguageTool-6.8/languagetool-commandline.jar"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            b = fh.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def run(argv, token, timeout=120):
    try:
        cp = subprocess.run(argv, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    except Exception as exc:
        raise SystemExit(token) from exc
    if cp.returncode != 0:
        raise SystemExit(token)
    return cp

php = shutil.which("php")
if not php:
    raise SystemExit("PHP_RUNTIME_UNAVAILABLE")
php_cp = run([php, "-r", "echo PHP_VERSION;"], "PHP_RUNTIME_NOT_EXECUTABLE")
if not php_cp.stdout.strip():
    raise SystemExit("PHP_RUNTIME_VERSION_UNAVAILABLE")

java = shutil.which("java")
if not java:
    raise SystemExit("JAVA_RUNTIME_UNAVAILABLE")
java_cp = run([java, "-version"], "JAVA_RUNTIME_NOT_EXECUTABLE")
java_version = (java_cp.stderr or java_cp.stdout).splitlines()[0].strip() if (java_cp.stderr or java_cp.stdout) else ""
if not java_version:
    raise SystemExit("JAVA_RUNTIME_VERSION_UNAVAILABLE")

if not PPM.is_file() or sha256(PPM) != PPM_SHA:
    raise SystemExit("PPM679_PACKAGE_HASH_MISMATCH")
if not PSERC.is_file() or sha256(PSERC) != PSERC_SHA:
    raise SystemExit("PSERC_FIX_PACKAGE_HASH_MISMATCH")
if not LT_JAR.is_file():
    raise SystemExit("LANGUAGETOOL_COMMANDLINE_JAR_MISSING")

smoke = ENV / "LANGUAGETOOL_SETUP_SMOKE.txt"
smoke.write_text("Das ist ein einfacher Testsatz.\n", encoding="utf-8")
try:
    lt_cp = run([java, "-Xmx1024m", "-jar", str(LT_JAR), "--json", "-l", "de-DE", str(smoke)], "LANGUAGETOOL_RUNTIME_NOT_EXECUTABLE")
    try:
        parsed = json.loads(lt_cp.stdout)
    except Exception as exc:
        raise SystemExit("LANGUAGETOOL_RUNTIME_OUTPUT_INVALID") from exc
    if not isinstance(parsed, dict):
        raise SystemExit("LANGUAGETOOL_RUNTIME_OUTPUT_INVALID")
finally:
    try:
        smoke.unlink()
    except FileNotFoundError:
        pass

proof = {
    "contract": "PFERDE_ATELIER_CODEX_RUNTIME_TOOLBOX_SETUP_V1",
    "status": "RUNTIME_TOOLBOX_SETUP_PASS",
    "php_executable": True,
    "php_version": php_cp.stdout.strip(),
    "java_executable": True,
    "java_version": java_version,
    "languagetool_real_execution": True,
    "ppm679_package_sha256": PPM_SHA,
    "pserc_fix_package_sha256": PSERC_SHA,
    "agent_network_required_after_setup": False,
    "content_semantics_inspected": False,
    "quality_authority": "NONE",
    "publish_allowed": False,
}
(ENV / "RUNTIME_TOOLBOX_SETUP.json").write_text(
    json.dumps(proof, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY

# Run the production preflight whenever this checkout is proven to be the
# current GitHub main commit, regardless of Codex's synthetic local branch name.
if [[ "$LOCAL_SHA" == "$MAIN_SHA" ]]; then
  python3 control/startmaster0107/codex-production-runtime/codex_environment_preflight.py
fi
