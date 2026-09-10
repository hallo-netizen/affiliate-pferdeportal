#!/usr/bin/env bash
set -euo pipefail

REPO_FULL_NAME="hallo-netizen/affiliate-pferdeportal"
REPO_URL="https://github.com/${REPO_FULL_NAME}.git"
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

TOOLBOX_MANIFEST="control/startmaster0107/codex-production-runtime/RUNTIME_TOOLBOX_MANIFEST.json"

# Never allow proof data from a previous cached Codex chat to survive.
rm -rf .pferde-environment
mkdir -p .pferde-environment

# The manifest is the single technical toolbox truth. It has zero workflow,
# content, quality, design, SEO or publish authority.
python3 - "$TOOLBOX_MANIFEST" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1])
if not p.is_file():
    raise SystemExit("RUNTIME_TOOLBOX_MANIFEST_MISSING")
m = json.loads(p.read_text(encoding="utf-8"))
if m.get("contract") != "PFERDE_ATELIER_RUNTIME_TOOLBOX_MANIFEST_V1":
    raise SystemExit("RUNTIME_TOOLBOX_MANIFEST_CONTRACT_INVALID")
if m.get("scope") != "TECHNICAL_RUNTIME_IDENTITY_ONLY":
    raise SystemExit("RUNTIME_TOOLBOX_MANIFEST_SCOPE_INVALID")
a = m.get("authority") or {}
required_none = (
    "chat_execution_authority",
    "chat_tool_selection_authority",
    "worker_tool_selection_authority",
    "workflow_navigation_authority",
    "repair_choice_authority",
    "content_semantics_authority",
    "quality_authority",
    "design_authority",
    "seo_authority",
)
for key in required_none:
    if a.get(key) != "NONE":
        raise SystemExit("RUNTIME_TOOLBOX_MANIFEST_AUTHORITY_INVALID:" + key)
if a.get("publish_allowed") is not False:
    raise SystemExit("RUNTIME_TOOLBOX_MANIFEST_PUBLISH_AUTHORITY_INVALID")
u = m.get("update_policy") or {}
if u.get("mode") != "EXACT_MANIFEST_ONLY_FAIL_CLOSED":
    raise SystemExit("RUNTIME_TOOLBOX_UPDATE_POLICY_INVALID")
for key in ("alternative_tool_allowed", "fallback_version_allowed", "worker_choice_allowed", "chat_choice_allowed"):
    if u.get(key) is not False:
        raise SystemExit("RUNTIME_TOOLBOX_UPDATE_CHOICE_INVALID:" + key)
agent = m.get("agent_phase") or {}
for key in ("network_required", "tool_install_allowed", "tool_update_allowed", "tool_selection_allowed"):
    if agent.get(key) is not False:
        raise SystemExit("RUNTIME_TOOLBOX_AGENT_POLICY_INVALID:" + key)
PY

manifest_value() {
  python3 - "$TOOLBOX_MANIFEST" "$1" <<'PY'
import json, sys
m = json.load(open(sys.argv[1], encoding="utf-8"))
v = m
for part in sys.argv[2].split("."):
    v = v[part]
if isinstance(v, bool):
    print("true" if v else "false")
else:
    print(v)
PY
}

# Resolve current GitHub main independently of the local Codex branch name.
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

if [[ "$CURRENT_BRANCH" == "main" && "$LOCAL_SHA" != "$MAIN_SHA" ]]; then
  git reset --hard "$MAIN_SHA"
  LOCAL_SHA="$(git rev-parse HEAD)"
  SYNC_MODE="HARD_SYNC_CURRENT_MAIN"
fi

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

# Deterministically select only the two system runtimes named by the manifest.
# No worker/chat choice and no fallback version is permitted.
JAVA_SELECTOR="$(manifest_value system_runtimes.java.selector)"
PHP_SELECTOR="$(manifest_value system_runtimes.php.selector)"
CODEX_RUNTIME_SELECTOR="/opt/codex/setup_universal.sh"
if [[ ! -x "$CODEX_RUNTIME_SELECTOR" ]]; then
  echo "CODEX_UNIVERSAL_RUNTIME_SELECTOR_UNAVAILABLE"
  exit 3
fi
CODEX_ENV_JAVA_VERSION="$JAVA_SELECTOR" \
CODEX_ENV_PHP_VERSION="$PHP_SELECTOR" \
"$CODEX_RUNTIME_SELECTOR"

# Fixed technical runtime dependency for ED25519 verification.
CRYPTO_VERSION="$(manifest_value python_packages.cryptography.version)"
if ! python3 - "$CRYPTO_VERSION" <<'PY' >/dev/null 2>&1
import cryptography, sys
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
assert cryptography.__version__ == sys.argv[1]
PY
then
  python3 -m pip install --disable-pip-version-check --no-input "cryptography==${CRYPTO_VERSION}"
fi
python3 - "$CRYPTO_VERSION" <<'PY'
import cryptography, sys
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
if cryptography.__version__ != sys.argv[1]:
    raise SystemExit("CRYPTOGRAPHY_VERSION_MISMATCH")
PY

# Materialize the exact LanguageTool dependency from the same manifest.
# The exact ZIP is cached. The extracted runtime is also cached by ZIP hash,
# so subsequent starts verify and reuse it instead of extracting 258 MB again.
python3 - "$TOOLBOX_MANIFEST" <<'PY'
from pathlib import Path
import hashlib
import json
import shutil
import sys
import urllib.request
import zipfile

MANIFEST_PATH = Path(sys.argv[1])
manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
lt = manifest["languagetool"]

ENV = Path(".pferde-environment")
cache_rel = Path(str(lt["persistent_cache_root"]))
if cache_rel.is_absolute() or ".." in cache_rel.parts:
    raise SystemExit("LANGUAGETOOL_CACHE_ROOT_INVALID")
CACHE = Path.home() / cache_rel
CACHE.mkdir(parents=True, exist_ok=True)

ASSET_URL = str(lt["source_url"])
INNER_SHA = str(lt["inner_zip_sha256"])
INNER_SIZE = int(lt["inner_zip_size"])
OUTER_REF = str(lt["historical_outer_ref"])
OUTER_SHA = str(lt["historical_outer_sha256"])
JAR_SHA = str(lt["commandline_jar_sha256"])
JAR_MANIFEST_SHA = str(lt["commandline_jar_manifest_sha256"])
ENGINE = str(lt["engine"])
COMPONENT_VERSION = str(lt["component_version"])

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            block = fh.read(1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()

inner = CACHE / f"LanguageTool-{COMPONENT_VERSION}.zip"
if not inner.is_file() or inner.stat().st_size != INNER_SIZE or sha256(inner) != INNER_SHA:
    tmp = CACHE / f"LanguageTool-{COMPONENT_VERSION}.zip.tmp"
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
            block = resp.read(1024 * 1024)
            if not block:
                break
            total += len(block)
            if total > INNER_SIZE:
                raise SystemExit("LANGUAGETOOL_DOWNLOAD_SIZE_OVERFLOW")
            h.update(block)
            out.write(block)
    if total != INNER_SIZE:
        raise SystemExit("LANGUAGETOOL_DOWNLOAD_SIZE_MISMATCH")
    if h.hexdigest() != INNER_SHA:
        raise SystemExit("LANGUAGETOOL_INNER_ZIP_HASH_MISMATCH")
    tmp.replace(inner)

runtime = CACHE / ("runtime-" + INNER_SHA)
jar = runtime / f"LanguageTool-{COMPONENT_VERSION}" / "languagetool-commandline.jar"

def runtime_valid() -> bool:
    if not jar.is_file() or sha256(jar) != JAR_SHA:
        return False
    try:
        with zipfile.ZipFile(jar) as zf:
            jar_manifest = zf.read("META-INF/MANIFEST.MF")
    except Exception:
        return False
    if hashlib.sha256(jar_manifest).hexdigest() != JAR_MANIFEST_SHA:
        return False
    return (f"ComponentVersion: {COMPONENT_VERSION}".encode("utf-8") in jar_manifest)

if not runtime_valid():
    if runtime.exists():
        shutil.rmtree(runtime)
    runtime.mkdir(parents=True)
    with zipfile.ZipFile(inner) as zf:
        root = runtime.resolve()
        for info in zf.infolist():
            target = (runtime / info.filename).resolve()
            if target != root and root not in target.parents:
                raise SystemExit("LANGUAGETOOL_ZIP_PATH_ESCAPE")
        zf.extractall(runtime)
    if not runtime_valid():
        raise SystemExit("LANGUAGETOOL_RUNTIME_CACHE_INVALID")

manifest_sha = sha256(MANIFEST_PATH)
proof = {
    "contract": "PFERDE_ATELIER_LANGUAGETOOL_RUNTIME_BINDING_V2",
    "status": "LANGUAGETOOL_RUNTIME_READY",
    "toolbox_manifest_ref": str(MANIFEST_PATH),
    "toolbox_manifest_sha256": manifest_sha,
    "engine": ENGINE,
    "source_url": ASSET_URL,
    "outer_dependency_ref": OUTER_REF,
    "outer_dependency_sha256": OUTER_SHA,
    "inner_dependency_cache_ref": str(inner),
    "inner_dependency_sha256": INNER_SHA,
    "inner_dependency_size": INNER_SIZE,
    "executed_component_version": COMPONENT_VERSION,
    "executed_commandline_jar_ref": str(jar.resolve()),
    "executed_commandline_jar_sha256": JAR_SHA,
    "executed_commandline_jar_manifest_sha256": JAR_MANIFEST_SHA,
    "command_argv_template": [
        "java", "-Xmx1024m", "-jar", str(jar.resolve()),
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

# Current-main production performs exactly one real toolbox validation here.
# Non-main candidates never receive production authority.
if [[ "$LOCAL_SHA" == "$MAIN_SHA" ]]; then
  python3 control/startmaster0107/codex-production-runtime/codex_environment_preflight.py
fi
